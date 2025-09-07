from fastapi import FastAPI, HTTPException
from .model import predict, PredictionInput, PredictionOutput

app = FastAPI(
    title="ML Model API",
    description="API for the Titanic survival prediction model.",
    version="0.1.0",
)

@app.get("/health", tags=["Health Check"])
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}

@app.post("/predict", response_model=PredictionOutput, tags=["Prediction"])
async def make_prediction(input_data: PredictionInput):
    """
    Receives passenger data and returns a survival prediction.
    - **Pclass**: Ticket class (1 = 1st, 2 = 2nd, 3 = 3rd)
    - **Sex**: Sex (`male` or `female`)
    - **Age**: Age in years
    - **SibSp**: # of siblings / spouses aboard the Titanic
    - **Parch**: # of parents / children aboard the Titanic
    - **Fare**: Passenger fare
    - **Embarked**: Port of Embarkation (C = Cherbourg, Q = Queenstown, S = Southampton)
    """
    try:
        result = predict(input_data)
        return result
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
