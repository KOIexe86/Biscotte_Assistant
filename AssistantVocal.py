# -------------------------------------------------------------- #
#                                                                #
# Project: Voice Assistant                                       #
#                                                                #
# File: AssistantVocal.py                                        #
# Author: KOIexe                                                 #
# Date: 02/02/2026                                               #
# Python: 3.12.1                                                 #
# Version: 2.0                                                   #
#                                                                #
# Description: A simple voice assistant in Python using          #
#              Vosk for speech recognition and edge-tts for      #
#              speech synthesis.                                 #
#                                                                #
# -------------------------------------------------------------- #


# --------------------------
#          Imports
# --------------------------

from playsound3 import playsound
import os
import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer
import imageio_ffmpeg as ffmpeg
import random
from rich import print
from rich.prompt import Prompt


# --------------------------
#          Modules
# --------------------------

import config
from modules.mod_utils import say
from modules.mod_ouvrir_web import Open_website
from modules.mod_meteo import get_weather
from modules.mod_ouvrir_prog import Open_prog
from modules.mod_web_search import web_search
from modules.mod_heure import get_time
from modules.mod_status import status
from modules.mod_googleAI import askAI


# --------------------------
#        Constants
# --------------------------

Debug = config.Debug

LANGUAGE = config.LANGUAGE
FFMPEG_PATH = ffmpeg.get_ffmpeg_exe()
MODEL_PATH = ""

SAMPLE_RATE = 16000

q = queue.Queue()  # Queue used to pass raw audio frames from callback to recognizer


# --------------------------
#        Variables
# --------------------------

stop = False
parler = True
assistant_actif = False
text = ""
commandeID = -1


# --------------------------
#    FFMPEG checks
# --------------------------
# Verify ffmpeg executable presence used by edge-tts / media handling

if not os.path.exists(FFMPEG_PATH):
    print("FFmpeg not found using imageio-ffmpeg")
else:
    if Debug:
        print(f"FFmpeg found: {FFMPEG_PATH}")


# --------------------------
#         Commands
# --------------------------
# List of trigger words / command keywords recognized by the assistant

list_commande_fr = ["stop", "ouvre", "lance", "cherche", "chercher", "heure", "pile", "météo", "statuts", "non",]
list_commande_en = ["stop", "open", "launch", "search", "search", "time", "tails", "weather", "status", "no",]


# --------------------------
#         Functions
# --------------------------
def audio_callback(indata, frames, time, status):   # Callback function to capture audio frames from the microphone
    if status:
        print(status)
    q.put(bytes(indata))


def ecouter():                     # Listen function: pop audio from queue and run recognizer
    global text

    try:
        data = q.get(timeout=2)
    except queue.Empty:
        print("No audio input detected")
        return ""

    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        text = json.loads(result)["text"]
        if Debug and text:
            print("Recognized:", text)
        return text
    return ""


def detectcommande():               # Detect command: search for command keywords in the recognized text
    global commandeID, assistant_actif

    commandeID = -1

    # Split recognized text into words for keyword matching
    text_diviser = text.split()
    if LANGUAGE == "en":
        list_commande = list_commande_en
    else:
        list_commande = list_commande_fr
    
    for i in list_commande:
        if i in text_diviser:
            # Find command ID from the keyword list
            commandeID = list_commande.index(i)
            if Debug:
                print(f'Command detected: "{i}" the ID is {commandeID}')

    if commandeID == -1:
        if config.AI:
            # Use AI to respond when no command keyword is found
            askAI(text)

        else:
             # Play 'not understood' sound to indicate no command detected
            if LANGUAGE == "en":
                playsound("sons\\en\\Not_understood.mp3")
            else:
                playsound("sons\\fr\\Pas_compris.mp3")
            
            assistant_actif = True
            if Debug:
                print(f"No command found in '{text}', assistant reactivated")
    return commandeID


def executecommande():         # Execute the command identified by detectcommande()
    global text, stop, assistant_actif

    if commandeID == 0:       # "stop" command
        if stop == False:     # First stop request (ask for confirmation)
            stop = True
            assistant_actif = True
            if LANGUAGE == "en":
                say("Are you sure you want to stop? To confirm say 'stop yes', to cancel say 'no'")
            else:
                say("Etes-vous sur de vouloir arrêter ? Pour confirmer dites 'stop oui', pour annuler dites 'stop'")

            if Debug:
                print("Stop requested \nAssistant reactivated for confirmation")

        else:   # Stop confirmation handling
            if "oui" or "yes" in text: 
                # Confirm and exit program
                print("Stopping the assistant as requested by the user.")
                if LANGUAGE == "en":
                    playsound("sons\\en\\Goodbye.mp3")
                else:
                    playsound("sons\\fr\\Au_revoir.mp3")
                exit()
            else:
                # Cancel stop request
                stop = False
                if LANGUAGE == "en":
                    say("Stop cancelled")
                else:
                    say("Annulation de l'arrêt")

                if Debug:
                    print("Stop cancelled")

    elif commandeID == 1:      # "ouvre" (open web)
        Open_website(text)

    elif commandeID == 2:       # Commande "lance"
        Open_prog(text)

    elif commandeID == 3 or commandeID == 4:       # Commande "cherche"
        web_search(text)

    elif commandeID == 5:       # Commande "heure"
        get_time()

    elif commandeID == 6:       # Commande "pile ou face"
        resultat = random.choice(["pile", "face"])
        if LANGUAGE == "en":
            if resultat == "face":
                resultat = "heads"
            else:
                resultat = "tails"
            say(f"It's {resultat}")
        else:
            say(f"C'est {resultat}")
        if Debug:
            print(f"Resault of the heads or tails: {resultat}")

    elif commandeID == 7:       # Commande "météo"
        get_weather()

    elif commandeID == 8:       # Commande "statuts"
        status()

    elif commandeID == 9:      # "non" command
        if Debug:
            print("Assistant asleep")


# --------------------------
#         Main Loop
# --------------------------
# If TEXTMODE is enabled, read commands from keyboard; otherwise use microphone loop
if config.TEXTMODE:

    print("[red]Text mode activated. Write your commands here.[/red]")
    while True:
        phrase = Prompt.ask("[blue]You[/blue]")
        text = phrase
        detectcommande()
        executecommande()
else:
    # Select models based on assistant language setting
    if LANGUAGE == "fr":
        SMALL_MODEL_PATH = config.FR_SMALL_MODEL_PATH
        BIG_MODEL_PATH = config.FR_BIG_MODEL_PATH 

    elif LANGUAGE == "en":
        SMALL_MODEL_PATH = config.EN_SMALL_MODEL_PATH
        BIG_MODEL_PATH = config.EN_BIG_MODEL_PATH
    else:
        print("[bright_red]Language not supported, default models used (french).[/bright_red]")
        SMALL_MODEL_PATH = config.FR_SMALL_MODEL_PATH
        BIG_MODEL_PATH = config.FR_BIG_MODEL_PATH
    
    # Model selection prompt (small or big)
    ask = Prompt.ask("[bright_yellow]What model size ? small (s) or big (b) (default: small)[/bright_yellow]").lower()
    if ask == "s" or ask == "S":
        MODEL_PATH = SMALL_MODEL_PATH
        ask = "small"
    elif ask == "b" or ask == "B":
        MODEL_PATH = BIG_MODEL_PATH
        ask = "big"
    else:
        print("[bright_red]Invalid choice, default model used ([white]small[bright_red]).[/bright_red]")
        MODEL_PATH = SMALL_MODEL_PATH
        ask = "small"
    
    # Validate model exists on disk before loading
    if not os.path.exists(MODEL_PATH):
        print ("[bright_red]The model is not in the active directory \nPlease download the model from[white] https://alphacephei.com/vosk/models [bright_red]and decompresse it in the active folder.[/bright_red]")
        exit(1)

    if Debug:
        print(f"[bright_yellow]Loading of the {ask} model...[/bright_yellow]")

    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)    # Initialize the speech recognizer

    # Microphone loop: open raw input stream and process audio continuously
    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype="int16", channels=1, callback=audio_callback):
        # Play greeting sound to signal start
        if LANGUAGE == "en":
            playsound("sons\\en\\Hello.mp3")
        else:
            playsound("sons\\fr\\Bonjour.mp3")


        try:
            while True:
                # Listen for speech and process recognizer results
                phrase = ecouter()
                if Debug:
                    print("écoute")

                # Detect wake name to enable command processing
                if config.NAME in phrase:
                    assistant_actif = True
                    if Debug:
                        print("Assistant activated")
                    # Play acknowledgement sound to indicate assistant activated
                    if LANGUAGE == "en":
                        playsound("sons\\en\\Yes.mp3")
                    else:
                        playsound("sons\\fr\\Oui.mp3")
                    continue

                if assistant_actif and phrase:
                    # After one command, put assistant back to sleep until wake name heard again
                    assistant_actif = False
                    if Debug:
                        print("Assistant asleep")

                    # Detect and execute the user's command
                    detectcommande()
                    executecommande()

        except KeyboardInterrupt:
            # User-requested program termination (Ctrl+C)
            print("[bright_red]User-requested program termination[/bright_red]")
