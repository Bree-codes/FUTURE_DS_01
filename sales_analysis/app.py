import streamlit as st
import pandas as pd
import plotly.express as px
from data_cleaning import clean_data
from analysis import analyze_data

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    layout="wide",
    page_icon="📊"
)

# -----------------------
# DARK THEME
# -----------------------
st.markdown("""
<style>
/* KPI metric title font */
.stMetricLabel {
    font-size: 16px !important;
}

/* KPI metric value font */
.stMetricValue {
    font-size: 15px !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# TITLE
# -----------------------
st.title("📊 Sales Analytics Dashboard")
st.markdown("Interactive business intelligence dashboard for sales performance analysis")

# -----------------------
# FILE UPLOAD
# -----------------------
uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

# -----------------------
# HANDLE DATA
# -----------------------
if uploaded_file:
    df = clean_data(uploaded_file)

    # Ensure 'cost' column exists; if not, estimate 30% profit
    if 'cost' not in df.columns:
        df['cost'] = df['sales'] * 0.7

    # Ensure month column exists
    if 'month' not in df.columns:
        df['month'] = pd.to_datetime(df['date'], errors='coerce').dt.to_period("M").dt.to_timestamp()
    else:
        df['month'] = pd.to_datetime(df['month'], errors='coerce')
        df = df.dropna(subset=['month'])

    results = analyze_data(df)

else:
    # Placeholder data
    df = pd.DataFrame({
        "region": ["Region A", "Region B", "Region C"],
        "sales": [0, 0, 0],
        "product": ["Product X", "Product Y", "Product Z"],
        "month": pd.to_datetime(["2026-01-01", "2026-02-01", "2026-03-01"])
    })
    results = {
        "total_revenue": 0,
        "profit": 0,
        "top_product": "N/A",
        "top_region": "N/A",
        "monthly_sales": {pd.Timestamp("2026-01-01"):0, pd.Timestamp("2026-02-01"):0, pd.Timestamp("2026-03-01"):0},
        "top_5_products": {"Product X":0,"Product Y":0,"Product Z":0},
        "growth_rate": 0,
        "sales_by_region": {"Region A":0,"Region B":0,"Region C":0}
    }

# -----------------------
# FILTERS
# -----------------------
st.sidebar.header(" Filters")
region_filter = st.sidebar.multiselect(
    "Select Region",
    options=df["region"].unique(),
    default=df["region"].unique()
)
df_filtered = df[df["region"].isin(region_filter)]

# -----------------------
# CUSTOM KPI CARDS
# -----------------------
st.subheader("📈 Key Performance Indicators")

# Create 5 equal columns
col1, col2, col3, col4, col5 = st.columns(5)

def kpi_card(column, title, value, emoji=""):
    column.markdown(f"""
    <div style="
        background-color:#1f1f1f; 
        padding:25px; 
        border-radius:10px; 
        text-align:center;
        color:white;
        ">
        <div style="font-size:17px;">{emoji} {title}</div>
        <div style="font-size:18px; font-weight:semi-bold;">{value}</div>
    </div>
    """, unsafe_allow_html=True)

# Place each card in its column
kpi_card(col1, "Total Revenue", f"${results['total_revenue']:,.0f}", "💰")
kpi_card(col2, "Profit", f"${results.get('profit',0):,.0f}", "💹")
kpi_card(col3, "Top Product", results['top_product'], "🏆")
kpi_card(col4, "Top Region", results['top_region'], "🌍")
kpi_card(col5, "Growth Rate", f"{results.get('growth_rate',0):.2f}%", "📈")

# -----------------------
# MAIN CHARTS
# -----------------------
col1, col2 = st.columns(2)

# Monthly Revenue Trend
monthly_df = pd.DataFrame(list(results["monthly_sales"].items()), columns=["Month", "Sales"])
monthly_df = monthly_df.sort_values("Month")
fig1 = px.line(monthly_df, x="Month", y="Sales", title="Monthly Revenue Trend", template="plotly_dark")
col1.plotly_chart(fig1, use_container_width=True)

# Top Products
top_products_df = pd.DataFrame(list(results["top_5_products"].items()), columns=["Product", "Sales"])
fig2 = px.bar(top_products_df, x="Product", y="Sales", text_auto=True, title="Top 5 Products", template="plotly_dark")
col2.plotly_chart(fig2, use_container_width=True)

st.divider()

# Sales by Region
st.subheader(" Sales by Region")
region_df = df_filtered.groupby("region")["sales"].sum().reset_index()
fig3 = px.bar(region_df.sort_values(by="sales", ascending=False), x="region", y="sales",
              title="Revenue by Region", template="plotly_dark")
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# -----------------------
# ADVANCED CHARTS
# -----------------------
st.subheader("💹 Advanced Analytics")
col1, col2 = st.columns(2)

# Monthly Profit Trend
if 'profit' not in df.columns:
    df['profit'] = df['sales'] * 0.3
df_profit = df.groupby('month')['profit'].sum().reset_index()
fig_profit = px.line(df_profit.sort_values('month'), x='month', y='profit',
                     title="Monthly Profit Trend", template="plotly_dark")
col1.plotly_chart(fig_profit, use_container_width=True)

# Regional Contribution Pie Chart
sales_by_region_df = pd.DataFrame(list(results['sales_by_region'].items()), columns=['Region', 'Sales'])
fig_pie = px.pie(sales_by_region_df, names='Region', values='Sales',
                 title="Regional Contribution to Total Sales", template="plotly_dark")
col2.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# -----------------------
# INSIGHTS
# -----------------------
st.subheader(" Business Insights")
st.markdown(f"""
**Key Findings:**
- Total Revenue: **${results['total_revenue']:,.0f}**
- Profit: **${results.get('profit',0):,.0f}**
- Top Product: **{results['top_product']}**
- Top Region: **{results['top_region']}**
- Growth Rate: **{results.get('growth_rate',0):.2f}%**

**Recommendations:**
- Invest in high-performing products.
- Expand operations in top regions.
- Monitor monthly trends to capture growth opportunities.
""")
