import polars as pl
import streamlit as st
import pandas as pd

def table_height(data):
    if type(data)==int:
        return (data+1)*35+7
    else:
        return (data.shape[0]+1)*35+7
    
def standings_table(data):
    st.dataframe(data,
                 height=table_height(data))

def team_results_table(data):
    team_results = data.sort(["date"], descending=True)

    styled_team_results = pd.DataFrame(team_results, columns=team_results.columns)[["date", "home_away", "result", "score_formatted", "opponent"]]
    styled_team_results = styled_team_results.style.map(lambda x: f"background-color: {'#70997b' if x=='W' else '#fc90a2' if x=='L' else '#c0becc'}", subset='result')

    st.dataframe(styled_team_results,
                 height=table_height(6),
                 use_container_width=True,
                 hide_index=True,
                 column_config={
                     "date":st.column_config.DateColumn("Date", format="DD/MM", width="small"),
                     "home_away":st.column_config.TextColumn("H/A", width="small"),
                     "result":st.column_config.TextColumn("Result", width="small"),
                     "score_formatted":st.column_config.TextColumn("Score (HT)", width="small"),
                     "opponent":st.column_config.TextColumn("Opponent", width="large"),
                 })
