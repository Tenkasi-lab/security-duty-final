import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# App Page Setup
st.set_page_config(page_title="Security Duty Rotation", layout="centered")
st.title("🛡️ Security Duty Rotation")

# Google Sheets Connection
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Full sheet read (First row as header)
    df = conn.read(worksheet=0, ttl=0)
    
    # Sidebar Filters
    st.sidebar.header("Control Panel")
    date = st.sidebar.number_input("Date select pannunga (1–31)", 1, 31, 4)
    shift = st.sidebar.selectbox("Shift select pannunga", ["A", "B", "C"])

    # Date column name (Sheet-la 1, 2, 3.. nu header irukkum)
    date_col = str(date)

    if date_col not in df.columns:
        st.error(f"⚠️ Error: Column '{date_col}' unga Google Sheet-la illa. Row 1-la 1-31 varai dates irukka-nu check pannunga.")
    else:
        # Extract only Name (Column B) + selected date column
        # Column B index 1, Date column index fetching moolama edukirom
        staff_df = df.iloc[:, [1, df.columns.get_loc(date_col)]]
        staff_df.columns = ["Staff Name", "Shift"]

        # Clean data (Empty rows remove pandrom)
        staff_df = staff_df.dropna(subset=["Staff Name"])
        staff_df["Shift"] = staff_df["Shift"].astype(str).str.strip().str.upper()

        # Select panna shift-ah mattum filter pandrom
        target_staff = staff_df[staff_df["Shift"] == shift].reset_index(drop=True)

        if target_staff.empty:
            st.warning(f"ℹ️ Inniku (Date {date}) Shift {shift}-la staff yarum illai.")
        else:
            total_staff = len(target_staff)
            points = [f"Point {i}" for i in range(1, 14)] # 13 Points

            # Rotation logic: Date-ah poruthu start point maarum
            start_idx = (date - 1) % total_staff

            duty_chart = []
            # 13 points-kkum staff-ah assign pandrom
            for i in range(13):
                idx = (start_idx + i) % total_staff
                duty_chart.append({
                    "Staff Name": target_staff.loc[idx, "Staff Name"],
                    "Duty Point": points[i]
                })

            result_df = pd.DataFrame(duty_chart)

            st.subheader(f"📋 Duty Chart: Date {date} | Shift {shift}")
            st.table(result_df) # Neet-ana Table format

except Exception as e:
    st.error(f"❌ Connection Error: {e}")
    st.info("Google Sheet-la 'Share' pōyi 'Anyone with the link' kuduthurukeengalā nu check pannunga.")
