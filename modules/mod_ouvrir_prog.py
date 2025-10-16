# ---------------------------------------------------------- #
#               Open programe module by KOIexe               #
# ---------------------------------------------------------- #
#  Description: Fournit la fonction pour ouvrir des          #
#               programes.                                   #
#  Fonctionne avec dic_programme dans dictionnaire.py.       #
#  Fonction disponible: ouvrir_prog(text)                    #
# ---------------------------------------------------------- #


# --------------------------
#          Imports
# --------------------------

from modules.mod_utils import dire
import os
from config import Debug
from config import dic_programme


# --------------------------
#         Fonctions
# --------------------------

def ouvrir_prog(text):
    for i in dic_programme.keys():
            # Chercher le programme dans le texte
            programme = text.find(i)

            if Debug:
                print(f"Recherche du programme: {i} dans le texte")
            if programme >= 0:
                # Récupérer le chemin du programme
                programme = dic_programme.get(i)
                try:
                    # Lancer le programme
                    os.startfile(programme)
                    dire(f"Lancement de {i}")

                    if Debug:
                        print(f"Lancement de {programme}")
                except Exception as e:
                    # Si une erreur survient
                    dire(f"Je n'ai pas pu lancer {i} \nproblème rencontré: {e}")

                    if Debug:
                        print(f"Impossible de lancer {programme}: {e}")
