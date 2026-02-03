import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Security Duty Rotation", layout="centered")
st.title("🛡️ Security Duty Rotation")

# Google Sheets connect (READ ONLY)
conn = st.connection("gsheets", type=GSheetsConnection)

# Full sheet read
df = conn.read(worksheet=0, ttl=0)

# User input
date = st.number_input("Date select pannunga (1–31)", 1, 31, 1)
shift = st.selectbox("Shift select pannunga", ["A", "B", "C"])

# Date column name (sheet-la date number header)
date_col = str(date)

if date_col not in df.columns:
    st.error(f"Date {date} column sheet-la illa")
else:
    # Extract only Name + selected date column
    staff_df = df.iloc[:, [2, df.columns.get_loc(date_col)]]
    staff_df.columns = ["Staff Name", "Shift"]

    # Clean data
    staff_df = staff_df.dropna()
    staff_df["Shift"] = staff_df["Shift"].astype(str).str.upper()

    # அந்த shift மட்டும் filter
    staff_df = staff_df[staff_df["Shift"] == shift].reset_index(drop=True)

    if staff_df.empty:
        st.warning("இந்த date & shift-க்கு staff இல்லை")
    else:
        total_staff = len(staff_df)
        points = list(range(1, 14))  # 13 points

        # Rotation logic
        start = (date - 1) % total_staff

        result = []
        for i in range(13):
            idx = (start + i) % total_staff
            result.append([
                staff_df.loc[idx, "Staff Name"],
                points[i]
            ])

        result_df = pd.DataFrame(
            result, columns=["Staff Name", "Assigned Point"]
        )

        st.subheader("📋 Duty Points Assignment")
        st.dataframe(result_df, use_container_width=True)

