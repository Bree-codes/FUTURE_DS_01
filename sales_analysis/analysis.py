import pandas as pd

def analyze_data(df):
    results = {}

    # -----------------------
    # Total revenue
    # -----------------------
    results["total_revenue"] = df["sales"].sum()

    # -----------------------
    # Profit
    # -----------------------
    if 'cost' in df.columns:
        df['profit'] = df['sales'] - df['cost']
        results['profit'] = df['profit'].sum()
    else:
        # Estimate profit at 30% if no cost column
        results['profit'] = results["total_revenue"] * 0.3

    # -----------------------
    # Top product
    # -----------------------
    if 'product' in df.columns and not df['product'].empty:
        results["top_product"] = df.groupby("product")["sales"].sum().idxmax()
    else:
        results["top_product"] = "N/A"

    # -----------------------
    # Top region
    # -----------------------
    if 'region' in df.columns and not df['region'].empty:
        results["top_region"] = df.groupby("region")["sales"].sum().idxmax()
    else:
        results["top_region"] = "N/A"

    # -----------------------
    # Monthly sales
    # -----------------------
    if 'month' not in df.columns:
        df['month'] = pd.to_datetime(df['date'], errors='coerce').dt.to_period("M").dt.to_timestamp()
    else:
        df['month'] = pd.to_datetime(df['month'], errors='coerce')
    df = df.dropna(subset=['month'])
    monthly_sales = df.groupby('month')['sales'].sum().sort_index()
    results['monthly_sales'] = monthly_sales.to_dict()

    # -----------------------
    # Growth rate (average month-over-month)
    # -----------------------
    if len(monthly_sales) > 1:
        growth_rates = monthly_sales.pct_change() * 100
        results['growth_rate'] = growth_rates.mean()
    else:
        results['growth_rate'] = 0

    # -----------------------
    # Top 5 products
    # -----------------------
    if 'product' in df.columns:
        top_5 = df.groupby('product')['sales'].sum().sort_values(ascending=False).head(5)
        results['top_5_products'] = top_5.to_dict()
    else:
        results['top_5_products'] = {}

    # -----------------------
    # Revenue by region
    # -----------------------
    if 'region' in df.columns:
        sales_by_region = df.groupby('region')['sales'].sum().sort_values(ascending=False).head(5)
        results['sales_by_region'] = sales_by_region.to_dict()
    else:
        results['sales_by_region'] = {}

    return results