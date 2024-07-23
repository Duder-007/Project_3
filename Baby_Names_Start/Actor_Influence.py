

import pandas as pd
import plotly.express as px
import streamlit as st

def load_data():
    baby_names_df = pd.read_csv('top_baby_names.csv')
    actors_df = pd.read_csv('AList.csv')
    return baby_names_df, actors_df

def get_decade(year):
    return (year // 10) * 10

def process_data(baby_names_df, actors_df):
    # Extract unique first names from actors list
    actor_first_names = actors_df['Fname'].unique()

    # Split the baby names into individual names and flatten the list
    female_names = baby_names_df['Female Names'].str.split(', ').explode().unique()
    male_names = baby_names_df['Male Names'].str.split(', ').explode().unique()

    # Convert to sets for easier comparison
    actor_names_set = set(actor_first_names)
    female_names_set = set(female_names)
    male_names_set = set(male_names)

    # Create a list to store the results
    results = []

    # Iterate through the actor DataFrame and check if their names appear in the baby names of each year
    for index, row in actors_df.iterrows():
        actor_name = row['Fname']
        actor_year = row['Year']

        # Check if the actor's name is in the baby names for the corresponding year
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

    # Convert results to a DataFrame
    results_df = pd.DataFrame(results)

    # Group by decades and actor names
    grouped_results_df = results_df.groupby(['Baby Decade', 'Actor Name']).size().reset_index(name='Count')

    # Calculate total baby names per decade
    baby_names_df['Baby Decade'] = baby_names_df['Year'].apply(get_decade)
    total_names_per_decade = baby_names_df.groupby('Baby Decade').size().reset_index(name='Total Names')

    # Merge the grouped results with total names per decade to calculate percentages
    merged_df = pd.merge(grouped_results_df, total_names_per_decade, on='Baby Decade')
    merged_df['Percentage'] = (merged_df['Count'] / merged_df['Total Names']) * 100

    return merged_df

def display_results(merged_df):
    # Display the table
    st.write("### Table of Actor Names Influencing Baby Names by Decade")
    st.dataframe(merged_df)

