import streamlit as st
import pandas as pd
import altair as alt
import folium
from streamlit.components.v1 import html

# setting up the page layout
st.set_page_config(
    page_title="US Baby Name Dashboard",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

# loading in data frames

df_top_baby_names_yr = pd.read_csv("Baby_Names_Start/top_five_names_per_state.csv")


# creating side bar with year list
with st.sidebar:
    st.title("US Baby Names Dashboard")
    
    year_list = list(df_top_baby_names_yr.Year.unique())
    selected_year = st.selectbox("Select a year", year_list)

    # df_selected_state = [df_top_baby_names_yr == selected_state]
    # df_selected_state_sorted = df_selected_state.sort_values(by="Count")

    # df_selected_state = [df_top_baby_names_yr == selected_state]
    # df_selected_state_sorted = df_selected_state.sort_values(by="Count")


# def make_heatmap(df_top_baby_names_yr, input_y, input_x, input_color, input_color_theme):
#     heatmap = alt.Chart(df_top_baby_names_yr).mark_rect().encode(
#         y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
#         x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
#         color=alt.Color(f'max({input_color}):Q', legend=None, scale=alt.Scale(scheme=input_color_theme)),
#         stroke=alt.value('black'),
#         strokeWidth=alt.value(0.25),
#     ).properties(width=900).configure_axis(
#         labelFontSize=12,
#         titleFontSize=12
#     )
#     return heatmap

# # Streamlit UI elements
# st.title('Baby Names Heatmap')

# # Selection boxes for user inputs
# input_y = st.selectbox('Select Y axis', df_top_baby_names_yr.columns, index=df_top_baby_names_yr.columns.get_loc('Year'))
# input_x = st.selectbox('Select X axis', df_top_baby_names_yr.columns, index=df_top_baby_names_yr.columns.get_loc('State'))
# input_color = st.selectbox('Select Color axis', df_top_baby_names_yr.columns, index=df_top_baby_names_yr.columns.get_loc('Count'))
# input_color_theme = st.selectbox('Select Color Theme', ['viridis', 'inferno', 'magma', 'plasma', 'blueorange', 'redblue'])

# # Generate and display heatmap
# heatmap_chart = make_heatmap(df_top_baby_names_yr, input_y, input_x, input_color, input_color_theme)
# st.altair_chart(heatmap_chart, use_container_width=True)

# def make_heatmap(df_top_baby_names_yr, input_y, input_x, input_color, input_color_theme):
#     heatmap = alt.Chart(df_top_baby_names_yr).mark_rect().encode(
#         y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
#         x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
#         color=alt.Color(f'max({input_color}):Q', legend=None, scale=alt.Scale(scheme=input_color_theme)),
#         stroke=alt.value('black'),
#         strokeWidth=alt.value(0.25),
#     ).properties(width=900).configure_axis(
#         labelFontSize=12,
#         titleFontSize=12
#     )
#     return heatmap


# # Generate Choropleth
# def make_choropleth(df_top_baby_names_yr):
#     df_top_baby_names_yr['State'] = df['State'].apply(lambda x: x.upper())
    
#     # Assuming df has columns 'State', 'Count', and you have a GeoJSON file for the US states
#     us_states = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json'

#     # Aggregate the data by state
#     state_data = df_top_baby_names_yr.groupby('State')['Count'].sum().reset_index()

#     # Initialize the map centered on the United States
#     m = folium.Map(location=[37.8, -96], zoom_start=4)

#     # Create the Choropleth map
#     folium.Choropleth(
#         geo_data=us_states,
#         name='choropleth',
#         data=state_data,
#         columns=['State', 'Count'],
#         key_on='feature.id',
#         fill_color='YlGn',
#         fill_opacity=0.7,
#         line_opacity=0.2,
#         legend_name='Total Count'
#     ).add_to(m)

#     # Add layer control
#     folium.LayerControl().add_to(m)

#     return m

# # Streamlit UI elements
# st.title('Baby Names Heatmap and Choropleth Map')

# # Selection boxes for user inputs
# input_y = st.selectbox('Select Y axis', df_top_baby_names_yr.columns, index=df_top_baby_names_yr.columns.get_loc('Year'))
# input_x = st.selectbox('Select X axis', df_top_baby_names_yr.columns, index=df_top_baby_names_yr.columns.get_loc('State'))
# input_color = st.selectbox('Select Color axis', df_top_baby_names_yr.columns, index=df_top_baby_names_yr.columns.get_loc('Count'))
# input_color_theme = st.selectbox('Select Color Theme', ['viridis', 'inferno', 'magma', 'plasma', 'blueorange', 'redblue'])

# # Generate and display heatmap
# heatmap_chart = make_heatmap(df_top_baby_names_yr, input_y, input_x, input_color, input_color_theme)
# st.altair_chart(heatmap_chart, use_container_width=True)

# # Generate and display Choropleth map
# choropleth_map = make_choropleth(df_top_baby_names_yr)
# choropleth_map.save('choropleth_map.html')

# # Display the Folium map in Streamlit
# with open('choropleth_map.html', 'r', encoding='utf-8') as f:
#     html_content = f.read()
# html(html_content, height=600)









def make_heatmap(df_top_baby_names_yr, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(df_top_baby_names_yr).mark_rect().encode(
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

def make_choropleth(df_top_baby_names_yr):
    # Ensure the DataFrame has state codes in the correct format
    df_top_baby_names_yr['State'] = df_top_baby_names_yr['State'].apply(lambda x: x.upper())

    # URL to the GeoJSON data
    us_states_url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json'

    # Aggregate the data by state
    state_data = df_top_baby_names_yr.groupby('State')['Count'].sum().reset_index()

    # Initialize the map centered on the United States
    m = folium.Map(location=[37.8, -96], zoom_start=4)

    # Create the Choropleth map
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

    # Add layer control
    folium.LayerControl().add_to(m)

    return m

# Streamlit UI elements
st.title('Baby Names Heatmap and Choropleth Map')

# Selection boxes for user inputs
input_y = st.selectbox('Select Y axis', df_top_baby_names_yr.columns, index=df_top_baby_names_yr.columns.get_loc('Year'))
input_x = st.selectbox('Select X axis', df_top_baby_names_yr.columns, index=df_top_baby_names_yr.columns.get_loc('State'))
input_color = st.selectbox('Select Color axis', df_top_baby_names_yr.columns, index=df_top_baby_names_yr.columns.get_loc('Count'))
input_color_theme = st.selectbox('Select Color Theme', ['viridis', 'inferno', 'magma', 'plasma', 'blueorange', 'redblue'])

# Generate and display heatmap
heatmap_chart = make_heatmap(df_top_baby_names_yr, input_y, input_x, input_color, input_color_theme)
st.altair_chart(heatmap_chart, use_container_width=True)

# Generate and display Choropleth map
choropleth_map = make_choropleth(df_top_baby_names_yr)
choropleth_map.save('choropleth_map.html')

# Display the Folium map in Streamlit
with open('choropleth_map.html', 'r', encoding='utf-8') as f:
    html_content = f.read()
html(html_content, height=600)



























# def make_choropleth(df_top_baby_names_yr):
#     # Assuming df has columns 'State', 'Count', and you have a GeoJSON file for the US states
#     us_states = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json'

#     # Aggregate the data by state
#     state_data = df_top_baby_names_yr.groupby('State')['Count'].sum().reset_index()

#     # Initialize the map centered on the United States
#     m = folium.Map(location=[37.8, -96], zoom_start=4)

#     # Create the Choropleth map
#     folium.Choropleth(
#         geo_data=us_states,
#         name='choropleth',
#         data=state_data,
#         columns=['State', 'Count'],
#         key_on='feature.id',
#         fill_color='YlGn',
#         fill_opacity=0.7,
#         line_opacity=0.2,
#         legend_name='Total Count'
#     ).add_to(m)

#     # Add layer control
#     folium.LayerControl().add_to(m)

#     return m

# # Streamlit UI elements
# st.title('Baby Names Heatmap and Choropleth Map')

# # Selection boxes for user inputs
# input_y = st.selectbox('Select Y axis', df_top_baby_names_yr.columns, index=df_top_baby_names_yr.columns.get_loc('Year'))
# input_x = st.selectbox('Select X axis', df_top_baby_names_yr.columns, index=df_top_baby_names_yr.columns.get_loc('State'))
# input_color = st.selectbox('Select Color axis', df_top_baby_names_yr.columns, index=df_top_baby_names_yr.columns.get_loc('Count'))
# input_color_theme = st.selectbox('Select Color Theme', ['viridis', 'inferno', 'magma', 'plasma', 'blueorange', 'redblue'])

# # Generate and display heatmap
# heatmap_chart = make_heatmap(df_top_baby_names_yr, input_y, input_x, input_color, input_color_theme)
# st.altair_chart(heatmap_chart, use_container_width=True)

# # Generate and display Choropleth map
# choropleth_map = make_choropleth(df_top_baby_names_yr)
# choropleth_map.save('choropleth_map.html')

# # Display the Folium map in Streamlit
# with open('choropleth_map.html', 'r', encoding='utf-8') as f:
#     html_content = f.read()
# html(html_content, height=600)





    
# def make_heatmap(df_top_baby_names_yr, input_y, input_x, input_color, input_color_theme):
#     heatmap = alt.Chart(df_top_baby_names_yr).mark_rect().encode(
#         y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
#         x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
#         color=alt.Color(f'max({input_color}):Q', legend=None, scale=alt.Scale(scheme=input_color_theme)),
#         stroke=alt.value('black'),
#         strokeWidth=alt.value(0.25),
#     ).properties(width=900
#     ).configure_axis(
#         labelFontSize=12,
#         titleFontSize=12
#     )
#     return heatmap

# # Streamlit UI elements
# st.title('Baby Names Heatmap')
# input_y = st.selectbox('Select Y axis', df_top_baby_names_yr.columns)
# input_x = st.selectbox('Select X axis', df_top_baby_names_yr.columns)
# input_color = st.selectbox('Select Color axis', df_top_baby_names_yr.columns)
# input_color_theme = st.selectbox('Select Color Theme', ['viridis', 'inferno', 'magma', 'plasma', 'blueorange', 'redblue'])

# # Generate and display heatmap
# heatmap_chart = make_heatmap(df_top_baby_names_yr, input_y, input_x, input_color, input_color_theme)
# st.altair_chart(heatmap_chart, use_container_width=True)

