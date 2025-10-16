# ---------------------------------------------------------- #
#                Web search module by KOIexe                 #
# ---------------------------------------------------------- #
#  Description: Fournit la fonction pour faire des recherche #
#               sur internet.                                #
#  Fonction disponible: web_search(text)                     #
# ---------------------------------------------------------- #


# --------------------------
#          Imports
# --------------------------


from config import Debug
from modules.mod_utils import dire
import webbrowser as wb

tolerance_google = ["cherche ", "chercher ", "google "]
tolerance_ytb = ["cherche ", "chercher ", "youtube "]


# --------------------------
#         Fonctions
# --------------------------

def web_search(text):
    if "google" in text:
        for i in tolerance_google:
            if i in text:
                cherche = "google"
                text_split = text.split(i,1)[1]      # Supprimer le début de la phrase et i
                if Debug:
                    print(f"{i} trouver dans la commande vidéo")

    elif "youtube" in text:
        for i in tolerance_ytb:
            if i in text:
                cherche = "youtube"
                text_split = text.split(i,1)[1]      # Supprimer le début de la phrase et i
                print(type(text_split))
                if Debug:
                    print(f"{i} trouver dans la commande chercher")

    else:
        print("Erreur dans la commande cherche")

    # Remplacer tous les espaces par des '+'
    text_modifie = ""
    for lettre in text_split:
        if lettre == " ":
            text_modifie += "+"
        else:
            text_modifie += lettre
    if Debug:
        print(f"Text de base: '{text}', text modifié: '{text_modifie}'")

    try:
        if cherche == "google":
            wb.open(f"https://www.google.com/search?q={text_modifie}")
            dire(f"Recherche de {text_split} sur google")

        elif cherche == "youtube":
            wb.open(f"https://www.youtube.com/search?q={text_modifie}")
            dire(f"Recherche de {text_split} sur youtube")

    except Exception as e:
        dire(f"Je n'ai pas pu faire la recherche de {text_split} \nproblème rencontré: {e}")

        if Debug:
            print(f"Impossible d'ouvrir la recherche google de {text}: {e}")