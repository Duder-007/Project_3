import streamlit as st
import pandas as pd
import altair as alt
import folium
from streamlit.components.v1 import html
import plotly.express as px

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
        top_baby_names_100yrs_df = pd.read_csv("Baby_Names_Start/2top_baby_names.csv")
        return df_top_baby_names_yr, biblical_names_df, df_top_five_names_per_state, top_baby_names_100yrs_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None

df_top_baby_names_yr, biblical_names_df, df_top_five_names_per_state, top_baby_names_100yrs_df = load_data()

if df_top_baby_names_yr is None or biblical_names_df is None or df_top_five_names_per_state is None or top_baby_names_100yrs_df is None:
    st.stop()

# Aggregate data over the last 100 years
df_aggregated = df_top_baby_names_yr.groupby('Name')['Count'].sum().reset_index()
df_aggregated = df_aggregated.sort_values(by='Count', ascending=False).head(5)

# Get the top 5 names
top_5_names = df_aggregated['Name'].tolist()

# Setting up the sidebar for selections
with st.sidebar:
    st.title("US Baby Names Dashboard")
    year_list = list(df_top_baby_names_yr.Year.unique())
    selected_year = st.selectbox("Select a year", year_list)
    name_list = df_top_baby_names_yr.Name.unique().tolist()
    selected_names = st.multiselect("Select names", name_list)
    color_themes = ["yellowgreen", "blues", "greens", "reds", "purples"]
    selected_color_theme = st.selectbox("Select Color Theme", color_themes, index=color_themes.index("yellowgreen"))
    selected_top_name = st.selectbox("Select a top name to view trends", top_5_names, index=0)

# Filter data based on selections
df_filtered = df_top_baby_names_yr[df_top_baby_names_yr["Year"] == selected_year]
if selected_names:
    df_filtered = df_filtered[df_filtered["Name"].isin(selected_names)]

# Calculating the percentage of biblical names
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
        names_chart = alt.Chart(top_names).mark_bar().encode(
            x='Name:N',
            y='Count:Q',
            color=alt.Color('Count:Q', scale=alt.Scale(scheme=input_color_theme)),
            tooltip=['Name', 'Count']
        ).properties(height=300, width=400)
        st.altair_chart(names_chart, use_container_width=True)

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
yearly_trends_chart = alt.Chart(df_yearly_trends).mark_line(point=True).encode(
    x='Year:O',
    y='Count:Q',
    tooltip=['Year', 'Count']
).properties(
    width=800,
    height=400,
    title=f"Yearly Trends of the Name {selected_top_name}"
)
st.altair_chart(yearly_trends_chart, use_container_width=True)

# Unisex names
df = pd.read_csv("Baby_Names_Start/usa_baby_names.csv")
# Find names that are both male and female
def find_unisex_names(df):
    male_names = df[df["sex"] == "M"]["first_name"].unique()
    female_names = df[df["sex"] == "F"]["first_name"].unique()
    unisex_names = list(set(male_names) & set(female_names))
    return unisex_names
unisex_names = find_unisex_names(df)

def find_years_for_unisex_names(df, unisex_names):
    years_for_unisex_names = {}
    for name in unisex_names:
        years = df[df["first_name"] == name]["year"].unique()
        years_for_unisex_names[name] = ', '.join(map(str, years))
    return years_for_unisex_names
years_for_unisex_names = find_years_for_unisex_names(df, unisex_names)

# Display the result
# st.write('Unisex Names and the Years They Appeared:', years_for_unisex_names)

markdown_text = '## Unisex Names and the Years They Appeared:\n'
for name, years in years_for_unisex_names.items():
    markdown_text += f'- **{name}**: {years}\n'
st.markdown(markdown_text)

# Load data function, pilgrim. Gotta get those CSV files read into DataFrames.
def load_data():
    baby_names_df = pd.read_csv('Baby_Names_Start/top_baby_names.csv')
    actors_df = pd.read_csv('Baby_Names_Start/AList.csv')
    return baby_names_df, actors_df

# Get decade from a year, partner. We're rounding down to the nearest decade.
def get_decade(year):
    return (year // 10) * 10

# Process data function, amigo. This one's the big kahuna.
def process_data(baby_names_df, actors_df):
    # Extract unique first names from the actors list, compadre.
    actor_first_names = actors_df['Fname'].unique()

    # Split those baby names into individual names and flatten the list, like a prairie.
    female_names = baby_names_df['Female Names'].str.split(', ').explode().unique()
    male_names = baby_names_df['Male Names'].str.split(', ').explode().unique()

    # Convert to sets for easier comparison, like keeping tabs on your posse.
    actor_names_set = set(actor_first_names)
    female_names_set = set(female_names)
    male_names_set = set(male_names)

    # Create a list to store the results, buckaroo.
    results = []

    # Iterate through the actor DataFrame and check if their names appear in the baby names of each year.
    for index, row in actors_df.iterrows():
        actor_name = row['Fname']
        actor_year = row['Year']

        # Check if the actor's name is in the baby names for the corresponding year.
        for i, baby_row in baby_names_df.iterrows():
            baby_year = baby_row['Year']
            baby_decade = get_decade(baby_year)
            female_names = baby_row['Female Names'].split(', ')
            male_names = baby_row['Male Names'].split(', ')

            if actor_name in female_names or actor_name in male_names:
                results.append({
                    'Actor Name': actor_name,
                    'Actor Year': get_decade(actor_year),
                    'Baby Decade': baby_decade,
                    'Gender': 'Female' if actor_name in female_names else 'Male'
                })

    # Convert results to a DataFrame, partner.
    results_df = pd.DataFrame(results)

    # Group by decades and actor names, just like rounding up cattle.
    grouped_results_df = results_df.groupby(['Baby Decade', 'Actor Name']).size().reset_index(name='Count')

    # Calculate total baby names per decade, tally 'em up.
    baby_names_df['Baby Decade'] = baby_names_df['Year'].apply(get_decade)
    total_names_per_decade = baby_names_df.groupby('Baby Decade').size().reset_index(name='Total Names')

    # Merge the grouped results with total names per decade to calculate percentages.
    merged_df = pd.merge(grouped_results_df, total_names_per_decade, on='Baby Decade')
    merged_df['Percentage'] = (merged_df['Count'] / merged_df['Total Names']) * 100

    # Ensure Baby Decade is formatted correctly without commas
    merged_df['Baby Decade'] = merged_df['Baby Decade'].astype(str)

    return merged_df

# Function to display results, saddle up!
def display_results(merged_df):
    # Display the table, like showing the spoils of your gold rush.
    st.write("### Table of Actor Names Influencing Baby Names by Decade")
    st.dataframe(merged_df)

    # Create a bar chart, visualize your journey through the data trail.
    fig = px.bar(merged_df, x='Baby Decade', y='Percentage', color='Actor Name', 
                 title='Percentage of Baby Names Influenced by Actor Names per Decade')
    st.plotly_chart(fig)

# Main function, where the action begins.
def main():
    st.title('Influence of Actor Names on Baby Names')
    baby_names_df, actors_df = load_data()
    merged_df = process_data(baby_names_df, actors_df)
    display_results(merged_df)

if __name__ == "__main__":
    main()
