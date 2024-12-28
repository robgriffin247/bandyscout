import streamlit as st
from sportradar.get_current_elitserien import get_current_elitserien

current_standings = get_current_elitserien(st.secrets["sportsradar"]["api_key"])


st.title("Elitserien 24/25")

standings_tab, fixtures_tab = st.tabs(["Standings", "Fixtures"])#, "Teams", "Players"])


with standings_tab:
    st.dataframe(current_standings)

with fixtures_tab:
    pass