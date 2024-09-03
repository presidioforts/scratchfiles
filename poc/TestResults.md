```
# Simulate a new log entry
user_input = 'ERROR: Authentication failed for \'https://github.com/your-repo/your-project.git\''
user_input_vectorized = vectorizer.transform([user_input]).astype(np.float32)
new_prediction = bst.predict(user_input_vectorized)
predicted_label = list(new_prediction[0]).index(max(new_prediction[0]))

# Display the prediction and suggested fix
print(f"Predicted issue label: {predicted_label}")
print(f"Suggested fix: {df['suggested_fix'][predicted_label]}")
```

## Model result:
```
C:\Users\krish\PycharmProjects\LightGPM\venv\Scripts\python.exe C:\Users\krish\PycharmProjects\LightGPM\rca2.py 
[LightGBM] [Warning] There are no meaningful features, as all feature values are constant.
[LightGBM] [Info] Total Bins 0
[LightGBM] [Info] Number of data points in the train set: 4, number of used features: 0
[LightGBM] [Info] Start training from score -34.538776
[LightGBM] [Info] Start training from score -0.693147
[LightGBM] [Info] Start training from score -1.386294
[LightGBM] [Info] Start training from score -1.386294
[LightGBM] [Warning] Stopped training because there are no more leaves that meet the split requirements
Training until validation scores don't improve for 10 rounds
[LightGBM] [Warning] Stopped training because there are no more leaves that meet the split requirements
[LightGBM] [Warning] Stopped training because there are no more leaves that meet the split requirements
[LightGBM] [Warning] Stopped training because there are no more leaves that meet the split requirements
[LightGBM] [Warning] Stopped training because there are no more leaves that meet the split requirements
[LightGBM] [Warning] Stopped training because there are no more leaves that meet the split requirements
[LightGBM] [Warning] Stopped training because there are no more leaves that meet the split requirements
[LightGBM] [Warning] Stopped training because there are no more leaves that meet the split requirements
[LightGBM] [Warning] Stopped training because there are no more leaves that meet the split requirements
[LightGBM] [Warning] Stopped training because there are no more leaves that meet the split requirements
[LightGBM] [Warning] Stopped training because there are no more leaves that meet the split requirements
Early stopping, best iteration is:
[1]	valid_0's multi_logloss: 0.405465
Model accuracy: 100.00%
Predicted issue label: 1
Suggested fix: Update the GitHub token in the Jenkins credentials or verify the SSH key configuration.

Process finished with exit code 0
```
