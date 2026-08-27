# AROH synthetic demonstration dataset

All records in this directory are **synthetic demonstration data** created for
the AROH SIH prototype. They do not represent Oil India Limited wells,
operations, measurements, events, or recommendations.

## Files

| File | Purpose |
| --- | --- |
| `wells.json` | Active and historical offset well profiles, locations, trajectories, and matching features. |
| `formation_intervals.json` | Formation tops and bases by well and measured depth. |
| `drilling_samples.json` | Sparse depth-indexed drilling measurements for the demonstration wells. |
| `drilling_events.json` | Historical operational events, mitigation, and outcomes. |
| `evidence_records.json` | Synthetic source records backing each historical event. |
| `drilling_scenarios.json` | Simulated active-well telemetry sequence for the later WebSocket demonstration. |

## Data model and relationships

`well_id` is the primary identifier. Formation intervals, drilling samples,
events, and telemetry scenarios reference it. `event_id` identifies a
historical event; its `evidence_ids` reference the supporting entries in
`evidence_records.json`.

Every record carries `data_classification: "synthetic_demo"`. Coordinates,
well names, measurements, and outcomes are invented solely for a software
demonstration.

## Support for later intelligence features

Analogue matching can compare the `matching_features` in `wells.json`:
spatial proximity, target formation, trajectory profile, total depth, and
section type. Formation intervals make depth comparisons formation-aware
rather than relying on raw measured depth alone.

Risk scoring can correlate the active scenario's depth and drilling samples
with historical events in the same formation. Any future risk result must cite
the contributing `event_id` values and their evidence records, and must be
labelled as a synthetic decision-support estimate.

## Demonstration scenario

`AROH-ACT-01` is a synthetic active directional well at 2,870 m MD in the
synthetic Boka Sand formation. Its simulated stream progresses toward
2,900–2,930 m MD, where two comparable synthetic offset wells recorded
lost-circulation events. The eventual demo should show the historical records,
their mitigations, and confidence/uncertainty before presenting any risk-ahead
message. This dataset itself makes no prediction.
