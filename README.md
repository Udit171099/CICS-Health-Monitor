import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

# Avg response time per region
if not filtered_df.empty:
    region_group = filtered_df.groupby("Region")["ResponseTime"].mean()

    fig, ax = plt.subplots()
    region_group.plot(kind="bar", ax=ax)
    ax.set_title("Average Response Time by Region")
    ax.set_ylabel("Response Time (sec)")
    st.pyplot(fig)

    # Avg response time per transaction
    txn_group = filtered_df.groupby("TransactionID")["ResponseTime"].mean().sort_values().head(15)
    fig2, ax2 = plt.subplots()
    txn_group.plot(kind="bar", ax=ax2, color="orange")
    ax2.set_title("Top 15 Transactions by Avg Response Time")
    ax2.set_ylabel("Response Time (sec)")
    st.pyplot(fig2)

# ---------------- Download ----------------
st.subheader("📥 Download Data")
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="transactions_report.csv",
    mime="text/csv"
)




# CICS Region Transaction Monitor

This project simulates monitoring of CICS regions and running transactions. It includes:

- Filtering by CICS region
- Prefix-based transaction ID filtering (e.g., TN*)
- Identifying slow transactions (response time > 200ms)
- Summary chart of transaction count by region

## How to Run

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Run the Streamlit app:
```
streamlit run main.py
```

3. Visit `http://localhost:8501` in your browser.

## Dataset

A sample dataset `transactions.csv` is provided with mock transactions and regions.
