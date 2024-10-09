
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

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Global variables
model = None
model_lock = threading.Lock()
model_file = 'model.txt'
vectorizer = CountVectorizer()

# Mock data (could be dynamic in production)
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

# Initialize the model
def initialize_model():
    global model, vectorizer
    if os.path.exists(model_file):
        try:
            model = lgb.Booster(model_file=model_file)
            logging.info(f"Model loaded from {model_file}")
        except Exception as e:
            logging.error(f"Failed to load model from {model_file}: {e}")
            model = create_new_model()
    else:
        model = create_new_model()

# Create a new model
def create_new_model():
    global vectorizer

    df = pd.DataFrame(data)
    X = df['log_entry']
    y = df['label']

    # Convert text to features (word counts)
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

    # Train a new model with early stopping
    callbacks = [lgb.early_stopping(stopping_rounds=10)]
    model = lgb.train(params, train_data, valid_sets=[test_data], num_boost_round=100, callbacks=callbacks)
    model.save_model(model_file)
    logging.info(f"New model created and saved to {model_file}")
    return model

# Initialize model on startup
initialize_model()

@app.post("/train")
async def train_model(request: dict):
    global model

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
            # Convert new data to features
            X_new = vectorizer.transform(new_data['log_entry']).astype(np.float32)
            y_new = new_data['label']

            # Prepare LightGBM dataset
            new_train_data = lgb.Dataset(X_new, label=y_new, free_raw_data=False)

            # Incrementally train the existing model
            model = lgb.train(
                model.params,
                new_train_data,
                num_boost_round=10,  # Adjust this based on how much new data you have
                init_model=model,
                keep_training_booster=True
            )

            # Save the updated model
            model.save_model(model_file)
            logging.info("Model trained and saved successfully.")
        except Exception as e:
            logging.error(f"Failed to train or save the model: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to train or save the model: {e}")

    return {"status": "success", "message": "Model trained and saved successfully."}

@app.post("/predict")
async def predict(request: dict):
    global model

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
