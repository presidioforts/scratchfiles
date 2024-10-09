import requests

url = "http://localhost:8000/predict"
data = {
    "log_entry": "ERROR: Unable to connect to database."
}

response = requests.post(url, json=data)

# Print the response
if response.status_code == 200:
    print(f"Prediction Response: {response.json()}")
else:
    print(f"Error {response.status_code}: {response.text}")
