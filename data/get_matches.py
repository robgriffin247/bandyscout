import httpx
import json
import polars as pl

def get_matches(api_key):

    url = f"https://api.sportradar.com/bandy/production/v2/en/seasons/sr:season:121299/summaries.json?api_key={api_key}"
        
    response = httpx.get(url)
    
    response.raise_for_status()

    content = json.loads(response.content)
    
    summaries = content["summaries"]

    selected_data = ([
        {"date": event["sport_event"]["start_time"],
         "round": event["sport_event"]["sport_event_context"]["round"]["number"],
         "home": event["sport_event"]["competitors"][0]["name"],
         "away": event["sport_event"]["competitors"][1]["name"],
         "status": event["sport_event_status"]["status"],
         "details": event["sport_event_status"]
        }
        for event in summaries])

    selected_data_scores = []
    for event in selected_data:
        if event["status"]=="closed":
            event["home_ht"]=f'({event["details"]["period_scores"][0]["home_score"]}'
            event["home_ft"]=event["details"]["home_score"]
            event["away_ht"]=f'{event["details"]["period_scores"][0]["away_score"]})'
            event["away_ft"]=event["details"]["away_score"]
            pass
        else:
            pass
        event.pop("details")
        selected_data_scores.append(event)

    data = pl.DataFrame(selected_data_scores)

    return data

