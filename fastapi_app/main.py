from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from joblib import load
import os
import pandas as pd
import uvicorn
from contextlib import asynccontextmanager


app = FastAPI()
model = None

# Define the input schema for prediction
class PredictionInput(BaseModel):
    ds: str  # Date string in the format Prophet expects

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    model_path = "./prophet_model_0.joblib"
    if os.path.exists(model_path):
        model = load(model_path)
        print("Model loaded successfully!")
    else:
        print("Model file not found!")
    yield
    # Cleanup code can go here if needed

app.router.lifespan_context = lifespan

@app.get("/")
def read_root():
    return {"message": "Welcome to the Prophet Model API"}

@app.post("/predict")
def predict(input: PredictionInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    # Create DataFrame from the input date
    df = pd.DataFrame({"ds": [input.ds]})
    forecast = model.predict(df)
    # Return the prediction details
    return {
        "ds": forecast["ds"].iloc[0],
        "yhat": forecast["yhat"].iloc[0],
        "yhat_lower": forecast["yhat_lower"].iloc[0],
        "yhat_upper": forecast["yhat_upper"].iloc[0]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
