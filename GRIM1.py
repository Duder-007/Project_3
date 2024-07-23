import streamlit as st
import pandas as pd
import altair as alt
import folium
from streamlit.components.v1 import html

# Set up the Streamlit dashboard
st.set_page_config(
    page_title="US Baby Name Dashboard",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for the sidebar toggle button
custom_css = """
<style>
button[data-testid="stSidebarNav"] { display: none; }

#toggle-btn {
    position: fixed;
    top: 16px; left: 16px;
    width: 30px; height: 30px;
    background-color: #4CAF50; color: white;
    border: none; border-radius: 5px;
    cursor: pointer; z-index: 999;
}

.css-1lcbmhc.e1fqkh3o3 {
    transition: transform 0.3s ease;
    transform: translateX(-300px);
}

.css-1lcbmhc.e1fqkh3o3.expanded {
    transform: translateX(0);
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
st.markdown('<button id="toggle-btn">☰</button>', unsafe_allow_html=True)

# JavaScript for the sidebar toggle button
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

# Load the data
@st.cache_data
def load_data():
    try:
        df_top_baby_names_yr = pd.read_csv("Baby_Names_Start/top_five_names_per_state.csv")
        biblical_names_df = pd.read_csv("Baby_Names_Start/biblical_names.csv")
        df_top_five_names_per_state = pd.read_csv("Baby_Names_Start/top_five_names_per_state.csv")
        return df_top_baby_names_yr, biblical_names_df, df_top_five_names_per_state
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None

df_top_baby_names_yr, biblical_names_df, df_top_five_names_per_state = load_data()

if df_top_baby_names_yr is None or biblical_names_df is None or df_top_five_names_per_state is None:
    st.stop()

# Sidebar selections
with st.sidebar:
    st.title("US Baby Names Dashboard")
    year_list = list(df_top_baby_names_yr.Year.unique())
    selected_year = st.selectbox("Select a year", year_list)
    name_list = df_top_baby_names_yr.Name.unique().tolist()
    selected_names = st.multiselect("Select names", name_list)
    color_themes = ["yellowgreen", "blues", "greens", "reds", "purples"]
    selected_color_theme = st.selectbox("Select Color Theme", color_themes, index=color_themes.index("yellowgreen"))

# Filter data
df_filtered = df_top_baby_names_yr[df_top_baby_names_yr["Year"] == selected_year]
if selected_names:
    df_filtered = df_filtered[df_filtered["Name"].isin(selected_names)]

# Calculate the percentage of biblical names
selected_biblical_names = set(df_filtered['Name']).intersection(set(biblical_names_df['Name']))
percent_biblical = len(selected_biblical_names) / len(set(df_filtered['Name'])) * 100 if df_filtered['Name'].any() else 0

# Create a donut chart
def make_donut_chart(percent, color_theme):
    color_dict = {
        "yellowgreen": ["#4CAF50", "#FFCCCB"],
        "blues": ["#1f77b4", "#aec7e8"],
        "greens": ["#2ca02c", "#98df8a"],
        "reds": ["#d62728", "#ff9896"],
        "purples": ["#9467bd", "#c5b0d5"]
    }
    data = pd.DataFrame({
        'category': ['Biblical Names', 'Other Names'],
        'value': [percent, 100 - percent]
    })
    chart = alt.Chart(data).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="value", type="quantitative"),
        color=alt.Color(field="category", type="nominal", scale=alt.Scale(range=color_dict[color_theme])),
        tooltip=["category", "value"]
    ).properties(width=200, height=200)
    return chart

donut_chart = make_donut_chart(percent_biblical, selected_color_theme)

# Create a heatmap
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

# Create a choropleth map
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

# Display the title
st.title('Baby Names In the US and Data that defines them')

# Two-column layout
col1, col2 = st.columns([3, 1])

# Left column
with col1:
    input_y = st.selectbox('Select Y axis', df_filtered.columns, index=df_filtered.columns.get_loc('Year'))
    input_x = st.selectbox('Select X axis', df_filtered.columns, index=df_filtered.columns.get_loc('State'))
    input_color = st.selectbox('Select Color axis', df_filtered.columns, index=df_filtered.columns.get_loc('Count'))
    input_color_theme = selected_color_theme

    # Display the heatmap
    heatmap_chart = make_heatmap(df_filtered, input_y, input_x, input_color, input_color_theme)
    st.altair_chart(heatmap_chart, use_container_width=True)

    # Generate and display the choropleth map
    choropleth_map = make_choropleth(df_filtered)
    choropleth_map.save('choropleth_map.html')
    with open('choropleth_map.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    html(html_content, height=600)

    # Display the donut chart
    st.title("Percentage of Selected Biblical Names")
    st.altair_chart(donut_chart, use_container_width=True)

# Right column
with col2:
    st.title("Top 5 Names per State")
    df_top_five_filtered = df_top_five_names_per_state[df_top_five_names_per_state["Year"] == selected_year]
    
    state_list = df_top_five_filtered['State'].unique().tolist()
    selected_state = st.selectbox("Select a state", state_list)
    
    if selected_state:
        top_names = df_top_five_filtered[df_top_five_filtered['State'] == selected_state][['Name', 'Count']]
        names_chart = alt.Chart(top_names).mark_bar().encode(
            x='Name:N',
            y='Count:Q',
            color=alt.Color('Count:Q', scale=alt.Scale(scheme=input_color_theme)),
            tooltip=['Name', 'Count']
        ).properties(height=300, width=400)
        st.altair_chart(names_chart, use_container_width=True)
# Load the data
@st.cache_data
def load_data():
    try:
        df_top_baby_names_yr = pd.read_csv("Baby_Names_Start/top_five_names_per_state.csv")
        return df_top_baby_names_yr
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df_top_baby_names_yr = load_data()

if df_top_baby_names_yr is None:
    st.stop()

# Aggregate data over the last 100 years
import streamlit as st
import pandas as pd
import altair as alt

# Load the data
@st.cache_data
def load_data():
    try:
        df_top_baby_names_yr = pd.read_csv("Baby_Names_Start/top_five_names_per_state.csv")
        return df_top_baby_names_yr
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df_top_baby_names_yr = load_data()

if df_top_baby_names_yr is None:
    st.stop()

# Aggregate data over the last 100 years
df_aggregated = df_top_baby_names_yr.groupby('Name')['Count'].sum().reset_index()
df_aggregated = df_aggregated.sort_values(by='Count', ascending=False).head(5)

# Get the top 5 names
top_5_names = df_aggregated['Name'].tolist()
default_name = top_5_names[0]

# Sidebar for selecting a name
st.sidebar.title("Top 5 Baby Names")
selected_name = st.sidebar.selectbox("Select a name", top_5_names, index=0)

# Yearly trends for the selected name
df_yearly_trends = df_top_baby_names_yr[df_top_baby_names_yr['Name'] == selected_name]

# Display the selected name and its total occurrences
total_occurrences = df_yearly_trends['Count'].sum()
st.title(f'Yearly Trends for the Name {selected_name}')
st.write(f"The name **{selected_name}** has a total of **{total_occurrences}** occurrences over the last 100 years.")

# Plot the yearly trends
yearly_trends_chart = alt.Chart(df_yearly_trends).mark_line(point=True).encode(
    x='Year:O',
    y='Count:Q',
    tooltip=['Year', 'Count']
).properties(
    width=800,
    height=400,
    title=f"Yearly Trends of the Name {selected_name}"
)

st.altair_chart(yearly_trends_chart, use_container_width=True)
