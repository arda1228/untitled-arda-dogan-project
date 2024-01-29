def calculate_journey_cost(distance, fuel_efficiency, fuel_price_per_liter):
    fuel_needed = distance / fuel_efficiency
    journey_cost = fuel_needed * fuel_price_per_liter
    return journey_cost

def driving_price(distance_km, car_type, fuel_type):

    # Set fuel efficiency based on car type and fuel type
    fuel_efficiencies = {
        'small': {'gasoline': 36, 'diesel': 43, 'electric': 132},
        'medium': {'gasoline': 36, 'diesel': 43, 'electric': 132},
        'large': {'gasoline': 36, 'diesel': 43, 'electric': 132}
    }

    # prices are per litre or per kWh
    fuel_prices = {
        'gasoline': 1.24,
        'diesel': 1.3,
        'electric': 0.163
    }

    # based on average yearly insurance prices estimates in the uk (divided by 365)
    insurances = {
        'small': {'gasoline': 2.05, 'diesel': 2.60, 'electric': 2.20},
        'medium': {'gasoline': 0.56, 'diesel': 2.74, 'electric': 0.60},
        'large': {'gasoline': 2.88, 'diesel': 1.28, 'electric': 3.10}
    }

    if car_type in fuel_efficiencies and fuel_type in fuel_efficiencies[car_type]:
        fuel_efficiency = fuel_efficiencies[car_type][fuel_type]
    else:
        return "Invalid car type or fuel type. Using provided fuel efficiency."

    journey_cost = calculate_journey_cost(distance_km, fuel_efficiency, fuel_prices[fuel_type]) + insurances[car_type][fuel_type]
    return f"The cost of the journey is £{journey_cost:.2f}"


import os
from dotenv import load_dotenv
import requests

load_dotenv()

co2_t_url = os.getenv('CO2_T_URL')
co2_st_api_key = os.getenv('CO2_ST_API_KEY')

def driving_distance(carSize, fuelType, starting_location, destination):

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
            distance = round(result['trips'][0]['steps'][0]['transport']['distance']/1000,2)
    
            return distance

        else:
            print(f"POST request failed with status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the POST request: {e}")
        return None

size = "large"
# gasoline, diesel, electric (but doesn't work for electric now)
fuel = "electric"
distance = driving_distance(carSize=size, fuelType=fuel, starting_location="london", destination="edinburgh")

print(driving_price(distance_km = distance, car_type=size, fuel_type=fuel))