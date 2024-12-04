import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sentence_transformers import SentenceTransformer

# Step 1: Expanded Dataset
data = {
    'error_message': [
        "ERR! adduser needs proper .npmrc setup",
        "Permission denied during installation",
        "Package xyz not found in registry",
        "Could not connect to npm registry",
        "Invalid package version specified",
        "Failed to fetch package from registry. Network issue?",
        "Access denied for user during npm install",
        "Invalid scope in package.json file",
        "Package xyz version mismatch with peer dependency",
        "Unexpected token error in JSON"
    ],
    'label': [0, 1, 2, 3, 4, 3, 1, 4, 2, 0]
}
df = pd.DataFrame(data)

# Debug: Check label distribution
print("Label Distribution:\n", df.groupby('label').size())

# Step 2: Define Fix Suggestions
suggested_fixes = {
    0: "Ensure the .npmrc file is properly configured. Add the necessary credentials or registry URL.",
    1: "Check your permissions. Use 'sudo' if required or ensure the current user has appropriate access rights.",
    2: "Verify the package name and check if it's available in the npm registry. Consider updating your npm version.",
    3: "Check your internet connection or npm registry settings.",
    4: "Ensure the specified package version exists. Use 'npm view <package>' to check available versions."
}

# Step 3: Sentence Embeddings
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
X = sentence_model.encode(df['error_message'].tolist())
y = df['label'].values

# Debug: Check embedding dimensions
print("Embedding Shape:", X.shape)

# Step 4: Stratified Train/Test Splits
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.5, random_state=42, stratify=y
)

# Debug: Ensure proper stratification
print("Training labels:", np.unique(y_train, return_counts=True))
print("Test labels:", np.unique(y_test, return_counts=True))

# Step 5: Train Logistic Regression Model
logistic_model = LogisticRegression(max_iter=1000, multi_class='multinomial', solver='lbfgs')
logistic_model.fit(X_train, y_train)

# Step 6: Evaluate Model
y_pred = logistic_model.predict(X_test)
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Step 7: Prediction Function
def predict_and_suggest_fix(error_message, logistic_model, sentence_model, suggested_fixes):
    """
    Predict the issue type and suggest a fix.
    """
    X_text = sentence_model.encode([error_message])
    predicted_label = logistic_model.predict(X_text)[0]
    confidence = max(logistic_model.predict_proba(X_text)[0])
    fix = suggested_fixes.get(predicted_label, "No suggestion available.")
    return predicted_label, confidence, fix

# Step 8: Test with a New Input
new_error = "Invalid package version specified"
label, confidence, fix = predict_and_suggest_fix(new_error, logistic_model, sentence_model, suggested_fixes)

# Print Results
print("\nPrediction Results:")
print(f"Predicted Label: {label}")
print(f"Confidence: {confidence:.2f}")
print(f"Suggested Fix: {fix}")
