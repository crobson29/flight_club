import os
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

SHEETY_END = os.environ["Sheety_GET"]


class DataManager:
    def __init__(self):
        self._user = os.environ["Sheety_User"]
        self._password = os.environ["Sheety_password"]
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.destination_data = {}
        
    def get_destination_data(self):
        response = requests.get(url=SHEETY_END)
        data = response.json()
        
        self.destination_data = data["flights"]
        
        return self.destination_data
    
    
    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "flight": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{SHEETY_END}/{city["id"]}", json=new_data)