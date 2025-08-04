def test_full_flow():
    import requests

    # 1. Load data file
    res = requests.get("http://localhost:8000/load_data/data2.csv")
    assert res.status_code == 200

    # 2. Clean & train
    res = requests.get("http://localhost:8000/clean_df_and_train_model")
    assert res.status_code == 200
    assert "accuracy" in res.json()

    # 3. Sync model to classifier
    res = requests.get("http://localhost:8080/sync_model_from_remote")
    assert res.status_code == 200

    # 4. Predict
    features = {"humidity": "low", "temperature": "hot", "whether": "sun"}
    res = requests.post("http://localhost:8080/predict", json=features)
    assert res.status_code == 200
    assert "prediction" in res.json()
