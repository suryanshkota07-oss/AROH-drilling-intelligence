"""Explainable risk-ahead assessment built from analogue-well evidence.

The implementation is intentionally deterministic. It produces synthetic
demonstration decision support, never a verified operational prediction.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from ai.analogue_matching import DEFAULT_DATA_DIR, DatasetError, find_analogues


RISK_WEIGHTS = {
    "analogue_similarity": 0.35,
    "historical_event_frequency": 0.20,
    "formation_similarity": 0.20,
    "depth_proximity": 0.15,
    "drilling_parameter_similarity": 0.10,
}
DEPTH_HORIZON_M = 300.0


def assess_risks(
    active_well_id: str, data_dir: Path | str | None = None
) -> list[dict[str, Any]]:
    """Return ranked, evidence-backed synthetic risk-ahead assessments.

    Only historical events in the active formation with valid evidence records
    are considered. Events whose mapped interval has already passed are
    excluded because this function assesses risk ahead, not retrospective risk.
    """
    directory = Path(data_dir) if data_dir is not None else DEFAULT_DATA_DIR
    analogues = find_analogues(active_well_id, data_dir=directory)
    wells = _load_records(directory, "wells.json")
    formations = _load_records(directory, "formation_intervals.json")
    evidence = {record.get("evidence_id") for record in _load_records(directory, "evidence_records.json")}

    active = next(well for well in wells if well.get("well_id") == active_well_id)
    formation_name = analogues[0]["formation"] if analogues else None
    active_interval = _formation_interval(active_well_id, formation_name, formations)
    current_depth = active.get("current_md_m")
    if formation_name is None or active_interval is None or current_depth is None:
        return []

    formation_matched = [
        analogue for analogue in analogues
        if _feature_score(analogue, "formation") == 100.0
    ]
    if not formation_matched:
        return []

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for analogue in formation_matched:
        for event in analogue["relevant_historical_events"]:
            evidence_ids = [item for item in event["evidence_ids"] if item in evidence]
            if not evidence_ids:
                continue
            mapped_interval = _map_interval(
                event["interval_md_m"], analogue["well_id"], formation_name, active_interval, formations
            )
            if mapped_interval is None or mapped_interval["end_md_m"] < current_depth:
                continue
            grouped[event["event_type"]].append(
                {
                    "analogue": analogue,
                    "event": event,
                    "mapped_interval": mapped_interval,
                    "evidence_ids": evidence_ids,
                }
            )

    assessments = [
        _build_assessment(event_type, occurrences, len(formation_matched), current_depth)
        for event_type, occurrences in grouped.items()
    ]
    return sorted(assessments, key=lambda item: (-item["risk_score"], item["event_type"]))


def _build_assessment(
    event_type: str,
    occurrences: list[dict[str, Any]],
    relevant_analogue_count: int,
    current_depth: float,
) -> dict[str, Any]:
    analogue_scores = [item["analogue"]["similarity_score"] / 100 for item in occurrences]
    formation_scores = [_feature_score(item["analogue"], "formation") / 100 for item in occurrences]
    depth_scores = [_depth_proximity(item["mapped_interval"]["start_md_m"], current_depth) for item in occurrences]
    drilling_scores = [
        _optional_feature_score(item["analogue"], "drilling_characteristics")
        for item in occurrences
    ]
    components: dict[str, float | None] = {
        "analogue_similarity": sum(analogue_scores) / len(analogue_scores),
        "historical_event_frequency": min(1.0, len(occurrences) / relevant_analogue_count),
        "formation_similarity": sum(formation_scores) / len(formation_scores),
        "depth_proximity": sum(depth_scores) / len(depth_scores),
        "drilling_parameter_similarity": _mean_available(drilling_scores),
    }
    available_weight = sum(RISK_WEIGHTS[name] for name, value in components.items() if value is not None)
    risk_score = 100 * sum(
        RISK_WEIGHTS[name] * value for name, value in components.items() if value is not None
    ) / available_weight

    predicted_interval = {
        "start_md_m": round(min(item["mapped_interval"]["start_md_m"] for item in occurrences), 1),
        "end_md_m": round(max(item["mapped_interval"]["end_md_m"] for item in occurrences), 1),
    }
    supporting_wells = [
        {
            "well_id": item["analogue"]["well_id"],
            "analogue_similarity_score": item["analogue"]["similarity_score"],
            "historical_event_id": item["event"]["event_id"],
            "historical_interval_md_m": item["event"]["interval_md_m"],
            "mapped_interval_md_m": item["mapped_interval"],
            "evidence_ids": item["evidence_ids"],
        }
        for item in occurrences
    ]
    confidence = _confidence(occurrences, components)
    return {
        "event_type": event_type,
        "risk_score": round(risk_score, 2),
        "severity": _severity(risk_score),
        "predicted_interval": predicted_interval,
        "confidence": round(confidence, 2),
        "supporting_wells": supporting_wells,
        "score_factors": _score_factors(components),
        "uncertainty": (
            "Synthetic demonstration estimate derived from historical analogue events; "
            "it is decision support, not a verified operational prediction."
        ),
        "data_classification": "synthetic_demo",
    }


def _load_records(directory: Path, filename: str) -> list[dict[str, Any]]:
    try:
        with (directory / filename).open(encoding="utf-8") as data_file:
            records = json.load(data_file)
    except (OSError, json.JSONDecodeError) as error:
        raise DatasetError(f"Unable to load {filename}: {error}") from error
    if not isinstance(records, list):
        raise DatasetError(f"{filename} must contain a JSON list")
    return records


def _formation_interval(well_id: str, formation_name: str | None, formations: list[dict[str, Any]]):
    return next(
        (
            item for item in formations
            if item.get("well_id") == well_id and item.get("formation_name") == formation_name
        ),
        None,
    )


def _map_interval(
    historical_interval: dict[str, float], historical_well_id: str, formation_name: str,
    active_interval: dict[str, float], formations: list[dict[str, Any]],
) -> dict[str, float] | None:
    historical_formation = _formation_interval(historical_well_id, formation_name, formations)
    if historical_formation is None:
        return None
    historical_span = historical_formation["base_md_m"] - historical_formation["top_md_m"]
    active_span = active_interval["base_md_m"] - active_interval["top_md_m"]
    if historical_span <= 0 or active_span <= 0:
        return None

    def map_depth(depth: float) -> float:
        fraction = (depth - historical_formation["top_md_m"]) / historical_span
        return active_interval["top_md_m"] + min(1.0, max(0.0, fraction)) * active_span

    return {
        "start_md_m": round(map_depth(historical_interval["start"]), 1),
        "end_md_m": round(map_depth(historical_interval["end"]), 1),
    }


def _feature_score(analogue: dict[str, Any], feature_name: str) -> float:
    score = _optional_feature_score(analogue, feature_name)
    return score if score is not None else 0.0


def _optional_feature_score(analogue: dict[str, Any], feature_name: str) -> float | None:
    item = next(
        (feature for feature in analogue["matching_features"] if feature["feature"] == feature_name),
        None,
    )
    return item.get("score") if item is not None else None


def _depth_proximity(interval_start: float, current_depth: float) -> float:
    if interval_start <= current_depth:
        return 1.0
    return max(0.0, 1.0 - (interval_start - current_depth) / DEPTH_HORIZON_M)


def _mean_available(values: list[float | None]) -> float | None:
    available = [value / 100 for value in values if value is not None]
    return sum(available) / len(available) if available else None


def _confidence(occurrences: list[dict[str, Any]], components: dict[str, float | None]) -> float:
    evidence_coverage = 1.0 if all(item["evidence_ids"] for item in occurrences) else 0.0
    sample_coverage = min(1.0, len(occurrences) / 3)
    component_coverage = sum(value is not None for value in components.values()) / len(components)
    return 100 * (0.45 * sample_coverage + 0.35 * evidence_coverage + 0.20 * component_coverage)


def _severity(risk_score: float) -> str:
    if risk_score >= 85:
        return "critical"
    if risk_score >= 70:
        return "elevated"
    if risk_score >= 45:
        return "watch"
    return "normal"


def _score_factors(components: dict[str, float | None]) -> list[dict[str, Any]]:
    descriptions = {
        "analogue_similarity": "Mean deterministic similarity of supporting offset wells.",
        "historical_event_frequency": "Event occurrences divided by relevant formation-matched analogues.",
        "formation_similarity": "Formation-match score of supporting analogue wells.",
        "depth_proximity": f"Mapped event proximity to current depth, with a {DEPTH_HORIZON_M:g} m horizon.",
        "drilling_parameter_similarity": "Comparable formation-relative drilling measurement similarity.",
    }
    return [
        {
            "factor": name,
            "score": round(value * 100, 2) if value is not None else None,
            "weight": RISK_WEIGHTS[name],
            "status": "included" if value is not None else "unavailable_excluded_from_score",
            "explanation": descriptions[name],
        }
        for name, value in components.items()
    ]
