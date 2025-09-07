import sys
import os
from fastapi.testclient import TestClient

# Add the project root to the Python path to allow imports from `app`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

# Create a TestClient instance
client = TestClient(app)


def test_health_check():
    """Tests the /health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_success():
    """Tests a successful prediction through the /predict endpoint."""
    payload = {
        "Pclass": 3,
        "Sex": "male",
        "Age": 22.0,
        "SibSp": 1,
        "Parch": 0,
        "Fare": 7.25,
        "Embarked": "S"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "probability" in data
    assert isinstance(data["prediction"], int)
    assert isinstance(data["probability"], float)


def test_predict_validation_error():
    """Tests the /predict endpoint with invalid data (missing field)."""
    payload = {
        "Pclass": 3,
        "Sex": "male",
        # "Age" is missing
        "SibSp": 1,
        "Parch": 0,
        "Fare": 7.25,
        "Embarked": "S"
    }
    response = client.post("/predict", json=payload)
    # FastAPI should return a 422 Unprocessable Entity for validation errors
    assert response.status_code == 422

def test_predict_invalid_type():
    """Tests the /predict endpoint with invalid data type."""
    payload = {
        "Pclass": 3,
        "Sex": "male",
        "Age": "twenty-two",  # Invalid type, should be a number
        "SibSp": 1,
        "Parch": 0,
        "Fare": 7.25,
        "Embarked": "S"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
