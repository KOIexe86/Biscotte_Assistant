# ---------------------------------------------------------- #
#                      Config by KOIexe                      #
# ---------------------------------------------------------- #
#  Description: Fournit des valeurs utilitaires, notamment   #
#               Debug ou VOICE                               #
# ---------------------------------------------------------- #

NAME = "biscotte"

TEXTMODE = False  # Mettre à True pour activer le mode texte (sans reconnaissance vocale)

Debug = True  # Mettre à True pour activer les messages de debug et False pour les désactiver

VOICE="fr-FR-RemyMultilingualNeural" # Voix utilissirée pour la synthèse vocale (edge-tts)

SMALL_MODEL_PATH = "vosk-model-small-fr-0.22" # Nom du petit model vosk

BIG_MODEL_PATH = "vosk-model-fr-0.22"   # Nom du gros model vosk

AI = True #Mettre à True pour activer l'IA (googleAI) ou False pour la désactiver




import json
try:
    with open("programmes.json", encoding="utf-8") as f:
        dic_programme = json.load(f)
except Exception as e:
    print(f"Impossible d'accéder au fichier programmes.json \nErreur: {e}")

try:
    with open("sites.json", encoding="utf-8") as f:
        dic_site = json.load(f)
except Exception as e:
        print(f"Impossible d'accéder au fichier sites.json \nErreur: {e}")