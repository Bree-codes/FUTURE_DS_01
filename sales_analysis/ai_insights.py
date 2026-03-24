from openai import OpenAI

client = OpenAI()

def generate_ai_insights(results):

    prompt = f"""
    You are a senior business data analyst.

    Based on the following data:
    - Total Revenue: {results['total_revenue']}
    - Top Product: {results['top_product']}
    - Top Region: {results['top_region']}
    - Monthly Sales: {results['monthly_sales']}
    - Top 5 Products: {results['top_5_products']}

    Provide:
    1. Executive Summary
    2. Key Insights
    3. Business Recommendations
    """

    response = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}]
    )

    insights = response.choices[0].message.content

    with open("outputs/insights.txt", "w") as f:
        f.write(insights)

    return insights