
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
