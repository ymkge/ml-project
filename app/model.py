import pickle
import pandas as pd
from pydantic import BaseModel

# --- Model Loading ---
MODEL_PATH = "app/model.pkl"

try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    # This is a fallback for when the app is run without a pre-trained model.
    # In a real scenario, you'd want to handle this more gracefully.
    model = None

# --- Prediction Logic ---

class PredictionInput(BaseModel):
    """Input data schema for prediction."""
    Pclass: int
    Sex: str
    Age: float
    SibSp: int
    Parch: int
    Fare: float
    Embarked: str

class PredictionOutput(BaseModel):
    """Output data schema for prediction."""
    prediction: int
    probability: float

def predict(input_data: PredictionInput) -> PredictionOutput:
    """Runs a prediction using the loaded model."""
    if model is None:
        raise RuntimeError(
            "Model is not loaded. Run the training notebook `notebooks/train.ipynb` first."
        )

    # Convert Pydantic model to DataFrame
    input_df = pd.DataFrame([input_data.model_dump()])

    # Get prediction (returns a list with one value)
    pred = model.predict(input_df)[0]
    
    # Get probability (returns a list of lists)
    prob = model.predict_proba(input_df)[0][int(pred)]

    return PredictionOutput(prediction=int(pred), probability=float(prob))
