from data.get_assets import get_results, get_standings
import streamlit as st
import duckdb 
import polars as pl

if 'results' not in st.session_state:
    st.session_state["results"] = get_results()

standings = get_standings(st.session_state["results"])

st.dataframe(standings)

def choose_team(data, menu):
    menu.selectbox("Team", key="team", options=st.session_state["results"]["team"].unique().sort().to_list())

    with duckdb.connect() as con:
        df = con.sql(f'''
                     select * from data where team='{st.session_state["team"]}'
                     ''').pl()
    return df

def choose_location(data, menu):
    menu.selectbox("Home/Away", key="location", options=["All", "Home", "Away"])
        
    if st.session_state["location"]=='Home':
        team_results = data.filter(pl.col("home"))
    elif st.session_state["location"]=='Away':
        team_results = data.filter(pl.col("home")==False)
    else:
        team_results = data

    return team_results

team_menu, location_menu = st.columns([6,4])

team_results = choose_team(st.session_state["results"], team_menu)
team_results = choose_location(team_results, location_menu)

st.dataframe(team_results[["date", "home", "opponent", "scored", "conceded", "result"]])
