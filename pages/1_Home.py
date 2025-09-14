# pages/1_Home.py
import streamlit as st

st.title("Home Page")
st.header("Welcome to Cricbuzz LiveStats")

st.markdown("""
### Project Overview
This project is a **Real-Time Cricket Analytics Dashboard** built with:
- Python
- Streamlit
- SQL (SQLite)
- Cricbuzz API
- Plotly (for graphs)

### Features
- Live match updates  
- Player statistics dashboard  
- SQL-driven analytics (25 queries: Beginner → Advanced)  
- CRUD operations on player/match data  

Use the sidebar to navigate between pages.
""")

st.info("This is your Home Page. Other modules (Live Match, Player Stats, SQL Analytics, CRUD) will be added step by step.")
