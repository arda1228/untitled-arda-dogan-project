import os
from dotenv import load_dotenv
import requests

load_dotenv()

co2_t_url = os.getenv('CO2_T_URL')
co2_st_api_key = os.getenv('CO2_ST_API_KEY')

def driving_emissions(carSize, fuelType, starting_location, destination):

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
                "type": f"car-{carSize}",
                "fuel": {
                    "type": f'{fuelType}'
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
            # return result['trips'][0]['co2e']
            distance = round(result['trips'][0]['steps'][0]['transport']['distance']/1000,2)
    
            return distance

        else:
            print(f"POST request failed with status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the POST request: {e}")
        return None

print(driving_emissions(carSize="small", fuelType="diesel", starting_location="twyford", destination="sheffield"))
