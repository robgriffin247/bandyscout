import polars as pl
import streamlit as st
import duckdb

def choose_team(data, menu):
    menu.selectbox("Team", key="team", options=st.session_state["results"]["team"].unique().sort().to_list())

    with duckdb.connect() as con:
        df = con.sql(f'''
                    select * from data where team='{st.session_state["team"]}'
                    ''').pl()
    return df

def choose_location(data, menu):
    menu.selectbox("Matches", key="location", options=["All", "Home", "Away"])
        
    if st.session_state["location"]=='Home':
        team_results = data.filter(pl.col("home"))
    elif st.session_state["location"]=='Away':
        team_results = data.filter(pl.col("home")==False)
    else:
        team_results = data

    return team_results
