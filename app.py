from data.get_assets import get_matches, get_results, get_standings
from streamlit_components.menus import choose_team, choose_location
from streamlit_components.tables import team_results_table, standings_table
from streamlit_components.figures import results_bar
import streamlit as st

import duckdb 
import pandas as pd
import plotly.express as px


# TODO:
# - hourly update limit
# - streaks on league

# Generate datasets
if 'matches' not in st.session_state:
    st.session_state["matches"] = get_matches(st.secrets["sportsradar"]["api_key"])
    st.session_state["results"] = get_results(st.session_state["matches"])
    st.session_state["standings"] = get_standings(st.session_state["results"])


# Page setup
team_form_tab, league_tab = st.tabs(["Teams", "League"])

# Tabs ------------------------------------------------------------------
with team_form_tab:

    team_menu, location_menu = st.columns([6,4])

    team_results = choose_team(st.session_state["results"], team_menu)
    team_results = choose_location(team_results, location_menu)
    
    team_results_table(team_results)

    results_figure, _ = st.columns([2,8])

    results_figure.plotly_chart(results_bar(team_results))

with league_tab:
    standings_table(st.session_state["standings"])
