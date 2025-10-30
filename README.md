CICS Transaction Health Monitoring Dashboard

This project is a Streamlit-based dashboard that simulates CICS transaction monitoring. It randomly samples transactions from a master pool and sends alert emails (via Mailtrap) for Failed and Long-running transactions on every refresh.

Files:
- main.py                     - Streamlit app
- transactions_master.csv     - Master transaction pool (200 approx)
- mailtrap_config_template.json - Template for Mailtrap SMTP credentials
- requirements.txt            - Python dependencies

Setup (GitHub + Streamlit Cloud):
1. Create a new GitHub repository and upload all files from this folder.
2. Rename 'mailtrap_config_template.json' to 'mailtrap_config.json' and edit it locally to add your Mailtrap SMTP credentials (do NOT commit this file to GitHub).
   Example values to replace:
   - SMTP_USER: your Mailtrap SMTP username
   - SMTP_PASS: your Mailtrap SMTP password
3. Deploy on Streamlit Cloud (share.streamlit.io) by connecting to your GitHub repo and selecting main.py.
4. Open your Mailtrap inbox (My Sandbox) to view generated emails when the app runs.

Local testing (optional):
- Install dependencies: pip install -r requirements.txt
- Run app locally: streamlit run main.py

Security note:
- Do not commit your real SMTP credentials to GitHub. Use mailtrap_config_template.json as template and keep the real config file private.
