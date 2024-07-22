import streamlit as st
import pandas as pd
import altair as alt
import folium
from streamlit.components.v1 import html

# Setting up the page layout
st.set_page_config(
    page_title="US Baby Name Dashboard",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for slide-in sidebar
custom_css = """
<style>
/* Hide default Streamlit sidebar toggle button */
button[data-testid="stSidebarNav"] { display: none; }

/* Create a new toggle button */
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

/* Sidebar styles */
.css-1lcbmhc.e1fqkh3o3 {
    transition: transform 0.3s ease;
    transform: translateX(-300px);
}

.css-1lcbmhc.e1fqkh3o3.expanded {
    transform: translateX(0);
}
</style>
"""

# Inject custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Sidebar toggle button
st.markdown('<button id="toggle-btn">☰</button>', unsafe_allow_html=True)

# JavaScript to toggle the sidebar
st.markdown("""
<script>
const toggleButton = document.getElementById('toggle-btn');
const sidebar = document.querySelector('.css-1lcbmhc.e1fqkh3o3');
toggleButton.addEventListener('click', () => {
    sidebar.classList.toggle('expanded');
});
</script>
""", unsafe_allow_html=True)

alt.themes.enable("dark")

# Loading in data frames
df_top_baby_names_yr = pd.read_csv("Baby_Names_Start/top_five_names_per_state.csv")

# Creating sidebar with year list and name filter
with st.sidebar:
    st.title("US Baby Names Dashboard")
    
    year_list = list(df_top_baby_names_yr.Year.unique())
    selected_year = st.selectbox("Select a year", year_list)
    
    name_list = df_top_baby_names_yr.Name.unique().tolist()
    selected_names = st.multiselect("Select names", name_list)

# Filter the dataframe based on the selected year and names
df_filtered = df_top_baby_names_yr[df_top_baby_names_yr["Year"] == selected_year]
if selected_names:
    df_filtered = df_filtered[df_filtered["Name"].isin(selected_names)]

# Function to create heatmap
def make_heatmap(df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(df).mark_rect().encode(
        y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
        x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
        color=alt.Color(f'max({input_color}):Q', legend=None, scale=alt.Scale(scheme=input_color_theme)),
        stroke=alt.value('black'),
        strokeWidth=alt.value(0.25),
    ).properties(width=900).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    )
    return heatmap

# Function to create choropleth map
def make_choropleth(df):
    df['State'] = df['State'].apply(lambda x: x.upper())
    
    us_states_url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json'
    
    state_data = df.groupby('State')['Count'].sum().reset_index()
    
    m = folium.Map(location=[37.8, -96], zoom_start=4)
    
    folium.Choropleth(
        geo_data=us_states_url,
        name='choropleth',
        data=state_data,
        columns=['State', 'Count'],
        key_on='feature.id',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Total Count'
    ).add_to(m)
    
    folium.LayerControl().add_to(m)
    
    return m

# Streamlit UI elements
st.title('Baby Names Heatmap and Choropleth Map')

# Selection boxes for user inputs
input_y = st.selectbox('Select Y axis', df_filtered.columns, index=df_filtered.columns.get_loc('Year'))
input_x = st.selectbox('Select X axis', df_filtered.columns, index=df_filtered.columns.get_loc('State'))
input_color = st.selectbox('Select Color axis', df_filtered.columns, index=df_filtered.columns.get_loc('Count'))
input_color_theme = st.selectbox('Select Color Theme', ['viridis', 'inferno', 'magma', 'plasma', 'blueorange', 'redblue'])

# Generate and display heatmap
heatmap_chart = make_heatmap(df_filtered, input_y, input_x, input_color, input_color_theme)
st.altair_chart(heatmap_chart, use_container_width=True)

# Generate and display Choropleth map
choropleth_map = make_choropleth(df_filtered)
choropleth_map.save('choropleth_map.html')

# Display the Folium map in Streamlit
with open('choropleth_map.html', 'r', encoding='utf-8') as f:
    html_content = f.read()
html(html_content, height=600)
