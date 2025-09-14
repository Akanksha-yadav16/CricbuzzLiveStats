# pages/2_Live_Match.py
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
from utils.api_handler import get_live_matches, get_match_score

st.title("Live Matches")

# Fetch live matches
matches = get_live_matches()

if not matches:
    st.error("❌ Could not fetch live matches. Please check your API key or internet connection.")
else:
    type_matches = matches.get("typeMatches", [])

    if not type_matches:
        st.info("ℹ️ No live matches at the moment.")
    else:
        # Collect live match list
        live_match_list = []
        for category in type_matches:
            for match in category.get("seriesMatches", []):
                series = match.get("seriesAdWrapper", {})
                for m in series.get("matches", []):
                    match_info = m.get("matchInfo", {})
                    match_id = match_info.get("matchId")
                    team1 = match_info.get("team1", {}).get("teamName")
                    team2 = match_info.get("team2", {}).get("teamName")
                    match_desc = match_info.get("matchDesc", "Unknown Match")
                    venue = match_info.get("venueInfo", {}).get("ground", "Unknown Venue")

                    if match_id and team1 and team2:
                        live_match_list.append({
                            "id": match_id,
                            "desc": f"{team1} vs {team2} - {match_desc} @ {venue}"
                        })

        if not live_match_list:
            st.info("ℹ️ No live matches available right now.")
        else:
            # Dropdown
            match_choice = st.selectbox(
                "Select a live match:",
                options=live_match_list,
                format_func=lambda x: x["desc"]
            )

            if match_choice:
                match_id = match_choice["id"]
                score_data = get_match_score(match_id)

                if not score_data:
                    st.error("❌ Could not fetch scorecard for this match.")
                else:
                    # Debug view
                    with st.expander("Raw API Response (Debug Mode)"):
                        st.json(score_data)

                    # Match summary
                    st.subheader("Match Summary")
                    match_header = score_data.get("matchHeader") or score_data.get("matchInfo") or {}
                    if match_header:
                        st.write(match_header)
                    else:
                        st.write("No match summary available.")

                    # ✅ Get innings from "scorecard"
                    innings = score_data.get("scorecard") or []

                    if not innings:
                        st.warning("⚠️ Full scorecard not available yet.")
                        mini = score_data.get("matchInfo") or {}
                        team1 = mini.get("team1", {}).get("teamName", "Team 1")
                        team2 = mini.get("team2", {}).get("teamName", "Team 2")
                        status = mini.get("status", "Status unavailable")

                        st.markdown(f"### 🏏 {team1} vs {team2}")
                        st.write(f"**Match Status:** {status}")
                    else:
                        # ✅ Full scorecard parsing
                        for inn in innings:
                            team_name = inn.get("batteamname") or f"Innings {inn.get('inningsid')}"
                            st.markdown(f"### 🏏 {team_name}")

                            # Batting table
                            batsmen = inn.get("batsman", [])
                            if batsmen:
                                bat_df = pd.DataFrame(batsmen)
                                keep_cols = [c for c in ["name", "runs", "balls", "fours", "sixes", "strkrate"] if c in bat_df.columns]
                                if keep_cols:
                                    bat_df = bat_df[keep_cols]
                                    bat_df = bat_df.rename(columns={
                                        "name": "Batsman",
                                        "runs": "Runs",
                                        "balls": "Balls",
                                        "fours": "4s",
                                        "sixes": "6s",
                                        "strkrate": "SR"
                                    })
                                    st.table(bat_df)
                            else:
                                st.write("No batting data available.")

                            # ✅ Safe Bowling table
                            bowlers = inn.get("bowler", [])
                            if bowlers:
                                bowl_df = pd.DataFrame(bowlers)
                                keep_cols = [c for c in ["name", "overs", "runs", "wickets", "economyrate"] if c in bowl_df.columns]
                                if keep_cols:
                                    bowl_df = bowl_df[keep_cols]
                                    bowl_df = bowl_df.rename(columns={
                                        "name": "Bowler",
                                        "overs": "Overs",
                                        "runs": "Runs",
                                        "wickets": "Wkts",
                                        "economyrate": "Econ"
                                    })
                                    st.table(bowl_df)
                                else:
                                    st.write("No bowling stats available.")
                            else:
                                st.write("No bowling data available.")

                            st.markdown("---")
