import os
from dotenv import load_dotenv
import requests

load_dotenv()

key = os.getenv('CITYMAPPER_KEY')
url = "https://api.external.citymapper.com/api/1/traveltimes"

req = requests.get(url=url, headers = {"Citymapper-Partner-Key": key}, params={
    "start":"51.525246,0.084672",
    "end":"51.559098,0.074503",
    "traveltime_types":["bike","transit"]
})


print(req.status_code)
print(req.json())