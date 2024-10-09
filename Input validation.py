I see, let's make sure everything is handled correctly for the input validation.

The error you're seeing ("Features and label are required") suggests that the input validation is failing because it’s not detecting the correct keys in the payload (log_entries and labels). Let's double-check and ensure that the input validation checks for the correct fields.

Updated Validation Logic:

Let me refine the validation logic to ensure that the required fields (log_entries and labels) are correctly identified and handled.

Updated Source Code (Fixing Input Validation):

from fastapi import FastAPI, HTTPException
import uvicorn
import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import threading
import os
import logging
import pickle

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Global variables
model = None
vectorizer = CountVectorizer()
model_lock = threading.Lock()
model_file = 'model.txt'
vectorizer_file = 'vectorizer.pkl'

# Mock data (for initial training)
data = {
    'log_entry': [
        "ERROR: Authentication failed for 'https://github.com/your-repo/your-project.git'",
        "ERROR: Could not read Username for 'https://github.com': terminal prompts disabled.",
        "ERROR: Could not resolve host: github.com",
        "ERROR: Repository not found.",
        "ERROR: Authentication failed for 'https://github.com/your-repo/your-project.git'"
    ],
    'label': [1, 1, 2, 3, 1],  # Labels corresponding to error types
    'suggested_fix': [
        "Update the GitHub token in the Jenkins credentials or verify the SSH key configuration.",
        "Update the GitHub token in the Jenkins credentials or verify the SSH key configuration.",
        "Check your network connection or DNS settings.",
        "Verify the repository URL and your access rights to the repository.",
        "Update the GitHub token in the Jenkins credentials or verify the SSH key configuration."
    ]
}

# Initialize the model and vectorizer
def initialize_model():
    global model, vectorizer
    if os.path.exists(model_file) and os.path.exists(vectorizer_file):
        try:
            model = lgb.Booster(model_file=model_file)
            with open(vectorizer_file, 'rb') as f:
                vectorizer = pickle.load(f)
            logging.info(f"Model and vectorizer loaded from {model_file} and {vectorizer_file}")
        except Exception as e:
            logging.error(f"Failed to load model/vectorizer: {e}")
            model = create_new_model()
    else:
        model = create_new_model()

# Create a new model and vectorizer
def create_new_model():
    global vectorizer

    df = pd.DataFrame(data)
    X = df['log_entry']
    y = df['label']

    # Fit vectorizer with initial data
    X = vectorizer.fit_transform(X).astype(np.float32)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Prepare the data for LightGBM
    train_data = lgb.Dataset(X_train, label=y_train)
    test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

    # Set the parameters for the LightGBM model
    params = {
        'objective': 'multiclass',
        'num_class': 4,  # Number of distinct error types
        'metric': 'multi_logloss',
        'boosting_type': 'gbdt',
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.9
    }

    # Train the model
    callbacks = [lgb.early_stopping(stopping_rounds=10)]
    model = lgb.train(params, train_data, valid_sets=[test_data], num_boost_round=100, callbacks=callbacks)

    # Save the model and vectorizer
    model.save_model(model_file)
    with open(vectorizer_file, 'wb') as f:
        pickle.dump(vectorizer, f)
    logging.info(f"New model and vectorizer created and saved.")

    return model

# Initialize model and vectorizer on startup
initialize_model()

@app.post("/train")
async def train_model(request: dict):
    global model, vectorizer

    # Input validation
    log_entries = request.get('log_entries')
    labels = request.get('labels')

    if log_entries is None or labels is None:
        raise HTTPException(status_code=400, detail="Log entries and labels are required.")

    if len(log_entries) != len(labels):
        raise HTTPException(status_code=400, detail="Log entries and labels must have the same length.")

    # Convert to DataFrame
    new_data = pd.DataFrame({'log_entry': log_entries, 'label': labels})

    with model_lock:
        try:
            # Update the vectorizer with the new data
            X_new = vectorizer.fit_transform(new_data['log_entry']).astype(np.float32)

            # Prepare LightGBM dataset
            new_train_data = lgb.Dataset(X_new, label=new_data['label'], free_raw_data=False)

            # Incrementally train the existing model
            model = lgb.train(
                model.params,
                new_train_data,
                num_boost_round=10,  # Adjust this based on the amount of new data
                init_model=model,
                keep_training_booster=True
            )

            # Save the updated model and vectorizer
            model.save_model(model_file)
            with open(vectorizer_file, 'wb') as f:
                pickle.dump(vectorizer, f)

            logging.info("Model and vectorizer trained and saved successfully.")
        except Exception as e:
            logging.error(f"Failed to train or save the model/vectorizer: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to train or save the model/vectorizer: {e}")

    return {"status": "success", "message": "Model and vectorizer trained and saved successfully."}

@app.post("/predict")
async def predict(request: dict):
    global model, vectorizer

    log_entry = request.get('log_entry')

    if log_entry is None:
        raise HTTPException(status_code=400, detail="Log entry is required.")

    with model_lock:
        try:
            # Vectorize the new log entry
            user_input_vectorized = vectorizer.transform([log_entry]).astype(np.float32)
            new_prediction = model.predict(user_input_vectorized)
            predicted_label = list(new_prediction[0]).index(max(new_prediction[0]))

            # Return the predicted label and suggested fix
            suggested_fix = data['suggested_fix'][predicted_label]
        except Exception as e:
            logging.error(f"Prediction failed: {e}")
            raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

    return {
        "status": "success",
        "predicted_label": predicted_label,
        "suggested_fix": suggested_fix
    }

if __name__ == "__main__":
    uvicorn.run("lightgbm_api:app", host="0.0.0.0", port=8000)

Changes in Input Validation:

1. Using request.get(): This method checks if log_entries and labels exist in the input payload. If not, it will raise a 400 error with the message "Log entries and labels are required."


2. Checking Field Lengths: Ensures that both log_entries and labels lists have the same length.



Updated Python Train Request:

import requests

url = "http://localhost:8000/train"
data = {
    "log_entries": [
        "ERROR: Could not resolve host: github.com",
        "ERROR: Repository not found.",
        "ERROR: Authentication failed for 'https://github.com/your-repo/your-project.git'"
    ],
    "labels": [2, 3, 1]
}

response = requests.post(url, json=data)
print(response.json())

Python Predict Request:

import requests

url = "http://localhost:8000/predict"
data = {
    "log_entry": "ERROR: Could not resolve host: github.com"
}

response = requests.post(url, json=data)
print(response.json())

Key Fixes:

1. Input Validation: Uses request.get() to check if fields are present and provides clear error messages.


2. Field Length Validation: Ensures the number of log entries and labels are equal.



This should fix the issue where the API was failing due to missing or incorrect fields. Let me know if this resolves your issue!


