import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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

# Load the data
@st.cache_data
def load_data():
    try:
        df_top_baby_names_yr = pd.read_csv("Baby_Names_Start/top_five_names_per_state.csv")
        biblical_names_df = pd.read_csv("Baby_Names_Start/biblical_names.csv")
        df_top_five_names_per_state = pd.read_csv("Baby_Names_Start/top_five_names_per_state.csv")
        top_baby_names_100yrs_df = pd.read_csv("Baby_Names_Start/2top_baby_names.csv")
        return df_top_baby_names_yr, biblical_names_df, df_top_five_names_per_state, top_baby_names_100yrs_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None

df_top_baby_names_yr, biblical_names_df, df_top_five_names_per_state, top_baby_names_100yrs_df = load_data()

if df_top_baby_names_yr is None or biblical_names_df is None or df_top_five_names_per_state is None or top_baby_names_100yrs_df is None:
    st.stop()

# Setting up the sidebar for selections
with st.sidebar:
    st.title("US Baby Names Dashboard")
    year_list = list(df_top_baby_names_yr.Year.unique())
    selected_year = st.selectbox("Select a year", year_list)

    # Filter names based on selected year
    filtered_names = df_top_baby_names_yr[df_top_baby_names_yr['Year'] == selected_year]['Name'].unique().tolist()

    selected_names = st.multiselect("Select names", filtered_names)
    color_themes = ["yellowgreen", "blues", "greens", "reds", "purples"]
    selected_color_theme = st.selectbox("Select Color Theme", color_themes, index=color_themes.index("yellowgreen"))

    # Top names from filtered list
    filtered_df_aggregated = df_top_baby_names_yr[df_top_baby_names_yr['Year'] == selected_year].groupby('Name')['Count'].sum().reset_index()
    filtered_df_aggregated = filtered_df_aggregated.sort_values(by='Count', ascending=False).head(5)
    top_5_filtered_names = filtered_df_aggregated['Name'].tolist()

    selected_top_name = st.selectbox("Select a top name to view trends", top_5_filtered_names, index=0)

# Filter data based on selections
df_filtered = df_top_baby_names_yr[df_top_baby_names_yr["Year"] == selected_year]
if selected_names:
    df_filtered = df_filtered[df_filtered["Name"].isin(selected_names)]

# Calculating the percentage of biblical names
selected_biblical_names = set(df_filtered['Name']).intersection(set(biblical_names_df['Name']))
percent_biblical = len(selected_biblical_names) / len(set(df_filtered['Name'])) * 100 if df_filtered['Name'].any() else 0

# Helper function to create a donut chart
def make_donut_chart(percent, color_theme):
    color_dict = {
        "yellowgreen": ["#4CAF50", "#FFCCCB"],
        "blues": ["#1f77b4", "#aec7e8"],
        "greens": ["#2ca02c", "#98df8a"],
        "reds": ["#d62728", "#ff9896"],
        "purples": ["#9467bd", "#c5b0d5"]
    }
    fig = go.Figure(data=[go.Pie(labels=['Biblical Names', 'Other Names'], values=[percent, 100 - percent], hole=.4)])
    fig.update_traces(marker=dict(colors=color_dict[color_theme]))
    return fig

# Helper function to create a heatmap using Plotly
def make_heatmap(df, input_y, input_x, input_color, input_color_theme):
    heatmap = px.density_heatmap(df, x=input_x, y=input_y, z=input_color, color_continuous_scale=input_color_theme)
    return heatmap

# Helper function to create a choropleth map
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
    st.plotly_chart(heatmap_chart, use_container_width=True)

    # Generate and display the choropleth map
    choropleth_map = make_choropleth(df_filtered)
    choropleth_map.save('choropleth_map.html')
    with open('choropleth_map.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    html(html_content, height=600)

    # Display the donut chart
    st.title("Percentage of Selected Biblical Names")
    donut_chart = make_donut_chart(percent_biblical, selected_color_theme)
    st.plotly_chart(donut_chart, use_container_width=True)

    # Most popular name over the last century
    st.title("Most Popular Name Over Last Century")
    most_popular_male_name = top_baby_names_100yrs_df["Male Names"].value_counts().idxmax()
    most_popular_female_name = top_baby_names_100yrs_df["Female Names"].value_counts().idxmax()
    st.markdown(f"## Male Name")
    st.markdown(f"### {most_popular_male_name}")
    st.write("")
    st.markdown(f"## Female Name")
    st.markdown(f"### {most_popular_female_name}")

# Right column
with col2:
    st.title("Top 5 Names per State")
    df_top_five_filtered = df_top_five_names_per_state[df_top_five_names_per_state["Year"] == selected_year]
    
    state_list = df_top_five_filtered['State'].unique().tolist()
    selected_state = st.selectbox("Select a state", state_list)
    
    if selected_state:
        top_names = df_top_five_filtered[df_top_five_filtered['State'] == selected_state][['Name', 'Count']]
        names_chart = px.bar(top_names, x='Name', y='Count', color='Count', color_continuous_scale=input_color_theme)
        st.plotly_chart(names_chart, use_container_width=True)

    # Top baby names by state
    top_names_states = pd.read_csv("Baby_Names_Start/top_five_names_per_state.csv")
    top_names_state_df = top_names_states.groupby(["State", "Gender", "Name"])["Count"].sum().reset_index()
    top_names_state_df = top_names_state_df.sort_values("Count", ascending=False).groupby(["State", "Gender"]).head(5)
    top_names_state_df = top_names_state_df.sort_values("State")
    st.title("Top Baby Names by State")
    st.write("Top baby names (top 5 for each gender) in each state:")
    st.dataframe(top_names_state_df)
    state_filter = st.selectbox("Select a state to filter:", top_names_state_df["State"].unique())
    filtered_df = top_names_state_df[top_names_state_df["State"] == state_filter]
    st.write(f"Top baby names in {state_filter}:")
    st.dataframe(filtered_df)

# Yearly trends for the selected top name
df_yearly_trends = df_top_baby_names_yr[df_top_baby_names_yr['Name'] == selected_top_name]
total_occurrences = df_yearly_trends['Count'].sum()
st.title(f'Yearly Trends for the Name {selected_top_name}')
st.write(f"The name **{selected_top_name}** has a total of **{total_occurrences}** occurrences over the last 100 years.")
yearly_trends_chart = px.line(df_yearly_trends, x='Year', y='Count', color='Gender', title=f"Yearly Trends of the Name {selected_top_name}")
st.plotly_chart(yearly_trends_chart, use_container_width=True)

# Display male and female names with the same name
st.title("Males and Females with the Same Name")
same_name_df = df_top_baby_names_yr.groupby(['Year', 'Name', 'Gender'])['Count'].sum().reset_index()
same_name_df = same_name_df.pivot_table(index=['Year', 'Name'], columns='Gender', values='Count').reset_index()
same_name_df = same_name_df.dropna().sort_values(by='Year')
st.dataframe(same_name_df)

# Display the total number of babies given any male/female name in the selected year
selected_name = st.selectbox("Select a name to see yearly counts", filtered_names)
name_yearly_counts = df_top_baby_names_yr[df_top_baby_names_yr['Name'] == selected_name]
yearly_counts_chart = px.line(name_yearly_counts, x='Year', y='Count', color='Gender', title=f"Yearly Counts for the Name {selected_name} by Gender")
st.plotly_chart(yearly_counts_chart, use_container_width=True)
