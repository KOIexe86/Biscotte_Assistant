# ---------------------------------------------------------- #
#                   Météo module by KOIexe                   #
# ---------------------------------------------------------- #
#  Description: Récupère et annonce la météo actuelle pour   #
#               une ville donnée.                            #
#  Utilise l'API OpenWeatherMap.                             #
#  Nécessite une clé API stockée dans Key.env.               #
#  Fonction disponible: meteo()                              #
# ---------------------------------------------------------- #


# --------------------------
#          Imports
# --------------------------

import os
import requests
import datetime
from dotenv import load_dotenv
from modules.mod_utils import dire
from config import Debug


# --------------------------
#        Variables
# --------------------------

load_dotenv("Key.env")
API_KEY = os.getenv("OWM_API_KEY")
FALLBACK_CITY = "Paris"


# --------------------------
#         Fonctions
# --------------------------

def get_location():
    """
    Try to get location via IP geolocation (ip-api.com).
    Returns dict with keys: city, lat, lon
    """
    try:
        resp = requests.get("http://ip-api.com/json/", timeout=5)
        data = resp.json()
        if data.get("status") == "success":
            return {"city": data.get("city"), "lat": data.get("lat"), "lon": data.get("lon")}
        if Debug:
            print("IP geolocation failed:", data)
    except Exception as e:
        if Debug:
            print("Error contacting IP geo service:", e)
    # Fallback if geolocation fails
    return {"city": FALLBACK_CITY, "lat": None, "lon": None}


def meteo():
    try:
        if Debug:
            print("Récupération de la localisation...")

        loc = get_location()
        CITY = loc.get("city") or FALLBACK_CITY
        if loc.get("lat") is not None and loc.get("lon") is not None:
            URL = f"http://api.openweathermap.org/data/2.5/weather?lat={loc['lat']}&lon={loc['lon']}&appid={API_KEY}&lang=fr"
        
            if Debug:
                print(f"Localisation trouvée: {CITY} (lat: {loc['lat']}, lon: {loc['lon']}) \nUtilisation des coordonnées pour la météo.")

        else:
            URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&lang=fr"

            if Debug:
                print(f"Utilisation du fall back pour la météo: {CITY}")

        response = requests.get(URL, timeout=10)
        data = response.json()
        
        # Récupérer et ajuster l'heure locale
        Timestamp = data['dt']
        Heure_table = datetime.datetime.fromtimestamp(Timestamp)

        # Formatage des heures du lever et coucher du soleil
        lever_soleil = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        coucher_soleil = datetime.datetime.fromtimestamp(data['sys']['sunset'])

        # Formatage de l'heure minuit/midi
        Heure = f"{Heure_table.hour}h"
        soleil = ""
        if Heure_table.hour == 0:
            #Formatage de l'heure du minuit
            Heure = "minuit"

        elif Heure_table.hour == 12:
            #Formatage de l'heure du midi
            Heure = "midi"

        else:
            Heure = f"{Heure_table.hour}h"


        # Déterminer le prochain lever ou coucher du soleil
        if Timestamp < data['sys']['sunset']:
            soleil = "coucher"
            # Formater l'heure du coucher de soleil
            heure_soleil = f"{coucher_soleil.hour}h{coucher_soleil.minute:02d}"

        elif Timestamp > data['sys']['sunrise']:
            soleil = "lever"
            # Formater l'heure de lever du soleil
            heure_soleil = f"{lever_soleil.hour}h{lever_soleil.minute:02d} demain"
        
        else:
            soleil = "coucher"
            heure_soleil = f"{coucher_soleil.hour}h{coucher_soleil.minute:02d}"

        # Récupérer la température
        temp_kelvin = data['main']['temp']
        # Convertir Kelvin en Celsius
        temp = round(temp_kelvin - 273.15, 1)

        # Récupérer la description
        desc = data['weather'][0]['description']

        # Annonce la météo
        if soleil:
            dire(f"A {CITY}, la température à {Heure} est de {temp} degrés avec {desc}. Le {soleil} du soleil est à {heure_soleil}.")
        else:
            dire(f"A {CITY}, la température à {Heure} est de {temp} degrés avec {desc}.")

        if Debug:
            print(f"Météo pour {CITY}: \ntemp: {temp}°C, \ndescription: {desc} \nHeure formater: {Heure} \nHeure non formater: {Heure_table.hour}h{Heure_table.minute:02d} \nSoleil: {soleil}")

    except Exception as e:
        dire(f"Je n'ai pas pu récupérer la météo, problème rencontré: {e}")

        if Debug:
            print(f"Erreur météo: {e}")

