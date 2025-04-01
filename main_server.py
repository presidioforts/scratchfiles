# FastAPI + Mocked Agentic Enhancements

from fastapi import FastAPI, Request
from pydantic import BaseModel
import os, json, time
from typing import List, Dict
from datetime import datetime
import random
import logging

app = FastAPI()

USE_CASE_DIR = "./use_cases"
LOG_FILE = "agentic_training.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def log_action(action: str, details: dict):
    logging.info(f"{action.upper()} - {json.dumps(details)}")

class PredictRequest(BaseModel):
    use_case_name: str
    input: str

class TrainRequest(BaseModel):
    use_case_name: str
    data: List[Dict[str, str]]
    model: str

@app.post("/validate")
def validate_use_case(req: TrainRequest):
    path = f"{USE_CASE_DIR}/{req.use_case_name}.json"
    if not os.path.exists(path):
        log_action("validate", {"use_case": req.use_case_name, "status": "new"})
        return {"status": "new", "message": "Use case not found. Training required."}
    with open(path, "r") as f:
        meta = json.load(f)
    log_action("validate", {"use_case": req.use_case_name, "status": "existing"})
    return {"status": "existing", "trained": meta.get("trained", False), "last_updated": meta.get("last_updated")}

@app.post("/train")
def train(req: TrainRequest):
    # Mock training response
    mock_response = {
        "status": "trained",
        "vector_count": len(req.data),
        "model": req.model,
        "accuracy": 0.95,
        "training_time": "2.5s"
    }
    
    use_case_meta = {
        "trained": True,
        "model": req.model,
        "accuracy": 0.95,
        "last_updated": datetime.utcnow().isoformat(),
        "data": req.data
    }
    
    os.makedirs(USE_CASE_DIR, exist_ok=True)
    with open(f"{USE_CASE_DIR}/{req.use_case_name}.json", "w") as f:
        json.dump(use_case_meta, f)

    log_action("train", {"use_case": req.use_case_name, "records": len(req.data)})
    return mock_response

@app.post("/retrain/{use_case_name}")
def retrain_with_synthetic(use_case_name: str):
    path = f"{USE_CASE_DIR}/{use_case_name}.json"
    if not os.path.exists(path):
        return {"error": "Use case not found"}
    
    with open(path, 'r') as f:
        meta = json.load(f)
    
    # Mock synthetic data generation
    base_data = meta.get("data", [])
    synthetic_count = len(base_data) * 2
    
    mock_response = {
        "status": "retrained",
        "original_records": len(base_data),
        "synthetic_records": synthetic_count,
        "total_records": len(base_data) + synthetic_count,
        "accuracy": 0.97
    }
    
    log_action("retrain", {"use_case": use_case_name, "real": len(base_data), "synthetic": synthetic_count})
    return mock_response

@app.post("/predict")
def predict(req: PredictRequest):
    # Mock prediction response
    mock_labels = ["compilation_error", "test_failure", "dependency_error", "resource_error"]
    mock_response = {
        "label": random.choice(mock_labels),
        "score": round(random.uniform(0.7, 0.99), 3),
        "confidence": "high"
    }
    
    log_action("predict", {"use_case": req.use_case_name, "input": req.input, "result": mock_response})
    return mock_response

@app.get("/status/{use_case_name}")
def get_status(use_case_name: str):
    path = f"{USE_CASE_DIR}/{use_case_name}.json"
    if not os.path.exists(path):
        return {"trained": False}
    
    with open(path, 'r') as f:
        meta = json.load(f)
    
    # Add some mock metrics
    mock_status = {
        "trained": meta.get("trained", False),
        "model": meta.get("model", "mock-model"),
        "accuracy": round(random.uniform(0.85, 0.98), 3),
        "last_updated": meta.get("last_updated"),
        "total_predictions": random.randint(100, 1000),
        "success_rate": round(random.uniform(0.9, 0.99), 3)
    }
    
    return mock_status

@app.get("/generate-synthetic/{use_case_name}")
def generate_synthetic(use_case_name: str):
    path = f"{USE_CASE_DIR}/{use_case_name}.json"
    if not os.path.exists(path):
        return {"error": "Use case not found"}
    
    with open(path, 'r') as f:
        meta = json.load(f)

    base_data = meta.get("data", [])
    synthetic_data = []
    
    # Generate mock synthetic data
    for d in base_data:
        text = d["input"]
        label = d["label"]
        variations = [
            text + "...",
            text.replace("failed", "did not complete"),
            text.replace("error", "issue"),
            text.upper(),
            f"[LOG] {text}"
        ]
        synthetic_data.extend([{"input": v, "label": label} for v in random.sample(variations, 2)])

    mock_response = {
        "synthetic": synthetic_data,
        "count": len(synthetic_data),
        "quality_score": round(random.uniform(0.8, 0.95), 3)
    }
    
    log_action("generate-synthetic", {"use_case": use_case_name, "count": len(synthetic_data)})
    return mock_response
