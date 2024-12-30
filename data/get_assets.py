import duckdb
import polars as pl
import streamlit as st
from data.get_matches import get_matches

def get_results():
    df = get_matches(st.secrets["sportsradar"]["api_key"])
    with duckdb.connect() as con:
        df = con.sql('''
                with source as (select * from df where status='closed'),
                    home as (select date, round, TRUE as home, home as team, away as opponent, home_ft as scored, away_ft as conceded from source),
                    away as (select date, round, FALSE as home, away as team, home as opponent, away_ft as scored, home_ft as conceded from source),
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
                        case when scored>conceded then 'win'
                            when scored=conceded then 'draw'
                            when scored<conceded then 'loss' 
                            else NULL end as result, 
                        case when scored>conceded then 2
                            when scored=conceded then 1
                            when scored<conceded then 0 
                            else NULL end as points
                        from fix_teamnames)
                select * from add_result order by date, team
                ''').pl() 
        
    return df


def get_standings(team_results):
    with duckdb.connect() as con:
        df = con.sql('''
                with source as (select * from team_results),
                     base_table as (select
                        team,
                        count(*) as matches,
                        sum(points) as points,
                        sum(case when result='win' then 1 else 0 end) as wins, 
                        sum(case when result='draw' then 1 else 0 end) as draws, 
                        sum(case when result='loss  ' then 1 else 0 end) as losses, 
                        sum(scored) as scored,
                        sum(conceded) as conceded,
                        sum(scored)-sum(conceded) as difference
                     from source
                     group by team
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