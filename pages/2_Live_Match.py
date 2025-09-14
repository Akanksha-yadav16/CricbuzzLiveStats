# pages/2_Live_Match.py
import streamlit as st
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.api_handler import get_live_matches, get_match_score

st.title("Live Matches")

# Fetch live matches
matches = get_live_matches()

if not matches:
    st.error("Could not fetch live matches. Please check your API key or internet connection.")
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
                    match_header = (
                        score_data.get("matchHeader")
                        or score_data.get("matchInfo")
                        or {}
                    )

                    if match_header:
                        st.write(match_header)
                    else:
                        st.write("No match summary available.")

                    # Try to get scorecards
                    innings = (
                        score_data.get("scoreCard")
                        or score_data.get("inningsScore")
                        or []
                    )

                    if not innings:
                        # ✅ Mini Scoreboard fallback
                        st.warning("⚠️ Full scorecard not available yet. Showing mini scoreboard.")

                        mini = score_data.get("matchInfo") or {}

                        team1 = mini.get("team1", {}).get("teamName", "Team 1")
                        team2 = mini.get("team2", {}).get("teamName", "Team 2")
                        status = mini.get("status", "Status unavailable")
                        venue = mini.get("venueInfo", {}).get("ground", "Unknown Venue")
                        match_desc = mini.get("matchDesc", "Unknown Match")

                        st.markdown(f"###  {team1} vs {team2} - {match_desc}")
                        st.write(f" Venue: {venue}")
                        st.write(f" Status: {status}")

                        # Try to show quick scores if available
                        # Try to show quick scores if available
                        quick_scores = score_data.get("matchScore", {})
                        if quick_scores:
                            st.subheader(" Quick Score")

                            score_rows = []
                            for team_key in ["team1Score", "team2Score"]:
                                team_score = quick_scores.get(team_key, {})
                                for inng, details in team_score.items():
                                    score_rows.append({
                                    "Team": team_key.replace("Score", "").capitalize(),
                                    "Innings": inng,
                                    "Runs": details.get("runs", 0),
                                    "Wickets": details.get("wickets", 0),
                                    "Overs": details.get("overs", "0.0")
                        })

                            if score_rows:
                                score_df = pd.DataFrame(score_rows)
                                st.table(score_df)
                            else:
                                 st.write("No quick score data available.")

                            # Batting table
                            batsmen = (
                                inn.get("batTeamDetails", {}).get("batsmenData", {}).values()
                                or inn.get("batsmen", [])
                            )
                            if batsmen:
                                bat_df = pd.DataFrame(batsmen)
                                keep_cols = [c for c in ["batName", "runs", "balls", "fours", "sixes", "strikeRate"] if c in bat_df.columns]
                                if keep_cols:
                                    bat_df = bat_df[keep_cols]
                                    bat_df.columns = ["Batsman", "Runs", "Balls", "4s", "6s", "SR"]
                                    st.table(bat_df)
                            else:
                                st.write("No batting data available.")

                            # Bowling table
                            bowlers = (
                                inn.get("bowlTeamDetails", {}).get("bowlersData", {}).values()
                                or inn.get("bowlers", [])
                            )
                            if bowlers:
                                bowl_df = pd.DataFrame(bowlers)
                                keep_cols = [c for c in ["bowlName", "overs", "maidens", "runs", "wickets", "economy"] if c in bowl_df.columns]
                                if keep_cols:
                                    bowl_df = bowl_df[keep_cols]
                                    bowl_df.columns = ["Bowler", "Overs", "Maidens", "Runs", "Wkts", "Econ"]
                                    st.table(bowl_df)
                            else:
                                st.write("No bowling data available.")

                            st.markdown("---")
