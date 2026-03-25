def analyze_data(df):
    results = {}

    # Total revenue
    results["total_revenue"] = df["sales"].sum()

    # Top product
    results["top_product"] = (
        df.groupby("product")["sales"].sum().idxmax()
    )

    # Top region
    results["top_region"] = (
        df.groupby("region")["sales"].sum().idxmax()
    )

    # Monthly revenue
    df["month"] = df["date"].dt.to_period("M")
    monthly_sales = df.groupby("month")["sales"].sum()

    results["monthly_sales"] = monthly_sales.to_dict()

    # Top 5 products
    results["top_5_products"] = (
        df.groupby("product")["sales"].sum()
        .nlargest(5)
        .to_dict()
    )

    # Revenue by country
    results["sales_by_region"] = (
        df.groupby("region")["sales"].sum()
        .sort_values(ascending=False)
        .head(5)
        .to_dict()
    )

    return results