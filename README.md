# 🧠 Naive Bayes Classifier — CLI + FastAPI

A learning project demonstrating a Naive Bayes classifier, built with a clean separation between a Python CLI and a FastAPI server.
This design also prepares you for container orchestration (e.g. Kubernetes), where `classifer_server` can be scaled horizontally under load.

In addition to `classifer_server`, a local `server/` directory exists. It also makes HTTP requests, but it keeps a local copy of the classifier code to avoid depending on external containerized services during internal accuracy testing. This is because the testing loop (which uses 30% of the dataset) calls the classifier many times, and doing so over HTTP would be inefficient.

The separation also allows `classifer_server` to evolve independently and be deployed at scale, while `server/` remains optimized for internal logic and control.

---

## 🚀 Features
- 📂 Load CSV files
- ✂️ Drop unwanted columns
- 📊 Train using Naive Bayes (with Laplace smoothing)
- 🧮 Predict classes from user input
- 🎯 Evaluate model accuracy

---

## 🗂️ Project Structure

```
naive_bayes_classsifier/
├── client/                    # CLI app
│   ├── main.py                # Entry point
│   ├── requirements.txt       # Dependencies
│   ├── Dockerfile
│   ├── managers/
│   │   └── manager.py         # Main controller on client-side
│   └── ui/
│       └── menu.py            # Text UI logic
│
├── classifer_server/         # FastAPI backend (can scale in Kubernetes)
│   ├── controller.py
│   ├── run_classifier_serrver.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── app_models/
│   │   └── classifier.py      # Classification logic
│   ├── app_server/
│   │   └── endpoints.py       # API route handlers
│   └── utils/
│       ├── cleaner.py
│       └── convert_types.py
│
├── server/                   # Alternate backend used in internal evaluation
│   ├── run.py
│   ├── requirements.txt
│   ├── app/
│   │   ├── app.py
│   │   ├── api_endpoints.py
│   │   └── endpoints.py
│   ├── core/
│   │   ├── classifier.py
│   │   └── naive_bayes_trainer.py
│   ├── services/
│   │   ├── Controller.py
│   │   └── api_controller.py
│   ├── utils/
│   │   ├── cleaner.py
│   │   ├── convert_numpy_types.py
│   │   └── extract.py
│   ├── tests/
│   │   ├── test_accuracy.py
│   │   └── tester.py
│   └── data/                  # Example CSV files
│
├── shared/                   # (Planned) shared modules to avoid duplication
│   └── classifier.py
│
├── README.md
└── .gitignore
```

---

## ⚙️ How to Run

### 🖥️ Start the Server:
```bash
cd classifer_server
python run_classifier_serrver.py
```

### 🧑‍💻 Start the Client:
```bash
cd client
python main.py
```

---

## 🛠 Requirements
- Python 3.9+
- fastapi, uvicorn, pandas, numpy, scikit-learn, requests

---

## 🧠 Notes
- Assumes target label is the last column in CSV.
- Works best with clean, categorical data.
- Educational design — not optimized for production yet.
- `classifer_server` is the scalable version meant for deployment.
- `server/` is a local copy with the same classifier logic, used to avoid performance hits during internal evaluation.
- Future plan includes consolidating duplicated classifier logic into a single `shared/` module.

---

## 🛠️ Potential Improvements
- ✅ Add persistent storage (pickle, SQLite)
- ✅ Add API schema validation with Pydantic
- ✅ Improve error handling and feedback
- ✅ Add unit tests (e.g. `pytest`)
