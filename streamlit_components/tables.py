import polars as pl
import streamlit as st
import duckdb

win_color="#78c975"
draw_color="#e6f1f5"
loss_color="#fa8578"


def table_height(data):
    if type(data)==int:
        return (data+1)*35+7
    else:
        return (data.shape[0]+1)*35+7
    

def standings_table(data, team=None, location=None, container=None):
    if location=="All":
        pass
    if location=="Home":
        data=data.filter(pl.col("home_away")=="H")
    if location=="Away":
        data=data.filter(pl.col("home_away")=="A")

    with duckdb.connect() as con:
        data = con.sql('''
                with source as (select * from data),
                    base_table as (select
                        team,
                        team_abb,
                        count(*) as matches,
                        sum(points) as points,
                        sum(case when result='W' then 1 else 0 end) as wins, 
                        sum(case when result='D' then 1 else 0 end) as draws, 
                        sum(case when result='L' then 1 else 0 end) as losses, 
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
        
    if team==None:
        pass
    else:
        team_rank = data.row(by_predicate=(pl.col("team") == team), named=True)["rank"]-1
        if team_rank==0:
            ranks = [0, 1, 2]
        elif team_rank==13:
            ranks=[11,12,13]
        else:
            ranks=[team_rank-1, team_rank, team_rank+1]
        data = data[ranks]

    if container==None:
        container = st.container()
        
    container.dataframe(data[["rank", "team", "matches", "points", "wins", "draws", "losses", "scored", "conceded", "difference"]],
                 height=table_height(data),
                 use_container_width=True,
                 column_config={
                     "rank":st.column_config.NumberColumn("#"),
                     "team":st.column_config.TextColumn("Team", width="medium"),
                     "matches":st.column_config.NumberColumn("M"),
                     "points":st.column_config.NumberColumn("P"),
                     "wins":st.column_config.NumberColumn("W"),
                     "draws":st.column_config.NumberColumn("D"),
                     "losses":st.column_config.NumberColumn("L"),
                     "scored":st.column_config.NumberColumn("GF"),
                     "conceded":st.column_config.NumberColumn("GA"),
                     "difference":st.column_config.NumberColumn("GD"),
                 })



