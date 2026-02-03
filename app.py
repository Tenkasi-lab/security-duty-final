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
        date_val = st.sidebar.number_input("Select Date", 1, 31, 3)
        shift_val = st.sidebar.selectbox("Select Shift", ["A", "B", "C"])

        # Column Mapping:
        # Column B (Index 1) is Staff Name
        # Column C (Index 2) is Shift / Attendance for Date 1
        # Logic: Date 1 = Index 2, Date 2 = Index 3, Date 3 = Index 4...
        target_col_idx = date_val + 1 

        staff_list = []
        # Row 2 (Index 1) la irundhu check pandrom
        for i in range(1, len(df)):
            try:
                name = str(df.iloc[i, 1]).strip() # Column B
                # Staff-oda shift status-ah edukkrom
                attendance_val = str(df.iloc[i, target_col_idx]).strip().upper()
                
                # Inga thaan logic: 'A', 'B', illa 'C' match aaganum
                if name and name != "None" and attendance_val == shift_val:
                    staff_list.append(name)
            except:
                continue
        
        if staff_list:
            points = ["MAIN GATE", "SECOND GATE", "CAR PARKING", "CAR PARKING ENTRANCE", 
                      "PATROLING", "DG", "C BLOCK", "B BLOCK", "A BLOCK", "CIVIL GATE", "NEW CANTEEN", "POINT 12", "POINT 13"]
            
            total_staff = len(staff_list)
            # Date poruthu rotation start point maarum
            start_idx = (date_val - 1) % total_staff

            result = []
            for i in range(min(13, total_staff)):
                idx = (start_idx + i) % total_staff
                result.append([staff_list[idx], points[i]])

            st.subheader(f"📋 Duty Chart: Date {date_val} | Shift {shift_val}")
            st.table(pd.DataFrame(result, columns=["Staff Name", "Duty Point"]))
        else:
            st.warning(f"Date {date_val} & Shift {shift_val}-kku staff yarum 'A/B/C' nu mark pannala. Check Column {chr(65+target_col_idx)} in your sheet.")
            
except Exception as e:
    st.error(f"Technical Error: {e}")
