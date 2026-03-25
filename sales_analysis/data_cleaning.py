import pandas as pd
import os

def clean_data(file_path):
    df = pd.read_csv(file_path, encoding='latin1')

    # Standardize column names
    df.columns = df.columns.str.lower().str.strip()

    # Convert date column
    df['invoicedate'] = pd.to_datetime(df['invoicedate'])

    # Remove missing values
    df = df.dropna()

    # Remove negative or zero values (important for this dataset)
    df = df[(df['quantity'] > 0) & (df['unitprice'] > 0)]

    # ✅ Create SALES column
    df['sales'] = df['quantity'] * df['unitprice']

    # Rename columns for consistency
    df = df.rename(columns={
        'invoicedate': 'date',
        'description': 'product',
        'country': 'region'
    })

    # Create folder if needed
    os.makedirs("data/processed", exist_ok=True)

    # Save cleaned data
    df.to_csv("data/processed/cleaned_sales.csv", index=False)

    return df