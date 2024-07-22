import pandas as pd

# Load the CSV files
biblical_masculine_names = pd.read_csv('Baby_Names_Start/biblical_masculine_names.csv')
biblical_feminine_names = pd.read_csv('Baby_Names_Start/biblical_feminine_names.csv')
top_five_names_per_state = pd.read_csv('Baby_Names_Start/top_five_names_per_state.csv')

# Extract the list of biblical names
masculine_names_list = biblical_masculine_names['Name'].tolist()
feminine_names_list = biblical_feminine_names['Name'].tolist()

# Filter the top_five_names_per_state for names that are in the biblical names lists
filtered_masculine_names = top_five_names_per_state[top_five_names_per_state['Name'].isin(masculine_names_list)]
filtered_feminine_names = top_five_names_per_state[top_five_names_per_state['Name'].isin(feminine_names_list)]

# Group by Year and Name, then count the occurrences
masculine_name_counts_per_year = filtered_masculine_names.groupby(['Year', 'Name']).size().reset_index(name='Count')
feminine_name_counts_per_year = filtered_feminine_names.groupby(['Year', 'Name']).size().reset_index(name='Count')

# Get the top two names per year for masculine and feminine names
top_two_masculine_names_per_year = masculine_name_counts_per_year.sort_values(['Year', 'Count'], ascending=[True, False]).groupby('Year').head(2)
top_two_feminine_names_per_year = feminine_name_counts_per_year.sort_values(['Year', 'Count'], ascending=[True, False]).groupby('Year').head(2)

# Display the result
print("Top two masculine biblical names per year:")
print(top_two_masculine_names_per_year.head(10))
print("\nTop two feminine biblical names per year:")
print(top_two_feminine_names_per_year.head(10))

# Save the results to new CSV files
top_two_masculine_names_per_year.to_csv('top_two_masculine_biblical_names_per_year.csv', index=False)
top_two_feminine_names_per_year.to_csv('top_two_feminine_biblical_names_per_year.csv', index=False)