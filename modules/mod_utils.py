# ---------------------------------------------------------- #
#                    TTS module by KOIexe                    #
# ---------------------------------------------------------- #
#  Description: Provides functions for TTS such as           #
#               tts_play and dire                            #
#  Available functions: tts_play(Text), dire(Text)           #
# ---------------------------------------------------------- #


# --------------------------
#          Imports
# --------------------------

import asyncio
import edge_tts
from playsound3 import playsound
import os
from rich import print
import random
from config import VOICE, Debug, TEXTMODE, LANGUAGE, sounds


# --------------------------
#         Functions
# --------------------------

# Asynchronous function for text-to-speech synthesis
async def tts_play(Texte):
    # Remove temporary file if it exists
    if os.path.exists("temp/temp.mp3"):
        os.remove("temp/temp.mp3")
    
    if Debug:
        print(f"Text-to-speech in progress for the text: {Texte}")
    if not Texte or not str(Texte).strip():
        if Debug:
            print("Empty text provided to tts_play, skipping synthesis.")
        return
    # Send the text to edge-tts
    communicate = edge_tts.Communicate(
        Texte,
        VOICE,
    )

    # Save temporary audio file and play it
    try:
        await communicate.save("temp/temp.mp3")
    except edge_tts.exceptions.NoAudioReceived as e:
        if Debug:
            print(f"No audio recived by edge-tts: {e}")
        raise
    except Exception as e:
        if Debug:
            print(f"Error in the audio generation by edge-tts: {e}")
        raise

    try:
        playsound("temp/temp.mp3")
    except Exception as e:
        if Debug:
            print(f"Error while playing the audio: {e}")

    if Debug:
        print("Audio playback completed, removing temporary file.")
    try:
        os.remove("temp/temp.mp3")
    except Exception:
        pass


# Simplified wrapper to trigger speech synthesis (prints text when TEXTMODE enabled)
def say(Texte):
    if TEXTMODE:
        print("[green]Biscotte:", Texte)
    else:
        try:
            asyncio.run(tts_play(Texte))
        except edge_tts.exceptions.NoAudioReceived:
            if Debug:
                print("No audio received from edge-tts, please check voice settings and network connection. Displaying text in consol instead.")
            print("[green]Biscotte:", Texte)
        except Exception as e:
            if Debug:
                print(f"Error during speech synthesis: {e} \nDisplaying text in consol instead.")
            print("[green]Biscotte:", Texte)


def play_sound(Category):
    try:
        if Category in sounds and LANGUAGE in sounds[Category]:
            sound = random.choice(sounds[Category][LANGUAGE])
            try:
                path = "sons\\" + Category + "\\" + LANGUAGE + "\\" + sound["File"]
                if os.path.exists(path):
                    playsound(path)

                    if Debug:
                        print(f"Playing sound: {sound['Name']} from file {path} with content: {sound['Content']}")
            
            except Exception as e:
                print(f"Error while trying to play sound {sound} \nError: {e}")

        else:
            print(f"Category '{Category}' not found in json.")

    except Exception as e:
        print(f"Error while trying to play category {Category} in json \nError: {e}")
