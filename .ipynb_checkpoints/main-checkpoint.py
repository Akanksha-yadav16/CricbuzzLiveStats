# main.py
import streamlit as st
from utils.db_connection import test_connection

st.set_page_config(page_title="Cricbuzz LiveStats", layout="wide")

st.title("🏏 Cricbuzz LiveStats")
st.subheader("Real-Time Cricket Analytics Dashboard")

# Test DB connection on app load
if test_connection():
    st.success("✅ Database connected successfully!")
else:
    st.error("❌ Database connection failed. Check logs.")

st.markdown("""
Welcome to **Cricbuzz LiveStats** – a cricket analytics dashboard powered by  
**Streamlit, SQL, and Cricbuzz API**.

 Use the sidebar to navigate between pages:
- Live Matches  
- Player Statistics  
- SQL Analytics  
- CRUD Operations  
""")
