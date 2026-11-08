import os
import pickle

import pandas as pd
from fastapi import FastAPI, HTTPException

from app.schemas import CorporateMetricsIn, BatchCorporateMetricsIn


app = FastAPI(
    title="ProfitIQ Analytics API",
    description="API for predicting corporate profit from financial metrics.",
    version="1.0.0",
)


model = None


@app.on_event("startup")
def load_model():
    global model

    model_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "model",
        "random_forest_model.pkl",
    )

    model_path = os.path.abspath(model_path)

    if not os.path.exists(model_path):
        raise RuntimeError(
            f"Trained model not found at: {model_path}"
        )

    with open(model_path, "rb") as file:
        model = pickle.load(file)

    print(f"Model loaded successfully from: {model_path}")


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
    }


@app.post("/api/v1/predict")
async def predict_profit(payload: CorporateMetricsIn):
    try:
        input_data = pd.DataFrame([
            {
                "rd_spend": payload.rd_spend,
                "admin_cost": payload.admin_cost,
                "marketing_spend": payload.marketing_spend,
            }
        ])

        prediction = model.predict(input_data)

        return {
            "status": "success",
            "input": {
                "rd_spend": payload.rd_spend,
                "admin_cost": payload.admin_cost,
                "marketing_spend": payload.marketing_spend,
            },
            "predicted_profit": round(float(prediction[0]), 2),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(exc)}",
        )


@app.post("/api/v1/predict/batch")
async def predict_profit_batch(payload: BatchCorporateMetricsIn):
    try:
        input_data = pd.DataFrame([
            {
                "rd_spend": record.rd_spend,
                "admin_cost": record.admin_cost,
                "marketing_spend": record.marketing_spend,
            }
            for record in payload.records
        ])

        predictions = model.predict(input_data)

        results = []

        for record, prediction in zip(
                payload.records,
                predictions,
        ):
            results.append({
                "rd_spend": record.rd_spend,
                "admin_cost": record.admin_cost,
                "marketing_spend": record.marketing_spend,
                "predicted_profit": round(float(prediction), 2),
            })

        return {
            "status": "success",
            "records_processed": len(results),
            "predictions": results,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Batch prediction failed: {str(exc)}",
        )