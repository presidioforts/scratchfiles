Certainly! Below is the updated complete source code that ensures both the training and prediction functions handle the CountVectorizer correctly. The CountVectorizer is now persisted and used consistently during both training and prediction.

Additionally, I will provide working Python requests examples for both train and predict requests.


---

Updated lightgbm_api.py Source Code

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
    if 'log_entries' not in request or 'labels' not in request:
        raise HTTPException(status_code=400, detail="Log entries and labels are required.")

    log_entries = request['log_entries']
    labels = request['labels']

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

    if 'log_entry' not in request:
        raise HTTPException(status_code=400, detail="Log entry is required.")

    log_entry = request['log_entry']

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

Key Updates:

1. Persisting the Vectorizer:

The CountVectorizer is now saved and loaded using pickle to ensure it is consistent across training and prediction. The vectorizer is saved to vectorizer.pkl.



2. Train Endpoint:

The /train endpoint now fits the vectorizer with new data and saves both the model and vectorizer after training.



3. Predict Endpoint:

The /predict endpoint ensures the vectorizer is loaded and applied to new log entries for predictions.





---

Train Request in Python

You can use the following Python code to send a training request:

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

Predict Request in Python

You can use the following Python code to send a prediction request:

import requests

url = "http://localhost:8000/predict"
data = {
    "log_entry": "ERROR: Could not resolve host: github.com"
}

response = requests.post(url, json=data)
print(response.json())

Expected Output:

For the train request:

{
  "status": "success",
  "message": "Model and vectorizer trained and saved successfully."
}

For the predict request:

{
  "status": "success",
  "predicted_label": 2,
  "suggested_fix": "Check your network connection or DNS settings."
}


---

Summary:

The vectorizer is now saved and loaded along with the model.

The /train endpoint updates the vectorizer with new training data and ensures both the model and vectorizer are persisted.

The /predict endpoint uses the loaded vectorizer to predict the label of new log entries.


Let me know how it goes during your testing!


