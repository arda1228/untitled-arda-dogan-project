import os
from dotenv import load_dotenv
import requests

load_dotenv()

uat_key = os.getenv('VES_KEY_UAT')

prod_key = os.getenv('VES_KEY_PROD')

prod_url = "https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles"

uat_url = "https://uat.driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles"

payload = "{\n\t\"registrationNumber\": \"AA19AAA\"\n}"
headers = {
  'x-api-key': uat_key,
  'Content-Type': 'application/json'
}

response = requests.request("POST", uat_url, headers=headers, data = payload)

print(response.text.encode('utf8'))
print(response.status_code)