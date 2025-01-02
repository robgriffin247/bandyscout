from data.get_assets import get_matches, get_results, get_standings
from streamlit_components.menus import choose_team, choose_location
from streamlit_components.tables import standings_table
from streamlit_components.figures import results_pie, form_bar
import streamlit as st
import os
import duckdb 
import pandas as pd
import plotly.express as px
import time

# TODO:
# - add fixture list
# - add league peek and next fixture to teams tab
# - hourly update limit
# - streaks on league
# - form in league table
# - change xaxis labels in form_figure
# - fix status for villa-gripen
# - dummy player & match data

st.set_page_config(page_title="BandyScout", 
                   page_icon=":field_hockey_stick_and_ball:", 
                   layout="centered", 
                   initial_sidebar_state="auto", 
                   menu_items=None)

# Generate datasets
if 'matches' not in st.session_state:
    st.session_state["matches"] = get_matches(st.secrets["sportsradar"]["api_key"])
    st.session_state["results"] = get_results(st.session_state["matches"])
    st.session_state["standings"] = get_standings(st.session_state["results"])


# Page setup
st.header("BandyScout")
team_form_tab, league_tab = st.tabs(["Teams", "League"])

# Tabs ------------------------------------------------------------------
with team_form_tab:

    st.write(" ")

    team_menu, location_menu = st.columns([6,4])

    team_results = choose_team(st.session_state["results"], team_menu)
    team_results = choose_location(team_results, location_menu)
    
    st.write(" ")
    #team_results_table(team_results)
    
    st.markdown("**Elitserien Standings**")
    standings_table(st.session_state["results"], st.session_state["team"], st.session_state["location"])

    st.write(" ")
    results_figure, form_figure = st.columns([4,8], gap="large")

    with results_figure:
        st.markdown("**Results**")
        st.plotly_chart(results_pie(team_results))
    
    with form_figure:
        st.markdown("**Recent Form**")
        st.plotly_chart(form_bar(team_results))
   



with league_tab:
    import polars as pl
    st.write(" ")
    table_container = st.container()
    standings_location_menu, _ = st.columns([4,6])
    standings_location_menu.selectbox("Matches", key="standings_location", options=["All", "Home", "Away"])
    standings_table( st.session_state["results"], location=st.session_state["standings_location"], container=table_container)



# Footer --------------------------------------------------------
st.markdown(f"""
            ----
            *Data refreshed: {time.strftime('%Y-%m-%d %H:%M', time.localtime(float(os.path.getmtime('data/matches.csv'))))}*
            """)
