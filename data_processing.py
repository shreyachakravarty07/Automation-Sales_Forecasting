# data_processing.py

import os
import pandas as pd
import numpy as np

# If you want to remain consistent with your code:
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
# ... (other imports if needed)

def main():
    # 1) Read CSV
    df = pd.read_csv("sales.csv")  # or pass in from Argo param

    # 2) Transform
    df['units_sold'] = df['units_sold'].astype('int64')
    df['TRANSACTION_DATE'] = pd.to_datetime(df['TRANSACTION_DATE'])
    df = df.drop(['sku', 'PROMO_YEAR_ID', 'PROMO_WEEK_NUMBER'], axis=1)

    revenue_by_category = df.groupby('product_category')['units_revenue'].sum().sort_values()
    max_revenue_category = revenue_by_category.idxmax()
    df_max_revenue_category = df[df['product_category'] == max_revenue_category]

    final_df = df_max_revenue_category.drop(['units_revenue', 'product_category'], axis=1)
    final_df = final_df.groupby(['TRANSACTION_DATE']).sum().reset_index()

    # 3) Save to CSV for next step
    output_path = "processed_data.csv"
    final_df.to_csv(output_path, index=False)

    print(f"Data processing complete. File saved to {output_path}")

if __name__ == "__main__":
    main()
