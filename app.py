import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Security Duty App", layout="wide")
st.title("🛡️ Security Duty Rotation - 43 Staff")

conn = st.connection("gsheets", type=GSheetsConnection)
url = "https://docs.google.com/spreadsheets/d/1v95g8IVPITIF4-mZghIvh1wyr5YUxHGmgK3jyWhtuEQ/"

try:
    # Spreadsheet-ai header illama padikkirom (Direct index)
    df = conn.read(spreadsheet=url, header=None)
    
    # Unga sheet-la B Column (Index 1) la Name, C Column (Index 2) la Shift irukku
    # Athai mattum thaniya pirichu edukkirom
    df_clean = pd.DataFrame({
        'NAME': df.iloc[1:, 1],  # Row 1-la irundhu Column B (Name)
        'SHIFT': df.iloc[1:, 2]  # Row 1-la irundhu Column C (Shift)
    })

    # Sidebar Filter
    st.sidebar.header("Control Panel")
    selected_shift = st.sidebar.selectbox("Select Shift", ["A", "B", "C"])
    selected_date = st.sidebar.number_input("Select Date", min_value=1, max_value=31, value=3)

    if st.sidebar.button("Generate Today's Chart"):
        # Shift filter pandrom
        shift_data = df_clean[df_clean['SHIFT'].str.upper() == selected_shift].copy()
        
        if not shift_data.empty:
            # 13 points rotation
            points = [f"Point {i}" for i in range(1, 14)]
            shift_data = shift_data.reset_index(drop=True)
            
            # Rotation logic based on date
            shift_data['Assigned Point'] = [points[(i + selected_date) % 13] for i in range(len(shift_data))]
            
            st.subheader(f"Duty Chart for {selected_date}-Feb | Shift {selected_shift}")
            st.table(shift_data[['NAME', 'Assigned Point']])
        else:
            st.warning(f"No staff found for Shift {selected_shift} in your sheet.")

except Exception as e:
    st.error(f"Sheet connect aagurathula prachinai: {e}")
