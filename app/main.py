import os
import pickle
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from app.schemas import CorporateMetricsIn

app = FastAPI(
    title="ProfitIQ Enterprise Optimization API",
    description="REST API processing high-fidelity corporate performance predictions.",
    version="1.1"
)

model = None

@app.on_event("startup")
def load_serialized_model():
    """
    Executes on container startup initialization.
    Loads the trained model into memory to guarantee sub-millisecond API response arrays.
    """
    global model
    model_path = os.path.join(os.path.dirname(__file__), "random_forest_model.pkl")

    if not os.path.exists(model_path):
        print("⚠️ Warning: Pre-trained binary model artifact not found. Initializing a mock regressor layer.")
        class MockModel:
            def predict(self, df):
                return np.array([df['rd_spend'].values * 0.85 + df['marketing_spend'].values * 0.05 + 50000.00])
        model = MockModel()
    else:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        print("✅ Production Random Forest model binary cleanly mapped into microservice execution RAM.")

@app.post("/api/v1/predict", status_code=200)
async def execute_profit_prediction(payload: CorporateMetricsIn):
    """
    Ingests validated JSON structures, maps them to dataframes, and returns predictive yields.
    """
    try:
        input_data = pd.DataFrame([{
            "rd_spend": payload.rd_spend,
            "admin_cost": payload.admin_cost,
            "marketing_spend": payload.marketing_spend
        }])

        predicted_yield = model.predict(input_data)

        return {
            "status": "PROCESSED",
            "evaluated_metrics": {
                "research_development_spend": payload.rd_spend,
                "administrative_overhead": payload.admin_cost,
                "marketing_allocation": payload.marketing_spend
            },
            "predicted_corporate_profit": round(float(predicted_yield), 2)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Core inference pipeline failure: {str(e)}")
