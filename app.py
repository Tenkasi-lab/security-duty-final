import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Security Duty Rotation", layout="centered")
st.title("🛡️ Security Duty Rotation")

conn = st.connection("gsheets", type=GSheetsConnection)
url = "https://docs.google.com/spreadsheets/d/1v95g8IVPITIF4-mZghIvh1wyr5YUxHGmgK3jyWhtuEQ/"

try:
    # Spreadsheet-ai header illama full-ah padikkirom
    df = conn.read(spreadsheet=url, header=None)
    
    if not df.empty:
        # Row 1-la irukkira dates-ah headers-ā mathugirom
        df.columns = df.iloc[0].astype(str).str.strip()
        df = df[1:].reset_index(drop=True)

        st.sidebar.header("Control Panel")
        # Unga sheet-la Date 3 varai thaan data irundha, 3 select pannunga
        date_val = st.sidebar.number_input("Date select pannunga (1–31)", 1, 31, 3)
        shift_val = st.sidebar.selectbox("Shift select pannunga", ["A", "B", "C"])

        date_col = str(date_val)

        if date_col not in df.columns:
            st.error(f"⚠️ Error: Column '{date_col}' sheet-la illa. Row 1-la '{date_col}' nu ezhudhirukka-nu check pannunga.")
        else:
            # Column B (Index 1) la Names, current date column-la shifts
            staff_df = df.iloc[:, [1, df.columns.get_loc(date_col)]]
            staff_df.columns = ["Staff Name", "Shift"]

            # Data cleaning
            staff_df = staff_df.dropna(subset=["Staff Name"])
            staff_df["Shift"] = staff_df["Shift"].astype(str).str.strip().str.upper()

            # Filter shift
            target_staff = staff_df[staff_df["Shift"] == shift_val].reset_index(drop=True)

            if target_staff.empty:
                st.warning(f"Inniku (Date {date_val}) Shift {shift_val}-la staff yarum illai.")
            else:
                # 13 points assignment
                points = ["MAIN GATE", "SECOND GATE", "CAR PARKING", "CAR PARKING ENTRANCE", 
                          "PATROLING", "DG", "C BLOCK", "B BLOCK", "A BLOCK", "CIVIL GATE", "NEW CANTEEN", "POINT 12", "POINT 13"]
                
                total_staff = len(target_staff)
                start_idx = (date_val - 1) % total_staff

                result = []
                for i in range(13):
                    idx = (start_idx + i) % total_staff
                    result.append([target_staff.loc[idx, "Staff Name"], points[i]])

                st.subheader(f"📋 Duty Chart: Date {date_val} | Shift {shift_val}")
                st.table(pd.DataFrame(result, columns=["Staff Name", "Duty Point"]))

except Exception as e:
    st.error(f"Technical Error: {e}")
