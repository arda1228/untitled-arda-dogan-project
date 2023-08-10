import os
from dotenv import load_dotenv
import requests

load_dotenv()

co2_st_url = os.getenv('CO2_ST_URL')
co2_t_url = os.getenv('CO2_T_URL')
co2_st_api_key = os.getenv('CO2_ST_API_KEY')

def pt_emissions(starting_location, destination):

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

# print(co2pt(starting_location="rg10 9ny", destination="co5 8gz"))

def newdiff(starting_location, destination):

    data = {
  "trips": [
    {
      "steps": [
        {
          "discovery": True,
          "location": {
            "placename": starting_location
          },
          "transport": {
            "type": "driving",
            "ways": 1,
            "people": 1,
            "vehicle": {
              "type": "car-small",
              "fuel": {
                "type": "gasoline"
              }
            }
          }
        },
        {
          "discovery": True,
          "location": {
            "placename": destination
          },
        }
      ]
    },
    {
      "steps": [
        {
          "discovery": True,
          "location": {
            "placename": starting_location
          },
          "transport": {
            "type": "public-transport",
            "ways": 1,
            "people": 1,
          }
        },
        {
          "discovery": True,
          "location": {
            "placename": destination
          },
        }
      ]
    }
  ]
}

    headers = {
        "Authorization": f"Bearer {co2_st_api_key}"
    }

    try:
        response = requests.post(co2_t_url, json=data, headers=headers)

        if response.status_code == 200:
            result = response.json()
            co2e_values = [trip["co2e"] for trip in result["trips"]]
            difference = co2e_values[0] - co2e_values[1]
            return f'by using public transport instead of driving, you saved {difference} kgs of co2!'
        else:
            print(f"POST request failed with status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the POST request: {e}")
        return None
    
print(newdiff(starting_location="twyford", destination="wargrave"))