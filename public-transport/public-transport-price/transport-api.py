import requests
import os
from dotenv import load_dotenv

load_dotenv()

app_key = os.getenv('TRANSPORT_APP_KEY')
app_id = os.getenv('TRANSPORT_APP_ID')
# API endpoint URL
url = "https://transportapi.com/v3/uk/public_journey.json"



# Query parameters
# not sure if it works
params = {
    "from":{"postcode":"EC2A+4JE"},
    "destination": "Manchester",
    "date": "2023-05-28",
    "time": "08:00",
    "api_key": "YOUR_API_KEY"
}

# Send GET request
response = requests.get(url, params=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Access the JSON response
    data = response.json()
    # Process the data as needed
    print(data)
else:
    print("Error:", response.status_code)
