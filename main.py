from data_manager import DataManager
from flight_data import FlightData
from flight_search import FlightSearch
from notification_manager import NotificationManager
from datetime import datetime, timedelta
import time

#Flight Search
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

#Origin Airport
ORIGIN_CITY_IATA = "ORD"

for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_destination_code(row['city'])
        time.sleep(2)
print(f"Sheet Data:\n {sheet_data}")

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

#Search for flights
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_now = datetime.now() + timedelta(days=180)

for destination in sheet_data:
    print(f"Getting flights for {destination}")
    flights = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_now
    )
    
    cheapest_flight = FlightData.find_cheap_flights(flights)
    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        carrier = flight_search.get_carrier_name(cheapest_flight.carrier)
        message = f"Subject: Low price for {cheapest_flight.destination_airport}\n\nLow price alert! Only ${cheapest_flight.price} to fly \nfrom {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport} on {carrier}, \non {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        message = message.encode(encoding='ascii', errors='namereplace')
        notification_manager.send_message(message=message)