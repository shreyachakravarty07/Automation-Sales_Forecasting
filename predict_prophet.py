# predict_prophet.py

import os
import pandas as pd
from prophet import Prophet
from joblib import load

def main():
    # 1) Load model
    model_path = "prophet_model.joblib"
    prophet_model = load(model_path)

    # 2) Generate predictions
    future = prophet_model.make_future_dataframe(periods=10)
    forecast = prophet_model.predict(future)
    prophet_predictions = forecast[['ds','yhat','yhat_lower','yhat_upper']].iloc[-10:]

    # 3) Save predictions to CSV
    output_path = "predictions.csv"
    prophet_predictions.to_csv(output_path, index=False)

    print(f"Predictions saved to {output_path}")
    print(prophet_predictions)

if __name__ == "__main__":
    main()
