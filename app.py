import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Security Duty Rotation", layout="centered")
st.title("🛡️ Security Duty Rotation Automation")

conn = st.connection("gsheets", type=GSheetsConnection)
url = "https://docs.google.com/spreadsheets/d/1v95g8IVPITIF4-mZghIvh1wyr5YUxHGmgK3jyWhtuEQ/"

try:
    # Read the full sheet data
    df = conn.read(spreadsheet=url, header=None)
    
    if not df.empty:
        st.sidebar.header("Control Panel")
        date_val = st.sidebar.number_input("Select Date", 1, 31, 3)
        shift_val = st.sidebar.selectbox("Select Shift", ["A", "B", "C"])

        # Row 1-la irukkira dates-ah kandupidikkirom
        header_row = df.iloc[0].astype(str).str.strip().tolist()
        
        target_col_idx = None
        # Date number headers-la enga irukku nu thedurom
        for i, val in enumerate(header_row):
            if val == str(date_val):
                target_col_idx = i
                break

        if target_col_idx is None:
            st.error(f"Date {date_val} heading Row 1-la illa. Row 1-la dates irukkā-nu check pannunga.")
        else:
            staff_list = []
            # Row 2 (Index 1) la irundhu check pandrom
            for i in range(1, len(df)):
                name = str(df.iloc[i, 1]).strip() # Column B
                # Staff-oda shift status-ah edukkrom
                attendance_val = str(df.iloc[i, target_col_idx]).strip().upper()
                
                # 'A', 'B', illa 'C' match aaganum
                if name and name != "None" and attendance_val == shift_val:
                    staff_list.append(name)
            
            if staff_list:
                points = ["MAIN GATE", "SECOND GATE", "CAR PARKING", "CAR PARKING ENTRANCE", 
                          "PATROLING", "DG", "C BLOCK", "B BLOCK", "A BLOCK", "CIVIL GATE", "NEW CANTEEN", "POINT 12", "POINT 13"]
                
                total_staff = len(staff_list)
                start_idx = (date_val - 1) % total_staff

                result = []
                for i in range(min(13, total_staff)):
                    idx = (start_idx + i) % total_staff
                    result.append([staff_list[idx], points[i]])

                st.subheader(f"📋 Duty Chart: Date {date_val} | Shift {shift_val}")
                st.table(pd.DataFrame(result, columns=["Staff Name", "Duty Point"]))
            else:
                st.warning(f"Date {date_val} & Shift {shift_val}-kku yarum mark pannala. Sheet-la '{date_val}' column-kku keela 'A/B/C' irukkā-nu check pannunga.")
            
except Exception as e:
    st.error(f"Technical Error: {e}")
