# ---------------------------------------------------------- #
#                    TTS module by KOIexe                    #
# ---------------------------------------------------------- #
#  Description: Fournit les fonctions pour le tts comme      #
#               tts_play ou dire                             #
#  Fonction disponible: tts_play(Text), dire(Text)           #
# ---------------------------------------------------------- #


# --------------------------
#          Imports
# --------------------------

import asyncio
import edge_tts
from playsound3 import playsound
import os
from config import VOICE, Debug
import threading
from win11toast import toast

# --------------------------
#         Variables
# --------------------------

mots_nombres = {
    "zéro": 0,
    "un": 1,
    "une": 1,
    "deux": 2,
    "trois": 3,
    "quatre": 4,
    "cinq": 5,
    "six": 6,
    "sept": 7,
    "huit": 8,
    "neuf": 9,
    "dix": 10,
    "onze": 11,
    "douze": 12,
    "treize": 13,
    "quatorze": 14,
    "quinze": 15,
    "seize": 16,
    "dix-sept": 17,
    "dix huit": 18,
    "dix-neuf": 19,
    "vingt": 20,
    "trente": 30,
    "quarante": 40,
    "cinquante": 50,
    "soixante": 60
}


# --------------------------
#         Fonctions
# --------------------------

def texte_en_nombre(mot):
    try:
        mot = mot.lower()
        if mot in mots_nombres:
            return mots_nombres[mot]
        return None
    except Exception as e:
        if Debug:
            print(f"Erreur lors de la traduction des mots en nombre: {e}")


async def tts_play(Texte):              # Fonction asynchrone pour la synthèse vocale
    # Suppression du fichier temporaire s'il existe
    if os.path.exists("temp.mp3"):
        os.remove("temp.mp3")

    # Envoi du texte à edge-tts
    communicate = edge_tts.Communicate(
        Texte,
        VOICE
    )
    # Sauvegarde temporaire et lecture du fichier audio
    await communicate.save("temp.mp3")
    playsound("temp.mp3")
    os.remove("temp.mp3")


def dire(Texte):                     # Fonction simplifier pour exécuter la synthèse vocale
    asyncio.run(tts_play(Texte))
