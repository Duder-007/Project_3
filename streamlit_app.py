import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="US Baby Name Dashboard",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

# loading in data frames

df_top_baby_names_yr = pd.read_csv("Baby_Names_Start/top_five_names_per_state.csv")


# creating side bar with year list
with st.sidebar:
    st.title("US Baby Names Dashboard")
    
    year_list = list(df_top_baby_names_yr.Year.unique())
    selected_year = st.selectbox("Select a year", year_list)

    # df_selected_state = [df_top_baby_names_yr == selected_state]
    # df_selected_state_sorted = df_selected_state.sort_values(by="Count")

    # df_selected_state = [df_top_baby_names_yr == selected_state]
    # df_selected_state_sorted = df_selected_state.sort_values(by="Count")