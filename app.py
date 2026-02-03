import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Security Duty App", layout="wide")
st.title("🛡️ Security Duty Staff List")

conn = st.connection("gsheets", type=GSheetsConnection)
url = "https://docs.google.com/spreadsheets/d/1v95g8IVPITIF4-mZghIvh1wyr5YUxHGmgK3jyWhtuEQ/"

try:
    # Full sheet-ah header illama simple-ah padikirom
    df = conn.read(spreadsheet=url)
    
    st.success("Sheet Connected! Neenga kela irukura table-la staff names-ah check pannikalam.")
    
    # 13 points rotation list
    points = [f"Point {i}" for i in range(1, 14)]
    st.sidebar.info(f"Available Points: {', '.join(points)}")

    # Unga moththa attendance sheet-aiyum inge kaatum
    st.subheader("Your Attendance Sheet Data")
    st.dataframe(df)

except Exception as e:
    st.error(f"Error: {e}. Sheet link settings-ah 'Anyone with the link' nu check pannunga.")
