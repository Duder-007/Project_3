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

    df_selected_year = df_top_baby_names_yr[df_top_baby_names_yr.Year == selected_year]
    df_selected_year_sorted = df_selected_year.sort_values(by="Count", ascending=False)


def calculate_most_popular_names(selected_year):
    df_selected_year = df_top_baby_names_yr[df_top_baby_names_yr.Year == selected_year]
    popular_five_male_name = df_selected_year[df_selected_year["Gender"] == "M"]["Name"].value_counts().idxmax()
    popular_five_female_name = df_selected_year[df_selected_year["Gender"] == "F"]["Name"].value_counts().idxmax()
    state_most_popular_male = df_selected_year[(df_selected_year["Name"] == popular_five_male_name) & (df_selected_year["Gender"] == "M")]["State"].value_counts().idxmax[0]
    state_most_popular_female = df_selected_year[(df_selected_year["Name"] == popular_five_female_name) & (df_selected_year["Gender"] == "F")]["State"].value_counts().idxmax[0]

    # print the results
    with st.sidebar:
        st.write(f"Most popular Male name in {selected_year} was {popular_five_male_name}, in {state_most_popular_male}")
        st.write(f"Most popular Female name in {selected_year} was {popular_five_female_name}, in {state_most_popular_female}")

calculate_most_popular_names(selected_year)

