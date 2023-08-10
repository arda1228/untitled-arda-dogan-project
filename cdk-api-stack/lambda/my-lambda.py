# this file defines the lambda function, which currently gives a boiler plate message
# the plan is to have layers working so that it can make a post request and return some data

import json
import os
import requests

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))

    carReg = json.loads(event['body'])['carReg']
    startingPoint = json.loads(event['body'])['startingPoint']
    destination = json.loads(event['body'])['destination']

    message = f'hello! my car\'s registration is {carReg}, and i want to know how much money and emissions i\'d save if i used public transport to get from {startingPoint} to {destination} instead of driving!\n\n'
    
    # Get the URL of the resource making the request
    origin_url = event.get('headers', {}).get('origin', '')



    co2_st_url = os.environ['CO2_ST_URL']
    co2_st_api_key = os.environ['CO2_ST_API_KEY']


    # finding driing emissions
    driving_data = {
        "from": startingPoint,
        "to": destination,
        "transport_types": [
            "driving"
        ]
    }

    headers = {
        "Authorization": f"Bearer {co2_st_api_key}"
    }

    try:
        driving_response = requests.post(co2_st_url, json=driving_data, headers=headers)

        if driving_response.status_code == 200:
            driving_result = driving_response.json()
            driving_emissions = driving_result['trips'][0]['co2e']

            # finding pt emissions
            pt_data = {
                "from": startingPoint,
                "to": destination,
                "transport_types": [
                    "public-transport"
                ]
            }

            try:
                pt_response = requests.post(co2_st_url, json=pt_data, headers=headers)

                if pt_response.status_code == 200:
                    pt_result = pt_response.json()
                    pt_emissions = pt_result['trips'][0]['co2e']

                    # comparing them

                    comparison_msg = f'you would save {driving_emissions - pt_emissions} kgs of carbon dioxide!'
                    return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'text/plain',
                        "Access-Control-Allow-Origin": os.environ['FRONTEND_URL'],
                        # "Access-Control-Allow-Origin": '*',
                        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                        "Access-Control-Allow-Headers": "Content-Type, Authorization"
                    },
                    'body': f"{message}\n\n{comparison_msg}\n\nRequest came from:{origin_url}\n\n"
                }

                else:
                    print(f"POST request failed with status code: {driving_response.status_code}")
                    return None

            except requests.exceptions.RequestException as e:
                print(f"An error occurred during the POST request: {e}")
                return None

        else:
            print(f"POST request failed with status code: {driving_response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the POST request: {e}")
        return None