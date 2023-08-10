# this file defines the lambda function, which currently gives a boiler plate message
# the plan is to have layers working so that it can make a post request and return some data

import json
import os
import requests

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))

    carSize = json.loads(event['body'])['carSize']
    fuelType = json.loads(event['body'])['fuelType']
    startingPoint = json.loads(event['body'])['startingPoint']
    destination = json.loads(event['body'])['destination']
    
    # Get the URL of the resource making the request
    origin_url = event.get('headers', {}).get('origin', '')


    co2_t_url = os.environ['CO2_T_URL']
    # co2_st_url = os.environ['CO2_ST_URL']
    co2_st_api_key = os.environ['CO2_ST_API_KEY']


    # finding driving emissions
    # driving_data = {
    #     "from": startingPoint,
    #     "to": destination,
    #     "transport_types": [
    #         "driving"
    #     ]
    # }

    

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
            difference = co2e_values[0] - co2e_values[1]
            msg = f'by using public transport instead of driving, you saved {difference} kgs of co2!'
            return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'text/plain',
                        # "Access-Control-Allow-Origin": os.environ['FRONTEND_URL'],
                        "Access-Control-Allow-Origin": '*',
                        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                        "Access-Control-Allow-Headers": "Content-Type, Authorization"
                    },
                    'body': f"{msg}\n\nRequest came from:{origin_url}\n\n"
                }
        else:
            print(f"POST request failed with status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the POST request: {e}")
        return None
    


