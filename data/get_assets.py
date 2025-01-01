import httpx
import json
import duckdb
import polars as pl
import streamlit as st


# Gets data from sportsradar into a table of matches (1 match per row)
# Records date, round, home team, away team, match status, home and away ft and ht goals scored
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
         "home_abb": event["sport_event"]["competitors"][0]["abbreviation"],
         "away": event["sport_event"]["competitors"][1]["name"],
         "away_abb": event["sport_event"]["competitors"][1]["abbreviation"],
         "status": event["sport_event_status"]["status"],
         "details": event["sport_event_status"]
        }
        for event in summaries])

    selected_data_scores = []
    for event in selected_data:
        if event["status"]=="closed":
            event["home_ht"]=event["details"]["period_scores"][0]["home_score"]
            event["home_ft"]=event["details"]["home_score"]
            event["away_ht"]=event["details"]["period_scores"][0]["away_score"]
            event["away_ft"]=event["details"]["away_score"]
            pass
        else:
            pass
        event.pop("details")
        selected_data_scores.append(event)

    data = pl.DataFrame(selected_data_scores)

    return data

# Takes the matches dataframe into one row per team per match (2 rows per match, one for home team, one for away team)
def get_results(data):
    with duckdb.connect() as con:
        df = con.sql('''
                with source as (select * from data where status='closed'),
                    home as (
                        select 
                            date, 
                            round, 
                            'H' as home_away, 
                            home as team, 
                            home_abb as team_abb, 
                            away as opponent, 
                            away_abb as opponent_abb,
                            home_ft as scored, 
                            away_ft as conceded,
                            home_ht as scored_ht, 
                            away_ht as conceded_ht 
                        from source),
                    away as (
                        select 
                            date, 
                            round, 
                            'A' as home_away, 
                            away as team, 
                            away_abb as team_abb, 
                            home as opponent, 
                            home_abb as opponent_abb,
                            away_ft as scored, 
                            home_ft as conceded,
                            away_ht as scored_ht, 
                            home_ht as conceded_ht 
                        from source),
                    all_matches as (select * from home union all select * from away),
                    fix_teamnames as (
                        select * exclude(team, opponent),
                            case when team='Bollnas GIF' then 'Bollnäs GIF'
                                 when team='Broberg/Soderhamn BS' then 'Broberg/Söderhamn BS'
                                 when team='Frillesaas BK' then 'Frillesås BK'
                                 when team='IFK Vanersborg' then 'IFK Vänersborg'
                                 when team='Villa-Lidkoping BK' then 'Villa-Lidköping BK'
                                 when team='Vasteraas SK' then 'Västerås SK'
                                 when team='Aby/Tjureda IF' then 'Åby/Tjureda IF'
                                 else team end as team,
                            case when opponent='Bollnas GIF' then 'Bollnäs GIF'
                                 when opponent='Broberg/Soderhamn BS' then 'Broberg/Söderhamn BS'
                                 when opponent='Frillesaas BK' then 'Frillesås BK'
                                 when opponent='IFK Vanersborg' then 'IFK Vänersborg'
                                 when opponent='Villa-Lidkoping BK' then 'Villa-Lidköping BK'
                                 when opponent='Vasteraas SK' then 'Västerås SK'
                                 when opponent='Aby/Tjureda IF' then 'Åby/Tjureda IF'
                                 else opponent end as opponent,
                        from all_matches
                    ),
                    add_result as (select *, 
                        case when scored>conceded then 'W'
                            when scored=conceded then 'D'
                            when scored<conceded then 'L' 
                            else NULL end as result, 
                        case when scored>conceded then 2
                            when scored=conceded then 1
                            when scored<conceded then 0 
                            else NULL end as points
                        from fix_teamnames),
                     add_formatted as (
                        select *, 
                            concat(scored, '-', conceded, '  (', scored_ht, '-', conceded_ht, ')') as score_formatted
                        from add_result
                     )
                select * from add_formatted order by date, team
                ''').pl() 
        
    return df


def get_standings(team_results):
    with duckdb.connect() as con:
        df = con.sql('''
                with source as (select * from team_results),
                     base_table as (select
                        team,
                        team_abb,
                        count(*) as matches,
                        sum(points) as points,
                        sum(case when result='win' then 1 else 0 end) as wins, 
                        sum(case when result='draw' then 1 else 0 end) as draws, 
                        sum(case when result='loss  ' then 1 else 0 end) as losses, 
                        sum(scored) as scored,
                        sum(conceded) as conceded,
                        sum(scored)-sum(conceded) as difference
                     from source
                     group by team, team_abb
                     ),
                     sort_table as (
                        select * from base_table order by points desc, difference desc, scored desc
                     ),
                     add_rank as (
                        select 
                            row_number() over (order by points desc, difference desc, scored desc) as rank, 
                            * 
                        from sort_table 
                     )
                    select * from add_rank
                ''').pl()
        
        return df