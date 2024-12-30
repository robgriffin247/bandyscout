import streamlit as st

def standings_table(data):
   
    st.dataframe(data[["rank", "team", "matches", "points", "won", "drawn", "lost", "scored", "conceded", "difference"]],
                hide_index=True,
                height=528,
                use_container_width=True,
                column_config={
                    "rank":st.column_config.NumberColumn("Pos"),
                    "team":st.column_config.TextColumn("Team"),
                    "matches":st.column_config.NumberColumn("Pld"),
                    "points":st.column_config.NumberColumn("Pts"),
                    "won":st.column_config.NumberColumn("Won"),
                    "drawn":st.column_config.NumberColumn("Drw"),
                    "lost":st.column_config.NumberColumn("Lst"),
                    "scored":st.column_config.NumberColumn("Gls +"),
                    "conceded":st.column_config.NumberColumn("Gls -"),
                    "difference":st.column_config.NumberColumn("Dif"),
                })


def results_table(data):

    st.dataframe(data[["event_datetime", "event_round", "home_team", "score", "away_team",]],
                use_container_width=True,
                height=528,
                column_config={
                    "event_datetime": st.column_config.DateColumn("Date", format="yyyy-MM-DD"),
                    "event_round":st.column_config.NumberColumn("Round"),
                    "home_team":st.column_config.TextColumn("Home"),
                    "score":st.column_config.TextColumn("Score (HT)"),
                    "away_team":st.column_config.TextColumn("Away"),
                })
