Here are sample requests for training and prediction using the FastAPI endpoints in your lightgbm_api.py application.

Sample Request for Training

Use this request to send new log entries and their corresponding labels for training the model:

POST /train

{
  "log_entries": [
    "ERROR: Could not resolve host: github.com",
    "ERROR: Repository not found.",
    "ERROR: Authentication failed for 'https://github.com/your-repo/your-project.git'"
  ],
  "labels": [2, 3, 1]
}

Explanation:

log_entries: This is a list of new error logs to be used for training.

labels: These are the corresponding labels (classes) for each log entry. The label 2 represents a network issue, 3 represents a repository issue, and 1 represents an authentication issue.



---

Sample Request for Prediction

Use this request to predict the issue type of a new log entry:

POST /predict

{
  "log_entry": "ERROR: Could not resolve host: github.com"
}

Explanation:

log_entry: This is the log entry you want to classify. The model will predict the type of error (label) and return the associated suggested fix.



---

Sample Responses

1. Response from /train:



{
  "status": "success",
  "message": "Model trained and saved successfully."
}

2. Response from /predict:



{
  "status": "success",
  "predicted_label": 2,
  "suggested_fix": "Check your network connection or DNS settings."
}


---

How to Test Using curl:

1. Train the model:



curl -X POST "http://localhost:8000/train" -H "Content-Type: application/json" -d '{
  "log_entries": [
    "ERROR: Could not resolve host: github.com",
    "ERROR: Repository not found.",
    "ERROR: Authentication failed for \"https://github.com/your-repo/your-project.git\""
  ],
  "labels": [2, 3, 1]
}'

2. Predict an issue:



curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '{
  "log_entry": "ERROR: Could not resolve host: github.com"
}'


---

How to Test Using Python's requests Library:

1. Training the model:



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

2. Predicting an issue:



import requests

url = "http://localhost:8000/predict"
data = {
    "log_entry": "ERROR: Could not resolve host: github.com"
}

response = requests.post(url, json=data)
print(response.json())


---

Let me know if you need more details or help with testing!


