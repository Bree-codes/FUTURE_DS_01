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
# DARK THEME + STYLING
# -----------------------
st.markdown("""
    <style>
    body {
        background-color:#0E1117;
        color:white;
    }
    .stButton>button {
        background-color: #0078d4;
        color: white;
    }
    .big-font {
        font-size:18px !important;
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
# PLACEHOLDER DATA (for empty dashboard)
# -----------------------
if uploaded_file:
    df = clean_data(uploaded_file)
    results = analyze_data(df)
else:
    df = pd.DataFrame({
        "region": ["Region A", "Region B", "Region C"],
        "sales": [0, 0, 0],
        "product": ["Product X", "Product Y", "Product Z"],
        "month": ["Jan", "Feb", "Mar"]
    })
    results = {
        "total_revenue": 0,
        "top_product": "N/A",
        "top_region": "N/A",
        "monthly_sales": {"Jan": 0, "Feb": 0, "Mar": 0},
        "top_5_products": {"Product X": 0, "Product Y": 0, "Product Z": 0},
        "profit": 0,
        "growth_rate": 0
    }

# -----------------------
# FILTERS
# -----------------------
st.sidebar.header("🔍 Filters")
region_filter = st.sidebar.multiselect(
    "Select Region",
    options=df["region"].unique(),
    default=df["region"].unique()
)
df_filtered = df[df["region"].isin(region_filter)]

# -----------------------
# KPI SECTION (Cards)
# -----------------------
st.subheader("📈 Key Performance Indicators")
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("💰 Total Revenue", f"${results['total_revenue']:,.0f}")
col2.metric("🏆 Top Product", results['top_product'])
col3.metric("🌍 Top Region", results['top_region'])
col4.metric("📈 Growth Rate", f"{results.get('growth_rate',0):.2f}%")
col5.metric("💹 Profit", f"${results.get('profit',0):,.0f}")

st.divider()

# -----------------------
# CHARTS SECTION
# -----------------------
col1, col2 = st.columns(2)

# Monthly Revenue Trend
monthly_df = pd.DataFrame(list(results["monthly_sales"].items()), columns=["Month", "Sales"])
fig1 = px.line(monthly_df, x="Month", y="Sales", title="Monthly Revenue Trend", template="plotly_dark")
col1.plotly_chart(fig1, use_container_width=True)

# Top Products
top_products_df = pd.DataFrame(list(results["top_5_products"].items()), columns=["Product", "Sales"])
fig2 = px.bar(top_products_df, x="Product", y="Sales", text_auto=True, title="Top 5 Products", template="plotly_dark")
col2.plotly_chart(fig2, use_container_width=True)

st.divider()

# Sales by Region
st.subheader("🌍 Sales by Region")
region_df = df_filtered.groupby("region")["sales"].sum().reset_index()
fig3 = px.bar(region_df.sort_values(by="sales", ascending=False), x="region", y="sales",
              title="Revenue by Region", template="plotly_dark")
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# -----------------------
# INSIGHTS
# -----------------------
st.subheader("🤖 Business Insights")
st.markdown(f"""
**Key Findings:**
- Total Revenue: **${results['total_revenue']:,.0f}**
- Top Product: **{results['top_product']}**
- Top Region: **{results['top_region']}**
- Growth Rate: **{results.get('growth_rate',0):.2f}%**
- Profit: **${results.get('profit',0):,.0f}**

**Recommendations:**
- Invest in high-performing products.
- Expand operations in top regions.
- Monitor monthly trends to capture growth opportunities.
""")

st.success("✅ Dashboard Ready!")