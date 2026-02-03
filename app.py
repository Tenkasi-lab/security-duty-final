import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Security Duty Rotation", layout="centered")
st.title("🛡️ Security Duty Rotation")

conn = st.connection("gsheets", type=GSheetsConnection)
url = "https://docs.google.com/spreadsheets/d/1v95g8IVPITIF4-mZghIvh1wyr5YUxHGmgK3jyWhtuEQ/"

try:
    # Spreadsheet-ai padikkirom
    df = conn.read(spreadsheet=url)
    
    # Column names-ah clean pandrom
    df.columns = [str(c).strip() for c in df.columns]

    st.sidebar.header("Control Panel")
    # Date 3-ah default-ah veikkirom (unga sheet-la irukku)
    date_val = st.sidebar.number_input("Date select pannunga (1–31)", 1, 31, 3)
    shift_val = st.sidebar.selectbox("Shift select pannunga", ["A", "B", "C"])

    date_col = str(date_val)

    if date_col not in df.columns:
        st.error(f"⚠️ Error: Column '{date_col}' sheet-la illa. Row 1-la dates (1, 2, 3...) irukka-nu check pannunga.")
    else:
        # Staff Name Column B (Index 1) la irukku
        staff_df = df.iloc[:, [1, df.columns.get_loc(date_col)]]
        staff_df.columns = ["Staff Name", "Shift"]

        # Clean data
        staff_df = staff_df.dropna(subset=["Staff Name"])
        staff_df["Shift"] = staff_df["Shift"].astype(str).str.strip().str.upper()

        # Filter shift
        target_staff = staff_df[staff_df["Shift"] == shift_val].reset_index(drop=True)

        if target_staff.empty:
            st.warning(f"Inniku (Date {date_val}) Shift {shift_val}-la staff yarum illai.")
        else:
            # 13 points definition
            points = ["MAIN GATE", "SECOND GATE", "CAR PARKING", "CAR PARKING ENTRANCE", 
                      "PATROLING", "DG", "C BLOCK", "B BLOCK", "A BLOCK", "CIVIL GATE", "NEW CANTEEN", "POINT 12", "POINT 13"]
            
            total_staff = len(target_staff)
            start_idx = (date_val - 1) % total_staff

            result = []
            # 13 perukku duty assign pandrom
            for i in range(13):
                idx = (start_idx + i) % total_staff
                result.append([target_staff.loc[idx, "Staff Name"], points[i]])

            st.subheader(f"📋 Duty Chart: Date {date_val} | Shift {shift_val}")
            st.table(pd.DataFrame(result, columns=["Staff Name", "Duty Point"]))

except Exception as e:
    st.error(f"Prachinai: {e}")
