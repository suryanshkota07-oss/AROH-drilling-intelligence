# AROH

## Adaptive Reservoir & Offset Intelligence Hub

### SIH Problem Statement

SIH26121 — eRTMAC-NWIS

Organization:
Oil India Limited

---

# 1. PURPOSE

AROH is an AI-assisted offset-well intelligence and drilling
decision-support platform designed to work alongside OIL's
existing real-time drilling monitoring ecosystem.

The system provides an institutional memory of historical
drilling operations.

---

# 2. PROBLEM

Historical drilling knowledge can exist across:

- Well Completion Reports
- Daily Drilling Reports
- Mud logging records
- Drilling databases
- Geological information
- Reservoir information
- Casing records
- Cementing records
- Operational event records
- Individual engineering experience

Finding relevant historical information can be slow.

---

# 3. CORE IDEA

AROH connects historical well knowledge with the active well.

It answers:

1. Which wells are actually analogous to the current well?
2. What happened at the corresponding formation/depth?
3. What worked or failed historically?
4. Is the current well approaching a similar risk?

---

# 4. CORE FEATURES

## Command Center

Shows:

- active wells
- current depth
- drilling status
- risk alerts
- data health

## Active Well

Shows:

- drilling parameters
- depth
- formation
- pressure
- trajectory
- current status

## Offset Explorer

Shows:

- nearby wells
- analogous wells
- distance
- similarity score
- formation

## Well DNA

Creates a structured profile of each well.

## Depth Correlation

Aligns current and historical wells by:

- depth
- formation
- drilling events

## Risk Ahead

Identifies historical patterns that may indicate
a potential upcoming drilling risk.

## Evidence

Every major prediction should show:

- supporting wells
- historical events
- depth
- source document
- confidence

## Knowledge Library

Search historical drilling knowledge.

## AI Copilot

Allows engineers to ask questions about:

- wells
- events
- formations
- historical experience
- mitigation outcomes

Answers should use evidence.

## Real-Time Simulation

Prototype simulates an active drilling stream.

---

# 5. CORE DIFFERENTIATOR

AROH is not simply:

- a map
- a dashboard
- a chatbot
- a document search engine
- a generic ML model

Its core workflow is:

Historical Wells
      ↓
Well DNA
      ↓
Analogue Matching
      ↓
Depth/Formation Correlation
      ↓
Historical Events
      ↓
Current Well
      ↓
Risk Ahead
      ↓
Evidence
      ↓
Decision Support

---

# 6. PROTOTYPE DATA

The SIH prototype will use public and/or synthetic
demonstration data.

The prototype must never claim that synthetic data
is actual OIL operational data.

Production architecture should support integration with
authorized OIL data sources.

---

# 7. SAFETY

AROH is a decision-support system.

It does not autonomously control drilling equipment.

The system should provide evidence and uncertainty
rather than presenting predictions as guaranteed facts.
