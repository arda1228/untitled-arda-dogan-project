import os
from dotenv import load_dotenv
import requests

load_dotenv()

co2_st_url = os.getenv('CO2_ST_URL')
co2_st_api_key = os.getenv('CO2_ST_API_KEY')

def co2driving(starting_location, destination):

    data = {
        "from": starting_location,
        "to": destination,
        "transport_types": [
            "driving"
        ]
    }

    headers = {
        "Authorization": f"Bearer {co2_st_api_key}"
    }

    try:
        response = requests.post(co2_st_url, json=data, headers=headers)

        if response.status_code == 200:
            result = response.json()
            return result['trips'][0]['co2e']
        else:
            print(f"POST request failed with status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the POST request: {e}")
        return None

def co2pt(starting_location, destination):

    data = {
        "from": starting_location,
        "to": destination,
        "transport_types": [
            "public-transport"
        ]
    }

    headers = {
        "Authorization": f"Bearer {co2_st_api_key}"
    }

    try:
        response = requests.post(co2_st_url, json=data, headers=headers)

        if response.status_code == 200:
            result = response.json()
            return result['trips'][0]['co2e']
        else:
            print(f"POST request failed with status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the POST request: {e}")
        return None

def diff(starting_location, destination):
    result = co2driving(starting_location, destination) - co2pt(starting_location, destination)
    
    return f'by using public transport instead of driving, you\'d save {result} kgs of carbon!'