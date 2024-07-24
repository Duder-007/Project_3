import pandas as pd 

# Load the CSV files
biblical_masculine_names = pd.read_csv('Baby_Names_Start/biblical_masculine_names.csv')
biblical_feminine_names = pd.read_csv('Baby_Names_Start/biblical_feminine_names.csv')
top_five_names_per_state = pd.read_csv('Baby_Names_Start/top_five_names_per_state.csv')

# Extract the list of biblical names
biblical_names_list = pd.concat([biblical_masculine_names, biblical_feminine_names])['Name'].tolist()

# Filter the top_five_names_per_state for names that are in the biblical names list
filtered_names = top_five_names_per_state[top_five_names_per_state['Name'].isin(biblical_names_list)]

# Group by Year and Name, then count the occurrences
biblical_name_counts_per_year = filtered_names.groupby(['Year', 'Name']).size().reset_index(name='Count')

# Display the result
print(biblical_name_counts_per_year.head(10))

# Save the results to a new CSV file
biblical_name_counts_per_year.to_csv('biblical_name_counts_per_year.csv', index=False)

# Calculate the total number of top five names per year
total_names_per_year = top_five_names_per_state.groupby('Year').size().reset_index(name='Total_Count')

# Merge the biblical name counts with the total counts
merged_data = pd.merge(biblical_name_counts_per_year, total_names_per_year, on='Year')

# Calculate the percentage
merged_data['Percentage'] = (merged_data['Count'] / merged_data['Total_Count']) * 100

# Display the result
print(merged_data.head(10))

# Save the results to a new CSV file
merged_data.to_csv('biblical_name_percentage_per_year.csv', index=False)