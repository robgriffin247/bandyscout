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
        {"rank": row["rank"],
         "change": row["change"],
         "team": row["competitor"]["name"], 
         "team_abb": row["competitor"]["abbreviation"], 
         "played": row["played"],
         "won": row["win"],
         "drawn": row["draw"],
         "lost": row["loss"],
         "points": row["points"],
         "scored": row["goals_for"],
         "conceded": row["goals_against"],
         "goal_diff": row["goals_diff"]} 
        for row in current_standings_list])

    return pl.DataFrame(standings_dict)
