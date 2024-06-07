import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"

class FlightSearch:
    def __init__(self):
        self._api_key = os.environ["Amadeus_Key"]
        self._api_secret = os.environ["Amadeus_Secret"]
        self._token = self._get_new_token()
        
    def _get_new_token(self):
        header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": self._api_key,
            "client_secret": self._api_secret
        }
        
        response = requests.post(url=TOKEN_ENDPOINT, headers=header, data=data)
        #print(f"Access token: {response.json()['access_token']}")
        
        return response.json()['access_token']
    
    def get_destination_code(self, city_name):
        headers = {
            "Authorization": f"Bearer {self._token}"
        }
        query = {
            "keyword": city_name,
            "max": "2",
            "include": "AIRPORTS"
        }
        response = requests.get(url=IATA_ENDPOINT, headers=headers, params=query)
        
        try:
            code = response.json()["data"][0]["iataCode"]
        except IndexError:
            print(f"IndexError: No Airport code found for {city_name}")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}")
            return "Not found"
        return code
    
    def check_flights(self, origin_code, destination_code, from_time, to_time):
        headers = {
            "Authorization": f"Bearer {self._token}"
        }
        
        query = {
            "originLocationCode": origin_code,
            "destinationLocationCode": destination_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "currencyCode": "GBP",
            "max": "10"            
        }
        
        response = requests.get(url=FLIGHT_ENDPOINT, headers=headers, params=query)
        
        if response.status_code != 200:
            print(f"check_flights response code: {response.status_code}")
            print(f"Response Body: {response.text}")
            return None
        return response.json()