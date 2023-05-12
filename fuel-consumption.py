import requests
import pandas as pd

df = pd.read_csv('vehicles.csv', low_memory=False)

final_table_columns = ['make', 'model', 'year', 'city08', 'highway08']

df = df[df.columns.intersection(final_table_columns)]


def carMpg(make, model, year):
    # based on make, model and year, get the average of the city08 and highway08 values (mpg)
    # Define the search values for each column
    search_values = {'make': make, 'model': model, 'year': year}

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
    
    print(avg_mpg)


carMpg("Nissan", "Stanza", 1985)