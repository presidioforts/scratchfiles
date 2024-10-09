
# Function to train a new model
def train_new_model(data):
    # Ensure labels start from 0
    data['label'] = data['label'].astype(int) - data['label'].min()  # Adjust so labels start from 0

    # Prepare features and labels
    X = data['log_entry']
    y = data['label']

    # Initialize vectorizer and fit on the entire dataset
    vectorizer = CountVectorizer()
    X_vectorized = vectorizer.fit_transform(X).astype(np.float32)

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X_vectorized, y, test_size=0.2, random_state=42
    )

    # Prepare LightGBM datasets
    train_data = lgb.Dataset(X_train, label=y_train)
    test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

    # Set LightGBM parameters
    num_classes = data['label'].nunique()
    params = {
        'objective': 'multiclass',
        'num_class': num_classes,  # Ensure this is correct by counting unique labels
        'metric': 'multi_logloss',
        'boosting_type': 'gbdt',
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.9
    }

    # Train the model
    callbacks = [lgb.early_stopping(stopping_rounds=10)]
    model = lgb.train(params, train_data, valid_sets=[test_data], num_boost_round=100, callbacks=callbacks)

    # Save model and vectorizer
    model.save_model(MODEL_FILE)
    with open(VECTORIZER_FILE, 'wb') as f:
        pickle.dump(vectorizer, f)
    logging.info("New model and vectorizer trained and saved.")

    return model, vectorizer
