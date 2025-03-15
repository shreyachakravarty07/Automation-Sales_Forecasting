import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
import numpy as np
np.float_ = np.float64
from typing import List, Dict
from prophet import Prophet
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import seaborn as sns
from sklearn.model_selection import GridSearchCV

# read
df = pd.read_csv(r"sales.csv")
# print(df['PROMO_YEAR_ID'].unique())
# df.head()

# "TRANSACTION_DATE" is supposed to be a date-field, and "units_sold" must be a whole number value
df['units_sold'] = df['units_sold'].astype('int64')
df['TRANSACTION_DATE'] = pd.to_datetime(df['TRANSACTION_DATE'])

# dropping 'sku', 'PROMO_YEAR_ID', 'PROMO_WEEK_NUMBER'
# - sku is an ID
# - 'PROMO_YEAR_ID' is an ID, so it is unnecessary since the data is in the same year and only has 4 weeks of records
# - 'PROMO_WEEK_NUMBER' is the week number of the year, showing no seasonal importance
df = df.drop(['sku', 'PROMO_YEAR_ID', 'PROMO_WEEK_NUMBER'], axis=1)
# df.head(15)

# finalizing the dataset
revenue_by_category = df.groupby('product_category')['units_revenue'].sum().sort_values()
max_revenue_category = revenue_by_category.idxmax()
df_max_revenue_category = df[df['product_category'] == max_revenue_category]
final_df = df_max_revenue_category.drop(['units_revenue', 'product_category'], axis=1)
final_df = final_df.groupby(['TRANSACTION_DATE']).sum().reset_index()
final_df.set_index('TRANSACTION_DATE', inplace=True)
final_df.index = pd.to_datetime(final_df.index)

df_prophet = final_df.reset_index().rename(columns={'TRANSACTION_DATE': 'ds', 'units_sold': 'y'})

#training
# Defining the training and testing period
train_size = 21  # First 3 weeks (21 days) for training

if __name__ == '__main__':
    prophet_model = Prophet()
    prophet_model.fit(df_prophet.iloc[:train_size])

    # Saving the model
    from joblib import dump
    import os

    # List all files in the directory
    path = "./models"
    file_list = os.listdir(path)
    # print("Files in directory:", file_list)

    if file_list:
        # file_list.sort()
        new = len(file_list) + 1
        # new = int(latest) + 1
        # print(new, latest)
        dump(prophet_model, os.path.join(path, f'prophet_model_{new}.joblib'))
        
    # print(file_list[-1])
    else:
        dump(prophet_model, os.path.join(path, 'prophet_model_1.joblib'))

    # Prophet model
    from joblib import load
    # print(os.listdir(path))
    file_list = os.listdir(path)
    file_list.sort()
    prophet_model = load(os.path.join(path, file_list[-1]))
    print(file_list[-1])

    # predictions
    future = prophet_model.make_future_dataframe(periods=10) # to forecast 7 days ahead
    forecast = prophet_model.predict(future)
    prophet_predictions = forecast['yhat'].iloc[-10:]
    print(prophet_predictions)


    
    # print