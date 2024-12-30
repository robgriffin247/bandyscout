import streamlit as st
import polars as pl
from sportradar.get_current_elitserien import get_current_elitserien
from sportradar.get_elitserien_fixtures import get_elitserien_fixtures
from streamlit_components.tables import standings_table, results_table
from streamlit_components.filters import matches_results_filter, matches_team_filter, matches_round_filter

if "standings" not in st.session_state:
    st.session_state["obt_standings"] = get_current_elitserien(st.secrets["sportsradar"]["api_key"])

if "matches" not in st.session_state:
    st.session_state["obt_fixtures"] = get_elitserien_fixtures(st.secrets["sportsradar"]["api_key"])
    

# Uniform components:
st.header("BandyScout")

standings_tab, results_tab = st.tabs(["Standings", "Results"])
standings_tab, results_tab, fixtures_tab, teams_tab, players_tab = st.tabs(["Standings", "Results", "Fixtures", "Teams", "Players"])


# Tabs:
with standings_tab:
    standings_table(st.session_state["obt_standings"])

with results_tab:
    
    teams_menu, rounds_menu = st.columns([6,4])

    st.session_state["results"] = matches_results_filter()
    st.session_state["results"] = matches_team_filter(st.session_state["results"], teams_menu)
    st.session_state["results"] = matches_round_filter(st.session_state["results"], rounds_menu)

    results_table(st.session_state["results"])


# TODO:
# - add fixtures, copying much of results
# - add team form tab
#   - form: color guide, home/away, opponent rank/form

