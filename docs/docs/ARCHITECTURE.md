# AROH Architecture

## Prototype Architecture

                    FRONTEND
                        |
                        v
                     FastAPI
                        |
        +---------------+---------------+
        |               |               |
        v               v               v
      Wells           Risk           Evidence
        |               |               |
        +---------------+---------------+
                        |
                        v
                  Prototype Data

AI Layer:

Documents
    ↓
Extraction
    ↓
Structured Events
    ↓
Well Knowledge
    ↓
Analogue Engine
    ↓
Risk Engine
    ↓
Evidence Retrieval
    ↓
AI Copilot

---

# Production Target

Frontend
    ↓
API Gateway
    ↓
FastAPI Services
    ↓
PostgreSQL
    ↓
PostGIS
    ↓
TimescaleDB
    ↓
pgvector

External/Existing Systems:

OIL eRTMAC
    ↓
Integration Adapter
    ↓
AROH

---

# Frontend

React
TypeScript
Vite
Tailwind CSS
MapLibre
Apache ECharts

---

# Backend

Python
FastAPI
Pydantic

---

# AI/ML

Python
Pandas
NumPy
scikit-learn
XGBoost/LightGBM

---

# Document Intelligence

PDF extraction
OCR
Table extraction
NLP
Entity extraction
Event extraction

---

# Prototype Principle

Keep the prototype simple.

Do not introduce unnecessary production infrastructure
during the SIH prototype build.
