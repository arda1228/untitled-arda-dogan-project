# this file defines the lambda function, which currently gives a boiler plate message
# the plan is to have layers working so that it can make a post request and return some data

import json
import os
# import co2

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))

    carReg = json.loads(event['body'])['carReg']
    startingPoint = json.loads(event['body'])['startingPoint']
    destination = json.loads(event['body'])['destination']

    message = f'hello! my car\'s registration is {carReg}, and i want to know how much money and emissions i\'d save if i used public transport to get from {startingPoint} to {destination} instead of driving!'
    # \n\n{co2.diff(starting_location=startingPoint, destination=destination)}'
    
    # Get the URL of the resource making the request
    origin_url = event.get('headers', {}).get('origin', '')
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain',
            # "Access-Control-Allow-Origin": os.environ['FRONTEND_URL'],
            "Access-Control-Allow-Origin": '*',
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization"
        },
        'body': f"{message}\n\nRequest came from: {origin_url}"
    }