import streamlit as st
import pandas as pd
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Siachen-Guard Command", page_icon="🛡️", layout="wide")

# --- SIDEBAR (The Control Panel) ---
st.sidebar.title("🛡️ Command Center")
st.sidebar.header("Filter Options")
soldier_id = st.sidebar.selectbox("Select Soldier Unit", ["Soldier-001 (Alpha)", "Soldier-002 (Bravo)", "Soldier-003 (Charlie)"])
view_mode = st.sidebar.radio("View Mode", ["Live Vitals", "Map View", "Historical Data"])

st.sidebar.markdown("---")
st.sidebar.write("Status: 🟢 **ONLINE**")
st.sidebar.write(f"Monitoring: **{soldier_id}**")

# --- MAIN APP ---
st.title(f"🇮🇳 Siachen-Guard: {soldier_id}")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv('soldier_data.csv')

try:
    data = load_data()
    
    # Get the LAST reading
    latest_reading = data.iloc[-1]
    last_hr = latest_reading['Heart_Rate']
    last_temp = latest_reading['Body_Temp']
    last_time = latest_reading['Time']

    # --- TOP METRICS ROW (Always Visible) ---
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="❤️ Heart Rate", value=f"{last_hr} bpm", delta="-2 bpm")
    with col2:
        st.metric(label="🌡️ Body Temp", value=f"{last_temp} °C", delta="0.1 °C")
    with col3:
        if last_temp < 35 or last_hr < 50:
            st.error("CRITICAL")
        else:
            st.success("NORMAL")
    with col4:
        st.metric(label="Last Update", value=str(last_time))
    
    st.divider()

    # --- CONDITIONAL VIEWS (Based on Sidebar) ---

    # VIEW 1: LIVE VITALS (Graphs & Rescue)
    if view_mode == "Live Vitals":
        # Emergency Button
        if last_temp < 35 or last_hr < 50:
            st.write("### ⚠️ EMERGENCY PROTOCOL ADVISED")
            if st.button("🚨 DISPATCH RESCUE TEAM (SOS)"):
                with st.spinner("Contacting Base Command..."):
                    time.sleep(2)
                st.success(f"Helicopter dispatched to {soldier_id} location!")
                st.balloons()
        
        # Graphs
        st.subheader("Vital Signs History")
        tab1, tab2 = st.tabs(["Heart Rate Graph", "Temperature Graph"])
        with tab1:
            st.line_chart(data.set_index('Time')['Heart_Rate'], color="#FF0000")
        with tab2:
            st.line_chart(data.set_index('Time')['Body_Temp'], color="#0000FF")

    # VIEW 2: MAP VIEW (The New Part!)
    elif view_mode == "Map View":
        st.subheader(f"📍 Location Tracker: {soldier_id}")
        
        # Coordinates for Siachen Glacier (approx)
        # We create a fake dataframe just for the map
        map_data = pd.DataFrame({
            'lat': [35.5], 
            'lon': [77.0]
        })

        # Display the map
        st.map(map_data, zoom=6)
        st.info("Satellite Lock: Stable | GPS Accuracy: 2m")

    # VIEW 3: HISTORICAL DATA (Raw Text)
    elif view_mode == "Historical Data":
        st.subheader("📋 Mission Log Data")
        st.dataframe(data)

except Exception as e:
    st.error(f"Error loading data: {e}")
  