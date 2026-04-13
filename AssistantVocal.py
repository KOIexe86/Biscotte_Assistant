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
from modules.mod_utils import say, play_sound
from modules.mod_ouvrir_web import mod_ouvrir_web
from modules.mod_weather import mod_weather
from modules.mod_ouvrir_prog import mod_ouvrir_prog
from modules.mod_web_search import mod_web_search
from modules.mod_heure import mod_heure
from modules.mod_status import mod_status
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
# List of all modules available in the assistant, 
# each module is a class that inherits from the base Modules class 
# and implements the executer() method to perform its specific function
# when triggered by a keyword in the user's command.

modules_list = [mod_heure(), mod_ouvrir_web(), mod_weather(), mod_ouvrir_prog(), mod_web_search(), mod_status()]


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
    global assistant_actif

    # Split recognized text into words for keyword matching
    text_diviser = text.split()

    # Check for stop or negative response keywords to immediately stop assistant if detected
    for i in text_diviser:
        if "stop" in i:
            play_sound("Goodbye")
            if Debug:
                print("Stop command detected, stopping assistant")
            exit(0)

        elif "no" in i or "non" in i:
            if Debug:
                print("Negative response detected, stopping assistant")
            return

    # Goes through all modules in modules_list
    for skill in modules_list:
        # Verify if the module's keywords match any word in the recognized text
        if skill.detecte(text_diviser):
            # We execute the module's command if a match is found
            skill.executer(text)
            return
    if Debug:
        print("No module detected in the command, checking for AI response")

    if config.AI:
        # Use AI to respond when no command keyword is found
        askAI(text)
        assistant_actif = True

    else:
            # Play 'not understood' sound to indicate no command detected
        play_sound("Not_understood")
        
        assistant_actif = True
        if Debug:
            print(f"No command found in '{text}', assistant reactivated")
    return


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
        play_sound("Hello")

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
                    play_sound("Yes")
                    continue

                if assistant_actif and phrase:
                    # After one command, put assistant back to sleep until wake name heard again
                    assistant_actif = False
                    if Debug:
                        print("Assistant asleep")

                    # Detect and execute the user's command
                    detectcommande()

        except KeyboardInterrupt:
            # User-requested program termination (Ctrl+C)
            print("[bright_red]User-requested program termination[/bright_red]")
