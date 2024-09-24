Certainly! Below is a complete, executable version of the code that sets up a FastAPI application to expose your LightGBM model as an API service endpoint. This code includes:

- Model initialization
- Training endpoint (`/train`)
- Prediction endpoint (`/predict`)
- Model persistence to prevent data loss upon service restarts
- Thread safety using locks
- Error handling and logging

---

### **Complete Code**

```python
# Filename: lightgbm_api.py

from fastapi import FastAPI, HTTPException
import uvicorn
import lightgbm as lgb
import numpy as np
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

def create_new_model():
    params = {
        'objective': 'binary',       # Adjust based on your use case
        'metric': 'binary_logloss',  # Adjust based on your use case
        'verbosity': -1
    }
    # Adjust the number of features according to your data
    num_features = 3  # For example, 3 features
    dummy_data = np.empty((0, num_features))
    dummy_labels = np.empty((0, ))
    train_data = lgb.Dataset(dummy_data, label=dummy_labels)
    model = lgb.train(params, train_data, num_boost_round=0)
    return model

def initialize_model():
    global model
    if os.path.exists(model_file):
        try:
            # Load the model from disk
            model = lgb.Booster(model_file=model_file)
            logging.info("Model loaded from %s", model_file)
        except Exception as e:
            logging.error("Failed to load model from %s: %s", model_file, e)
            # Initialize a new model if loading fails
            model = create_new_model()
            logging.info("Initialized new model after load failure.")
    else:
        # Initialize a new model
        model = create_new_model()
        logging.info("Initialized new model.")

initialize_model()

@app.post("/train")
async def train_model(request: dict):
    global model
    data = request

    # Input validation
    if 'features' not in data or 'labels' not in data:
        raise HTTPException(status_code=400, detail="Features and labels are required.")

    features = data['features']
    labels = data['labels']

    if len(features) != len(labels):
        raise HTTPException(status_code=400, detail="Features and labels must have the same length.")

    # Convert to numpy arrays
    X = np.array(features)
    y = np.array(labels)

    # Ensure the number of features matches the model's expected input
    expected_num_features = model.num_feature()
    if X.shape[1] != expected_num_features:
        raise HTTPException(status_code=400, detail=f"Each feature vector must have {expected_num_features} elements.")

    # Create LightGBM dataset
    lgb_data = lgb.Dataset(X, label=y, free_raw_data=False)

    # Lock the model for thread-safe updates
    with model_lock:
        try:
            # Continue training the existing model with new data
            model = lgb.train(
                model.params,
                lgb_data,
                num_boost_round=10,  # Adjust based on your needs
                init_model=model,
                keep_training_booster=True
            )
            # Save the updated model to disk atomically
            temp_model_file = model_file + '.tmp'
            model.save_model(temp_model_file)
            os.replace(temp_model_file, model_file)
            logging.info("Model trained and saved successfully.")
        except Exception as e:
            logging.error("Failed to train or save the model: %s", e)
            raise HTTPException(status_code=500, detail=f"Failed to train or save the model: {e}")

    return {"status": "success", "message": "Model trained and saved successfully."}

@app.post("/predict")
async def predict(request: dict):
    global model
    data = request

    if 'features' not in data:
        raise HTTPException(status_code=400, detail="Features are required.")

    features = data['features']
    X = np.array(features)

    # Ensure the number of features matches the model's expected input
    expected_num_features = model.num_feature()
    if X.shape[1] != expected_num_features:
        raise HTTPException(status_code=400, detail=f"Each feature vector must have {expected_num_features} elements.")

    with model_lock:
        try:
            predictions = model.predict(X).tolist()
        except Exception as e:
            logging.error("Prediction failed: %s", e)
            raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

    return {"status": "success", "predictions": predictions}

if __name__ == "__main__":
    uvicorn.run("lightgbm_api:app", host="0.0.0.0", port=8000)
```

---

### **Instructions**

#### **1. Save the Code**

- Save the above code into a file named `lightgbm_api.py`.

#### **2. Install Required Packages**

Ensure you have **Python 3.6** or higher installed.

Install the required packages using `pip`:

```bash
pip install fastapi uvicorn lightgbm numpy
```

#### **3. Run the API Service**

Start the FastAPI application by running:

```bash
python lightgbm_api.py
```

The service will start and listen on `http://0.0.0.0:8000`.

#### **4. Test the API Endpoints**

##### **Training the Model**

Send a POST request to `/train` with JSON data containing `features` and `labels`.

**Example using `curl`:**

```bash
curl -X POST "http://localhost:8000/train" -H "Content-Type: application/json" -d '{
  "features": [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]],
  "labels": [0, 1]
}'
```

**Example using Python `requests`:**

```python
import requests

url = "http://localhost:8000/train"
data = {
    "features": [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]],
    "labels": [0, 1]
}

response = requests.post(url, json=data)
print(response.json())
```

##### **Making Predictions**

Send a POST request to `/predict` with JSON data containing `features`.

**Example using `curl`:**

```bash
curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '{
  "features": [[0.1, 0.2, 0.3]]
}'
```

**Example using Python `requests`:**

```python
import requests

url = "http://localhost:8000/predict"
data = {
    "features": [[0.1, 0.2, 0.3]]
}

response = requests.post(url, json=data)
print(response.json())
```

#### **5. Verify Persistence Across Restarts**

1. **Train the Model:**
   - Send a training request as shown above.

2. **Stop the Service:**
   - Press `Ctrl+C` in the terminal where the service is running.

3. **Start the Service Again:**
   - Run `python lightgbm_api.py` to restart the service.

4. **Make Predictions:**
   - Send a prediction request. The model should retain its trained state.

#### **6. Adjust Number of Features**

- **Important:** Adjust the `num_features` variable in `create_new_model()` to match the actual number of features in your data.

  ```python
  num_features = 3  # Set this to the number of features in your dataset
  ```

- Ensure that the input features in your training and prediction requests match this number.

#### **7. Logging**

- The application uses Python's `logging` module to log important events.
- Logs are printed to the console, showing when the model is loaded, trained, or if any errors occur.

#### **8. Error Handling**

- The code includes error handling for:
  - Input validation errors (HTTP 400)
  - Training or prediction failures (HTTP 500)
- Error messages are returned in the HTTP response.

#### **9. Thread Safety**

- A threading lock (`model_lock`) is used to prevent race conditions when multiple users are training or predicting concurrently.

#### **10. Model Saving**

- The model is saved to `model.txt` after each training session.
- Uses atomic file replacement to prevent file corruption.

---

### **Additional Information**

#### **Requirements File (Optional)**

You can create a `requirements.txt` file to manage dependencies:

```txt
fastapi
uvicorn
lightgbm
numpy
```

Install dependencies using:

```bash
pip install -r requirements.txt
```

#### **Dockerization (Optional)**

To run the application inside a Docker container:

**Create a `Dockerfile`:**

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "lightgbm_api:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Build the Docker Image:**

```bash
docker build -t lightgbm-api .
```

**Run the Docker Container:**

```bash
docker run -p 8000:8000 lightgbm-api
```

#### **Security Considerations**

- **Authentication and Authorization:** For production use, implement security measures to restrict access.
- **Data Validation:** Ensure that all input data is validated and sanitized.
- **HTTPS:** Use SSL/TLS to encrypt data in transit.

#### **Scalability and Persistence**

- If running multiple instances, store `model.txt` on shared storage accessible by all instances.
- Alternatively, use a centralized database or object storage (e.g., AWS S3) for model persistence.

#### **Advanced Features (Optional)**

- **Model Versioning:** Implement a system to keep track of different versions of the model.
- **Asynchronous Tasks:** Use background tasks or job queues for long-running training sessions.
- **Monitoring:** Integrate monitoring tools to track the performance and health of the API.

---

### **Testing the Application**

#### **Training the Model**

```python
import requests

url = "http://localhost:8000/train"
data = {
    "features": [
        [0.5, 0.2, 0.1],
        [0.9, 0.7, 0.3],
        [0.4, 0.5, 0.6]
    ],
    "labels": [0, 1, 0]
}

response = requests.post(url, json=data)
print("Training Response:", response.json())
```

#### **Making Predictions**

```python
import requests

url = "http://localhost:8000/predict"
data = {
    "features": [
        [0.1, 0.2, 0.3],
        [0.8, 0.5, 0.7]
    ]
}

response = requests.post(url, json=data)
print("Prediction Response:", response.json())
```

---

### **Conclusion**

This complete code provides a working API service endpoint for your LightGBM model with persistence across restarts. You can further enhance this code by:

- Adjusting LightGBM parameters based on your specific requirements.
- Implementing security measures for a production environment.
- Integrating with cloud services or databases for scalability.

---

**Feel free to reach out if you have any questions or need further assistance!**
