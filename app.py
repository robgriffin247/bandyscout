import streamlit as st
from sportradar.get_current_elitserien import get_current_elitserien
from sportradar.get_elitserien_fixtures import get_elitserien_fixtures

st.header("BandyScout")


standings = get_current_elitserien(st.secrets["sportsradar"]["api_key"])

fixtures = get_elitserien_fixtures(st.secrets["sportsradar"]["api_key"])

standings_tab, fixtures_tab = st.tabs(["Standings", "Fixtures"])

with standings_tab:

    st.dataframe(standings[["team_name", "games", "points", "games_won", "games_drawn", "games_lost", "goals_scored", "goals_conceded", "goals_difference"]],
                hide_index=True,
                use_container_width=True,
                column_config={
                    "team_name":st.column_config.TextColumn("Lag"),
                    "games":st.column_config.NumberColumn("Matcher"),
                    "points":st.column_config.NumberColumn("Poäng"),
                    "games_won":st.column_config.NumberColumn("V"),
                    "games_drawn":st.column_config.NumberColumn("O"),
                    "games_lost":st.column_config.NumberColumn("F"),
                    "goals_scored":st.column_config.NumberColumn("+"),
                    "goals_conceded":st.column_config.NumberColumn("-"),
                    "goals_difference":st.column_config.NumberColumn("+/-"),
                })


with fixtures_tab:
    
    st.dataframe(fixtures)


