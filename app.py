import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Security Duty Rotation", layout="centered")
st.title("🛡️ Security Duty Rotation")

# Google Sheets connect
conn = st.connection("gsheets", type=GSheetsConnection)

# Full sheet read
df = conn.read(worksheet=0, ttl=0)

# User input
date = st.sidebar.number_input("Date select pannunga (1–31)", 1, 31, 4)
shift = st.sidebar.selectbox("Shift select pannunga", ["A", "B", "C"])

# Date column name
date_col = str(date)

if date_col not in df.columns:
    st.error(f"Date {date} column sheet-la illa. Row 1-la dates irukka-nu check pannunga.")
else:
    # Column B (index 1) la Name irukku 
    staff_df = df.iloc[:, [1, df.columns.get_loc(date_col)]]
    staff_df.columns = ["Staff Name", "Shift"]

    # Clean data
    staff_df = staff_df.dropna()
    staff_df["Shift"] = staff_df["Shift"].astype(str).str.upper()

    # Filter by shift
    target_staff = staff_df[staff_df["Shift"] == shift].reset_index(drop=True)

    if target_staff.empty:
        st.warning(f"Inniku (Date {date}) Shift {shift}-la staff yarum illai.")
    else:
        # 13 points rotation logic
        points = ["MAIN GATE", "SECOND GATE", "CAR PARKING", "CAR PARKING ENTRANCE", 
                  "PATROLING", "DG", "C BLOCK", "B BLOCK", "A BLOCK", "CIVIL GATE", "NEW CANTEEN", "POINT 12", "POINT 13"]
        
        total_staff = len(target_staff)
        start = (date - 1) % total_staff

        result = []
        for i in range(13):
            idx = (start + i) % total_staff
            result.append([target_staff.loc[idx, "Staff Name"], points[i]])

        result_df = pd.DataFrame(result, columns=["Staff Name", "Duty Point"])

        st.subheader(f"📋 Duty Chart: Date {date} | Shift {shift}")
        st.table(result_df)
