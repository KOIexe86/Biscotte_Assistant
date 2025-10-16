# ---------------------------------------------------------- #
#                   Heure module by KOIexe                   #
# ---------------------------------------------------------- #
#  Description: Fournit les fonction en rapport avec l'heure #
#  Fonction disponible: heure(), ajout_rappel(text),         #
#                       verifier_rappels()                   #
# ---------------------------------------------------------- #


# --------------------------
#          Imports
# --------------------------

from config import Debug
from modules.mod_utils import dire, texte_en_nombre
import datetime
import time
import threading
from win11toast import toast


# --------------------------
#         Variables
# --------------------------

list_rappels = []


# --------------------------
#         Fonctions
# --------------------------

def get_heure():

    now = datetime.now()
    heure = now.strftime("%H:%M")
    dire(f"Il est {heure}")

    if Debug:
        print(f"Heure actuelle: {heure}")


def Formatage(text):
    brute = text.split("rappel ",1)[1]      # Supprimer le début de la phrase et rappel 
    mots = brute.split()
    
    if "dans" in mots:
        try:
            idx = mots.index("dans")
            mot_nombre = mots[idx + 1]
            minutes = texte_en_nombre(mot_nombre)

            if minutes is None:
                dire("Je n'ai pas compris le nombre de minutes.")
            else:
                contenu = " ".join(mots[0:idx])  # texte avant "dans"
                print(contenu)
                return contenu, minutes

        except Exception as e:
            dire("Je n'ai pas compris le rappel.")
            if Debug:
                print(f"Erreur ajout rappel: {e}")


def ajout_rappel(text):
    try:
        # Formate pour récuperer le contenue et nombre de minutes
        contenu, minutes = Formatage(text)

        if Debug:
            print(f"Contenue du rappel: {contenu} \nDans {minutes} minutes")

        # Détermine l'heure du déclanchement du rappel
        heure = datetime.datetime.now() + datetime.timedelta(minutes=minutes)

        # Ajout du rappel a la list des rappels
        list_rappels.append({"heure": heure, "nom": contenu})

        # Confirme l'ajoute du rappel
        dire(f"Rappel ajouté pour {minutes} minutes : {contenu}")

        if Debug:
            print(f"Ajout du rappel: {contenu}, dans: {minutes}mins soit à: {heure}")

    except Exception as e:
        dire(f"Impossible d'ajouter le rappel, erreur {e}")

        if Debug:
            print(f"Impossible d'ajouter le rappel \nErreur: {e}")


def verifier_rappels():

    # Boucle qui vérifie si un rappel doit être déclenché
    def boucle():
        while True:

            # Récupère l'heure actuel
            maintenant = datetime.datetime.now()

            # Verifie tout les rappels dans list_rappels
            for rappel in list_rappels[:]:  # Copie pour éviter les erreurs
                if maintenant >= rappel["heure"]:
                    # Envoie un toast
                    notif_thread = threading.Thread(
                        target=toast,
                        args=(rappel['nom'], 'Le rappel est passer',),
                        kwargs={'audio': 'ms-winsoundevent:Notification.Reminder'}
                    )
                    notif_thread.start

                    # Dit le rappel
                    dire(f"Rappel : {rappel['nom']}")

                    # Supprime le rappel
                    list_rappels.remove(rappel)

                    if Debug:
                        print(f"Rappel {rappel['nom']} attein et supprimé")

            time.sleep(10)  # Vérifie toutes les 10 secondes

    # Lance la boucle sur un autre thread
    t = threading.Thread(
        target=boucle,
        )
    t.start()
