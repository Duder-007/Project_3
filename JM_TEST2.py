import streamlit as st
import pandas as pd
import altair as alt
import folium
from streamlit.components.v1 import html

# We’re settin’ up the Streamlit page with a title (“US Baby Name Dashboard”), an icon (👶), and a wide layout.
st.set_page_config(
    page_title="US Baby Name Dashboard",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# The custom CSS hides the default sidebar toggle button and adds our own toggle button (that little “☰” symbol) for the sidebar.
custom_css = """
<style>
/* When that toggle button is clicked, it expands or collapses the sidebar. Just like pullin’ a lever on a train! */
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
const sidebar = document.querySelector('.css-1lcbmh3.e1fqkh3o3');
toggleButton.addEventListener('click', () => {
    sidebar.classList.toggle('expanded');
});
</script>
""", unsafe_allow_html=True)

alt.themes.enable("dark")

# We’re loadin’ in data frames from CSV files: df_top_baby_names_yr, biblical_names_df, and df_top_five_names_per_state
df_top_baby_names_yr = pd.read_csv("Baby_Names_Start/top_five_names_per_state.csv")
biblical_names_df = pd.read_csv("Baby_Names_Start/biblical_names.csv")
df_top_five_names_per_state = pd.read_csv("Baby_Names_Start/top_five_names_per_state.csv")

# The sidebar lets users select a year and multiple names.
with st.sidebar:
    st.title("US Baby Names Dashboard")
    
    year_list = list(df_top_baby_names_yr.Year.unique())
    selected_year = st.selectbox("Select a year", year_list)
    
    name_list = df_top_baby_names_yr.Name.unique().tolist()
    selected_names = st.multiselect("Select names", name_list)

# Based on their choices, we filter the df_filtered dataframe
df_filtered = df_top_baby_names_yr[df_top_baby_names_yr["Year"] == selected_year]
if selected_names:
    df_filtered = df_filtered[df_filtered["Name"].isin(selected_names)]

# We calculate the percentage of selected names that are biblical.
# If no names are selected, we set the percentage to 0.
biblical_names = set(biblical_names_df["Name"].str.upper())
selected_biblical_names = set(name.upper() for name in selected_names if name.upper() in biblical_names)
percent_biblical = len(selected_biblical_names) / len(selected_names) * 100 if selected_names else 0

# We create a donut chart showin’ the proportion of biblical names versus other names.
# The green slice represents biblical names, and the pink slice represents other names.
def make_donut_chart(percent):
    data = pd.DataFrame({
        'category': ['Biblical Names', 'Other Names'],
        'value': [percent, 100 - percent]
    })
    
    chart = alt.Chart(data).transform_calculate(
        angle="datum.value * 2 * PI / 100",
        color="datum.category"
    ).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="value", type="quantitative"),
        color=alt.Color(field="category", type="nominal", scale=alt.Scale(range=["#4CAF50", "#FFCCCB"])),
        tooltip=["category", "value"]
    ).properties(width=200, height=200)
    
    return chart

donut_chart = make_donut_chart(percent_biblical)

# We’ve got a function (make_heatmap) to create a heatmap
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

# It takes a dataframe, input columns, and color theme as parameters.
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

# Titel for map, be creative
st.title('Baby Names In the US and Data that defines them')

# Using a  two-column layout
col1, col2 = st.columns([3, 1])

# Left column (main content)
with col1:
    # Selection boxes for user inputs
    input_y = st.selectbox('Select Y axis', df_filtered.columns, index=df_filtered.columns.get_loc('Year'))
    input_x = st.selectbox('Select X axis', df_filtered.columns, index=df_filtered.columns.get_loc('State'))
    input_color = st.selectbox('Select Color axis', df_filtered.columns, index=df_filtered.columns.get_loc('Count'))
    input_color_theme = st.selectbox('Select Color Theme', ['viridis', 'inferno', 'magma', 'plasma', 'blueorange', 'redblue'])

    # Show the heatmap and display the colors
    heatmap_chart = make_heatmap(df_filtered, input_y, input_x, input_color, input_color_theme)
    st.altair_chart(heatmap_chart, use_container_width=True)

    # Map generation
    choropleth_map = make_choropleth(df_filtered)
    choropleth_map.save('choropleth_map.html')

    # Display the Folium map in Streamlit
    with open('choropleth_map.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    html(html_content, height=600)

    # Display the donut chart
    st.title("Percentage of Selected Biblical Names")
    st.altair_chart(donut_chart, use_container_width=True)

# Right column (Top 5 names per state dropdown)
with col2:
    st.title("Top 5 Names per State")
    df_top_five_filtered = df_top_five_names_per_state[df_top_five_names_per_state["Year"] == selected_year]
    
    state_list = df_top_five_filtered['State'].unique().tolist()
    selected_state = st.selectbox("Select a state", state_list)
    
    top_names = df_top_five_filtered[df_top_five_filtered['State'] == selected_state][['Name', 'Count']].reset_index(drop=True)
    st.table(top_names)
