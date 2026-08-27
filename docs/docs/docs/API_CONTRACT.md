# AROH API Contract

## GET /api/wells

Return available wells.

---

## GET /api/wells/{well_id}

Return detailed information about a well.

---

## GET /api/wells/{well_id}/analogues

Return historically/geologically similar wells.

Response should include:

- well_id
- similarity_score
- distance
- formation
- reasons_for_similarity

---

## GET /api/wells/{well_id}/events

Return historical events.

---

## GET /api/risk/{well_id}

Return current risk information.

Response:

- risk_score
- severity
- event_type
- risk_interval
- confidence
- evidence_count

---

## GET /api/risk/{well_id}/timeline

Return risk scores across depth.

---

## GET /api/evidence/{event_id}

Return evidence supporting an event/prediction.

---

## WebSocket

/ws/drilling/{well_id}

Used for simulated real-time drilling data.

Example:

{
  "depth": 2930,
  "rop": 31.8,
  "wob": 14.2,
  "rpm": 81,
  "torque": 22.4,
  "mud_weight": 1.18
}
