from fastapi import FastAPI
from backend.services.pipeline import run_full_pipeline

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok"}


@app.get("/dashboard/{persona}")
def dashboard(persona: str):
    return run_full_pipeline(persona)