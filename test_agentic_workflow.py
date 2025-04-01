import requests
import json
import os
from datetime import datetime

API_BASE = "http://localhost:8000"

def test_ci_cd_workflow():
    print("\n=== Testing CI/CD Build Failures Workflow ===\n")
    
    # Test data
    use_case_name = "ci_cd_build_failures"
    test_data = {
        "use_case_name": use_case_name,
        "data": [
            {"input": "Build failed due to compilation errors in src/main.cpp", "label": "compilation_error"},
            {"input": "Pipeline failed: Unit tests failed in test_suite.py", "label": "test_failure"},
            {"input": "Docker build failed: Unable to resolve dependencies", "label": "dependency_error"},
            {"input": "Deployment failed: Insufficient memory in production environment", "label": "resource_error"}
        ],
        "model": "mock-model"
    }

    # Step 1: Validate use case
    print("1. Validating use case...")
    response = requests.post(f"{API_BASE}/validate", json=test_data)
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200, "Validation failed"

    # Step 2: Train the model
    print("\n2. Training model...")
    response = requests.post(f"{API_BASE}/train", json=test_data)
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200, "Training failed"
    assert response.json()["status"] == "trained", "Training status incorrect"

    # Step 3: Check status
    print("\n3. Checking model status...")
    response = requests.get(f"{API_BASE}/status/{use_case_name}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200, "Status check failed"
    assert response.json()["trained"] == True, "Model not marked as trained"

    # Step 4: Generate synthetic data
    print("\n4. Generating synthetic data...")
    response = requests.get(f"{API_BASE}/generate-synthetic/{use_case_name}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200, "Synthetic data generation failed"
    assert "synthetic" in response.json(), "No synthetic data generated"

    # Step 5: Retrain with synthetic data
    print("\n5. Retraining with synthetic data...")
    response = requests.post(f"{API_BASE}/retrain/{use_case_name}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200, "Retraining failed"
    assert response.json()["status"] == "retrained", "Retraining status incorrect"

    # Step 6: Make predictions
    print("\n6. Testing predictions...")
    test_inputs = [
        "Build failed due to compilation errors",
        "Pipeline failed: Unit tests failed",
        "Docker build failed: Dependencies missing"
    ]
    
    for input_text in test_inputs:
        print(f"\nPredicting for: {input_text}")
        response = requests.post(f"{API_BASE}/predict", json={
            "use_case_name": use_case_name,
            "input": input_text
        })
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        assert response.status_code == 200, f"Prediction failed for: {input_text}"
        assert "label" in response.json(), "No label in prediction response"
        assert "score" in response.json(), "No score in prediction response"

    print("\n=== All tests passed successfully! ===")

def test_error_handling():
    print("\n=== Testing Error Handling ===\n")
    
    # Test invalid use case
    print("1. Testing invalid use case...")
    response = requests.get(f"{API_BASE}/status/nonexistent_use_case")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.json()["trained"] == False, "Invalid use case should return untrained status"

    # Test prediction without training
    print("\n2. Testing prediction without training...")
    response = requests.post(f"{API_BASE}/predict", json={
        "use_case_name": "untrained_case",
        "input": "Test input"
    })
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200, "Prediction should still work with mock implementation"

    print("\n=== Error handling tests passed! ===")

if __name__ == "__main__":
    print("Starting Agentic Workflow Tests...")
    test_ci_cd_workflow()
    test_error_handling()
    print("\nAll tests completed!") 