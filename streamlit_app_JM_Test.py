import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px 

st.set_page_config(
    page_title="US Baby Name Dashboard",
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

# Heatmap function
def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
        y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
        x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
        color=alt.Color(f'max({input_color}):Q',
                        legend=None,
                        scale=alt.Scale(scheme=input_color_theme)),
        stroke=alt.value('black'),
        strokeWidth=alt.value(0.25),
    ).properties(
        width=900
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    )
    return heatmap

# Filter data based on selected year
filtered_df = df_top_baby_names_yr[df_top_baby_names_yr['Year'] == selected_year]

# Generate heatmap
heatmap = make_heatmap(filtered_df, 'Year', 'State', 'Count', selected_color_theme)

# Display heatmap in the main section
st.altair_chart(heatmap, use_container_width=True)
