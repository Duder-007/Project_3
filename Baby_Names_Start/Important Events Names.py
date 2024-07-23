import streamlit as st
import pandas as pd
import re

# File paths
baby_names_path = '/Users/jenleemcnew/Library/Mobile Documents/com~apple~CloudDocs/SMU BC Classwork/Module 17 - Project 3/Project_3-1/Baby_Names_Start/top_baby_names.csv'
events_path = '/Users/jenleemcnew/Library/Mobile Documents/com~apple~CloudDocs/SMU BC Classwork/Module 17 - Project 3/Project_3-1/Baby_Names_Start/Most_Important_Events.csv'

# Read CSV files
baby_names_df = pd.read_csv(baby_names_path)
events_df = pd.read_csv(events_path)

# Extract the years from the event descriptions
def extract_year(event_text):
    match = re.search(r'\b(19|20)\d{2}\b', event_text)
    return int(match.group()) if match else None

events_df['Year'] = events_df['Event'].apply(extract_year)
events_years = events_df['Year'].dropna().unique()

# Filter the baby names DataFrame for these years
filtered_baby_names_df = baby_names_df[baby_names_df['Year'].isin(events_years)]

# Merge the events DataFrame with the filtered baby names DataFrame on 'Year'
merged_df = pd.merge(events_df[['Event', 'Year']], filtered_baby_names_df, on='Year', how='inner')


merged_df

# # Display the results
# st.write("Top baby names for the years represented in the events:")
# st.dataframe(merged_df)