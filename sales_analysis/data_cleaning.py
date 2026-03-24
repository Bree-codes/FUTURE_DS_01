import pandas as pd

def clean_data(file_path):
    df = pd.read_csv(file_path)

    # Standardize column names
    df.columns = df.columns.str.lower().str.strip()

    # Handle missing values
    df = df.dropna()

    # Convert date column
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])

    # Ensure numeric columns
    if 'sales' in df.columns:
        df['sales'] = pd.to_numeric(df['sales'], errors='coerce')

    df = df.dropna()

    # Save cleaned data
    df.to_csv("data/processed/cleaned_sales.csv", index=False)

    return df