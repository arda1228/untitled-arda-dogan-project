import json

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))

    carReg = json.loads(event['body'])['carReg']
    startingPoint = json.loads(event['body'])['startingPoint']
    destination = json.loads(event['body'])['destination']

    message = f'my car\'s registration is {carReg}, and i want to know how much money and emissions i\'d save if i used public transport to get from {startingPoint} to {destination} instead of driving!'
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': message
    }