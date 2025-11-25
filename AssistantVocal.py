# -------------------------------------------------------------- #
#                                                                #
# Projet: Assistant Vocal                                        #
#                                                                #
# Fichier: AssistantVocal.py                                     #
# Auteur: KOIexe                                                 #
# Date: 18/09/2025                                               #
# Python: 3.12.1                                                 #
# Version: 1.5                                                   #
#                                                                #
# Description: Un assistant vocal simple en Python utilisant     #
#              Vosk pour la reconnaissance vocale et edge-tts    #
#              pour la synthèse vocale.                          #
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
from modules.mod_utils import dire
from modules.mod_ouvrir_web import ouvrir_web
from modules.mod_meteo import meteo
from modules.mod_ouvrir_prog import ouvrir_prog
from modules.mod_web_search import web_search
from modules.mod_heure import get_heure, ajout_rappel, verifier_rappels
from modules.mod_status import status
from modules.mod_googleAI import askAI


# --------------------------
#        Constantes
# --------------------------

Debug = config.Debug

FFMPEG_PATH = ffmpeg.get_ffmpeg_exe()
MODEL_PATH = ""

SAMPLE_RATE = 16000

q = queue.Queue()


# --------------------------
#        Variables
# --------------------------

stop = False
parler = True
assistant_actif = False
text = ""
commandeID = -1


# --------------------------
#    Verifications FFMPEG
# --------------------------

if not os.path.exists(FFMPEG_PATH):
    print("FFmpeg introuvable via imageio-ffmpeg")
else:
    if Debug:
        print(f"FFmpeg trouvé: {FFMPEG_PATH}")


# --------------------------
#         Commandes
# --------------------------

list_commande = ["stop", "ouvre", "lance", "cherche", "chercher", "heure", "pile", "météo", "statuts", "rappel", "non",]


# --------------------------
#         Fonctions
# --------------------------

def audio_callback(indata, frames, time, status):   # Fonction de rappel pour capturer l'audio
    if status:
        print(status)
    q.put(bytes(indata))


def ecouter():                     # Fonction pour écouter et reconnaître la parole
    global text

    try:
        data = q.get(timeout=2)
    except queue.Empty:
        print("Pas de signale du micro")
        return ""

    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        text = json.loads(result)["text"]
        if Debug and text:
            print("Reconnu:", text)
        return text
    return ""


def detectcommande():               # Fonction pour détecter les commandes dans le texte reconnu
    global commandeID, assistant_actif

    commandeID = -1

    # Diviser le texte en mots
    text_diviser = text.split()
    for i in list_commande:
        if i in text_diviser:
            # Trouver l'ID de la commande
            commandeID = list_commande.index(i)
            if Debug:
                print(f'Commande détécter: "{i}" son ID est {commandeID}')
    if commandeID == -1:
        if config.AI:
            # Utiliser l'IA pour répondre si aucune commande n'est trouvée
            askAI(text)
        else:
             # Joue le son Pas_compris.mp3 pour signaler que la commande n'a pas été comprise
            playsound("sons\\Pas_compris.mp3")
            assistant_actif = True
            if Debug:
                print(f"Aucune commande trouvé dans {text}, assistant réactivé")
    return commandeID


def executecommande():         # Fonction pour exécuter les commandes détectées
    global text, stop, assistant_actif

    if commandeID == 0:       # Commande "stop"
        if stop == False:     # Première demande d'arrêt
            stop = True
            assistant_actif = True
            dire("Etes-vous sur de vouloir arrêter ? Pour confirmer dites 'stop oui', pour annuler dites 'stop'")
            if Debug:
                print("Arrêt demandé \nAssistant réactivé")

        else:   # Confirmation d'arrêt
            if "oui" in text: 
                # Confirmation de l'arrêt

                print("Arret du programe")
                playsound("sons\\Au_revoir.mp3")
                # Stoppe le programme
                exit()

            else:
                # Annulation de l'arrêt
                
                stop = False
                dire("Annulation de l'arrêt")
                if Debug:
                    print("Arrêt annulé")

    elif commandeID == 1:      # Commande "ouvre"
        ouvrir_web(text)

    elif commandeID == 2:       # Commande "lance"
        ouvrir_prog(text)

    elif commandeID == 3 or commandeID == 4:       # Commande "cherche"
        web_search(text)

    elif commandeID == 5:       # Commande "heure"
        get_heure()

    elif commandeID == 6:       # Commande "pile ou face"
        resultat = random.choice(["pile", "face"])
        dire(f"C'est {resultat}")
        if Debug:
            print(f"Résultat du pile ou face: {resultat}")

    elif commandeID == 7:       # Commande "météo"
        meteo()

    elif commandeID == 8:
        status()
    
    elif commandeID == 9:
        ajout_rappel(text)

    elif commandeID == 10:       # Commande "non"
        if Debug:
            print("Assistant mis en veille")


# --------------------------
#         Main Loop
# --------------------------
if config.TEXTMODE:

    print("[red]Mode texte activé. Tapez vos commandes ci-dessous.[/red]")
    while True:
        phrase = Prompt.ask("[blue]Vous[/blue]")
        text = phrase
        detectcommande()
        executecommande()
else:
    #Choix du modèle
    ask = Prompt.ask("[bright_yellow]Utiliser le modèle petit (p) ou grand (g) ? (p/g)[/bright_yellow]").lower()
    if ask == "p":
        MODEL_PATH = config.SMALL_MODEL_PATH
        ask = "petit"
    elif ask == "g":
        MODEL_PATH = config.BIG_MODEL_PATH
        ask = "grand"
    else:
        print("[bright_red]Choix invalide, utilisation du modèle par défaut ([white]petit[bright_red]).[/bright_red]")
        MODEL_PATH = "vosk-model-small-fr-0.22"
        ask = "petit"

    # Vérification de l'existence du modèle
    if not os.path.exists(MODEL_PATH):
        print ("[bright_red]Veuillez télécharger le modèle depuis https://alphacephei.com/vosk/models et le décompresser dans le dossier courant.[/bright_red]")
        exit(1)

    if Debug:
        print(f"[bright_yellow]Chargement du {ask} modèle ...[/bright_yellow]")

    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)    #Initialisation du reconnaisseur

    #Mic Loop
    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype="int16", channels=1, callback=audio_callback):
        # Joue le son Bonjour.mp3 pour signaler le début du programme
        playsound("sons\\Bonjour.mp3")

        # Commance a verifier les rappels
        verifier_rappels()
        try:
            while True:
                # Écoute pour détéction
                phrase = ecouter()
                if Debug:
                    print("écoute")

                # Détéction de NAME pour commancer l'utilisation des commandes
                if config.NAME in phrase:
                    # Active l'utilisation des commandes
                    assistant_actif = True
                    if Debug:
                        print("Assistant activé")
                    # Joue le son Oui.mp3 pour prévenire que les commandes sont activer
                    playsound("sons\\Oui.mp3")
                    continue

                if assistant_actif and phrase:
                    # Désactive l'utilisation des commandes pour la prochaine utillisation
                    assistant_actif = False
                    if Debug:
                        print("Assistant en veille")

                    # Détècte et execute la commande de l'utilisateur
                    detectcommande()
                    executecommande()

        except KeyboardInterrupt:
            # Si L'utilisateur fait Ctrl + C
            print("[bright_red]Fin du programme demandée par l'utilisateur[/bright_red]")
