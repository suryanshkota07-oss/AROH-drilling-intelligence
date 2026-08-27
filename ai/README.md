# AROH analogue matching

`analogue_matching.py` ranks synthetic historical offsets without an LLM.
The score is a weighted mean of formation (30%), trajectory (25%), proximity
(20%), planned depth (15%), and comparable drilling characteristics (10%).
Missing input excludes that weight; it is never silently interpreted as a
match. Known mismatches score zero.

Outputs are synthetic demonstration decision-support data. They contain the
individual feature scores, calculation explanations, and the relevant
historical event/evidence identifiers required by later risk scoring.

Run the tests from the repository root:

```bash
python -m unittest discover -s ai/tests -v
```

## Risk Ahead

`risk_ahead.py` groups evidence-backed historical events from formation-matched
analogues. It scores each event type using analogue similarity (35%), historical
event frequency (20%), formation similarity (20%), formation-normalized depth
proximity (15%), and comparable drilling-parameter similarity (10%).

The result includes every historical event ID, mapped depth interval, and
evidence ID used in the assessment. Missing factors are disclosed and excluded
from the weighted score. Outputs remain synthetic demonstration estimates and
must not be treated as operational fact or autonomous drilling guidance.

## Evidence Retrieval

`evidence_retrieval.py` follows the event and evidence IDs emitted by Risk
Ahead back to `data/drilling_events.json` and `data/evidence_records.json`.
It returns only source-validated records and exposes well, event, formation,
severity, historical depth, and relevance score. `build_risk_explanations()`
groups those records for a UI's **WHY THIS RISK?** view, including supporting
wells and a source-grounded historical-pattern statement.
