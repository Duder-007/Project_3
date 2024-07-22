import streamlit as st
import pandas as pd
import altair as alt
import folium
from streamlit.components.v1 import html

# Function to generate the time series chart for selected names
def create_time_series(data, name):
    highlight = alt.selection(type='single', on='mouseover', fields=['Name'], nearest=True)
    base = alt.Chart(data).encode(
        x='Year:O',  # O for ordinal
        y='Count:Q',  # Q for quantitative
        color='Name:N'  # N for nominal
    ).properties(
        width=700,
        height=400
    )
    
    lines = base.mark_line().encode(
        size=alt.condition(~highlight, alt.value(1), alt.value(3))
    )
    points = base.mark_circle().encode(
        opacity=alt.condition(highlight, alt.value(1), alt.value(0))
    ).add_selection(highlight)

    return points + lines

def make_heatmap(df, input_y, input_x, input_color, input_color_theme):
    """
    Creates a heatmap chart using Altair with given dataframe and configuration.
    """
    heatmap = alt.Chart(df).mark_rect().encode(
        y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
        x=alt.X(f'{input_x}:O', axis=alt.Axis(title="State", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
        color=alt.Color(f'max({input_color}):Q', legend=None, scale=alt.Scale(scheme=input_color_theme)),
        stroke=alt.value('black'),
        strokeWidth=alt.value(0.25)
    ).properties(
        width=900,
        height=400
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    )
    return heatmap

# Set up the Streamlit page
st.set_page_config(
    page_title="US Baby Name Dashboard",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to style the sidebar and toggle button
st.markdown(
    """
    <style>
    button[data-testid="stSidebarNav"] { display: none; }
    #toggle-btn {
        position: fixed;
        top: 16px;
        left: 16px;
        width: 30px;
        height: 30px;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        z-index: 999;
    }
    .css-1lcbmhc.e1fqkh3o3 {
        transition: transform 0.3s ease;
        transform: translateX(-300px);
    }
    .css-1lcbmhc.e1fqkh3o3.expanded {
        transform: translateX(0);
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<button id="toggle-btn">☰</button>', unsafe_allow_html=True)

# JavaScript to handle the sidebar toggle
st.markdown(
    """
    <script>
    const toggleButton = document.getElementById('toggle-btn');
    const sidebar = document.querySelector('.css-1lcbmh3.e1fqkh3o3');
    toggleButton.addEventListener('click', () => {
        sidebar.classList.toggle('expanded');
    });
    </script>
    """,
    unsafe_allow_html=True
)

# Load the data
df_top_baby_names_yr = pd.read_csv("Baby_Names_Start/top_five_names_per_state.csv")
biblical_names_df = pd.read_csv("Baby_Names_Start/biblical_names.csv")

# Sidebar setup
with st.sidebar:
    st.title("US Baby Names Dashboard")
    year_list = list(df_top_baby_names_yr.Year.unique())
    selected_year = st.selectbox("Select a year", year_list)
    name_list = df_top_baby_names_yr.Name.unique().tolist()
    selected_names = st.multiselect("Select names", name_list)

# Data filtering
df_filtered = df_top_baby_names_yr[df_top_baby_names_yr["Year"] == selected_year]
if selected_names:
    df_filtered = df_filtered[df_filtered["Name"].isin(selected_names)]

# Layout for content
col1, col2 = st.columns([3, 1])
with col1:
    if selected_names:
        for name in selected_names:
            df_name = df_filtered[df_filtered['Name'] == name]
            time_series_chart = create_time_series(df_name, name)
            st.altair_chart(time_series_chart, use_container_width=True)

    heatmap_chart = make_heatmap(df_filtered, "Year", "State", "Count", "viridis")
    st.altair_chart(heatmap_chart, use_container_width=True)

with col2:
    st.title("Top 5 Names per State")
    df_top_five_filtered = df_top_baby_names_yr[df_top_baby_names_yr["Year"] == selected_year]
    state_list = df_top_five_filtered['State'].unique().tolist()
    selected_state = st.selectbox("Select a state", state_list)
    
    if selected_state:
        top_names = df_top_five_filtered[df_top_five_filtered['State'] == selected_state][['Name', 'Count']]
        names_chart = alt.Chart(top_names).mark_bar().encode(
            x='Name:N',
            y='Count:Q',
            color=alt.Color('Count:Q', scale=alt.Scale(scheme='redblue')),
            tooltip=['Name', 'Count']
        ).properties(height=300, width=400)
        st.altair_chart(names_chart, use_container_width=True)
