import os
from dotenv import load_dotenv

import co2_pt
import co2_driving

load_dotenv()

co2_st_url = os.getenv('CO2_ST_URL')
co2_st_api_key = os.getenv('CO2_ST_API_KEY')


def diff(starting_location, destination):
    result = co2_driving.driving_emissions(starting_location, destination) - co2_pt.pt_emissions(starting_location, destination)
    
    return f'by using public transport instead of driving, you\'d save {result} kgs of carbon!'