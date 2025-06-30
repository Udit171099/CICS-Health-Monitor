
import streamlit as st
import pandas as pd
import random
import altair as alt

# Simulated CICS transactions data
def generate_transaction_data(n=10):
    transaction_ids = [f"TXN{1000+i}" for i in range(n)]
    response_times = [round(random.uniform(0.1, 5.0), 2) for _ in range(n)]
    statuses = ["Running" if rt < 2 else "Warning" if rt < 4 else "Critical" for rt in response_times]
    return pd.DataFrame({
        "Transaction ID": transaction_ids,
        "Response Time (s)": response_times,
        "Status": statuses
    })

# Page setup
st.set_page_config(page_title="CICS Transaction Health Monitor", layout="wide")
st.title("🖥️ CICS Transaction Health Monitoring Dashboard")
st.markdown("This dashboard simulates real-time health monitoring of CICS transactions using simulated data.")

# Generate data
df = generate_transaction_data()

# Main data table
st.subheader("📊 Simulated Transaction Data")
st.dataframe(df, use_container_width=True)

# Charts
st.subheader("📈 Response Time by Transaction")
bar_chart = alt.Chart(df).mark_bar().encode(
    x='Transaction ID',
    y='Response Time (s)',
    color='Status'
)
st.altair_chart(bar_chart, use_container_width=True)

st.subheader("🧮 Status Distribution")
status_counts = df["Status"].value_counts().reset_index()
status_counts.columns = ["Status", "Count"]
pie_chart = alt.Chart(status_counts).mark_arc().encode(
    theta=alt.Theta(field="Count", type="quantitative"),
    color=alt.Color(field="Status", type="nominal"),
    tooltip=["Status", "Count"]
)
st.altair_chart(pie_chart, use_container_width=True)

# Alerts
st.subheader("🔔 Alerts")
critical_alerts = df[df["Status"] == "Critical"]
if not critical_alerts.empty:
    for _, row in critical_alerts.iterrows():
        st.error(f"⚠️ Transaction {row['Transaction ID']} is in CRITICAL state! Response Time: {row['Response Time (s)']}s")
else:
    st.success("✅ No critical transactions at this time.")

# Manual check
st.subheader("🔍 Manual Transaction Check")
txn_id = st.text_input("Enter Transaction ID (e.g., TXN1001):")
if txn_id:
    if txn_id in df["Transaction ID"].values:
        txn = df[df["Transaction ID"] == txn_id].iloc[0]
        st.info(f"Transaction {txn_id} status: {txn['Status']} | Response Time: {txn['Response Time (s)']}s")
    else:
        st.warning("Transaction ID not found in current simulation.")
