import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("transactions.csv")

df = load_data()

st.title("CICS Transaction Monitoring Dashboard")

# ---------------- Filters ----------------
st.sidebar.header("🔍 Filters")
regions = st.sidebar.multiselect("Select Region(s)", df["Region"].unique())
transactions = st.sidebar.text_input("Search Transaction (e.g., TN*, EN01)")

filtered_df = df.copy()

# Apply region filter
if regions:
    filtered_df = filtered_df[filtered_df["Region"].isin(regions)]

# Apply transaction filter (supports prefix search like TN*)
if transactions:
    if transactions.endswith("*"):
        prefix = transactions[:-1]
        filtered_df = filtered_df[filtered_df["TransactionID"].str.startswith(prefix)]
    else:
        filtered_df = filtered_df[filtered_df["TransactionID"] == transactions]

# ---------------- Show All Transactions ----------------
st.subheader("📋 All Transactions (Filtered)")
st.dataframe(filtered_df)

# ---------------- Failed Transactions ----------------
st.subheader("🚨 Failed Transactions")
failed_df = filtered_df[filtered_df["Status"] == "FAILED"]
if not failed_df.empty:
    st.dataframe(failed_df)
else:
    st.success("No failed transactions detected ✅")

# ---------------- High Response Time ----------------
st.subheader("⚡ High Response Time Transactions (>= 5 sec)")
high_resp_df = filtered_df[filtered_df["ResponseTime"] >= 5]
if not high_resp_df.empty:
    st.warning("Some transactions are taking longer than expected!")
    st.dataframe(high_resp_df)
else:
    st.success("All transactions are within normal response time.")

# ---------------- Charts ----------------
st.subheader("📊 Visualization")

if not filtered_df.empty:
    # Avg response time per region
    region_group = filtered_df.groupby("Region")["ResponseTime"].mean().reset_index()
    st.bar_chart(region_group.set_index("Region"))

    # Avg response time per transaction (top 15)
    txn_group = (
        filtered_df.groupby("TransactionID")["ResponseTime"]
        .mean()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )
    st.bar_chart(txn_group.set_index("TransactionID"))

# ---------------- Download ----------------
st.subheader("📥 Download Data")
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="transactions_report.csv",
    mime="text/csv"
)
