import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Security Duty App", layout="wide")
st.title("🛡️ Security Duty Rotation - 43 Staff")

# Google Sheets Connection
conn = st.connection("gsheets", type=GSheetsConnection)
url = "https://docs.google.com/spreadsheets/d/1v95g8IVPITIF4-mZghIvh1wyr5YUxHGmgK3jyWhtuEQ/"

try:
    # Data-vai sheet-la irundhu edukkirom
    df = conn.read(spreadsheet=url)
    st.success("Data Connected Successfully!")

    # Sidebar Options
    st.sidebar.header("Filter")
    selected_shift = st.sidebar.selectbox("Select Shift", ["A", "B", "C"])
    selected_date = st.sidebar.number_input("Select Date", min_value=1, max_value=31, value=3)

    if st.sidebar.button("Generate Today's Chart"):
        # Shift filter pandrom
        shift_data = df[df['SHIFT'] == selected_shift].copy()
        
        if not shift_data.empty:
            # Rotation Logic: 13 points-ah 13 perukku rotate pandrom
            # (Date-ah poruthu points maarum)
            points = [f"Point {i}" for i in range(1, 14)]
            
            # Simple rotation based on date
            shift_data['Assigned Point'] = [points[(i + selected_date) % 13] for i in range(len(shift_data))]
            
            st.subheader(f"Duty Chart: Date {selected_date} | Shift {selected_shift}")
            st.dataframe(shift_data[['NAME', 'Assigned Point']], use_container_width=True)
        else:
            st.warning("No staff found for this shift.")

except Exception as e:
    st.error(f"Error: {e}")
