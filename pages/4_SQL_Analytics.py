# pages/4_SQL_Analytics.py
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# -------------------------
# DB Connection
# -------------------------
DB_PATH = "cricbuzz.db"

def run_query(query: str):
    """Execute SQL query and return DataFrame"""
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"SQL Error: {e}")
        return pd.DataFrame()

# -------------------------
# Predefined Queries (all 25 from Cricbuzz.pdf)
# -------------------------
queries = {
    "Q1. List all players with their country and role": """
        SELECT full_name, country, playing_role FROM players;
    """,
    "Q2. Total number of players per country": """
        SELECT country, COUNT(*) AS total_players FROM players GROUP BY country ORDER BY total_players DESC;
    """,
    "Q3. Find players with more than 50 centuries": """
        SELECT p.full_name, ps.centuries FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        WHERE ps.centuries > 50;
    """,
    "Q4. Average runs scored by players in ODI": """
        SELECT AVG(batting_avg) AS avg_batting_average FROM player_stats WHERE format = 'ODI';
    """,
    "Q5. Count of players by role": """
        SELECT playing_role, COUNT(*) AS player_count FROM players GROUP BY playing_role;
    """,
    "Q6. Top 10 ODI run scorers": """
        SELECT p.full_name, ps.total_runs, ps.batting_avg, ps.centuries
        FROM player_stats ps
        JOIN players p ON p.player_id = ps.player_id
        WHERE ps.format = 'ODI'
        ORDER BY ps.total_runs DESC
        LIMIT 10;
    """,
    "Q7. Top 10 wicket takers (ODI)": """
        SELECT p.full_name, ps.wickets, ps.bowling_avg, ps.five_wkts
        FROM player_stats ps
        JOIN players p ON p.player_id = ps.player_id
        WHERE ps.format = 'ODI'
        ORDER BY ps.wickets DESC
        LIMIT 10;
    """,
    "Q8. Players with strike rate above 150 in T20": """
        SELECT p.full_name, ps.strike_rate
        FROM player_stats ps
        JOIN players p ON p.player_id = ps.player_id
        WHERE ps.format = 'T20' AND ps.strike_rate > 150;
    """,
    "Q9. Highest individual score per format": """
        SELECT format, MAX(highest_score) AS highest_score
        FROM player_stats GROUP BY format;
    """,
    "Q10. Players who played in more than 200 matches": """
        SELECT p.full_name, ps.matches
        FROM player_stats ps
        JOIN players p ON p.player_id = ps.player_id
        WHERE ps.matches > 200;
    """,
    "Q11. Players with more than 400 wickets": """
        SELECT p.full_name, ps.wickets
        FROM player_stats ps
        JOIN players p ON p.player_id = ps.player_id
        WHERE ps.wickets > 400;
    """,
    "Q12. Average economy rate of bowlers in ODI": """
        SELECT AVG(economy) AS avg_economy
        FROM player_stats
        WHERE format = 'ODI' AND economy IS NOT NULL;
    """,
    "Q13. Players with most fifties": """
        SELECT p.full_name, ps.fifties
        FROM player_stats ps
        JOIN players p ON p.player_id = ps.player_id
        ORDER BY ps.fifties DESC
        LIMIT 10;
    """,
    "Q14. Country with most centuries by players": """
        SELECT p.country, SUM(ps.centuries) AS total_centuries
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        GROUP BY p.country
        ORDER BY total_centuries DESC
        LIMIT 5;
    """,
    "Q15. Youngest player in database": """
        SELECT full_name, country, date_of_birth
        FROM players
        ORDER BY date_of_birth DESC
        LIMIT 1;
    """,
    "Q16. Oldest player in database": """
        SELECT full_name, country, date_of_birth
        FROM players
        ORDER BY date_of_birth ASC
        LIMIT 1;
    """,
    "Q17. Players with more than 100 catches": """
        SELECT p.full_name, ps.catches
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        WHERE ps.catches > 100;
    """,
    "Q18. Countries with most players": """
        SELECT country, COUNT(*) AS total_players
        FROM players
        GROUP BY country
        ORDER BY total_players DESC
        LIMIT 10;
    """,
    "Q19. Players with highest batting average in ODI (min 1000 runs)": """
        SELECT p.full_name, ps.batting_avg
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        WHERE ps.format = 'ODI' AND ps.total_runs > 1000
        ORDER BY ps.batting_avg DESC
        LIMIT 10;
    """,
    "Q20. Players with most sixes in T20": """
        SELECT p.full_name, ps.sixes
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        WHERE ps.format = 'T20'
        ORDER BY ps.sixes DESC
        LIMIT 10;
    """,
    "Q21. Country with highest number of wickets": """
        SELECT p.country, SUM(ps.wickets) AS total_wickets
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        GROUP BY p.country
        ORDER BY total_wickets DESC
        LIMIT 5;
    """,
    "Q22. Players with highest strike rate in ODI": """
        SELECT p.full_name, ps.strike_rate
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        WHERE ps.format = 'ODI'
        ORDER BY ps.strike_rate DESC
        LIMIT 10;
    """,
    "Q23. Total matches played by each country": """
        SELECT p.country, SUM(ps.matches) AS total_matches
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        GROUP BY p.country
        ORDER BY total_matches DESC
        LIMIT 10;
    """,
    "Q24. Players with more than 10,000 runs across formats": """
        SELECT p.full_name, SUM(ps.total_runs) AS career_runs
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        GROUP BY p.full_name
        HAVING career_runs > 10000
        ORDER BY career_runs DESC;
    """,
    "Q25. Top 10 all-rounders (runs + wickets)": """
        SELECT p.full_name, SUM(ps.total_runs) AS runs, SUM(ps.wickets) AS wickets
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        GROUP BY p.full_name
        ORDER BY (SUM(ps.total_runs) + SUM(ps.wickets)) DESC
        LIMIT 10;
    """
}

# -------------------------
# Streamlit UI
# -------------------------
st.title("SQL Analytics Dashboard")
st.markdown("Run **25 Predefined SQL Queries** with **Charts + Tables** automatically.")

query_choice = st.selectbox("Choose a predefined query:", ["-- Select --"] + list(queries.keys()))

if query_choice != "-- Select --":
    sql = queries[query_choice]
    st.code(sql, language="sql")
    result = run_query(sql)

    if not result.empty:
        st.subheader(" Query Result")
        st.dataframe(result)

        # Auto visualization if suitable
        num_cols = result.select_dtypes(include=["int", "float"]).columns
        cat_cols = result.select_dtypes(include=["object"]).columns

        if len(num_cols) > 0 and len(cat_cols) > 0:
            x = cat_cols[0]
            y = num_cols[0]
            st.subheader("Visualization")
            fig, ax = plt.subplots()
            ax.bar(result[x], result[y], color="skyblue")
            ax.set_ylabel(y)
            ax.set_xlabel(x)
            plt.xticks(rotation=45, ha="right")
            st.pyplot(fig)

        elif len(num_cols) == 1 and len(result) < 20:
            st.subheader("Pie Chart")
            fig, ax = plt.subplots()
            ax.pie(result[num_cols[0]], labels=result[cat_cols[0]] if len(cat_cols) > 0 else None, autopct="%1.1f%%")
            ax.axis("equal")
            st.pyplot(fig)

    else:
        st.warning("⚠️ No data returned for this query.")

st.markdown("---")

# Custom Query
st.subheader("Run Custom SQL")
custom_sql = st.text_area("Enter your SQL query here:", height=150)

if st.button("Run Custom Query"):
    if custom_sql.strip():
        result = run_query(custom_sql)
        if not result.empty:
            st.dataframe(result)

            # auto-chart for custom queries
            num_cols = result.select_dtypes(include=["int", "float"]).columns
            cat_cols = result.select_dtypes(include=["object"]).columns
            if len(num_cols) > 0 and len(cat_cols) > 0:
                x = cat_cols[0]
                y = num_cols[0]
                st.subheader(" Visualization")
                fig, ax = plt.subplots()
                ax.bar(result[x], result[y], color="orange")
                plt.xticks(rotation=45, ha="right")
                st.pyplot(fig)

        else:
            st.warning("⚠️ No data returned for this query.")
    else:
        st.error("❌ Please enter a query before running.")
