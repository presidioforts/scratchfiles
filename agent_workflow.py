# agent_workflow.py

import requests
import json
import os

API = "http://localhost:8000"

class AgenticTrainer:
    def __init__(self, use_case_name):
        self.use_case = use_case_name

    def validate(self):
        res = requests.post(f"{API}/validate", json={"use_case_name": self.use_case, "data": [], "model": ""})
        status = res.json()
        print(f"[VALIDATE] {self.use_case} => {status}")
        return status.get("status")

    def train(self):
        with open(f"use_cases/{self.use_case}.json") as f:
            meta = json.load(f)
        res = requests.post(f"{API}/train", json={
            "use_case_name": self.use_case,
            "data": meta["data"],
            "model": meta["model"]
        })
        print(f"[TRAIN] Result => {res.json()}")
        return res.json()

    def retrain(self):
        res = requests.post(f"{API}/retrain/{self.use_case}")
        print(f"[RETRAIN] Result => {res.json()}")
        return res.json()

    def predict(self, user_input: str):
        res = requests.post(f"{API}/predict", json={
            "use_case_name": self.use_case,
            "input": user_input
        })
        print(f"[PREDICT] '{user_input}' => {res.json()}")
        return res.json()

    def synthetic_data_preview(self):
        res = requests.get(f"{API}/generate-synthetic/{self.use_case}")
        synthetic = res.json()
        print(f"[SYNTHETIC PREVIEW] Generated {synthetic['count']} items")
        return synthetic

    def status(self):
        res = requests.get(f"{API}/status/{self.use_case}")
        print(f"[STATUS] => {json.dumps(res.json(), indent=2)}")
        return res.json()

# Example Flow
if __name__ == "__main__":
    use_case = input("Enter use case name: ").strip()
    agent = AgenticTrainer(use_case)

    if agent.validate() == "new":
        agent.train()
    else:
        agent.status()

    preview = input("Preview synthetic data before retrain? (y/n): ").strip().lower()
    if preview == 'y':
        agent.synthetic_data_preview()

    retrain = input("Proceed with retraining on synthetic data? (y/n): ").strip().lower()
    if retrain == 'y':
        agent.retrain()

    while True:
        user_input = input("\nEnter input for prediction (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        agent.predict(user_input)