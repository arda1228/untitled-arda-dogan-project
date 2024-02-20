# this file defines the lambda function, which currently gives a boiler plate message
# the plan is to have layers working so that it can make a post request and return some data

from geopy.distance import geodesic
import json
import os
import requests

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))

    carSize = json.loads(event['body'])['carSize']
    fuelType = json.loads(event['body'])['fuelType']
    startingPoint = json.loads(event['body'])['startingPoint']
    destination = json.loads(event['body'])['destination']

    # start fuel prices
    try:
        response = requests.get(
            f"https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates?singleLine={startingPoint}&f=json&maxLocations=1",
            verify=False  # Disable SSL certificate verification for this request
        )
        if response.status_code == 200:
            location_data = response.json()
            if 'candidates' in data and data['candidates']:
                location = location_data['candidates'][0]['location']
                latitude, longitude = location['y'], location['x']
        print(f"Could not find coordinates for postcode {startingPoint}")
    except Exception as e:
        print(f"Error fetching coordinates: {e}")

    closest_station = None
    try:
        min_distance = float('inf')

        for station in stations_data['stations']:
            station_coordinates = (station['location']['latitude'], station['location']['longitude'])
            distance = geodesic(coordinates, station_coordinates).kilometers
            if distance < min_distance:
                closest_station = station
                min_distance = distance
                
    except Exception as e:
        print(f"Error processing JSON data: {e}")

    # latitude, longitude = y_coordinate, x_coordinate
    if latitude is not None and longitude is not None:
        coordinates = (latitude, longitude)
        if closest_station:
            prices = closest_station.get('prices', {})
            e10_price = prices.get('E10')
            e5_price = prices.get('E5')
            b7_price = prices.get('B7')
    try:
        response = requests.get('https://api.sainsburys.co.uk/v1/exports/latest/fuel_prices_data.json', verify=False)
        if response.status_code == 200:
            stations_data = response.json()
        else:
            print(f"Failed to fetch stations data. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error fetching stations data: {e}")


    fuel_prices = {
        'gasoline': e5_price,
        'diesel': b7_price,
        'electric': 0.163
    }
    # end fuel prices
    
    
    co2_t_url = os.environ['CO2_T_URL']
    co2_st_api_key = os.environ['CO2_ST_API_KEY']

    data = {
    "trips": [
        {
        "steps": [
            {
            "discovery": True,
            "location": {
                "placename": startingPoint
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
                "placename": startingPoint
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
            difference = round(co2e_values[0] - co2e_values[1],2)
            driving_distance = round(result['trips'][0]['steps'][0]['transport']['distance']/1000,2)


             # Set fuel efficiency based on car type and fuel type
            fuel_efficiencies = {
                'small': {'gasoline': 36, 'diesel': 43, 'electric': 132},
                'medium': {'gasoline': 36, 'diesel': 43, 'electric': 132},
                'large': {'gasoline': 36, 'diesel': 43, 'electric': 132}
            }

            

            # based on average yearly insurance prices estimates in the uk (divided by 365)
            insurances = {
                'small': {'gasoline': 2.05, 'diesel': 2.60, 'electric': 2.20},
                'medium': {'gasoline': 0.56, 'diesel': 2.74, 'electric': 0.60},
                'large': {'gasoline': 2.88, 'diesel': 1.28, 'electric': 3.10}
            }

            if carSize in fuel_efficiencies and fuelType in fuel_efficiencies[carSize]:
                fuel_efficiency = fuel_efficiencies[carSize][fuelType]
            else:
                return "Invalid car type or fuel type. Using provided fuel efficiency."

            fuel_needed = driving_distance / fuel_efficiency
            driving_price = fuel_needed * fuel_prices[fuelType]
            driving_price += insurances[carSize][fuelType]

            msg = f'by using public transport instead of driving, you saved {difference} kgs of co2 on your {driving_distance}km trip! driving would have cost you £{round(driving_price,2)}!'
            

            return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'text/plain',
                        "Access-Control-Allow-Origin": os.environ['FRONTEND_URL'],
                        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                        "Access-Control-Allow-Headers": "Content-Type, Authorization"
                    },
                    'body': f"{msg}"
                }
        else:
            print(f"POST request failed with status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the POST request: {e}")
        return None
    


