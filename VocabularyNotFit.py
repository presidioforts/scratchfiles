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
            # Update the vectorizer with the new data
            vectorizer.fit(new_data['log_entry'])  # Fit vectorizer with the new log entries

            # Convert new data to features
            X_new = vectorizer.transform(new_data['log_entry']).astype(np.float32)
            y_new = new_data['label']

            # Prepare LightGBM dataset
            new_train_data = lgb.Dataset(X_new, label=y_new, free_raw_data=False)

            # Incrementally train the existing model
            model = lgb.train(
                model.params,
                new_train_data,
                num_boost_round=10,  # Adjust based on the amount of new data
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
