import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Security Duty Rotation", layout="centered")
st.title("🛡️ Security Duty Rotation Automation")

conn = st.connection("gsheets", type=GSheetsConnection)
url = "https://docs.google.com/spreadsheets/d/1v95g8IVPITIF4-mZghIvh1wyr5YUxHGmgK3jyWhtuEQ/"

try:
    # Read the sheet
    df = conn.read(spreadsheet=url, header=None)
    
    if not df.empty:
        # Step 1: Row 1-la irukkira dates-ah header-ā set pandrom
        df.columns = df.iloc[0].astype(str).str.strip()
        df = df[1:].reset_index(drop=True)

        st.sidebar.header("Control Panel")
        date_val = st.sidebar.number_input("Select Date", 1, 31, 3)
        shift_val = st.sidebar.selectbox("Select Shift", ["A", "B", "C"])

        # Step 2: Date column-ah manual-ā search pandrom (Exact match matching)
        target_col = None
        for col in df.columns:
            if str(col) == str(date_val):
                target_col = col
                break

        if target_col is None:
            st.error(f"⚠️ Column '{date_val}' kandupidiçha mudiyaala. Unga sheet-la Row 1-la '{date_val}' nu ezhudhirukkā-nu check pannunga.")
        else:
            # Column B (Index 1) is Name, target_col is Shift
            staff_df = pd.DataFrame({
                'NAME': df.iloc[:, 1],
                'SHIFT': df[target_col]
            }).dropna(subset=['NAME'])

            # Clean Shift data
            staff_df['SHIFT'] = staff_df['SHIFT'].astype(str).str.strip().str.upper()

            # Filter shift
            final_list = staff_df[staff_df['SHIFT'] == shift_val].reset_index(drop=True)

            if final_list.empty:
                st.warning(f"Date {date_val}-la Shift {shift_val}-kku yarum illai.")
            else:
                # 13 points assignment
                points = ["MAIN GATE", "SECOND GATE", "CAR PARKING", "CAR PARKING ENTRANCE", 
                          "PATROLING", "DG", "C BLOCK", "B BLOCK", "A BLOCK", "CIVIL GATE", "NEW CANTEEN", "POINT 12", "POINT 13"]
                
                total_staff = len(final_list)
                start_idx = (date_val - 1) % total_staff

                result = []
                for i in range(min(13, total_staff)):
                    idx = (start_idx + i) % total_staff
                    result.append([final_list.loc[idx, 'NAME'], points[i]])

                st.subheader(f"📋 Duty Chart: Date {date_val} | Shift {shift_val}")
                st.table(pd.DataFrame(result, columns=["Staff Name", "Duty Point"]))

except Exception as e:
    st.error(f"Technical Error: {e}")
