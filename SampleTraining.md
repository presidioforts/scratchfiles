
Certainly! Here’s the complete code that walks you through the steps to train a LightGBM model using sample data from a Jenkins build log, focusing on Groovy errors. This code includes data preparation, feature engineering, model training, and querying the model with new data.

### Complete Python Code:

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import lightgbm as lgb

# Step 1: Create Sample Data
# Example log parsed into structured data
data = {
    'error_type': ['java.lang.NoClassDefFoundError', 'java.lang.ClassNotFoundException', 'java.lang.NullPointerException'],
    'script_name': ['myscript.groovy', 'anotherscript.groovy', 'yetanotherscript.groovy'],
    'class_name': ['MyClass', 'AnotherClass', 'NullClass'],
    'pipeline_stage': ['Execute shell', 'Execute shell', 'Execute shell'],
    'error_occurrence': [1, 1, 1],  # 1 indicates an error occurred
    'error_length': [
        len('java.lang.NoClassDefFoundError: Could not initialize class MyClass'),
        len('java.lang.ClassNotFoundException: AnotherClass'),
        len('java.lang.NullPointerException: NullClass')
    ]
}

df = pd.DataFrame(data)

# Step 2: Label the Data
# Assuming any log with an error is labeled as 'failure' (0)
df['label'] = [0, 0, 0]  # 0 for failure, 1 for success

# Step 3: One-Hot Encode Categorical Features
df_encoded = pd.get_dummies(df.drop(columns=['label']))

# Features (X) and target variable (y)
X = df_encoded
y = df['label']

# Step 4: Train LightGBM Model
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a LightGBM dataset
train_data = lgb.Dataset(X_train, label=y_train)

# Set parameters for LightGBM
params = {
    'boosting_type': 'gbdt',
    'objective': 'binary',
    'metric': 'binary_logloss',
    'num_leaves': 31,
    'learning_rate': 0.05,
    'feature_fraction': 0.9
}

# Train the model
model = lgb.train(params, train_data, num_boost_round=100)

# Step 5: Make Predictions
# Predict on the test set
y_pred = model.predict(X_test)
y_pred_binary = (y_pred > 0.5).astype(int)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred_binary)
print(f'Accuracy: {accuracy * 100:.2f}%')

# Step 6: Query with New Data
# Create new data point to simulate a new build log
new_log = {
    'error_type': ['java.lang.ClassNotFoundException'],
    'script_name': ['anotherscript.groovy'],
    'class_name': ['AnotherClass'],
    'pipeline_stage': ['Execute shell'],
    'error_occurrence': [1],
    'error_length': [len('java.lang.ClassNotFoundException: AnotherClass')]
}

new_df = pd.DataFrame(new_log)
new_df_encoded = pd.get_dummies(new_df)

# Align the columns with the training data
new_df_encoded = new_df_encoded.reindex(columns=X_train.columns, fill_value=0)

# Predict using the trained model
new_pred = model.predict(new_df_encoded)
new_pred_binary = (new_pred > 0.5).astype(int)

print("Predicted outcome:", "Failure" if new_pred_binary[0] == 0 else "Success")
```

### What This Code Does:
1. **Data Preparation**:
   - Simulates build logs with Groovy-related errors.
   - Converts categorical data (like error types, script names) into numerical format using one-hot encoding.

2. **Model Training**:
   - Trains a LightGBM model on the prepared data to predict whether a build will fail based on the provided logs.

3. **Model Evaluation**:
   - The model's accuracy is printed out to understand how well it's performing.

4. **Prediction with New Data**:
   - Simulates a new build log and predicts whether it will result in a failure or success.

### Next Steps:
You can extend this by:
- Adding more logs and different types of errors.
- Fine-tuning the features or hyperparameters to improve model performance.
- Integrating this into a real Jenkins pipeline with live data.

Feel free to test this out, and let me know if you encounter any issues or if you need further customization!
