import requests
import pandas as pd


# print(df.to_string()) 

df = pd.read_csv('vehicles.csv', low_memory=False)
# print(df.head())

# Get the list of all column names from headers
column_headers = list(df.columns.values)
print("The Column Header :", column_headers)

final_table_columns = ['make', 'model', 'year', 'city08', 'highway08']

df = df[df.columns.intersection(final_table_columns)]

column_headers = list(df.columns.values)
print("The new Column Header :", column_headers)

# Define a DataFrame
# df = pd.DataFrame({
#     'column1': ['value1', 'value2', 'value3', 'value4'],
#     'column2': ['value5', 'value6', 'value7', 'value8'],
#     'column3': ['value9', 'value10', 'value11', 'value12']
# })

# Define the search values for each column
search_values = {'make': 'Nissan', 'model': 'Stanza', 'year': 1985}

# Define the column to return
return_columns = {'city08', 'highway08'}

# Use loc to search for rows based on column values and return the specified column
result_df = df.loc[(df['make'] == search_values['make']) & (df['model'] == search_values['model']) & (df['year'] == search_values['year']), return_columns]

# Print the result
print(result_df)

total_city_mpg = result_df['city08'].sum()
total_highway_mpg = result_df['highway08'].sum()

avg_highway_mpg = total_highway_mpg/len(result_df)
avg_city_mpg = total_city_mpg/len(result_df)

avg_mpg = (avg_city_mpg + avg_highway_mpg)/2

print("avgmpg:", avg_mpg)

def carMpg(make, model, year):
    # based on make, model and year, get the average of the city08 and highway08 values (mpg)
    print("empty function")
