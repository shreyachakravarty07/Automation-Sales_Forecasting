# train_prophet.py

import os
import pandas as pd
from prophet import Prophet
from joblib import dump

def main():
    # 1) Read processed data
    df = pd.read_csv("processed_data.csv")  # Produced by data_processing.py
    df['TRANSACTION_DATE'] = pd.to_datetime(df['TRANSACTION_DATE'])

    # 2) Prepare for Prophet
    df_prophet = df.rename(columns={'TRANSACTION_DATE': 'ds', 'units_sold': 'y'})
    train_size = 21

    # 3) Train
    prophet_model = Prophet()
    prophet_model.fit(df_prophet.iloc[:train_size])

    # 4) Save model
    # By default let's just name it prophet_model.joblib
    model_path = "prophet_model.joblib"
    dump(prophet_model, model_path)

    print(f"Model trained and saved to {model_path}")

if __name__ == "__main__":
    main()
