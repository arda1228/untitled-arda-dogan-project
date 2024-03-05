import json
import os
import requests
import numpy as np

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))

    carSize = json.loads(event['body'])['carSize']
    fuelType = json.loads(event['body'])['fuelType']
    startingPoint = json.loads(event['body'])['startingPoint']
    destination = json.loads(event['body'])['destination']
    yearlyInsurance = json.loads(event['body'])['yearlyInsurance']
    fuelEfficiency = json.loads(event['body'])['fuelEfficiency']

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
                'small': {'gasoline': 36 * 1.175, 'diesel': 47 * 1.175, 'electricity': 136 * 1.175},
                'normal': {'gasoline': 36, 'diesel': 43, 'electricity': 132},
                'large': {'gasoline': 32 * 0.8, 'diesel': 39 * 0.8, 'electricity': 128 * 0.8}
            }


            # based on average yearly insurance prices estimates in the uk (divided by 365)
            average_insurance_normal = float(561/365)
            average_insurance_small = average_insurance_normal * 0.875
            average_insurance_large = average_insurance_normal * 1.175

            insurances = {
                'small': {'gasoline': average_insurance_small, 'diesel': average_insurance_small * 1.1, 'electricity': average_insurance_small * 1.175},
                'normal': {'gasoline': average_insurance_normal, 'diesel': average_insurance_normal * 1.1, 'electricity': average_insurance_normal * 1.175},
                'large': {'gasoline': average_insurance_large, 'diesel': average_insurance_large * 1.1, 'electricity': average_insurance_large * 1.175}
            }

            if fuelEfficiency != '':
                fuel_efficiency = float(fuelEfficiency)
            elif (carSize in fuel_efficiencies and fuelType in fuel_efficiencies[carSize]):
                fuel_efficiency = fuel_efficiencies[carSize][fuelType]
            else:
                return "Invalid car type or fuel type. Using provided fuel efficiency."

            msg = ''
            
            # fetch fuel prices from sainsbury's api
            try:
                sainos_response = requests.get('https://api.sainsburys.co.uk/v1/exports/latest/fuel_prices_data.json', verify=False)
                if sainos_response.status_code == 200:
                    print(sainos_response.json().get('last_updated'))
                else:
                    msg += f"Failed to fetch stations data. Status code: {sainos_response.status_code}"
            except Exception as e:
                msg += f"Error fetching stations data: {e}"

            # geocode the starting postcode
            try:
                geocode_response_start = requests.get(
                    f"https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates?singleLine={startingPoint}&f=json&maxLocations=1",
                    verify=False  # Disable SSL certificate verification for this request
                )
                if geocode_response_start.status_code == 200:
                    data = geocode_response_start.json()
                    if 'candidates' in data and data['candidates']:
                        location = data['candidates'][0]['location']
                        start_lat, start_lon = location['y'], location['x']
                        print(f"Coordinates for {startingPoint}: {start_lat}, {start_lon}")
                    else:
                        start_lon, start_lat = None
                        msg += f"Could not find coordinates for postcode {startingPoint}"
                else:
                    msg += f"Failed to fetch coordinates. Status code: {geocode_response_start.status_code}"
            except Exception as e:
                msg += f"Error fetching coordinates: {e}"
            
            # geocode the destination postcode
            closest_station = None
            min_distance = 99999
            R = 6371.0  # earth radius in kilometers
            for station in sainos_response.json().get('stations'):
                lat2, lon2 = station['location']['latitude'], station['location']['longitude']
                lon1, lat1, lon2, lat2 = map(np.radians, [start_lon, start_lat, lon2, lat2])
                dlon = lon2 - lon1
                dlat = lat2 - lat1
                a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
                c = 2 * np.arcsin(np.sqrt(a))
                distance = R * c
                if distance < min_distance:
                    closest_station = station
                    min_distance = distance

                # 315 stations in the UK!

            # prices are per litre or per kWh
            fuel_prices = {
                'gasoline': closest_station['prices']['E10'] / 100,
                'diesel': closest_station['prices']['B7'] / 100,
                'electricity': 0.163
            }

            fuel_needed = driving_distance / fuel_efficiency
            driving_price = fuel_needed * fuel_prices[fuelType]

            if yearlyInsurance != '':
                driving_price += float(yearlyInsurance) / 365
            else:
                driving_price += insurances[carSize][fuelType]

            pt_price = 0.175 * driving_distance

            price_difference = driving_price - pt_price

            msg += f'By using public transport instead of driving, you saved {difference} kgs of co2-equivalent emissions on your {driving_distance}km trip, User! \nDriving would have cost you £{round(driving_price,2)}!\nPublic Transport would have cost an estimated £{pt_price}, meaning you saved £{round(price_difference,2)}!'

            # msg += f"shortest distance between {startingPoint} and a sainsbury's petrol station is {min_distance} km to address: {closest_station['address']}, {closest_station['postcode']}!"

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
    


