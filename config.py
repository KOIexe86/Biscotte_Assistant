# ---------------------------------------------------------- #
#                      Config by KOIexe                      #
# ---------------------------------------------------------- #
#  Description: Provides utility values, including           #
#               Debug or VOICE                               #
# ---------------------------------------------------------- #


# --------------------------
#      General Config
# --------------------------

TEXTMODE = False  # Set to True to enable text mode (without voice recognition)
Debug = True  # Set to True to enable debug messages and False to disable them

# English configuration
VOICE="en-US-BrianNeural" # Voice used for speech synthesis (edge-tts)
LANGUAGE = "en"  # Language of the voice assistant ('en' for English,)
NAME = "biscuit" # Wake name of the voice assistant

# French configuration
# LANGUAGE = "fr"  # Language of the voice assistant ('fr' for French)
# NAME = "biscotte" # Wake name of the voice assistant
# VOICE="fr-FR-RemyMultilingualNeural" # Voice used for speech synthesis (edge-tts)

# Recommended voices:
# French: 
#   Female: fr-FR-VivienneMultilingualNeural
#   Male: fr-FR-RemyMultilingualNeural
# 
# English: 
#   Female: en-US-AvaNeural, en-US-EmmaNeural
#   Male: en-US-BrianNeural, en-US-SteffanNeural
# 
# See https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support?tabs=tts for more voices.
# Or test them here: https://tts.travisvn.com/


# --------------------------
#        Vosk Models
# --------------------------

# Vosk speech recognition model paths
FR_SMALL_MODEL_PATH = "vosk-model-small-fr-0.22" # Name of the small french Vosk model
FR_BIG_MODEL_PATH = "vosk-model-fr-0.22"   # Name of the large french Vosk model

EN_SMALL_MODEL_PATH = "vosk-model-small-en-us-0.15" # Name of the small english Vosk model
EN_BIG_MODEL_PATH = "vosk-model-en-us-0.22"   # Name of the large english Vosk model
# See https://alphacephei.com/vosk/models for more Vosk models.


# --------------------------
#         AI Config
# --------------------------

AI = True # Set to True to enable AI (googleAI) or False to disable it
Vision = True # Set to True to enable AI image analysis or False to disable it


# --------------------------
#    Program & Site Lists
# --------------------------

# Load the mapping of program names and websites used by the assistant.
import json
try:
    with open("programmes.json", encoding="utf-8") as f:
        dic_programme = json.load(f)
except Exception as e:
    print(f"Error while trying to open programmes.json \nError: {e}")

# Load site shortcuts / favorites used by the web-open module.
try:
    with open("sites.json", encoding="utf-8") as f:
        dic_site = json.load(f)
except Exception as e:
        print(f"Error while trying to open sites.json \nError: {e}")