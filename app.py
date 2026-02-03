import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Page setup
st.set_page_config(page_title="Security Duty App", layout="wide")
st.title("🛡️ Security Duty Rotation Automation")

# Connection setup
conn = st.connection("gsheets", type=GSheetsConnection)

# Spreadsheet URL
url = "https://docs.google.com/spreadsheets/d/1v95g8IVPITIF4-mZghIvh1wyr5YUxHGmgK3jyWhtuEQ/"

try:
    # Read data
    df = conn.read(spreadsheet=url)
    st.success("Connected to Google Sheets!")

    # Sidebar for filters
    st.sidebar.header("Control Panel")
    month = st.sidebar.selectbox("Select Month", ["FEBRUARY-2026"])
    shift = st.sidebar.selectbox("Select Shift", ["A", "B", "C"])
    date = st.sidebar.number_input("Select Date", min_value=1, max_value=28, value=3)

    if st.sidebar.button("Generate Duty Chart"):
        st.subheader(f"Duty Chart for {date}-{month} | Shift {shift}")
        # Basic display for testing
        st.table(df.head(15))

except Exception as e:
    st.error(f"Error connecting to Sheet: {e}")
