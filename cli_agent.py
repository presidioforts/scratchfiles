import argparse
import requests
import json
import os

API_BASE = "http://localhost:8000"

def list_use_cases():
    print("Available use cases:")
    for f in os.listdir("use_cases"):
        if f.endswith(".json"):
            print(" -", f.replace(".json", ""))

def status(use_case_name):
    res = requests.get(f"{API_BASE}/status/{use_case_name}")
    print(json.dumps(res.json(), indent=2))

def train(use_case_name):
    with open(f"use_cases/{use_case_name}.json") as f:
        use_case = json.load(f)
    payload = {
        "use_case_name": use_case_name,
        "data": use_case["data"],
        "model": use_case["model"]
    }
    res = requests.post(f"{API_BASE}/train", json=payload)
    print(res.json())

def retrain(use_case_name):
    res = requests.post(f"{API_BASE}/retrain/{use_case_name}")
    print(res.json())

def predict(use_case_name, text):
    payload = {
        "use_case_name": use_case_name,
        "input": text
    }
    res = requests.post(f"{API_BASE}/predict", json=payload)
    print(res.json())

def main():
    parser = argparse.ArgumentParser(description="Agentic CLI Interface")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("list")
    
    s = sub.add_parser("status")
    s.add_argument("use_case")

    t = sub.add_parser("train")
    t.add_argument("use_case")

    rt = sub.add_parser("retrain")
    rt.add_argument("use_case")

    p = sub.add_parser("predict")
    p.add_argument("use_case")
    p.add_argument("text")

    args = parser.parse_args()

    if args.cmd == "list":
        list_use_cases()
    elif args.cmd == "status":
        status(args.use_case)
    elif args.cmd == "train":
        train(args.use_case)
    elif args.cmd == "retrain":
        retrain(args.use_case)
    elif args.cmd == "predict":
        predict(args.use_case, args.text)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()