import pandas as pd

# Load the CSV files
baby_names_df = pd.read_csv('Baby_Names_Start/top_baby_names.csv')
actors_df = pd.read_csv('Baby_Names_Start/AList.csv')

# Extract unique first names from actors list
actor_first_names = actors_df['Fname'].unique()

# Split the baby names into individual names and flatten the list
female_names = baby_names_df['Female Names'].str.split(', ').explode().unique()
male_names = baby_names_df['Male Names'].str.split(', ').explode().unique()

# Convert to sets for easier comparison
actor_names_set = set(actor_first_names)
female_names_set = set(female_names)
male_names_set = set(male_names)

# Find intersections
common_female_names = actor_names_set.intersection(female_names_set)
common_male_names = actor_names_set.intersection(male_names_set)

# Create a list to store the results
results = []

# Iterate through the actor DataFrame and check if their names appear in the baby names of each year
for index, row in actors_df.iterrows():
    actor_name = row['Fname']
    actor_year = row['Year']
    
    # Check if the actor's name is in the baby names for the corresponding year
    for i, baby_row in baby_names_df.iterrows():
        baby_year = baby_row['Year']
        female_names = baby_row['Female Names'].split(', ')
        male_names = baby_row['Male Names'].split(', ')
        
        if actor_name in female_names or actor_name in male_names:
            results.append({
                'Actor Name': actor_name,
                'Actor Year': actor_year,
                'Baby Year': baby_year,
                'Gender': 'Female' if actor_name in female_names else 'Male'
            })

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Display the DataFrame
results_df