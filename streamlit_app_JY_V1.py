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
    st.write("")
    st.write("")

    df_selected_year = df_top_baby_names_yr[df_top_baby_names_yr.Year == selected_year]
    df_selected_year_sorted = df_selected_year.sort_values(by="Count", ascending=False)

# func to iterate off of selected year
def calculate_most_popular_names(selected_year):

    df_selected_year = df_top_baby_names_yr[df_top_baby_names_yr.Year == selected_year]
    popular_male_name = df_selected_year[df_selected_year["Gender"] == "M"]["Name"].value_counts().idxmax()
    popular_female_name = df_selected_year[df_selected_year["Gender"] == "F"]["Name"].value_counts().idxmax()

    # excess code, might be useful later:
    # state_most_popular_male = df_selected_year[(df_selected_year["Name"] == popular_male_name) & (df_selected_year["Gender"] == "M")]["State"].value_counts().idxmax()
    # state_most_popular_female = df_selected_year[(df_selected_year["Name"] == popular_female_name) & (df_selected_year["Gender"] == "F")]["State"].value_counts().idxmax()

    df_popular_male = df_selected_year[(df_selected_year["Name"] == popular_male_name) & (df_selected_year["Gender"] == "M")]
    df_popular_female = df_selected_year[(df_selected_year["Name"] == popular_female_name) & (df_selected_year["Gender"] == "F")]
    most_pop_state_male = df_popular_male.groupby("State")["Count"].sum().idxmax()
    most_pop_state_female = df_popular_female.groupby("State")["Count"].sum().idxmax()

    # writing in print statements when func is called to update output
    with st.sidebar:
        st.markdown(f"# Male Name")
        st.markdown(f"## State: {most_pop_state_male}")
        st.markdown(f"### {popular_male_name}")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.markdown(f"# Female Name")
        st.markdown(f"## State: {most_pop_state_female}")
        st.markdown(f"### {popular_female_name}")
        

        # st.write(f"Most popular Male name in {selected_year} was {popular_male_name}, in {most_pop_state_male}")
        # st.write(f"Most popular Female name in {selected_year} was {popular_female_name}, in {most_pop_state_female}")

# running func
calculate_most_popular_names(selected_year)

