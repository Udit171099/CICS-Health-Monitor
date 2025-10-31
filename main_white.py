import streamlit as st
import pandas as pd
import random, time, json, smtplib
from email.mime.text import MIMEText
from pathlib import Path

CONFIG_FILE = "mailtrap_config.json"

def load_config():
    cfg_path = Path(CONFIG_FILE)
    if not cfg_path.exists():
        st.error(f"Missing config file: {CONFIG_FILE}")
        st.stop()
    return json.loads(cfg_path.read_text())

cfg = load_config()
SMTP_HOST = cfg.get("SMTP_HOST", "sandbox.smtp.mailtrap.io")
SMTP_PORT = cfg.get("SMTP_PORT", 587)
SMTP_USER = cfg.get("SMTP_USER")
SMTP_PASS = cfg.get("SMTP_PASS")
SENDER_EMAIL = cfg.get("SENDER_EMAIL", "cics-monitor@demo.com")
RECEIVER_EMAIL = cfg.get("RECEIVER_EMAIL", "uditrai.10@gmail.com")
THRESHOLD = float(cfg.get("THRESHOLD_SECONDS", 5))

def send_email(txn, category):
    subject = f"Alert: {category} transaction {txn['TransactionID']} in region {txn['Region']}"
    body = f"""Transaction ID: {txn['TransactionID']}
Region: {txn['Region']}
Status: {txn['Status']}
Response Time: {txn['ResponseTime']} sec
Category: {category}
Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}
"""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        return False

@st.cache_data
def load_master():
    return pd.read_csv("transactions_master.csv")

df_master = load_master()

st.set_page_config(page_title="CICS Transaction Health Monitoring Dashboard", layout="wide")
st.title("CICS Transaction Health Monitoring Dashboard")

st.sidebar.header("Simulation Controls")
sample_size = st.sidebar.slider("Sample size per run", 40, 50, 45)
threshold = st.sidebar.number_input("Alert threshold (sec)", value=int(THRESHOLD), step=1)
AUTO_REFRESH_SECONDS = 60
countdown_placeholder = st.sidebar.empty()

def generate_sample(df, n):
    sample = df.sample(n, replace=True).reset_index(drop=True)
    for i in random.sample(range(n), random.randint(2, 3)):
        if random.random() > 0.5:
            sample.at[i, "Status"] = "FAILED"
            sample.at[i, "ResponseTime"] = round(random.uniform(0.5, threshold - 0.1), 2)
        else:
            sample.at[i, "Status"] = "SUCCESS"
            sample.at[i, "ResponseTime"] = round(random.uniform(threshold + 0.5, threshold + 6.0), 2)
    return sample

if 'sample_df' not in st.session_state:
    st.session_state['sample_df'] = generate_sample(df_master, sample_size)

if st.button("Generate Random Sample Now"):
    st.session_state['sample_df'] = generate_sample(df_master, sample_size)

sample_df = st.session_state['sample_df']

def categorize(row):
    if row["Status"] == "FAILED":
        return "Failed"
    elif row["ResponseTime"] > threshold:
        return "Long Running"
    else:
        return "Normal"

sample_df["Category"] = sample_df.apply(categorize, axis=1)

st.subheader("Transactions")
st.dataframe(sample_df)

st.subheader("Summary")
summary = sample_df["Category"].value_counts().reset_index()
summary.columns = ["Category", "Count"]
st.table(summary)

st.subheader("Average Response Time by Region")
region_group = sample_df.groupby("Region")["ResponseTime"].mean().reset_index()
if not region_group.empty:
    st.bar_chart(region_group.set_index("Region"))

st.subheader("Transaction Status Distribution")
status_group = sample_df["Category"].value_counts().reset_index()
status_group.columns = ['Status', 'Count']
if not status_group.empty:
    st.bar_chart(status_group.set_index("Status"))

st.subheader("Alerts Sent")
alerts = []
for _, row in sample_df.iterrows():
    if row["Category"] in ["Failed", "Long Running"]:
        ok = send_email(row, row["Category"])
        alerts.append({"TransactionID": row["TransactionID"], "Region": row["Region"], "Category": row["Category"], "EmailSent": ok})
st.dataframe(pd.DataFrame(alerts))

csv = sample_df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "transactions.csv", "text/csv")

countdown_js = f"""
<div id='countdown' style='font-weight:bold;color:black;'></div>
<script>
var s = {AUTO_REFRESH_SECONDS};
function tick() {{
 document.getElementById('countdown').innerText = 'Next refresh in: ' + s + 's';
 if (s<=0) window.location.reload();
 else {{ s--; setTimeout(tick,1000);}}
}}
tick();
</script>
"""
countdown_placeholder.markdown(countdown_js, unsafe_allow_html=True)
