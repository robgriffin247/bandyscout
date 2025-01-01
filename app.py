from data.get_assets import get_matches, get_results, get_standings
from streamlit_components.tables import table_height, standings_table
from streamlit_components.menus import choose_team, choose_location
import streamlit as st

import duckdb 
import polars as pl
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

    st.dataframe(team_results[["date", "home_away", "result", "score_formatted",  "opponent"]].sort(["date"], descending=True),
                 height=table_height(6),
                 use_container_width=True,
                 column_config={
                     "date":st.column_config.DateColumn("Date", format="DD/MM", width="small"),
                     "home_away":st.column_config.TextColumn("H/A", width="small"),
                     "result":st.column_config.TextColumn("Result", width="small"),
                     "score_formatted":st.column_config.TextColumn("Score (HT)", width="small"),
                     "opponent":st.column_config.TextColumn("Opponent", width="large"),
                 })


    form_pie_chart, _ = st.columns(2)

    def form_pie(data):
        
        with duckdb.connect() as con:
            counts = con.sql('select result, count(result) as n from data group by result').pl()

        form_pie = px.pie(counts, values='n', names='result',
                          hole=0.6
                          )

        return form_pie
    
    form_pie_chart.plotly_chart(form_pie(team_results))

with league_tab:
    standings_table(st.session_state["standings"])


