"""Deterministic, evidence-oriented analogue well matching for AROH.

This module uses only the synthetic demonstration dataset. It intentionally
does not make operational recommendations or use an LLM.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


DEFAULT_DATA_DIR = Path(__file__).resolve().parents[1] / "data"
WEIGHTS = {
    "formation": 0.30,
    "trajectory": 0.25,
    "proximity": 0.20,
    "depth": 0.15,
    "drilling_characteristics": 0.10,
}
PROXIMITY_CUTOFF_KM = 25.0


class WellNotFoundError(ValueError):
    """Raised when a requested well identifier is absent from the dataset."""


class DatasetError(ValueError):
    """Raised when a required synthetic dataset file cannot be interpreted."""


def find_analogues(
    active_well_id: str, data_dir: Path | str | None = None, limit: int | None = None
) -> list[dict[str, Any]]:
    """Return ranked historical offsets for an active well.

    Scores are deterministic and rounded to two decimal places on a 0–100
    scale. A feature with unavailable input data is excluded from the weighted
    average; known mismatches receive a score of zero.
    """
    directory = Path(data_dir) if data_dir is not None else DEFAULT_DATA_DIR
    wells = _load_records(directory, "wells.json")
    formations = _load_records(directory, "formation_intervals.json")
    samples = _load_records(directory, "drilling_samples.json")
    events = _load_records(directory, "drilling_events.json")

    well_by_id = {well.get("well_id"): well for well in wells}
    active = well_by_id.get(active_well_id)
    if active is None:
        raise WellNotFoundError(f"Unknown well_id: {active_well_id}")
    if active.get("well_role") != "active":
        raise ValueError(f"well_id is not an active well: {active_well_id}")

    active_formation = _current_formation(active, formations)
    results = []
    for candidate in wells:
        if candidate.get("well_role") != "historical_offset":
            continue
        result = _score_candidate(active, candidate, active_formation, formations, samples, events)
        results.append(result)

    results.sort(
        key=lambda item: (
            -item["similarity_score"],
            item["distance"] if item["distance"] is not None else math.inf,
            item["well_id"],
        )
    )
    return results[:limit] if limit is not None else results


def _score_candidate(
    active: dict[str, Any],
    candidate: dict[str, Any],
    active_formation: str | None,
    formations: list[dict[str, Any]],
    samples: list[dict[str, Any]],
    events: list[dict[str, Any]],
) -> dict[str, Any]:
    formation_score = _formation_score(active, candidate, active_formation)
    trajectory_score = _trajectory_score(active, candidate)
    distance_km, proximity_score = _proximity_score(active, candidate)
    depth_score = _depth_score(active, candidate)
    drilling_score = _drilling_score(active, candidate, active_formation, formations, samples)

    components = {
        "formation": formation_score,
        "trajectory": trajectory_score,
        "proximity": proximity_score,
        "depth": depth_score,
        "drilling_characteristics": drilling_score,
    }
    available_weight = sum(WEIGHTS[name] for name, score in components.items() if score is not None)
    weighted_score = (
        sum(WEIGHTS[name] * score for name, score in components.items() if score is not None)
        / available_weight
        if available_weight
        else 0.0
    )
    matching_features = _matching_features(components, active_formation)
    relevant_events = [
        {
            "event_id": event["event_id"],
            "event_type": event["event_type"],
            "severity": event["severity"],
            "interval_md_m": event["interval_md_m"],
            "evidence_ids": event["evidence_ids"],
        }
        for event in events
        if event.get("well_id") == candidate.get("well_id")
        and (active_formation is None or event.get("formation_name") == active_formation)
    ]
    return {
        "well_id": candidate["well_id"],
        "similarity_score": round(weighted_score * 100, 2),
        "distance": round(distance_km, 2) if distance_km is not None else None,
        "distance_unit": "km",
        "formation": active_formation,
        "matching_features": matching_features,
        "relevant_historical_events": relevant_events,
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


def _current_formation(well: dict[str, Any], formations: list[dict[str, Any]]) -> str | None:
    current_depth = well.get("current_md_m")
    if current_depth is None:
        return well.get("matching_features", {}).get("target_formation")
    for interval in formations:
        if (
            interval.get("well_id") == well.get("well_id")
            and interval.get("top_md_m", math.inf) <= current_depth <= interval.get("base_md_m", -math.inf)
        ):
            return interval.get("formation_name")
    return well.get("matching_features", {}).get("target_formation")


def _formation_score(active: dict[str, Any], candidate: dict[str, Any], active_formation: str | None) -> float | None:
    candidate_formation = candidate.get("matching_features", {}).get("target_formation")
    if active_formation is None or candidate_formation is None:
        return None
    return 1.0 if active_formation == candidate_formation else 0.0


def _trajectory_score(active: dict[str, Any], candidate: dict[str, Any]) -> float | None:
    left, right = active.get("trajectory"), candidate.get("trajectory")
    if not isinstance(left, dict) or not isinstance(right, dict):
        return None
    profile = 1.0 if left.get("profile") == right.get("profile") else 0.0
    inclination = _linear_similarity(left.get("max_inclination_deg"), right.get("max_inclination_deg"), 45.0)
    azimuth = _azimuth_similarity(left.get("azimuth_deg"), right.get("azimuth_deg"))
    available = [score for score in (inclination, azimuth) if score is not None]
    if not available:
        return profile
    return 0.5 * profile + 0.5 * (sum(available) / len(available))


def _proximity_score(active: dict[str, Any], candidate: dict[str, Any]) -> tuple[float | None, float | None]:
    active_location, candidate_location = active.get("location"), candidate.get("location")
    if not isinstance(active_location, dict) or not isinstance(candidate_location, dict):
        return None, None
    values = (
        active_location.get("latitude"), active_location.get("longitude"),
        candidate_location.get("latitude"), candidate_location.get("longitude"),
    )
    if any(value is None for value in values):
        return None, None
    distance = _haversine_km(*values)
    return distance, max(0.0, 1.0 - distance / PROXIMITY_CUTOFF_KM)


def _depth_score(active: dict[str, Any], candidate: dict[str, Any]) -> float | None:
    left = active.get("matching_features", {}).get("planned_target_depth_md_m")
    right = candidate.get("matching_features", {}).get("planned_target_depth_md_m")
    if left is None or right is None:
        return None
    return _linear_similarity(float(left), float(right), 500.0)


def _drilling_score(
    active: dict[str, Any], candidate: dict[str, Any], formation_name: str | None,
    formations: list[dict[str, Any]], samples: list[dict[str, Any]],
) -> float | None:
    if formation_name is None:
        return None
    active_sample = _nearest_sample(active, formation_name, formations, samples, active.get("current_md_m"))
    candidate_sample = _nearest_equivalent_sample(active, candidate, formation_name, formations, samples)
    if active_sample is None or candidate_sample is None:
        return None
    tolerances = {
        "rop_m_per_hr": 12.0,
        "wob_klbf": 5.0,
        "rpm": 25.0,
        "torque_klbf_ft": 10.0,
        "mud_weight_sg": 0.15,
        "standpipe_pressure_bar": 40.0,
    }
    feature_scores = [
        _linear_similarity(active_sample.get(field), candidate_sample.get(field), tolerance)
        for field, tolerance in tolerances.items()
    ]
    available = [score for score in feature_scores if score is not None]
    return sum(available) / len(available) if available else None


def _nearest_equivalent_sample(active, candidate, formation_name, formations, samples):
    active_interval = _formation_interval(active["well_id"], formation_name, formations)
    candidate_interval = _formation_interval(candidate["well_id"], formation_name, formations)
    current_depth = active.get("current_md_m")
    if active_interval is None or candidate_interval is None or current_depth is None:
        return None
    active_span = active_interval["base_md_m"] - active_interval["top_md_m"]
    if active_span <= 0:
        return None
    fraction = (current_depth - active_interval["top_md_m"]) / active_span
    target_depth = candidate_interval["top_md_m"] + fraction * (candidate_interval["base_md_m"] - candidate_interval["top_md_m"])
    return _nearest_sample(candidate, formation_name, formations, samples, target_depth)


def _nearest_sample(well, formation_name, formations, samples, target_depth):
    interval = _formation_interval(well["well_id"], formation_name, formations)
    if interval is None or target_depth is None:
        return None
    candidates = [
        sample for sample in samples
        if sample.get("well_id") == well["well_id"]
        and interval["top_md_m"] <= sample.get("md_m", -math.inf) <= interval["base_md_m"]
    ]
    return min(candidates, key=lambda sample: abs(sample["md_m"] - target_depth), default=None)


def _formation_interval(well_id, formation_name, formations):
    return next((item for item in formations if item.get("well_id") == well_id and item.get("formation_name") == formation_name), None)


def _linear_similarity(left: float | None, right: float | None, tolerance: float) -> float | None:
    if left is None or right is None:
        return None
    return max(0.0, 1.0 - abs(float(left) - float(right)) / tolerance)


def _azimuth_similarity(left: float | None, right: float | None) -> float | None:
    if left is None or right is None:
        return None
    difference = abs((float(left) - float(right) + 180.0) % 360.0 - 180.0)
    return 1.0 - difference / 180.0


def _haversine_km(lat_a: float, lon_a: float, lat_b: float, lon_b: float) -> float:
    radius_km = 6371.0088
    lat_delta = math.radians(lat_b - lat_a)
    lon_delta = math.radians(lon_b - lon_a)
    value = math.sin(lat_delta / 2) ** 2 + math.cos(math.radians(lat_a)) * math.cos(math.radians(lat_b)) * math.sin(lon_delta / 2) ** 2
    return 2 * radius_km * math.asin(math.sqrt(value))


def _matching_features(components: dict[str, float | None], formation_name: str | None) -> list[dict[str, Any]]:
    labels = {
        "formation": f"Current formation: {formation_name or 'unavailable'}",
        "trajectory": "Trajectory profile, inclination, and azimuth",
        "proximity": f"Geographic proximity (linear decline to 0 at {PROXIMITY_CUTOFF_KM:g} km)",
        "depth": "Planned target-depth similarity (500 m tolerance)",
        "drilling_characteristics": "Comparable formation-relative drilling measurements",
    }
    return [
        {
            "feature": name,
            "score": round(score * 100, 2) if score is not None else None,
            "weight": WEIGHTS[name],
            "status": "included" if score is not None else "unavailable_excluded_from_score",
            "explanation": labels[name],
        }
        for name, score in components.items()
    ]
