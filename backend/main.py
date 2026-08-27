from fastapi import FastAPI

app = FastAPI(
    title="AROH API",
    description="Adaptive Reservoir & Offset Intelligence Hub",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "name": "AROH",
        "status": "online",
        "message": "AROH drilling intelligence API is running",
    }


@app.get("/api/health")
def health():
    return {
        "status": "healthy"
    }