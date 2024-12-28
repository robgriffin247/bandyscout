import httpx
import json
import polars as pl

def get_current_elitserien(api_key):

    standings_url = f"https://api.sportradar.com/bandy/production/v2/en/seasons/sr:season:121299/standings.json?api_key={api_key}"
    
    standings_response = httpx.get(standings_url)
    
    standings_response.raise_for_status()

    standings_json = json.loads(standings_response.content)

    current_standings_list = standings_json["standings"][0]["groups"][0]["standings"]

    standings_dict = ([
        {"team_rank": row["rank"],
         "rank_change": row["change"],
         "team_name": row["competitor"]["name"], 
         "team_abb": row["competitor"]["abbreviation"], 
         "games": row["played"],
         "games_won": row["win"],
         "games_drawn": row["draw"],
         "games_lost": row["loss"],
         "points": row["points"],
         "goals_scored": row["goals_for"],
         "goals_conceded": row["goals_against"],
         "goals_difference": row["goals_diff"],
        } 
        for row in current_standings_list])

    standings = pl.DataFrame(standings_dict)



    return standings