def generate_ai_insights(results):
    insights = f"""
    ===============================
    📊 EXECUTIVE SUMMARY
    ===============================
    The business generated a total revenue of {results['total_revenue']}.
    The top-performing product is {results['top_product']}, while the leading region is {results['top_region']}.

    ===============================
    🔍 KEY INSIGHTS
    ===============================
    - The highest revenue contribution comes from {results['top_product']}, indicating strong product-market fit.
    - {results['top_region']} is the best-performing region, suggesting higher demand or better market penetration.

    - Top 5 products by revenue:
    """

    for product, value in results["top_5_products"].items():
        insights += f"\n  • {product}: {value}"

    insights += f"""

    ===============================
    💡 RECOMMENDATIONS
    ===============================
    - Increase investment in {results['top_product']} to maximize revenue growth.
    - Expand operations and marketing in {results['top_region']} to capitalize on strong performance.
    - Analyze lower-performing products to identify improvement opportunities.
    - Maintain consistent monitoring of monthly sales trends to detect growth opportunities.

    """

    # Save to file
    with open("outputs/insights.txt", "w") as f:
        f.write(insights)

    return insights


# from openai import OpenAI
#
# client = OpenAI()
#
# def generate_ai_insights(results):
#
#     prompt = f"""
#     You are a senior business data analyst.
#
#     Based on the following data:
#     - Total Revenue: {results['total_revenue']}
#     - Top Product: {results['top_product']}
#     - Top Region: {results['top_region']}
#     - Monthly Sales: {results['monthly_sales']}
#     - Top 5 Products: {results['top_5_products']}
#
#     Provide:
#     1. Executive Summary
#     2. Key Insights
#     3. Business Recommendations
#     """
#
#     response = client.chat.completions.create(
#         model="gpt-5",
#         messages=[{"role": "user", "content": prompt}]
#     )
#
#     insights = response.choices[0].message.content
#
#     with open("outputs/insights.txt", "w") as f:
#         f.write(insights)
#
#     return insights
