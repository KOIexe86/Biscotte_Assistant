# ---------------------------------------------------------- #
#                Web browser module by KOIexe                #
# ---------------------------------------------------------- #
#  Description: Fournit la fonction pour ouvrir des sites    #
#               internet.                                    #
#  Fonctionne avec dic_site dans dictionnaire.py.            #
#  Fonction disponible: ouvrir_web(text)                     #
# ---------------------------------------------------------- #


# --------------------------
#          Imports
# --------------------------

from modules.mod_utils import dire
import webbrowser as wb
from config import Debug
from config import dic_site


# --------------------------
#         Fonctions
# --------------------------

def ouvrir_web(text):
    for i in dic_site.keys():
            # Chercher le site dans le texte
            site = text.find(i)

            if Debug:
                print(f"Recherche du site: {i} dans le texte")

            if site >= 0:
                # Récupérer l'URL du site
                site = dic_site.get(i)
                try:
                    # Ouvrir le site dans le navigateur par défaut
                    wb.open(site)
                    dire(f"Ouverture de {i}")

                    if Debug:
                        print(f"Ouverture de {site}")
                except Exception as e:
                    # Si une erreur survient
                    dire(f"Je n'ai pas pu ouvrir {i} \nproblème rencontré: {e}")

                    if Debug:
                        print(f"Impossible d'ouvrir {site}: {e}")
                break
