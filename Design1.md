
High-Level Design Document for LightGBM API with Incremental Model Training


---

1. Introduction

This document describes the high-level design for a REST API built with FastAPI that allows users to train a LightGBM model incrementally and perform predictions. The model is saved to a file (model.txt) and updated incrementally with each training request. The system supports both training and inference (predictions), and uses state management to persist the model, ensuring it is not lost between service restarts.


---

2. System Overview

The system consists of a web service that exposes endpoints for training and predicting with a LightGBM model. It manages the state of the model in a persistent file (model.txt) to ensure that the model can be incrementally trained and retained across restarts.

Key Components:

1. FastAPI Application: The API server that provides endpoints for training and predicting.


2. LightGBM Model: The machine learning model used for training and predictions.


3. Model State Management (model.txt): Manages the persistence of the model between service restarts.


4. Concurrency Management: Ensures that multiple clients can safely train and predict concurrently without race conditions.




---

3. Core Functionalities

3.1. Training Endpoint (/train)

Input: JSON payload containing features (list of feature vectors) and labels (corresponding labels for supervised learning).

Output: JSON response indicating success or failure of training.

Model Update: The model is incrementally updated with new training data. Once the training is complete, the updated model is saved back to the file (model.txt).


3.2. Prediction Endpoint (/predict)

Input: JSON payload containing features (list of feature vectors for prediction).

Output: JSON response with predicted values.

Model Usage: The current state of the model (model.txt) is used to make predictions.



---

4. Model State Management (model.txt)

The model.txt file is critical to maintaining the state of the model across training sessions and service restarts. It ensures the following:

1. Persistence: After every training session, the model is saved to model.txt to ensure that its state is preserved.


2. Incremental Training: Each new training request continues training from the previous state, loading the model from model.txt.


3. Atomic Updates: The model is saved atomically using a temporary file (model.txt.tmp), which is renamed to model.txt after the save is successful. This prevents corruption in case of system failures.


4. Concurrency Safety: A threading lock is used to ensure only one training or prediction operation can modify the model at a time, ensuring thread safety in multi-client environments.




---

5. Model Lifecycle

5.1. Initialization

On startup, the system checks if model.txt exists.

If the file exists: The model is loaded from the file into memory using lgb.Booster().

If the file does not exist: A new model is initialized with default parameters (objective='binary', metric='binary_logloss'), ready for training.



5.2. Training Flow

The user sends a POST request to /train with the new features and labels.

The system performs the following steps:

1. Input Validation: Validates the input format and consistency.


2. Model Update: If a model already exists (model.txt), the existing model is used for incremental training. If no model exists, a new model is created and trained.


3. Persistence: After training, the model is saved atomically to a temporary file (model.txt.tmp) and then renamed to model.txt. This ensures that any failure during the save process does not corrupt the model file.




5.3. Prediction Flow

The user sends a POST request to /predict with new feature data.

The system performs the following steps:

1. Input Validation: Ensures the input features are in the correct format and match the expected number of features for the model.


2. Prediction: The model makes predictions based on the input features using the current state of the model.


3. Concurrency Handling: Uses a lock to ensure that predictions are consistent and not affected by concurrent training sessions.





---

6. Detailed Components and Flow

6.1. FastAPI Application

The FastAPI application is the web server that provides the following endpoints:

/train: Used to train the model with new data.

/predict: Used to predict outcomes based on the current model.


6.2. LightGBM Model

The LightGBM model is a gradient boosting framework that allows efficient and accurate training on large datasets. It supports incremental training through the keep_training_booster=True option, which continues training an existing model.

6.3. Concurrency Management

Concurrency is handled using Python's threading.Lock to ensure that multiple clients can safely perform training and prediction operations without race conditions or inconsistent model states.

6.4. Model File (model.txt)

The model.txt file stores the serialized version of the trained LightGBM model. It is read when the service starts, and it is written to after every training session. The file is updated atomically to prevent corruption in the event of a system failure.


---

7. Data Flow Diagram

Below is a high-level view of the data flow for training and prediction operations:

+---------------------------+
               |       User Request         |
               +---------------------------+
                       |        |             
               +--------+        +--------+
               |                         |
        /train request             /predict request
               |                         |
     +---------------------+    +-------------------+
     | Input Validation     |    | Input Validation  |
     +---------------------+    +-------------------+
               |                         |
     +---------------------+    +-------------------+
     | Lock the Model       |    | Lock the Model    |
     +---------------------+    +-------------------+
               |                         |
     +---------------------+    +-------------------+
     | Incremental Training |    | Make Prediction   |
     +---------------------+    +-------------------+
               |                         |
     +---------------------+    +-------------------+
     | Save model.txt       |    | Return Predictions|
     +---------------------+    +-------------------+
               |
     +---------------------+
     | Return Success       |
     +---------------------+


---

8. Error Handling and Edge Cases

Invalid Input: If the features or labels are missing or malformed, the system returns an HTTP 400 error.

Model Inconsistency: If the number of features in the input does not match the model's expected number of features, the system returns an HTTP 400 error.

Training/Predicting Failure: If there is any issue with training or predicting, the system returns an HTTP 500 error, with detailed logging of the failure.



---

9. Security Considerations

Input Validation: The system ensures all input data is validated before training or predicting.

Thread Safety: The system uses locks to prevent concurrent access to the model during training or prediction, ensuring consistency.

Atomic Writes: Model updates are written to a temporary file and then atomically renamed to prevent file corruption.



---

10. Future Considerations

Model Versioning: Introduce versioning for model.txt to maintain multiple versions of the model and enable rollback if necessary.

Scalability: Use a distributed file system or cloud storage (e.g., AWS S3, Google Cloud Storage) for model.txt to support multiple instances of the API.

Advanced Security: Add user authentication and authorization to control access to the training and prediction endpoints.



---

11. Conclusion

This high-level design explains the architecture of the LightGBM-based incremental training system. The key element of the design is state management using model.txt to ensure that the model can be trained incrementally and persists across restarts. The API is designed to handle multiple concurrent users safely and provide reliable training and prediction services.


---

This document provides an overview that can be presented to developers to understand how the system operates and how the model.txt file is managed. Let me know if you need further details or have questions!



