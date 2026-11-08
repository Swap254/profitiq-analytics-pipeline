from fastapi.testclient import TestClient

from app.main import app


def test_health_check():
    with TestClient(app) as client:
        response = client.get("/health")

        assert response.status_code == 200

        data = response.json()

        assert data["status"] == "healthy"
        assert data["model_loaded"] is True


def test_single_prediction():
    with TestClient(app) as client:
        payload = {
            "rd_spend": 165349.20,
            "admin_cost": 136897.80,
            "marketing_spend": 471784.10,
        }

        response = client.post(
            "/api/v1/predict",
            json=payload,
        )

        assert response.status_code == 200

        data = response.json()

        assert data["status"] == "success"
        assert "predicted_profit" in data
        assert isinstance(data["predicted_profit"], float)


def test_negative_value_rejected():
    with TestClient(app) as client:
        payload = {
            "rd_spend": -1000,
            "admin_cost": 50000,
            "marketing_spend": 100000,
        }

        response = client.post(
            "/api/v1/predict",
            json=payload,
        )

        assert response.status_code == 422


def test_batch_prediction():
    with TestClient(app) as client:
        payload = {
            "records": [
                {
                    "rd_spend": 165349.20,
                    "admin_cost": 136897.80,
                    "marketing_spend": 471784.10,
                },
                {
                    "rd_spend": 300000,
                    "admin_cost": 100000,
                    "marketing_spend": 250000,
                },
            ]
        }

        response = client.post(
            "/api/v1/predict/batch",
            json=payload,
        )

        assert response.status_code == 200

        data = response.json()

        assert data["status"] == "success"
        assert data["records_processed"] == 2
        assert len(data["predictions"]) == 2


def test_empty_batch_rejected():
    with TestClient(app) as client:
        payload = {
            "records": []
        }

        response = client.post(
            "/api/v1/predict/batch",
            json=payload,
        )

        assert response.status_code == 422