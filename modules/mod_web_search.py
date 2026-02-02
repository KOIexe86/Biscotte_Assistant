# ---------------------------------------------------------- #
#                Web search module by KOIexe                 #
# ---------------------------------------------------------- #
#  Description: Provides function to perform web searches    #
#               (Google / YouTube).                          #
#  Available function: web_search(text)                      #
# ---------------------------------------------------------- #


# --------------------------
#          Imports
# --------------------------

import webbrowser as wb
from config import Debug, LANGUAGE
from modules.mod_utils import say


# --------------------------
#         Variables
# --------------------------

# Keywords tolerated before the search term for Google and YouTube
tolerance_google = ["cherche ", "chercher ", "google "]
tolerance_ytb = ["cherche ", "chercher ", "youtube "]


# --------------------------
#         Functions
# --------------------------

def web_search(text):
    # Determine target (google or youtube) and extract search query
    if "google" in text:
        for i in tolerance_google:
            if i in text:
                cherche = "google"
                text_split = text.split(i,1)[1]      # Delete the beginning of the sentence and i
                if Debug:
                    print(f"{i} found in the search command")

    elif "youtube" in text:
        for i in tolerance_ytb:
            if i in text:
                cherche = "youtube"
                text_split = text.split(i,1)[1]      # Delete the beginning of the sentence and i
                print(type(text_split))
                if Debug:
                    print(f"{i} found in the search command")

    else:
        # Handle case where target is not determined
        if Debug:
            print("Error in the search command")
        if LANGUAGE == "en":
            say("I couldn't determine where to search (google or youtube).")
        else:
            say("Je n'ai pas pu déterminer où faire la recherche (google ou youtube).")
        return

    # Check if search query is empty
    if text_split == "":
        if LANGUAGE == "en":
            say("You didn't specify what to search for.")
        else:
            say("Vous n'avez pas précisé ce que je dois rechercher.")
        return
    
    # Replace spaces with '+' for URL encoding (simple approach)
    text_modifie = ""
    for lettre in text_split:
        if lettre == " ":
            text_modifie += "+"
        else:
            text_modifie += lettre
    if Debug:
        print(f"Text input: '{text}', modified text: '{text_modifie}'")

    try:
        if cherche == "google":
            wb.open(f"https://www.google.com/search?q={text_modifie}")
            if LANGUAGE == "en":
                say(f"Searching for {text_split} on google")
            else:
                say(f"Recherche de {text_split} sur google")

        elif cherche == "youtube":
            wb.open(f"https://www.youtube.com/search?q={text_modifie}")
            if LANGUAGE == "en":
                say(f"Searching for {text_split} on youtube")
            else:
                say(f"Recherche de {text_split} sur youtube")

    except Exception as e:
        # Inform user via speech helper and log details if debug enabled
        if LANGUAGE == "en":
            say(f"I was unable to search for {text_split} \nproblem encountered: {e}")
        else:
            say(f"Je n'ai pas pu faire la recherche de {text_split} \nproblème rencontré: {e}")

        if Debug:
            print(f"Unable to open search for '{text}': {e}")