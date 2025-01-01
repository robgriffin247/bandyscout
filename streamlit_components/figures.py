import duckdb
import plotly.express as px

def results_pie(data):
    
    with duckdb.connect() as con:
        counts = con.sql('select result_long, count(result_long) as n from data group by result_long, points order by points desc').pl()

    fig = px.pie(counts, values='n', names='result_long', hole=0.75,
                        category_orders={"result_long":["Win", "Draw", "Loss"]},
                        color_discrete_map={'Win':'#70997b', 'Draw':'#fc90a2', 'Loss':'#c0becc'})
                        
    fig.update_traces(textposition='inside', textinfo='value', hovertemplate='<i>%{label}</i>: %{value} (%{percent})')

    return fig


def results_bar(data):

    with duckdb.connect() as con:
        counts = con.sql('select result_long, count(result_long) as n from data group by result_long, points order by points desc').pl()

    fig = px.bar(counts, x="result_long", y="n", height=300)
    
    fig.update_layout(xaxis_title=None, yaxis_title=None)
    fig.update_traces(hovertemplate='<i>%{label}</i>: %{value}')

    return fig