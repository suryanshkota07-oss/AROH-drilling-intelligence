"""Dataset-backed evidence retrieval for AROH Risk Ahead assessments."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from ai.analogue_matching import DEFAULT_DATA_DIR, DatasetError
from ai.risk_ahead import DEPTH_HORIZON_M, assess_risks


def retrieve_evidence(
    active_well_id: str, data_dir: Path | str | None = None
) -> list[dict[str, Any]]:
    """Retrieve dataset records that support each current risk-ahead result.

    An item is emitted only when the risk's supporting event, well, and
    evidence record all agree. No text is generated and no evidence is inferred
    when a source record is absent.
    """
    directory = Path(data_dir) if data_dir is not None else DEFAULT_DATA_DIR
    risks = assess_risks(active_well_id, data_dir=directory)
    events = {item.get("event_id"): item for item in _load_records(directory, "drilling_events.json")}
    evidence = {item.get("evidence_id"): item for item in _load_records(directory, "evidence_records.json")}
    wells = {item.get("well_id"): item for item in _load_records(directory, "wells.json")}
    current_depth = wells[active_well_id].get("current_md_m")

    records: list[dict[str, Any]] = []
    for risk in risks:
        for support in risk["supporting_wells"]:
            event = events.get(support["historical_event_id"])
            if event is None or event.get("well_id") != support["well_id"]:
                continue
            for evidence_id in support["evidence_ids"]:
                source = evidence.get(evidence_id)
                if not _is_valid_source(source, event, support["well_id"]):
                    continue
                records.append(
                    {
                        "well_id": support["well_id"],
                        "event_id": event["event_id"],
                        "event_type": event["event_type"],
                        "event_depth": event["interval_md_m"],
                        "formation": event["formation_name"],
                        "severity": event["severity"],
                        "relevance_score": _relevance_score(risk, support, current_depth),
                        "evidence_id": source["evidence_id"],
                        "source_record_id": source["source_record_id"],
                        "source_type": source["source_type"],
                        "source_summary": source["summary"],
                        "mapped_event_depth": support["mapped_interval_md_m"],
                        "risk_score": risk["risk_score"],
                        "data_classification": "synthetic_demo",
                    }
                )
    return sorted(records, key=lambda item: (-item["relevance_score"], item["well_id"], item["event_id"]))


def build_risk_explanations(
    active_well_id: str, data_dir: Path | str | None = None
) -> list[dict[str, Any]]:
    """Create UI-ready, source-grounded `WHY THIS RISK?` groupings."""
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in retrieve_evidence(active_well_id, data_dir=data_dir):
        grouped[record["event_type"]].append(record)

    explanations = []
    for event_type, records in grouped.items():
        wells = sorted({record["well_id"] for record in records})
        formation = records[0]["formation"]
        explanations.append(
            {
                "event_type": event_type,
                "supporting_wells": wells,
                "historical_pattern": (
                    f"{len(records)} evidence-backed historical {event_type} event(s) in "
                    f"the similar {formation} formation/depth interval."
                ),
                "evidence": records,
                "data_classification": "synthetic_demo",
            }
        )
    return sorted(explanations, key=lambda item: item["event_type"])


def _load_records(directory: Path, filename: str) -> list[dict[str, Any]]:
    try:
        with (directory / filename).open(encoding="utf-8") as data_file:
            records = json.load(data_file)
    except (OSError, json.JSONDecodeError) as error:
        raise DatasetError(f"Unable to load {filename}: {error}") from error
    if not isinstance(records, list):
        raise DatasetError(f"{filename} must contain a JSON list")
    return records


def _is_valid_source(source: dict[str, Any] | None, event: dict[str, Any], well_id: str) -> bool:
    return bool(
        source
        and source.get("event_id") == event.get("event_id")
        and source.get("well_id") == well_id
        and source.get("data_classification") == "synthetic_demo"
    )


def _relevance_score(risk: dict[str, Any], support: dict[str, Any], current_depth: float | None) -> float:
    mapped_start = support["mapped_interval_md_m"]["start_md_m"]
    if current_depth is None or mapped_start <= current_depth:
        depth_proximity = 1.0
    else:
        depth_proximity = max(0.0, 1.0 - (mapped_start - current_depth) / DEPTH_HORIZON_M)
    score = (
        0.60 * risk["risk_score"]
        + 0.25 * support["analogue_similarity_score"]
        + 0.15 * depth_proximity * 100
    )
    return round(score, 2)
