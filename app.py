import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Security Duty Rotation", layout="centered")
st.title("🛡️ Security Duty Rotation Automation")

conn = st.connection("gsheets", type=GSheetsConnection)
url = "https://docs.google.com/spreadsheets/d/1v95g8IVPITIF4-mZghIvh1wyr5YUxHGmgK3jyWhtuEQ/"

try:
    # Spreadsheet-ai header illama full-ah padikkirom
    df = conn.read(spreadsheet=url, header=None)
    
    if not df.empty:
        st.sidebar.header("Control Panel")
        # Date selection (Date 3-ah default-ah veikkirom)
        date_val = st.sidebar.number_input("Select Date", 1, 31, 3)
        shift_val = st.sidebar.selectbox("Select Shift", ["A", "B", "C"])

        # Row 1-la dates (1, 2, 3...) irukku. 
        # So Date 1-na Column C (index 2), Date 2-na Column D (index 3)...
        # Intha logic: Column Index = Selected Date + 1
        try:
            target_col_idx = date_val + 1 
            
            # Staff names Column B (Index 1)-la irukku
            # Shift data andha date column-la irukku
            staff_list = []
            for i in range(1, len(df)): # Row 1 skip pandrom
                name = str(df.iloc[i, 1]).strip()
                s_shift = str(df.iloc[i, target_col_idx]).strip().upper()
                
                if name and name != "None" and s_shift == shift_val:
                    staff_list.append(name)
            
            if staff_list:
                points = ["MAIN GATE", "SECOND GATE", "CAR PARKING", "CAR PARKING ENTRANCE", 
                          "PATROLING", "DG", "C BLOCK", "B BLOCK", "A BLOCK", "CIVIL GATE", "NEW CANTEEN", "POINT 12", "POINT 13"]
                
                total_staff = len(staff_list)
                # Formula: start point moves daily
                start_idx = (date_val - 1) % total_staff

                result = []
                # Max 13 staff members-kku duty poduvom
                for i in range(min(13, total_staff)):
                    idx = (start_idx + i) % total_staff
                    result.append([staff_list[idx], points[i]])

                st.subheader(f"📋 Duty Chart: Date {date_val} | Shift {shift_val}")
                st.table(pd.DataFrame(result, columns=["Staff Name", "Duty Point"]))
            else:
                st.warning(f"Date {date_val} & Shift {shift_val}-kku staff list kaaliya irukku. Check if 'A/B/C' is marked in Column {chr(65+target_col_idx)}.")
                
        except Exception as col_err:
            st.error(f"Column access error: {col_err}. Check if date column exists.")

except Exception as e:
    st.error(f"Technical Error: {e}")
