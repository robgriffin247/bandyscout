import polars as pl
import streamlit as st

def table_height(data):
    if type(data)==int:
        return (data+1)*35+7
    else:
        return (data.shape[0]+1)*35+7
    
def standings_table(data):
    st.dataframe(data,
                 height=table_height(data))
    