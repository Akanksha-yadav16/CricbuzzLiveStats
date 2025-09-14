# pages/5_CRUD.py
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import sqlite3

DB_PATH = "cricbuzz.db"

# -------------------------
# Utility Functions
# -------------------------
def run_query(query, params=(), fetch=False):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query, params)
        if fetch:
            rows = cursor.fetchall()
            cols = [col[0] for col in cursor.description]
            conn.close()
            return pd.DataFrame(rows, columns=cols)
        else:
            conn.commit()
            conn.close()
            return True
    except Exception as e:
        st.error(f"❌ SQL Error: {e}")
        return pd.DataFrame() if fetch else False

def view_table(table):
    df = run_query(f"SELECT * FROM {table} LIMIT 20;", fetch=True)
    if not df.empty:
        st.dataframe(df)
    else:
        st.warning("⚠️ No records found.")
    return df

# -------------------------
# Streamlit UI
# -------------------------
st.title("Cricbuzz Database CRUD Dashboard")
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Players", "Player Stats", "Venues", "Matches", "Series"]
)

# -------------------------
# PLAYERS CRUD
# -------------------------
with tab1:
    st.header(" Manage Players")
    df = view_table("players")

    # Insert
    with st.expander("➕ Add Player"):
        full_name = st.text_input("Full Name", key="player_fullname")
        role = st.selectbox("Playing Role", ["Batsman", "Bowler", "All-rounder", "Wicket-Keeper"], key="player_role")
        bat_style = st.text_input("Batting Style", key="player_batstyle")
        bowl_style = st.text_input("Bowling Style", key="player_bowlstyle")
        country = st.text_input("Country", key="player_country")
        dob = st.date_input("Date of Birth", key="player_dob")

        if st.button("Add Player", key="add_player_btn"):
            run_query(
                "INSERT INTO players (full_name, playing_role, batting_style, bowling_style, country, date_of_birth) VALUES (?, ?, ?, ?, ?, ?)",
                (full_name, role, bat_style, bowl_style, country, str(dob)),
            )
            st.success("✅ Player added!")

    # Update
    with st.expander("✏️ Update Player"):
        if not df.empty:
            player_id = st.selectbox("Select Player ID", df["player_id"], key="update_player_id")
            new_country = st.text_input("New Country", key="update_player_country")
            if st.button("Update Player", key="update_player_btn"):
                run_query("UPDATE players SET country = ? WHERE player_id = ?", (new_country, player_id))
                st.success("✅ Player updated!")

    # Delete
    with st.expander("Delete Player"):
        if not df.empty:
            player_id = st.selectbox("Delete Player ID", df["player_id"], key="delete_player_id")
            if st.button("Delete Player", key="delete_player_btn"):
                run_query("DELETE FROM players WHERE player_id = ?", (player_id,))
                st.success("✅ Player deleted!")

# -------------------------
# PLAYER STATS CRUD
# -------------------------
with tab2:
    st.header("Manage Player Stats")
    df = view_table("player_stats")

    with st.expander("➕ Add Player Stats"):
        player_id = st.number_input("Player ID", min_value=1, step=1, key="stats_player_id")
        fmt = st.selectbox("Format", ["ODI", "T20", "Test"], key="stats_format")
        runs = st.number_input("Total Runs", min_value=0, key="stats_runs")
        avg = st.number_input("Batting Average", min_value=0.0, key="stats_avg")
        hundreds = st.number_input("Centuries", min_value=0, key="stats_centuries")
        hs = st.number_input("Highest Score", min_value=0, key="stats_hs")
        wickets = st.number_input("Wickets", min_value=0, key="stats_wickets")
        econ = st.number_input("Economy", min_value=0.0, key="stats_economy")

        if st.button("Add Stats", key="add_stats_btn"):
            run_query(
                "INSERT INTO player_stats (player_id, format, total_runs, batting_avg, centuries, highest_score, wickets, economy) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (player_id, fmt, runs, avg, hundreds, hs, wickets, econ),
            )
            st.success("✅ Stats added!")

# -------------------------
# VENUES CRUD
# -------------------------
with tab3:
    st.header("Manage Venues")
    df = view_table("venues")

    with st.expander("➕ Add Venue"):
        ground = st.text_input("Ground", key="venue_ground")
        city = st.text_input("City", key="venue_city")
        country = st.text_input("Country", key="venue_country")

        if st.button("Add Venue", key="add_venue_btn"):
            run_query("INSERT INTO venues (ground, city, country) VALUES (?, ?, ?)", (ground, city, country))
            st.success("✅ Venue added!")

# -------------------------
# MATCHES CRUD
# -------------------------
with tab4:
    st.header("Manage Matches")
    df = view_table("matches")

    with st.expander("➕ Add Match"):
        series_id = st.number_input("Series ID", min_value=1, step=1, key="match_series_id")
        venue_id = st.number_input("Venue ID", min_value=1, step=1, key="match_venue_id")
        team1 = st.text_input("Team 1", key="match_team1")
        team2 = st.text_input("Team 2", key="match_team2")
        status = st.text_input("Match Status", key="match_status")

        if st.button("Add Match", key="add_match_btn"):
            run_query(
                "INSERT INTO matches (series_id, venue_id, team1, team2, status) VALUES (?, ?, ?, ?, ?)",
                (series_id, venue_id, team1, team2, status),
            )
            st.success("✅ Match added!")

# -------------------------
# SERIES CRUD
# -------------------------
with tab5:
    st.header("Manage Series")
    df = view_table("series")

    with st.expander("➕ Add Series"):
        series_name = st.text_input("Series Name", key="series_name")
        start_date = st.date_input("Start Date", key="series_start")
        end_date = st.date_input("End Date", key="series_end")

        if st.button("Add Series", key="add_series_btn"):
            run_query(
                "INSERT INTO series (series_name, start_date, end_date) VALUES (?, ?, ?)",
                (series_name, str(start_date), str(end_date)),
            )
            st.success("✅ Series added!")
