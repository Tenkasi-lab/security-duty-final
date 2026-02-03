import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Security Duty App", layout="wide")
st.title("🛡️ Security Duty Rotation Automation")

conn = st.connection("gsheets", type=GSheetsConnection)
url = "https://docs.google.com/spreadsheets/d/1v95g8IVPITIF4-mZghIvh1wyr5YUxHGmgK3jyWhtuEQ/"

try:
    # Spreadsheet-ai header illama full-ah padikkirom
    df = conn.read(spreadsheet=url, header=None)
    
    if not df.empty:
        # --- SHIFT COLUMN FINDER ---
        shift_col = None
        # Row 1-la irundhu Row 50 varai check pandrom (A, B, or C theda)
        for col in df.columns:
            if df[col].astype(str).str.strip().str.upper().isin(['A', 'B', 'C']).any():
                shift_col = col
                break
        
        # Staff Names eppovum Shift column-kku munnadi (Left side) irukkum
        name_col = shift_col - 1 if shift_col and shift_col > 0 else 0
        
        if shift_col is not None:
            st.success("Sheet Scan Complete!")
            
            # Data cleaning
            df_clean = pd.DataFrame({
                'NAME': df.iloc[:, name_col],
                'SHIFT': df.iloc[:, shift_col]
            }).dropna()

            # Sidebar Filter
            st.sidebar.header("Settings")
            selected_shift = st.sidebar.selectbox("Select Shift", ["A", "B", "C"])
            selected_date = st.sidebar.number_input("Select Date", min_value=1, max_value=31, value=4)

            if st.sidebar.button("Generate Today's Chart"):
                # Filter by shift
                shift_data = df_clean[df_clean['SHIFT'].astype(str).str.strip().str.upper() == selected_shift].copy()
                
                if not shift_data.empty:
                    # 13 point rotation logic
                    points = [f"Point {i}" for i in range(1, 14)]
                    shift_data = shift_data.reset_index(drop=True)
                    # Logic: (Staff Index + Date) % 13
                    shift_data['Assigned Point'] = [points[(i + int(selected_date)) % 13] for i in range(len(shift_data))]
                    
                    st.subheader(f"Duty Chart for Date: {selected_date} | Shift: {selected_shift}")
                    st.table(shift_data[['NAME', 'Assigned Point']])
                else:
                    st.warning(f"Shift '{selected_shift}' kaana staff yarum sheet-la illai.")
        else:
            st.error("Sheet-la 'A', 'B', illa 'C' (Shift) irukkura column-ah kandupidiçha mudiyaala. Please ensure your sheet has a column with just A, B, or C.")
    else:
        st.error("Sheet is empty!")

except Exception as e:
    st.error(f"Error: {e}")
