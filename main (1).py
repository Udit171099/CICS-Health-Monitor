
# Advanced CICS Transaction Health Monitoring with Alerts and Region Support

import streamlit as st
import pandas as pd
import numpy as np
import smtplib
from email.mime.text import MIMEText
import altair as alt

# Simulated Email Alert Function (you'll need real credentials in production)
def send_email_alert(subject, message):
    try:
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = 'your.email@gmail.com'
        msg['To'] = 'recipient.email@example.com'

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('your.email@gmail.com', 'your-app-password')
            smtp.send_message(msg)
    except Exception as e:
        st.error(f"Email sending failed: {e}")

# Simulated Transaction Data Generator
def generate_data():
    regions = [f'PRDCICS{i:02}' for i in range(1, 10)]
    statuses = ['Running', 'Warning', 'Critical']
    data = []
    for i in range(1, 21):
        region = np.random.choice(regions)
        txn_id = f"TXN{i:03}"
        response_time = np.random.randint(50, 500)
        if response_time > 350:
            status = 'Critical'
        elif response_time > 200:
            status = 'Warning'
        else:
            status = 'Running'
        data.append([txn_id, region, response_time, status])
    return pd.DataFrame(data, columns=["Transaction ID", "Region", "Response Time", "Status"])

st.title("Advanced CICS Transaction Health Monitor")

# Generate or simulate data
df = generate_data()

# Region Status Analysis
st.subheader("📍 Region Health Summary")
region_summary = df.groupby("Region")['Status'].apply(lambda x: (x=='Critical').sum())
st.dataframe(region_summary.rename("Critical Count"))

# Check for Region Down Alert
down_regions = df.groupby("Region").filter(lambda x: all(x["Status"] == "Critical"))
if not down_regions.empty:
    st.error("⚠️ One or more regions are fully Critical!")
    for reg in down_regions['Region'].unique():
        send_email_alert("Region Down Alert", f"Region {reg} is fully critical.")

# Main Dashboard
df_display = df.copy()
st.subheader("📊 Transaction Status Table")
st.dataframe(df_display)

# Email Alerts for individual Critical entries
for _, row in df.iterrows():
    if row['Status'] == 'Critical' and row['Response Time'] > 400:
        send_email_alert("High Response Time Alert", f"Transaction {row['Transaction ID']} in {row['Region']} exceeded response time with {row['Response Time']} ms")

# Charts
st.subheader("📈 Response Time Chart")
bar_chart = alt.Chart(df).mark_bar().encode(
    x='Transaction ID',
    y='Response Time',
    color='Status',
    tooltip=['Transaction ID', 'Response Time', 'Status', 'Region']
)
st.altair_chart(bar_chart, use_container_width=True)

st.subheader("🥧 Status Distribution")
status_pie = df['Status'].value_counts().reset_index()
status_pie.columns = ['Status', 'Count']
pie_chart = alt.Chart(status_pie).mark_arc().encode(
    theta='Count',
    color='Status',
    tooltip=['Status', 'Count']
)
st.altair_chart(pie_chart, use_container_width=True)

# Manual Control Panel
st.subheader("🔧 Manual Response Time Reset")
selected_txn = st.selectbox("Select a transaction to reset", df['Transaction ID'])
if st.button("Reset Response Time"):
    df.loc[df['Transaction ID'] == selected_txn, 'Response Time'] = 120
    df.loc[df['Transaction ID'] == selected_txn, 'Status'] = 'Running'
    st.success(f"Response time for {selected_txn} reset to 120 ms.")
