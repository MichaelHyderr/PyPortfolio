import requests
from datetime import datetime, timedelta
from google_sheets import GoogleSheetAPI
import math
import os


def date(json_date):
    raw_date = json_date.split("T")[0].split("-")  # .split crea una lista in cui elementi sono separati da il char fra le parentesi
    date_f = f"{raw_date[2]}/{raw_date[1]}/{raw_date[0]}"
    return date_f


def flight_time(time):
    mins = int((time % 3600) / 60)
    hours = math.floor(time / 3600)
    return f"{hours}:{mins}"

# ISTRUZIONI : https://tequila.kiwi.com/portal/getting-started

tomorrow = (datetime.now() + timedelta(1)).strftime("%d/%m/%Y")  # .now() è oggi + timedelta(1) cioè un giorno in più e poi con strftime cambio la formattazione
six_months = (datetime.now() + timedelta(6 * 30)).strftime("%d/%m/%Y")

kiwi_api_key = os.getenv('kiwi_api_key')
kiwi_api_key_header = {"apikey": kiwi_api_key}

google = GoogleSheetAPI()
google.spreadsheet = os.getenv("flight_deals_sheet_id")
google.range_name = "destinations"
google_result = google.execute_google_method("read")  # leggo la tabella

data_sheet = google_result.json


# -------- POPOLA IATA CODES IN CASO NON SIANO PRESENTI --------

for n in range(len(data_sheet["IATA Code"])):  # n rappresenta il numero di destinazioni nello sheet
    if data_sheet["IATA Code"][n] == "":  # se sullo sheet non è presente uno IATA code di una città che ho selezionato
        city = data_sheet["City"][n]
        kiwi_endpoint = "https://api.tequila.kiwi.com/locations/query"
        kiwi_params = {"term": city}
        kiwi_response = requests.get(url=kiwi_endpoint, params=kiwi_params, headers=kiwi_api_key_header)
        kiwi_response.raise_for_status()
        kiwi_data = kiwi_response.json()
        city_code = (kiwi_data["locations"][0]["code"])

        google.range_name = f"B{n + 2}"
        google.values = [[city_code]]
        google_result = google.execute_google_method("update")
        print(google_result)


# ------------------------- SHEET SEARCH --------------------------

kiwi_endpoint = "https://api.tequila.kiwi.com/v2/search"

line = 1
for city_code in data_sheet["IATA Code"]:  # creo i parametri per kiwi
    line += 1
    kiwi_params = {
        "fly_from": "ROM",
        "fly_to": city_code,
        "date_from": tomorrow,
        "date_to": six_months,
        "nights_in_dst_from": 7,
        "nights_in_dst_to": 28,
        "flight_type": "round",
        "one_for_city": 1,  # prezzo più basso
        "max_stopovers": 0,  # num di scali andata + ritorno
        "curr": "EUR"
    }
    kiwi_response = requests.get(url=kiwi_endpoint, params=kiwi_params, headers=kiwi_api_key_header)
    kiwi_response.raise_for_status()
    data = kiwi_response.json()
    flight = data["data"]

    row = []  # preparo la lista da dare a google API per popolare lo sheet
    try:
        row.append(flight[0]["price"])
        row.append(date(flight[0]["route"][0]["local_departure"].split("T")[0]))
        row.append(flight[0]["route"][0]["local_departure"].split("T")[1].split(".")[0])
        row.append(date(flight[0]["route"][0]["local_arrival"].split("T")[0]))
        row.append(flight[0]["route"][0]["local_arrival"].split("T")[1].split(".")[0])
        row.append(flight_time(flight[0]["duration"]["departure"]))
        row.append(flight[0]["nightsInDest"])
        row.append(date(flight[0]["route"][1]["local_departure"].split("T")[0]))
        row.append(flight[0]["route"][1]["local_departure"].split("T")[1].split(".")[0])
        row.append(date(flight[0]["route"][1]["local_arrival"].split("T")[0]))
        row.append(flight[0]["route"][1]["local_arrival"].split("T")[1].split(".")[0])
        row.append(flight_time(flight[0]["duration"]["return"]))

        google.range_name = f"C{line}"  # line corrisponde alla riga dello sheet che ad ogni for loop aumenta di 1
        google.values = [row]
        google_result = google.execute_google_method("update")
        print(google_result)

    except IndexError:
        print("Flight Not Found")
        continue
