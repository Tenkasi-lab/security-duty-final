import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Security Duty App", layout="wide")
st.title("🛡️ Security Duty Rotation")

conn = st.connection("gsheets", type=GSheetsConnection)
url = "https://docs.google.com/spreadsheets/d/1v95g8IVPITIF4-mZghIvh1wyr5YUxHGmgK3jyWhtuEQ/"

try:
    df = conn.read(spreadsheet=url, header=None)
    
    if not df.empty:
        # Sheet-la 'A', 'B', 'C' enga irukku-nu kandupidiçhu fix pandrom
        # Column level searching
        shift_col_idx = None
        for col in df.columns:
            if df[col].astype(str).str.strip().str.upper().isin(['A', 'B', 'C']).any():
                shift_col_idx = col
                break
        
        if shift_col_idx is not None:
            # Shift letters irukkira column kandupidiçhaachu
            # Athukku munnadi irukkira column-ah Name column-ah edukkum
            name_col_idx = shift_col_idx - 1 if shift_col_idx > 0 else 0
            
            # Clean data
            df_final = pd.DataFrame({
                'NAME': df.iloc[:, name_col_idx],
                'SHIFT': df.iloc[:, shift_col_idx]
            }).dropna()

            st.sidebar.header("Settings")
            selected_shift = st.sidebar.selectbox("Select Your Shift", ["A", "B", "C"])
            selected_date = st.sidebar.number_input("Select Date", 1, 31, 4)

            if st.sidebar.button("Generate Duty Chart"):
                # Staff-ah filter pandrom
                result = df_final[df_final['SHIFT'].astype(str).str.strip().str.upper() == selected_shift].copy()
                
                if not result.empty:
                    points = [f"Point {i}" for i in range(1, 14)]
                    result = result.reset_index(drop=True)
                    # Logic: yarukkum ore point thirumba varama rotate aagum
                    result['Assigned Point'] = [points[(i + int(selected_date)) % 13] for i in range(len(result))]
                    
                    st.subheader(f"Duty Chart: Date {selected_date} | Shift {selected_shift}")
                    st.table(result[['NAME', 'Assigned Point']])
                else:
                    st.warning(f"Shift {selected_shift}-la staff yarum illai. Check Column C.")
        else:
            st.error("Sheet-la A/B/C details-ah app-ala kandupidiçha mudiyaala.")

except Exception as e:
    st.error(f"Something went wrong: {e}")
