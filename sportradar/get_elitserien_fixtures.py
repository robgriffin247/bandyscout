import httpx
import json
import polars as pl

def get_elitserien_fixtures(api_key):

    fixtures_url = f"https://api.sportradar.com/bandy/production/v2/en/seasons/sr:season:121299/summaries.json?api_key={api_key}"
        
    fixtures_response = httpx.get(fixtures_url)
    
    fixtures_response.raise_for_status()

    fixtures_json = json.loads(fixtures_response.content)
    
    fixture_summaries = fixtures_json["summaries"]

    fixtures_dicts = ([
        {"event_datetime": event["sport_event"]["start_time"],
         "event_round": event["sport_event"]["sport_event_context"]["round"]["number"],
         "home_team": event["sport_event"]["competitors"][0]["name"],
         "away_team": event["sport_event"]["competitors"][1]["name"],
         "match_status": event["sport_event_status"]["status"],
         "match_details": event["sport_event_status"]
        }
        for event in fixture_summaries])

    updated_fixtures_dicts = []
    for event in fixtures_dicts:
        if event["match_status"]=="closed":
            event["home_score_ht"]=f'({event["match_details"]["period_scores"][0]["home_score"]}'
            event["home_score_ft"]=event["match_details"]["home_score"]
            event["away_score_ht"]=f'{event["match_details"]["period_scores"][0]["away_score"]})'
            event["away_score_ft"]=event["match_details"]["away_score"]
            pass
        else:
            pass
        event.pop("match_details")
        updated_fixtures_dicts.append(event)

    fixtures = pl.DataFrame(updated_fixtures_dicts)
                
    team_name_mapping = {
        "Broberg/Soderhamn BS":"Broberg/Söderhamn BS",
        "Villa-Lidkoping BK":"Villa-Lidköping BK",
        "Vasteraas SK":"Västerås SK",
        "Bollnas GIF":"Bollnäs GIF",
        "IFK Vanersborg":"IFK Vänersborg",
        "Frillesaas BK":"Frillesås BK",
        "Aby/Tjureda IF":"Åby/Tjureda IF",
    }

    fixtures = fixtures.with_columns(pl.col("home_team").replace(team_name_mapping))
    fixtures = fixtures.with_columns(pl.col("away_team").replace(team_name_mapping))

    fixtures = fixtures.with_columns(
        pl.concat_str([
            pl.col("home_score_ft"),
            pl.col("away_score_ft"),
        ], separator="-").alias("score_ft")
    )

    fixtures = fixtures.with_columns(
        pl.concat_str([
            pl.col("home_score_ht"),
            pl.col("away_score_ht"),
        ], separator="-").alias("score_ht")
    )

    fixtures = fixtures.with_columns(
        pl.concat_str([
            pl.col("score_ft"),
            pl.col("score_ht"),
        ], separator=" ").alias("score")
    )

    return fixtures