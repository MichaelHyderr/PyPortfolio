import os
import requests
from datetime import datetime, timedelta


tomorrow = (datetime.now() + timedelta(1)).strftime("%d/%m/%Y")
six_months = (datetime.now() + timedelta(6 * 30)).strftime("%d/%m/%Y")

# ------------------- MANUAL SEARCH ONLY -------------------
kiwi_endpoint = "https://api.tequila.kiwi.com/v2/search"
kiwi_api_key = os.getenv('kiwi_api_key')
kiwi_api_key_header = {"apikey": kiwi_api_key}


kiwi_params = {
    "fly_from": "NBO",
    "fly_to": "ROM",
    "date_from": tomorrow,
    "date_to": six_months,
    # "dtime_to": "08:00", # orario massimo di partenza
    "nights_in_dst_from": 5,
    "nights_in_dst_to": 10,
    "flight_type": "round",
    # "select_airlines": "ET",
    "one_for_city": 1,
    "max_stopovers": 2,
    "curr": "EUR",
}
# For more options click here : https://tequila.kiwi.com/portal/docs/tequila_api/search_api

kiwi_response = requests.get(url=kiwi_endpoint, params=kiwi_params, headers=kiwi_api_key_header)
data = kiwi_response.json()
flight = data["data"]
print(flight)
price = flight[0]["price"]

print(f"Flight: €{price}")
