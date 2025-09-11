import sys
import os
from fastapi.testclient import TestClient
from unittest.mock import patch

# Add the project root to the Python path to allow imports from `app`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.model import PredictionOutput

# Create a TestClient instance
client = TestClient(app)


def test_health_check():
    """Tests the /health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("app.main.predict")
def test_predict_success(mock_predict):
    """Tests a successful prediction through the /predict endpoint."""
    # Configure the mock to return a dummy prediction
    mock_predict.return_value = PredictionOutput(prediction=1, probability=0.9)
    
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
    assert data["prediction"] == 1
    assert data["probability"] == 0.9


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
