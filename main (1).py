import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("transactions.csv")

df = load_data()

st.title("CICS Transaction Monitoring Dashboard")

# Show all transactions
st.subheader("All Transactions")
st.dataframe(df)

# Show failed transactions
st.subheader("🚨 Failed Transactions")
failed_df = df[df["Status"] == "FAILED"]
if not failed_df.empty:
    st.dataframe(failed_df)
else:
    st.success("No failed transactions detected ✅")

# High response time alert
st.subheader("⚡ High Response Time Transactions (>= 5 sec)")
high_resp_df = df[df["ResponseTime"] >= 5]
if not high_resp_df.empty:
    st.warning("Some transactions are taking longer than expected!")
    st.dataframe(high_resp_df)
else:
    st.success("All transactions are within normal response time.")

# Download option
st.subheader("📥 Download Data")
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="transactions_report.csv",
    mime="text/csv"
)
