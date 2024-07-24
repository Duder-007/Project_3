# Project_3
Baby Names
TEAM 3
Project Title:
Baby Names Trend Analysis
Track #2:  Data Engineering

Description: 
Baby names can have a curious origin so can we identify some trends that make people choose the names they do?  Over the past 100 years we will attempt to identify popular names and some trends that influence the outcome.
Research questions:
## Deliverables
1. Investigate names that have been given to babies of either sex every year for the 100 years from 1924 through 2024..
    Using dropdown from 1910-2024 find the names
2. Traditional names, faddish names.  Popularity according to the number of years that the name appears in the dataset, does it re-appear during certain times?  
    Actor names, percentage found
3. Top-ranked female/male names since 1924:  Highest-ranked American female names in our dataset. 
4. Movie/Actor names popular by decade.
5. Biblical names by state, vs. common names, how often do biblical names appear on average?
6. What is the most popular name in 100 years, how often does it occur?  Yearly trends?    
7. Males and Females with the same name, years and the number of babies given any male/female name in that year.
8. The most years at number one, list of first names that have been the top male/female first name in any year along with a count of the number of years that name has been the top name.
    
Source:
https://www.ssa.gov/oact/babynames/
https://www.imdb.com/list/ls025653489/
https://en.wikipedia.org/wiki/List_of_actors_with_Hollywood_Walk_of_Fame_motion_picture_stars
https://news.gallup.com/poll/3427/most-important-events-century-from-viewpoint-people.aspx
https://www.usatoday.com/picture-gallery/life/2020/09/06/the-worlds-most-important-event-every-year-since-1920/42346845/
https://www.behindthename.com/names/
https://rpubs.com/toldham2/babynames

Data Engineering Track:

Data engineering is a critical aspect of any data-driven organization, where data scientists and analysts work with large amounts of data to extract insights and make data-driven decisions. In recent years, Streamlit has become a popular framework for building interactive data applications, making it easier for data engineers to create and share data-driven applications with their team members.  For the data engineering in this project, Team 3 will be using Streamlit to showcase the data.

Team 3 choose the Streamlit library for different reasons, the intuitive, interactive customizable API, real time updates, forward support growth with machine learning as well as the ease of coding.  Using simple maintainable code base that does not require complex coding techniques.

**Objective**: Follow data engineering processes. **Requirements**:
Tasks:
Main Repo/Readme/Proposal/Project Lead:  Jeremiah C Mergenthaler
Website Deploy:  Thierno Diallo/Jack Yeager
SQL:  Sylvia Turner/Jennifer McNew
New Library:  Jack Yeager/Thierno Diallo
ETL Workflows:  Jennifer McNew/Sylvia Turner
Database:  Team

1. **Database**: Use a SQL or NoSQL database with at least two tables or collections and 1000 records.
Tables in SQL created using DBeaver, all csv's converted to tables and data cleaned.

2. **ETL Workflows**: Ingest and transform data before storing it in the database.
Data Scraped using Beautiful Soup/Jupiter into CSV for storage into SQL.

3. **Data Display**: Provide a method to read data from the database using:
Python and Pandas DataFrame used to display data, streamlit functions used for interactivity

4. **New Library**: Use an additional data engineering library not covered in class:
Streamlit, Altier

5. **README.md**: Include an overview, instructions, documentation of the database choice, ETL workflow, ethical considerations, and references.
MS Word

6. **Optional User Interaction**: Add user-driven interaction before or after the ETL process.
Using Streamlit

Points of Contact:
Thierno Diallo; thamiru@live.com
Jeremiah Mergenthaler; jeremiah.mergenthaler@gmail.com 
Sylvia Turner; sturner6207@gmail.com
Jennifer McNew; jen.lee.mcnew@gmail.com
Jack Yeager; jackyeager45@gmail.com

#Application and ETL Workflow Analysis
#Application Overview
The "US Baby Name Dashboard" is a Streamlit-based application designed to visualize baby names data from multiple perspectives. The dashboard leverages various data visualization libraries like Altair, Plotly, and Folium to create interactive and informative charts and maps. The primary features of the dashboard include:
1.	Yearly Trends Analysis: Allows users to see the trends of baby names over selected years.
2.	Top Names Visualization: Provides insights into the most popular names by state and overall trends for the past century.
3.	Biblical Names Percentage: Displays the percentage of selected biblical names among all names chosen.
4.	Heatmap and Choropleth Maps: Visualizes the distribution and count of names across different states and years.
5.	Unisex Names Identification: Identifies and displays names used for both males and females.
ETL Workflow
The ETL (Extract, Transform, Load) workflow for this application involves several steps to ensure that the data is correctly processed and visualized. Below is a detailed breakdown:
1. Extract
The data extraction process involves reading multiple CSV files containing baby names data and additional datasets, such as biblical names and actor names:
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
2. Transform
The transformation process includes several key operations:
•	Aggregation: Aggregating data to get the top names over the last 100 years.
df_aggregated = df_top_baby_names_yr.groupby('Name')['Count'].sum().reset_index()
df_aggregated = df_aggregated.sort_values(by='Count', ascending=False).head(5)
•	Filtering: Filtering data based on user selections from the sidebar. 
df_filtered = df_top_baby_names_yr[df_top_baby_names_yr["Year"] == selected_year]
if selected_names:
    df_filtered = df_filtered[df_filtered["Name"].isin(selected_names)]
•	Percentage Calculation: Calculating the percentage of biblical names among the selected names.
selected_biblical_names = set(df_filtered['Name']).intersection(set(biblical_names_df['Name']))
percent_biblical = len(selected_biblical_names) / len(set(df_filtered['Name'])) * 100 if df_filtered['Name'].any() else 0
•	Data Grouping: Grouping and summarizing data for choropleth maps and heatmaps.
state_data = df.groupby('State')['Count'].sum().reset_index()
•	Unisex Names Identification: Finding names that are both male and female.
def find_unisex_names(df):
    male_names = df[df["sex"] == "M"]["first_name"].unique()
    female_names = df[df["sex"] == "F"]["first_name"].unique()
    unisex_names = list(set(male_names) & set(female_names))
    return unisex_names
3. Load
The load phase involves presenting the transformed data through various interactive visualizations:
•	Donut Chart: Showing the percentage of biblical names.
donut_chart = make_donut_chart(percent_biblical, selected_color_theme)
st.altair_chart(donut_chart, use_container_width=True)
•	Heatmap: Visualizing the distribution of names across states and years.
heatmap_chart = make_heatmap(df_filtered, input_y, input_x, input_color, input_color_theme)
st.altair_chart(heatmap_chart, use_container_width=True)
•	Choropleth Map: Displaying the count of names by state.
choropleth_map = make_choropleth(df_filtered)
choropleth_map.save('choropleth_map.html')
with open('choropleth_map.html', 'r', encoding='utf-8') as f:
    html_content = f.read()
html(html_content, height=600)
•	Bar Chart and Trends: Visualizing top names by state and yearly trends.
names_chart = alt.Chart(top_names).mark_bar().encode(
    x='Name:N',
    y='Count:Q',
    color=alt.Color('Count:Q', scale=alt.Scale(scheme=input_color_theme)),
    tooltip=['Name', 'Count']
).properties(height=300, width=400)
st.altair_chart(names_chart, use_container_width=True)
In conclusion, this Streamlit application provides a comprehensive analysis and interactive visualization of baby names in the US, leveraging a well-structured ETL process to ensure data integrity and usability.  Streamlit’s capabilities go far beyond what is done here and will be a proven tool in the future.

