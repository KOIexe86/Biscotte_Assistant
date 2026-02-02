# ---------------------------------------------------------- #
#               Open program module by KOIexe                #
# ---------------------------------------------------------- #
#  Description: Provides the function to open programs.      #
#               Works with dic_programme defined             #
#               in progreammes.json                          #
#  Available function: ouvrir_prog(text)                     #
# ---------------------------------------------------------- #


# --------------------------
#          Imports
# --------------------------

from modules.mod_utils import say
import os
from config import Debug, LANGUAGE
from config import dic_programme


# --------------------------
#         Functions
# --------------------------

def Open_prog(text):
    for i in dic_programme.keys():
            # Search for the program name substring in the provided text
            programme = text.find(i)

            if Debug:
                print(f"Searching program: {i} in texte")
            if programme >= 0:
                # Get the actual program path from the dictionary
                programme = dic_programme.get(i)
                try:
                    # Launch the program using the OS
                    os.startfile(programme)
                    if LANGUAGE == "en":
                        say(f"Launching {i}")
                    else:
                        say(f"Lancement de {i}")

                    if Debug:
                        print(f"Launching {programme}")
                except Exception as e:
                    # Handle any exception raised while trying to start the file
                    if LANGUAGE == "en":
                        say(f"I couldn't launch {i} \nproblem encountered: {e}")
                    else:
                        say(f"Je n'ai pas pu lancer {i} \nproblème rencontré: {e}")

                    if Debug:
                        print(f"Lunching {programme} was not possible, error: {e}")
                break
