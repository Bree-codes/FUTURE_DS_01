import matplotlib.pyplot as plt

def create_visuals(df, results):

    # Monthly sales trend
    months = list(results["monthly_sales"].keys())
    sales = list(results["monthly_sales"].values())

    plt.figure()
    plt.plot(months, sales)
    plt.title("Monthly Sales Trend")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("visuals/monthly_sales.png")

    # Top products
    products = list(results["top_5_products"].keys())
    values = list(results["top_5_products"].values())

    plt.figure()
    plt.bar(products, values)
    plt.title("Top 5 Products")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("visuals/top_products.png")