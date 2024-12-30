import streamlit as st
import polars as pl


def matches_results_filter():
    return st.session_state["obt_fixtures"].filter(pl.col("match_status")=="closed")


def matches_team_filter(data, menu):
    team_names = data["home_team"].unique().sort().to_list()
    team_names.insert(0, "All")

    menu.selectbox("Team", key="chosen_team", options=team_names)

    if st.session_state["chosen_team"]=="All":
        return data

    else:
        return data.filter((pl.col("home_team")==st.session_state["chosen_team"]) | 
                        (pl.col("away_team")==st.session_state["chosen_team"]))



def matches_round_filter(data, menu):
        
    rounds = [i for i in range(1, data["event_round"].max()+1)]
    rounds.insert(0, "All")

    menu.selectbox("Round", key="chosen_round", options=rounds)

    if st.session_state["chosen_round"]=="All":
        return data
    else:
        return data.filter(pl.col("event_round")==st.session_state["chosen_round"])