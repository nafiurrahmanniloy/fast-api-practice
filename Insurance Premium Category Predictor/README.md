# 🚀 Insurance Premium Prediction API (FastAPI)

This project shows how to wrap a trained Machine Learning model in a clean, production-style API using FastAPI, and then plug that API into a simple frontend for interactive insurance premium predictions.

![App Screenshot](Screenshot-2025-12-09-232440.png)

## 🔧 What this project does

We take a trained insurance premium model saved as `model.pkl` and:

- Load it once at server startup in `app.py`.
- Expose a `/predict` endpoint using FastAPI.
- Validate incoming JSON with Pydantic models.
- Return the predicted premium category (for example: Low / Medium / High) as JSON.
- Call this API from a UI (`frontend.py`) so users can fill a form and see the prediction instantly.

## 🧠 How the API is built

- The model is deserialized from `model.pkl` when the FastAPI app starts, so it stays in memory and predictions are fast.
- A Pydantic `BaseModel` defines the request body with fields like:
  - age  
  - city  
  - weight (kg)  
  - height (meters)  
  - income (LPA)  
  - occupation  
  - smoker (boolean or yes/no)  
- The `POST /predict` endpoint:
  - Receives the JSON body matching this schema.
  - Optionally computes extra features (for example, BMI from height and weight) and encodes categorical variables.
  - Calls `model.predict(...)` with the processed features.
  - Returns a JSON response such as: `{ "predicted_category": "Low" }`.

## 🖥️ Frontend: how it uses the API

The `frontend.py` file acts as a client (for example, with Streamlit):

- Renders a form where the user enters age, city, weight, height, income, occupation and smoker status.
- Builds a JSON payload from the form inputs.
- Sends a `POST` request to `/predict` on the FastAPI backend.
- Displays the returned `predicted_category` in the UI (for example, “Predicted Category: Low” with a colored banner).

## 🏁 Running the project

1. Install dependencies (example):

   `pip install fastapi uvicorn streamlit scikit-learn pandas`

2. Start the FastAPI backend:

   `uvicorn app:app --reload`

3. Start the frontend (adjust if you wired it differently):

   `streamlit run frontend.py`

