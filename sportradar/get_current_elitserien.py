import httpx
import json
import polars as pl
import streamlit as st
def get_current_elitserien(api_key):

    standings_url = f"https://api.sportradar.com/bandy/production/v2/en/seasons/sr:season:121299/standings.json?api_key={api_key}"
    
    standings_response = httpx.get(standings_url)
    
    standings_response.raise_for_status()

    standings_json = json.loads(standings_response.content)
    st.write(standings_json)
    current_standings_list = standings_json["standings"][0]["groups"][0]["standings"]

    standings_dict = ([
        {"rank": row["rank"],
         "rank_change": row["change"],
         "team": row["competitor"]["name"], 
         "team_abb": row["competitor"]["abbreviation"], 
         "matches": row["played"],
         "won": row["win"],
         "drawn": row["draw"],
         "lost": row["loss"],
         "points": row["points"],
         "scored": row["goals_for"],
         "conceded": row["goals_against"],
         "difference": row["goals_diff"],
        } 
        for row in current_standings_list])

    standings = pl.DataFrame(standings_dict)

    team_name_mapping = {
        "Broberg/Soderhamn BS":"Broberg/Söderhamn BS",
        "Villa-Lidkoping BK":"Villa-Lidköping BK",
        "Vasteraas SK":"Västerås SK",
        "Bollnas GIF":"Bollnäs GIF",
        "IFK Vanersborg":"IFK Vänersborg",
        "Frillesaas BK":"Frillesås BK",
        "Aby/Tjureda IF":"Åby/Tjureda IF",
    }

    standings = standings.with_columns(pl.col("team").replace(team_name_mapping))





    return standings