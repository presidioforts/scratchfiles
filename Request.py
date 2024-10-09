import requests

url = "http://localhost:8000/train"
data = {
    "log_entries": [
        "ERROR: Unable to connect to database.",
        "WARNING: Deprecated API usage."
    ],
    "labels": [4, 5],
    "suggested_fixes": [
        "Check database connection settings.",
        "Update the API usage to the latest version."
    ]
}

response = requests.post(url, json=data)

# Print raw response content and status code
print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}")

# Then try to parse JSON
try:
    print(response.json())
except requests.exceptions.JSONDecodeError:
    print("Invalid JSON response")








{
    "log_entries": [
        "ERROR: Unable to connect to database.",
        "WARNING: Deprecated API usage."
    ],
    "labels": [4, 5],
    "suggested_fixes": [
        "Check database connection settings.",
        "Update the API usage to the latest version."
    ]
}
