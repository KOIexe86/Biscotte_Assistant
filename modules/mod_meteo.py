# ---------------------------------------------------------- #
#                  Weather module by KOIexe                  #
# ---------------------------------------------------------- #
#  Description: Retrieves and announces current weather for  #
#               a given city.                                #
#  Uses the OpenWeatherMap API.                              #
#  Requires an API key stored in Key.env.                    #
#  Available function: meteo()                               #
# ---------------------------------------------------------- #


# --------------------------
#          Imports
# --------------------------

import os
import requests
import datetime
from dotenv import load_dotenv
from modules.mod_utils import say
from config import Debug, LANGUAGE


# --------------------------
#        Variables
# --------------------------

# Load API key from environment file
load_dotenv("Key.env")
API_KEY = os.getenv("OWM_API_KEY")
# Default fallback city when geolocation fails
FALLBACK_CITY = "Paris"


# --------------------------
#         Functions
# --------------------------

def get_location():
	# Try to get approximate location from IP-based geolocation service
	try:
		resp = requests.get("http://ip-api.com/json/", timeout=5)
		data = resp.json()
		if data.get("status") == "success":
			# Return city and coordinates on success
			return {"city": data.get("city"), "lat": data.get("lat"), "lon": data.get("lon")}
		if Debug:
			print("IP geolocation failed:", data)
	# Log exceptions when in debug mode
	except Exception as e:
		if Debug:
			print("Error contacting IP geo service:", e)
	# Fallback if geolocation fails: return default city with no coordinates
	return {"city": FALLBACK_CITY, "lat": None, "lon": None}


def get_weather():
    try:
        if Debug:
            print("Collecting localization information...")

        # Get location (city and optional coordinates)
        loc = get_location()
        CITY = loc.get("city") or FALLBACK_CITY

        # Build OpenWeatherMap request using coordinates if available, otherwise by city name
        if loc.get("lat") is not None and loc.get("lon") is not None:
            URL = f"http://api.openweathermap.org/data/2.5/weather?lat={loc['lat']}&lon={loc['lon']}&appid={API_KEY}&lang=fr"
            if Debug:
                print(f"Localization found: {CITY} (lat: {loc['lat']}, lon: {loc['lon']}) \nUsing coordinates for weather infos")
        else:
            URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&lang=fr"
            if Debug:
                print(f"Using fallback city for weather: {CITY}")

        # Query the weather API
        response = requests.get(URL, timeout=10)
        data = response.json()

        # Retrieve and adjust local time from the returned timestamp
        Timestamp = data['dt']
        Heure_table = datetime.datetime.fromtimestamp(Timestamp)

        # Format sunrise and sunset times
        lever_soleil = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        coucher_soleil = datetime.datetime.fromtimestamp(data['sys']['sunset'])

        # Format hour display, handling midnight and noon
        Heure = f"{Heure_table.hour}h"
        soleil = ""
        if Heure_table.hour == 0:
            # Format midnight
            if LANGUAGE == "en":
                Heure = "midnight"
            else:
                Heure = "minuit"

        elif Heure_table.hour == 12:
            # Format noon
            if LANGUAGE == "en":
                Heure = "noon"
            else:
                Heure = "midi"
                
        else:
            Heure = f"{Heure_table.hour}h"

        # Determine next sunrise or sunset and format its time
        if Timestamp < data['sys']['sunset']:
            # It's before sunset: next event is sunset
            if LANGUAGE == "en":
                soleil = "sunset"
            else:
                soleil = "coucher"
            # Format sunset time with minutes zero-padded
            heure_soleil = f"{coucher_soleil.hour}h{coucher_soleil.minute:02d}"

        elif Timestamp > data['sys']['sunrise']:
            # It's after sunrise: next event is the next day's sunrise
            if LANGUAGE == "en":
                soleil = "sunrise"
            else:
                soleil = "lever"
            # Indicate the sunrise occurs tomorrow
            if LANGUAGE == "en":
                heure_soleil = f"{lever_soleil.hour}h{lever_soleil.minute:02d} tomorrow"
            else:
                heure_soleil = f"{lever_soleil.hour}h{lever_soleil.minute:02d} demain"

        else:
            # Fallback: treat as sunset
            if LANGUAGE == "en":
                soleil = "sunset"
            else:
                soleil = "coucher"
            heure_soleil = f"{coucher_soleil.hour}h{coucher_soleil.minute:02d}"

        # Retrieve temperature in Kelvin and convert to Celsius
        temp_kelvin = data['main']['temp']
        temp = round(temp_kelvin - 273.15, 1)

        # Retrieve weather description text
        desc = data['weather'][0]['description']

        # Announce the weather
        if soleil:
            if LANGUAGE == "en":
                say(f"In {CITY}, the temperature at {Heure} is {temp} degrees with {desc}. The {soleil} of the sun is at {heure_soleil}.")
            else:
                say(f"A {CITY}, la température à {Heure} est de {temp} degrés avec {desc}. Le {soleil} du soleil est à {heure_soleil}.")
        else:
            if LANGUAGE == "en":
                say(f"In {CITY}, the temperature at {Heure} is {temp} degrees with {desc}.")
            else:
                say(f"A {CITY}, la température à {Heure} est de {temp} degrés avec {desc}.")

        if Debug:
            print(f"Weather for {CITY}: \ntemp: {temp}°C, \ndescription: {desc} \nFormated hour: {Heure} \nNon-formated hour: {Heure_table.hour}h{Heure_table.minute:02d} \nSun: {soleil}")

	    # Handle exceptions and announce failure
    except Exception as e:
        if LANGUAGE == "en":
            say(f"I couldn't retrieve the weather, encountered issue: {e}")
        else:
            say(f"Je n'ai pas pu récupérer la météo, problème rencontré: {e}")

        if Debug:
            print(f"Weather error: {e}")

