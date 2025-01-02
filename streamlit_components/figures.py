import duckdb
import plotly.express as px

win_color="#78c975"
draw_color="#e6f1f5"
loss_color="#fa8578"

def results_pie(data):
    
    with duckdb.connect() as con:
        counts = con.sql('select result_long, result, count(result_long) as n from data group by result_long, result, points order by points desc').pl()

    fig = px.pie(counts, values='n', names='result', hole=0.5, height=300,
                 color='result',
                 category_orders={"result":["W", "D", "L"]},
                 color_discrete_map={"W": win_color, "D": draw_color, "L": loss_color})
                        
    fig.update_traces(customdata=counts["result_long"], 
                      textinfo="label",
                      hovertemplate="%{customdata} (%{value}; %{percent})<extra></extra>")
    fig.update_layout(showlegend=False)
    fig.update_layout(
        margin={'t':0,'l':0,'b':0,'r':0}
    )

    return fig


def form_bar(team_results):
    with duckdb.connect() as con:
        df = con.sql('''
            select opponent, round, concat(cast(round as string), ': ', opponent_abb, ' (', home_away, ')') as xlab, result, result_long, concat(scored, '-', conceded) as score, home_away, opponent, scored as n, 'Scored' as Goals
            from team_results
            union all
            select opponent, round, concat(cast(round as string), ': ', opponent_abb, ' (', home_away, ')') as xlab, result, result_long, concat(scored, '-', conceded) as score, home_away, opponent, conceded as n, 'Conceded' as Goals
            from team_results
        ''').pl()
    
    fig = px.bar(df, x="xlab", y="n", color="Goals", barmode="group", height=300)
    fig.update_traces(customdata=df["result_long", "opponent", "home_away", "score"], 
                      hovertemplate="<b>%{customdata[1]}</b><br>%{customdata[3]} %{customdata[0]} (%{customdata[2]})" + "<extra></extra>")
    fig.update_xaxes(range=[df.shape[0]/2-7.15, df.shape[0]/2-0.5])
    fig.update_layout(legend=dict(title=None, orientation="h", yanchor="bottom", y=0.95, xanchor="right", x=1),
                      xaxis_title=None, yaxis_title=None)
    fig.update_layout(
        margin={'t':0,'l':0,'b':0,'r':0}
    )

    return fig