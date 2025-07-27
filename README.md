# 🧠 Naive Bayes Classifier — CLI + FastAPI

A modular learning project implementing a Naive Bayes classifier using a microservices-based architecture, with a clear separation between a Python CLI, a data-processing server, and a classification server.

---

## ✨ Features

* 📂 Load and manage CSV files
* ✂️ Drop unnecessary columns interactively
* 📊 Train a Naive Bayes classifier (with Laplace smoothing)
* 🎯 Evaluate classifier accuracy using test split (30%)
* 🧮 Predict classes from user input via `classifier_server`

---

## 📂 Project Structure and Responsibilities

```
naive_bayes_classsifier/
├── client/                            # CLI interface for user interaction
│   ├── main.py                        # Entry point
│   ├── managers/
│   │   └── manager.py                # Handles user requests and orchestrates flow
│   ├── ui/
│   │   └── menu.py                   # CLI menu interface logic
│   └── requirements.txt              # Client-side dependencies
│
├── classifer_server/                 # Stateless prediction service
│   ├── run_classifier_serrver.py     # Launch FastAPI server for classification
│   ├── controller.py                 # Maintains current model and parameters
│   ├── app_models/
│   │   └── classifier.py             # Actual classification logic using trained model
│   ├── app_server/
│   │   └── Api_endpoints.py          # API routes for prediction and syncing model
│   ├── utils/
│   │   └── convert_numpy_types.py    # Type converters for JSON compatibility
│   └── requirements.txt              # Server-side dependencies for classifier
│
├── server/                           # Training service and internal evaluation
│   ├── run.py                        # Launch FastAPI training server
│   ├── app/
│   │   ├── app.py                    # FastAPI app setup
│   │   └── api_endpoints.py         # API routes for data handling and model training
│   ├── core/
│   │   ├── classifier.py             # Inference logic for trained model
│   │   └── naive_bayes_trainer.py   # Model training logic (with Laplace smoothing)
│   ├── dal/
│   │   └── dal.py                   # Data access layer (e.g. reading CSV files)
│   ├── services/
│   │   └── api_controller.py         # Coordinates between app and logic layers
│   ├── utils/
│   │   ├── cleaner.py                # Data cleaning utilities
│   │   ├── convert_numpy_types.py   # Converts numpy types for JSON
│   │   └── extract.py                # Extracts column names, unique values, etc.
│   └── data/                         # Sample CSV datasets for demo purposes
│
└── README.md
```

---

## 📡 API Endpoints Overview

### 🔸 Server (Training Backend)

| Endpoint                    | Method | Purpose                     |
| --------------------------- | ------ | --------------------------- |
| `/get_list_of_files`        | GET    | List available CSVs         |
| `/load_data/{file}`         | GET    | Load a selected CSV         |
| `/drop_requested_columns`   | POST   | Drop specified columns      |
| `/get_list_of_columns`      | GET    | Return current column names |
| `/clean_df_and_train_model` | GET    | Clean and train model       |
| `/get_latest_model`         | GET    | Return latest trained model |

### 🔸 Classifier Server (Prediction Backend)

| Endpoint                          | Method | Purpose                           |
| --------------------------------- | ------ | --------------------------------- |
| `/get_features_and_unique_values` | GET    | Get available feature values      |
| `/sync_model_from_remote`         | GET    | Load model from server            |
| `/classify`                       | POST   | Predict outcome based on features |

---

## 🔁 Flow of Operations

1. **Get file list:** `GET /get_list_of_files`
2. **Load data file:** `GET /load_data/{filename}`
3. **Drop columns (optional):** `POST /drop_requested_columns`
4. **Train model:** `GET /clean_df_and_train_model`
5. **Sync classifier:** `GET /sync_model_from_remote`
6. **Predict result:** `POST /classify` with JSON payload

---

## ⚙️ How to Run

### 🖥️ Start the Classifier Server:

```bash
cd classifer_server
python run_classifier_serrver.py
```

### 🧑‍💻 Start the CLI:

```bash
cd client
python main.py
```

### 🧪 Start the Internal Training Server (Optional):

```bash
cd server
python run.py
```

---

## 🛠 Requirements

* Python 3.9+
* fastapi, uvicorn
* pandas, numpy, requests

---

## 🧠 Notes

* Assumes target label is the last column in the CSV.
* Works best with clean, categorical data.
* `classifier_server` performs predictions only, while `server/` handles training logic.
* This modular design enables flexibility and testing of each component independently.

---

## 🛠️ Potential Improvements

* ✅ Add API schema validation with Pydantic
* ✅ Improve error handling and feedback
* ✅ Add unit tests (e.g. `pytest`)
