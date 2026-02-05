import streamlit as st
import pandas as pd
import plotly.express as px
from database_manager import DatabaseManager
import time

st.set_page_config(page_title="AI Ops Dashboard", layout="wide")

st.title("Predictive Maintenance System & Ops Dashboard")
st.markdown("---")

db = DatabaseManager()

st.sidebar.header("Settings")
update_interval = st.sidebar.slider("Update interval (seconds)", 1, 5, 2)

placeholder = st.empty()

def load_data():
    query = "SELECT * FROM telemetry ORDER BY timestamp DESC LIMIT 100"
    with db.get_connection() as conn:
        df = pd.read_sql_query(query, conn)
    return df

while True:
    df = load_data()

    if not df.empty:
        with placeholder.container():
            last_entry = df.iloc[0]

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(f"Temperature", f"{last_entry['temperature']} °C")
            col2.metric(f"Vibration", f"{last_entry['vibration']} mm/s")
            col3.metric(f"Preasure", f"{last_entry['preasure']} bar")
            
            status = "CRITICAL" if last_entry['failure_label'] == 1 else "OK"
            col4.metric("System Status", status)

            c1, c2 = st.columns(2)

            fig_temp = px.line(df, x='timestamp', y='temperature', title="Temperature Trend")
            c1.plotly_chart(fig_temp, use_container_width=True)

            fig_vib = px.line(df, x='timestamp', y='vibration', title="Vibration Analysis")
            c2.plotly_chart(fig_vib, use_container_width=True)

            st.subheader("Recent Logs")
            st.dataframe(df.head(10), use_container_width=True)
    
    time.sleep(update_interval)
