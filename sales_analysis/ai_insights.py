import os

def generate_ai_insights(results):

    insights = f"""
===============================
📊 EXECUTIVE SUMMARY
===============================
The business generated a total revenue of {results['total_revenue']:.2f}.
The top-performing product is "{results['top_product']}", and the leading region is {results['top_region']}.

===============================
🔍 KEY INSIGHTS
===============================
- The top product "{results['top_product']}" contributes significantly to overall revenue.
- {results['top_region']} dominates sales, indicating strong market demand in this region.

- Top 5 Products by Revenue:
"""

    for product, value in results["top_5_products"].items():
        insights += f"\n  • {product}: {value:.2f}"

    insights += """

===============================
💡 BUSINESS RECOMMENDATIONS
===============================
- Increase inventory and marketing efforts for top-performing products.
- Expand operations in high-performing regions to maximize revenue.
- Investigate underperforming products and optimize pricing or promotion strategies.
- Monitor monthly sales trends to identify growth opportunities and seasonality patterns.

===============================
📈 CONCLUSION
===============================
The analysis highlights key revenue drivers and growth opportunities. Strategic focus on high-performing products and regions can significantly improve overall business performance.
"""

    # Ensure outputs folder exists
    os.makedirs("outputs", exist_ok=True)

    # Save insights
    with open("outputs/insights.txt", "w") as f:
        f.write(insights)

    return insights