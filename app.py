import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Security Duty App", layout="wide")
st.title("🛡️ Security Duty Rotation - 43 Staff")

conn = st.connection("gsheets", type=GSheetsConnection)
url = "https://docs.google.com/spreadsheets/d/1v95g8IVPITIF4-mZghIvh1wyr5YUxHGmgK3jyWhtuEQ/"

try:
    # Spreadsheet-ai header illama full-ah padikkirom
    df = conn.read(spreadsheet=url, header=None)
    
    if not df.empty:
        st.success("Sheet Connected!")
        
        # FAIL-SAFE: Column B (1) matrum C (2) irukka nu check pandrom
        # Illana available columns-ah edukkum
        try:
            names = df.iloc[1:, 1]  # B Column
            shifts = df.iloc[1:, 2] # C Column
        except:
            names = df.iloc[1:, 0]  # Back-up: A Column
            shifts = df.iloc[1:, 1] # Back-up: B Column

        df_clean = pd.DataFrame({'NAME': names, 'SHIFT': shifts}).dropna()

        selected_shift = st.sidebar.selectbox("Select Shift", ["A", "B", "C"])
        selected_date = st.sidebar.number_input("Select Date", min_value=1, max_value=31, value=4)

        if st.sidebar.button("Generate Today's Chart"):
            # Shift filter (case insensitive)
            shift_data = df_clean[df_clean['SHIFT'].astype(str).str.contains(selected_shift, case=False)].copy()
            
            if not shift_data.empty:
                points = [f"Point {i}" for i in range(1, 14)]
                shift_data = shift_data.reset_index(drop=True)
                
                # 13 point rotation logic
                shift_data['Assigned Point'] = [points[(i + int(selected_date)) % 13] for i in range(len(shift_data))]
                
                st.subheader(f"Duty Chart for Date: {selected_date} | Shift: {selected_shift}")
                st.table(shift_data[['NAME', 'Assigned Point']])
            else:
                st.warning(f"Shift '{selected_shift}' kaana staff yarum sheet-la illai. Check Column C.")
    else:
        st.error("Sheet kaaliyaaga irukku!")

except Exception as e:
    st.error(f"Prachinai: {e}")
