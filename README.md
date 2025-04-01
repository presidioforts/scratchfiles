# Agentic Training System

A FastAPI-based system for training and deploying text-based classification models with support for synthetic data generation.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create required directories:
```bash
mkdir use_cases
```

## Running the Server

Start the FastAPI server:
```bash
python -m uvicorn main_server:app --reload
```

The server will be available at http://localhost:8000

## Using the CLI

The CLI provides several commands for interacting with the system:

```bash
# List available use cases
python cli_agent.py list

# Check status of a use case
python cli_agent.py status <use_case_name>

# Train a model
python cli_agent.py train <use_case_name>

# Retrain with synthetic data
python cli_agent.py retrain <use_case_name>

# Make predictions
python cli_agent.py predict <use_case_name> "your text here"
```

## Example Use Case

1. Create a use case file in `use_cases/example.json`:
```json
{
    "model": "all-MiniLM-L6-v2",
    "data": [
        {"input": "System started successfully", "label": "success"},
        {"input": "Failed to start system", "label": "error"},
        {"input": "System running normally", "label": "success"}
    ]
}
```

2. Train the model:
```bash
python cli_agent.py train example
```

3. Make predictions:
```bash
python cli_agent.py predict example "System failed to initialize"
```

## Running Tests

The system includes a comprehensive test suite to verify the functionality:

```bash
# Start the server in one terminal
python -m uvicorn main_server:app --reload

# Run tests in another terminal
python test_agentic_workflow.py
```

The test suite verifies:
- Complete CI/CD workflow
- Model training and validation
- Synthetic data generation
- Prediction functionality
- Error handling
- Status checking

Test output will show detailed information about each step and verify that:
- All API endpoints are working
- Responses contain expected data
- Error cases are handled properly
- The workflow functions as expected

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
.
├── main_server.py      # FastAPI server implementation
├── cli_agent.py        # Command-line interface
├── test_agentic_workflow.py  # Test suite
├── requirements.txt    # Project dependencies
└── use_cases/         # Directory for use case definitions
    └── *.json         # Use case configuration files
```

## Dependencies

- FastAPI 0.95.0
- Uvicorn 0.21.1
- Pydantic 1.10.7
- Python-multipart 0.0.5
- Requests 2.26.0

## Logging

All actions are logged to `agentic_training.log` with timestamps and details. 