import polars as pl
import streamlit as st
import pandas as pd

win_color="#78c975"
draw_color="#e6f1f5"
loss_color="#fa8578"


def table_height(data):
    if type(data)==int:
        return (data+1)*35+7
    else:
        return (data.shape[0]+1)*35+7
    
def standings_table(data, team=None):
    if team==None:
        df=data
    else:
        team_rank = data.row(by_predicate=(pl.col("team") == team), named=True)["rank"]-1
        if team_rank==0:
            ranks = [0, 1, 2]
        elif team_rank==13:
            ranks=[11,12,13]
        else:
            ranks=[team_rank-1, team_rank, team_rank+1]
        df = st.session_state["standings"][ranks]

    st.markdown("**Elitserien Standings**")
    st.dataframe(df, height=table_height(df))


def team_results_table(data):
    
    team_results = data.sort(["date"], descending=True)

    styled_team_results = pd.DataFrame(team_results, columns=team_results.columns)[["date", "home_away", "result", "score_formatted", "opponent"]]
    styled_team_results = styled_team_results.style.map(lambda x: f"background-color: {win_color if x=='W' else loss_color if x=='L' else draw_color}", subset='result')
    
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
