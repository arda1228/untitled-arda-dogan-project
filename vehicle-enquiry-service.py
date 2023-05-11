import os
from dotenv import load_dotenv
import requests

load_dotenv()

key = os.getenv('VES_KEY_TEST')
url = "https://uat.driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles"

# real url below
# https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles

# test url below
# https://uat.driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles

payload = "{\n\t\"registrationNumber\": \"RJ04ULE\"\n}"
headers = {
  'x-api-key': key,
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))
print(response.status_code)