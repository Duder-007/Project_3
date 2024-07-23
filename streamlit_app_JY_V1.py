# import streamlit as st
# import pandas as pd
# import altair as alt

# st.set_page_config(
#     page_title="US Baby Name Dashboard",
#     page_icon="👶",
#     layout="wide",
#     initial_sidebar_state="expanded")

# alt.themes.enable("dark")

# # loading in data frames

# df_top_baby_names_yr = pd.read_csv("Baby_Names_Start/top_five_names_per_state.csv")


# # creating side bar with year list
# with st.sidebar:
#     st.title("US Baby Names Dashboard")
    
#     year_list = list(df_top_baby_names_yr.Year.unique())
#     selected_year = st.selectbox("Select a year", year_list)
#     st.write("")
#     st.write("")

#     df_selected_year = df_top_baby_names_yr[df_top_baby_names_yr.Year == selected_year]
#     df_selected_year_sorted = df_selected_year.sort_values(by="Count", ascending=False)

# # func to iterate off of selected year
# def calculate_most_popular_names(selected_year):

#     df_selected_year = df_top_baby_names_yr[df_top_baby_names_yr.Year == selected_year]
#     popular_male_name = df_selected_year[df_selected_year["Gender"] == "M"]["Name"].value_counts().idxmax()
#     popular_female_name = df_selected_year[df_selected_year["Gender"] == "F"]["Name"].value_counts().idxmax()

#     # excess code, might be useful later:
#     # state_most_popular_male = df_selected_year[(df_selected_year["Name"] == popular_male_name) & (df_selected_year["Gender"] == "M")]["State"].value_counts().idxmax()
#     # state_most_popular_female = df_selected_year[(df_selected_year["Name"] == popular_female_name) & (df_selected_year["Gender"] == "F")]["State"].value_counts().idxmax()

#     df_popular_male = df_selected_year[(df_selected_year["Name"] == popular_male_name) & (df_selected_year["Gender"] == "M")]
#     df_popular_female = df_selected_year[(df_selected_year["Name"] == popular_female_name) & (df_selected_year["Gender"] == "F")]
#     most_pop_state_male = df_popular_male.groupby("State")["Count"].sum().idxmax()
#     most_pop_state_female = df_popular_female.groupby("State")["Count"].sum().idxmax()

#     # writing in print statements when func is called to update output
#     with st.sidebar:
#         st.markdown(f"# Male Name")
#         st.markdown(f"## State: {most_pop_state_male}")
#         st.markdown(f"### {popular_male_name}")
#         st.write("")
#         st.write("")
#         st.write("")
#         st.write("")
#         st.write("")
#         st.markdown(f"# Female Name")
#         st.markdown(f"## State: {most_pop_state_female}")
#         st.markdown(f"### {popular_female_name}")
        

#         # st.write(f"Most popular Male name in {selected_year} was {popular_male_name}, in {most_pop_state_male}")
#         # st.write(f"Most popular Female name in {selected_year} was {popular_female_name}, in {most_pop_state_female}")

# # running func
# calculate_most_popular_names(selected_year)

import streamlit as st
import pandas as pd
import altair as alt
import folium
from streamlit.components.v1 import html

# We’re saddling up for a ride with this Streamlit dashboard, setting up with all the trimmings.
st.set_page_config(
    page_title="US Baby Name Dashboard", # Like putting a name on a ranch gate.
    page_icon="👶", # Little tyke's the symbol of our focus here.
    layout="wide", # Spread out wide, like a prairie.
    initial_sidebar_state="collapsed" # We're starting with the sidebar tucked away.
)


# This here’s the custom CSS to keep that sidebar behaving, hidden until called.
custom_css = """
<style>
button[data-testid="stSidebarNav"] { display: none; }  # Hide the usual toggle, like hiding the key to the liquor cabinet.

#toggle-btn {  # This is our own button, like branding our cattle.
    position: fixed;  # Fixed in place, like a post in dry concrete.
    top: 16px; left: 16px;  # Just right of the top corner, where it's easy to spot.
    width: 30px; height: 30px;  # Small but noticeable.
    background-color: #4CAF50; color: white;  # Green as the grass after a rain, with white like a cowboy's hat.
    border: none; border-radius: 5px;  # Smooth and rounded, no sharp edges here.
    cursor: pointer; z-index: 999;  # Stands out on top, like a sheriff at a town meeting.
}

.css-1lcbmhc.e1fqkh3o3 {
    transition: transform 0.3s ease;  # Smooth as a good whiskey.
    transform: translateX(-300px);  # Start hidden out of sight.
}

.css-1lcbmhc.e1fqkh3o3.expanded {
    transform: translateX(0);  # Slide into view when needed.
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
st.markdown('<button id="toggle-btn">☰</button>', unsafe_allow_html=True)  # The button that brings the sidebar into view.

# Little script to make that custom button work, like teaching a horse to trot on command.
st.markdown("""
<script>
const toggleButton = document.getElementById('toggle-btn');  # Grab our custom button.
const sidebar = document.querySelector('.css-1lcbmh3.e1fqkh3o3');  # Find the sidebar.
toggleButton.addEventListener('click', () => {
    sidebar.classList.toggle('expanded');  # Toggle the view like flipping a coin.
});
</script>
""", unsafe_allow_html=True)

alt.themes.enable("dark")  # Set a dark theme for our charts, easy on the eyes like a shady porch.

# Loading up the data like loading a wagon for a long journey.
df_top_baby_names_yr = pd.read_csv("Baby_Names_Start/top_five_names_per_state.csv")
biblical_names_df = pd.read_csv("Baby_Names_Start/biblical_names.csv")
df_top_five_names_per_state = pd.read_csv("Baby_Names_Start/top_five_names_per_state.csv")

# Setting up the sidebar for selections, like choosing the right tool for the job.
with st.sidebar:
    st.title("US Baby Names Dashboard")  # Marking our territory.
    year_list = list(df_top_baby_names_yr.Year.unique())  # Get all the years available.
    selected_year = st.selectbox("Select a year", year_list)  # Choose a year.
    name_list = df_top_baby_names_yr.Name.unique().tolist()  # All the names rounded up.
    selected_names = st.multiselect("Select names", name_list)  # Pick the names you're interested in.

# Filter data based on selections like sorting cattle by brand.
df_filtered = df_top_baby_names_yr[df_top_baby_names_yr["Year"] == selected_year]
if selected_names:
    df_filtered = df_filtered[df_filtered["Name"].isin(selected_names)]

# Calculating the percentage of biblical names, like figuring out how much of your herd is prize-winning.
# Calculate the percentage of biblical names in the selected year
df_filtered = df_top_baby_names_yr[df_top_baby_names_yr['Year'] == selected_year]
selected_biblical_names = set(df_filtered['Name']).intersection(set(biblical_names_df['Name']))
percent_biblical = len(selected_biblical_names) / len(set(df_filtered['Name'])) * 100 if df_filtered['Name'].any() else 0

#st.write(f"Percentage of biblical names in the top baby names for {selected_year}: {percent_biblical:.2f}%")



#biblical_names = set(biblical_names_df["Name"].str.upper())
#selected_biblical_names = set(name.upper() for name in selected_names if name.upper() in biblical_names)
#percent_biblical = len(selected_biblical_names) / len(selected_names) * 100 if selected_names else 0

# Creating a donut chart, simple as pie.
def make_donut_chart(percent):
    data = pd.DataFrame({
        'category': ['Biblical Names', 'Other Names'],
        'value': [percent, 100 - percent]
    })
    chart = alt.Chart(data).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="value", type="quantitative"),
        color=alt.Color(field="category", type="nominal", scale=alt.Scale(range=["#4CAF50", "#FFCCCB"])),
        tooltip=["category", "value"]
    ).properties(width=200, height=200)
    return chart

donut_chart = make_donut_chart(percent_biblical)

# Drawing up the heatmap, like laying out a map for a new territory.
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

# Building a choropleth map, marking out the lay of the land.
def make_choropleth(df):
    df['State'] = df['State'].apply(lambda x: x.upper())  # Standardize the state names.
    
    us_states_url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json'  # Map data, like a good sturdy map.
    
    state_data = df.groupby('State')['Count'].sum().reset_index()  # Sum up the counts by state.
    
    m = folium.Map(location=[37.8, -96], zoom_start=4)  # Set the starting point of the map.
    
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
    ).add_to(m)  # Apply the choropleth overlay.
    
    folium.LayerControl().add_to(m)  # Add control layers to switch views.
    
    return m

# Putting up a title like hanging a sign over a saloon.
st.title('Baby Names In the US and Data that defines them')

# Setting up a two-column layout, like having two horses in the stable.
col1, col2 = st.columns([3, 1])

# In the left column, we're showing all the main attractions.
with col1:
    input_y = st.selectbox('Select Y axis', df_filtered.columns, index=df_filtered.columns.get_loc('Year'))  # Choosing what goes on the Y-axis.
    input_x = st.selectbox('Select X axis', df_filtered.columns, index=df_filtered.columns.get_loc('State'))  # Choosing what goes on the X-axis.
    input_color = st.selectbox('Select Color axis', df_filtered.columns, index=df_filtered.columns.get_loc('Count'))  # Choosing the data for color coding.
    input_color_theme = st.selectbox('Color Theme', ["yellowgreen"])  # setting a color scheme to match.

    # Display the heatmap, bright as a new silver dollar.
    heatmap_chart = make_heatmap(df_filtered, input_y, input_x, input_color, input_color_theme)
    st.altair_chart(heatmap_chart, use_container_width=True)

    # Generate and display the choropleth map, showing where the action is.
    choropleth_map = make_choropleth(df_filtered)
    choropleth_map.save('choropleth_map.html')  # Save the map to a file.
    with open('choropleth_map.html', 'r', encoding='utf-8') as f:
        html_content = f.read()  # Read the map from the file.
    html(html_content, height=600)  # Show the map in the dashboard.

    # Show the donut chart, as inviting as a pie cooling on a windowsill.
    st.title("Percentage of Selected Biblical Names")
    st.altair_chart(donut_chart, use_container_width=True)

# In the right column, like a sidearm in a holster, we're ready to draw.
with col2:
    st.title("Top 5 Names per State")  # Announcing what we're aiming to show.
    df_top_five_filtered = df_top_five_names_per_state[df_top_five_names_per_state["Year"] == selected_year]  # Filter the data for the selected year.
    
    state_list = df_top_five_filtered['State'].unique().tolist()  # Get a list of all states from the filtered data.
    selected_state = st.selectbox("Select a state", state_list)  # Allow the user to pick a state.
    
    if selected_state:  # If a state is selected, show the top names.
        top_names = df_top_five_filtered[df_top_five_filtered['State'] == selected_state][['Name', 'Count']]
        names_chart = alt.Chart(top_names).mark_bar().encode(
            x='Name:N',
            y='Count:Q',
            color=alt.Color('Count:Q', scale=alt.Scale(scheme='yellowgreen')),
            tooltip=['Name', 'Count']
        ).properties(height=300, width=400)
        st.altair_chart(names_chart, use_container_width=True)  # Display the bar chart.

        import pandas as pd

# deliverable 7

# creating output underneath for most popular names over the last century

# writing in a title
st.title("Most Popular Name Over Last Century")

# reading csv file
top_baby_names_100yrs_df = pd.read_csv("Baby_Names_Start/2top_baby_names.csv")

# finding the most popular names over the df
most_popular_male_name = top_baby_names_100yrs_df["Male Names"].value_counts().idxmax()
most_popular_female_name = top_baby_names_100yrs_df["Female Names"].value_counts().idxmax()

# formatting for output
st.markdown(f"## Male Name")
st.markdown(f"### {most_popular_male_name}")
st.write("")
st.write("")
st.write("")
st.markdown(f"## Female Name")
st.markdown(f"### {most_popular_female_name}")

# deliverable 9

with col2:
    # Top Baby Names by States
    top_names_states = pd.read_csv("Baby_Names_Start/top_five_names_per_state.csv")
    # Group by State, Gender, and Name and sum the Counts
    top_names_state_df = top_names_states.groupby(["State", "Gender", "Name"])["Count"].sum().reset_index()
    # Grab the top 5 (each gender) from each state
    top_names_state_df = top_names_state_df.sort_values("Count", ascending=False).groupby(["State", "Gender"]).head(5)
    # Sorting by state name
    top_names_state_df = top_names_state_df.sort_values("State")
    # Streamlit Title
    st.title("Top Baby Names by State")
    # Display the DataFrame
    st.write("Top baby names (top 5 for each gender) in each state:")
    st.dataframe(top_names_state_df)
    # Select a state to filter the data
    state_filter = st.selectbox("Select a state to filter:", top_names_state_df["State"].unique())
    filtered_df = top_names_state_df[top_names_state_df["State"] == state_filter]
    st.write(f"Top baby names in {state_filter}:")
    st.dataframe(filtered_df)