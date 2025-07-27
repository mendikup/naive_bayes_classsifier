# 🧠 Naive Bayes Classifier — CLI + FastAPI

A learning project demonstrating a Naive Bayes classifier, built with a clean separation between a Python CLI and a FastAPI server. This version keeps the classifier logic inside the same `server/` structure — no separate scalable classifier server is used.

This design simplifies development and testing, without the need to manage inter-server communication for classification requests. The classifier is imported and used directly inside the main API logic.

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
│   ├── managers/             # Logic wrapper (e.g. Manager)
│   │   └── manager.py
│   ├── ui/                   # Text UI logic
│   │   └── menu.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── server/                   # All server-side logic (FastAPI + classifier)
│   ├── app/                  # FastAPI routing
│   │   ├── app.py
│   │   └── api_endpoints.py
│   ├── core/                 # Classifier and trainer
│   │   ├── classifier.py
│   │   ├── naive_bayes_trainer.py
│   │   └── dal/dal.py
│   ├── data/                 # Example CSVs
│   ├── services/             # Controller abstraction
│   │   └── Controller.py
│   ├── utils/                # Cleaning, conversion, testing tools
│   │   ├── cleaner.py
│   │   ├── extract.py
│   │   ├── convert_numpy_types.py
│   │   └── test_accuracy.py
│   ├── run.py                # Server entrypoint
│   ├── requirements.txt
│   └── Dockerfile
│
├── .gitignore
└── README.md
```

---

## ⚙️ How to Run

### 🖥️ Start the Server:
```bash
cd server
python run.py
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
- Classifier is now **directly used** by the API server (no separate microservice).
- Ideal for learning and testing without managing distributed deployment.

---

## 🛠️ Potential Improvements
- ✅ Add persistent storage (pickle, SQLite)
- ✅ Add API schema validation with Pydantic
- ✅ Improve error handling and feedback
- ✅ Add unit tests (e.g. `pytest`)
