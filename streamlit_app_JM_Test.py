import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px 

st.set_page_config(
    page_title="USSR Baby Name Dashboard",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enabling Altair's dark theme
alt.themes.enable("dark")

# Loading data frames
try:
    df_top_baby_names_yr = pd.read_csv("Baby_Names_Start/top_five_names_per_state.csv")
except FileNotFoundError:
    st.error("The data file was not found. Please ensure the file path is correct.")
    st.stop()

# Creating sidebar with year list
with st.sidebar:
    st.title("US Baby Names Dashboard")

    if df_top_baby_names_yr.empty:
        st.warning("The data frame is empty. Please check the data file.")
    else:
        year_list = list(df_top_baby_names_yr.Year.unique())
        if not year_list:
            st.warning("No unique years found in the data.")
        else:
            selected_year = st.selectbox("Select a year", year_list)
            
            color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
            selected_color_theme = st.selectbox('Select a color theme', color_theme_list)

# Continue with the rest of the dashboard implementation
# Example: Visualizing top baby names for the selected year and color theme
# ...


    # df_selected_state = [df_top_baby_names_yr == selected_state]
    # df_selected_state_sorted = df_selected_state.sort_values(by="Count")

    # df_selected_state = [df_top_baby_names_yr == selected_state]
    # df_selected_state_sorted = df_selected_state.sort_values(by="Count")
    