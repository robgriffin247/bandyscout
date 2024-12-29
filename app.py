import streamlit as st
from sportradar.get_current_elitserien import get_current_elitserien
from sportradar.get_elitserien_fixtures import get_elitserien_fixtures
import polars as pl


st.header("BandyScout")


if "standings" not in st.session_state:
    st.session_state["standings"] = get_current_elitserien(st.secrets["sportsradar"]["api_key"])

if "fixtures" not in st.session_state:
    st.session_state["fixtures"] = get_elitserien_fixtures(st.secrets["sportsradar"]["api_key"])
    

standings_tab, results_tab, fixtures_tab = st.tabs(["Standings", "Results", "Fixtures"])




with standings_tab:

    st.dataframe(st.session_state["standings"][["team_rank", "team_name", "games", "points", "games_won", "games_drawn", "games_lost", "goals_scored", "goals_conceded", "goals_difference"]],
                hide_index=True,
                height=528,
                use_container_width=True,
                column_config={
                    "team_rank":st.column_config.NumberColumn("Pos"),
                    "team_name":st.column_config.TextColumn("Team"),
                    "games":st.column_config.NumberColumn("Pld"),
                    "points":st.column_config.NumberColumn("Pts"),
                    "games_won":st.column_config.NumberColumn("Won"),
                    "games_drawn":st.column_config.NumberColumn("Drw"),
                    "games_lost":st.column_config.NumberColumn("Lst"),
                    "goals_scored":st.column_config.NumberColumn("Gl+"),
                    "goals_conceded":st.column_config.NumberColumn("Gl-"),
                    "goals_difference":st.column_config.NumberColumn("Dif"),
                })



with results_tab:

    team_names = st.session_state["standings"]["team_name"]
    team_names = team_names.sort().to_list()
    team_names.insert(0, "All")

    team_menu, round_menu = st.columns([6,3])

    team_menu.selectbox("Team", key="chosen_team", options=team_names)

    if st.session_state["chosen_team"]=="All":
        results = st.session_state["fixtures"].filter(pl.col("match_status")=="closed")

    else:
        results = st.session_state["fixtures"].filter(
            (pl.col("match_status")=="closed") & 
            ((pl.col("home_team")==st.session_state["chosen_team"]) | (pl.col("away_team")==st.session_state["chosen_team"]))
            )
    
    rounds = [i for i in range(1, results["event_round"].max()+1)]
    rounds.insert(0, "All")

    round_menu.selectbox("Round", key="chosen_round", options=rounds)

    if st.session_state["chosen_round"]=="All":
        pass
    else:
        results = results.filter(pl.col("event_round")==st.session_state["chosen_round"])

    st.dataframe(results[["event_datetime", "event_round", "home_team", "score", "away_team",]],
                 use_container_width=True,
                 height=528)


# TODO:
# - add round filter to results
# - add result to results
# - format results
# - add fixtures, copying much of results
# - add team form tab
#   - form: color guide, home/away, opponent rank/form