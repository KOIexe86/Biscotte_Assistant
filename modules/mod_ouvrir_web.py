# ---------------------------------------------------------- #
#                Web browser module by KOIexe                #
# ---------------------------------------------------------- #
#  Description: Provides the function to open websites       #
#               Works with dic_site in dictionnaire.py       #
#  Available function: ouvrir_web(text)                      #
# ---------------------------------------------------------- #


# --------------------------
#          Imports
# --------------------------

from modules.mod_utils import say
import webbrowser as wb
from config import Debug, LANGUAGE
from config import dic_site


# --------------------------
#         Functions
# --------------------------

def Open_website(text):
    for i in dic_site.keys():
        # Search for the site keyword in the input text
        site = text.find(i)

        if Debug:
            print(f"Searching site: {i} in texte")

        if site >= 0:
            # Retrieve the URL associated with the found keyword
            site = dic_site.get(i)
            try:
                # Open the URL in the default web browser
                wb.open(site)
                if LANGUAGE == "en":
                    say(f"Opening {i}")
                else:
                    say(f"Ouverture de {i}")

                if Debug:
                    print(f"Opening {site}")
            except Exception as e:
                # If an error occurs, provide feedback in the configured language
                if LANGUAGE == "en":
                    say(f"I couldn't open {i} \nproblem encountered: {e}")
                else:
                    say(f"Je n'ai pas pu ouvrir {i} \nproblème rencontré: {e}")

                if Debug:
                    # Debug: log the URL and error
                    print(f"Not able to open {site}, error: {e}")
            break
    if LANGUAGE == "en":
        say("I couldn't find the website you asked for.")
    else:
        say("Je n'ai pas trouvé le site web que vous avez demandé.")
    if Debug:
        print("Website not found in the list.")
    return
