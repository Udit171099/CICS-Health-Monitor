
import streamlit as st
import pandas as pd

st.set_page_config(page_title="CICS Region Monitor", layout="wide")

# Title
st.title("🖥️ CICS Region Transaction Monitor")

# Load Data
df = pd.read_csv("transactions.csv")

# Sidebar Filters
st.sidebar.header("Filter Options")
regions = df['CICS_Region'].unique()
selected_region = st.sidebar.selectbox("Select CICS Region", options=["All"] + list(regions))

prefix_input = st.sidebar.text_input("Enter Transaction Prefix (e.g., TN*)", value="")

# Filter Logic
filtered_df = df.copy()

if selected_region != "All":
    filtered_df = filtered_df[filtered_df['CICS_Region'] == selected_region]

if prefix_input:
    prefix = prefix_input.rstrip("*")
    filtered_df = filtered_df[filtered_df['Transaction_ID'].str.startswith(prefix)]

# Display Table
st.subheader("Filtered Transactions")
st.dataframe(filtered_df, use_container_width=True)

# Alert on High Response Time
threshold = 200
slow_txns = filtered_df[filtered_df['Response_Time'] > threshold]

if not slow_txns.empty:
    st.error(f"⚠️ {len(slow_txns)} Slow Transactions Found (Response Time > {threshold} ms)")
    st.dataframe(slow_txns, use_container_width=True)

# Summary Chart
st.subheader("📊 Transaction Count by Region")
chart_data = df['CICS_Region'].value_counts()
st.bar_chart(chart_data)
