# ---------------------------------------------------------- #
#                  Status module by KOIexe                   #
# ---------------------------------------------------------- #
#  Description: Fournit le status actuel de la machine       #
#  Fonction disponible: status()                             #
# ---------------------------------------------------------- #


# --------------------------
#          Imports
# --------------------------

import time
import psutil
from modules.mod_utils import dire
from config import Debug


# --------------------------
#         Fonctions
# --------------------------

def get_network_speed(interval=1):
    net1 = psutil.net_io_counters()
    time.sleep(interval)
    net2 = psutil.net_io_counters()

    bytes_sent = net2.bytes_sent - net1.bytes_sent
    bytes_recv = net2.bytes_recv - net1.bytes_recv

    # Convertir en kb/s
    upload_speed = bytes_sent / interval / 1024
    download_speed = bytes_recv / interval / 1024

    return round(upload_speed, 2), round(download_speed, 2)

def status():
    # Utilisation CPU
    cpu_usage = psutil.cpu_percent(interval=1)

    # Utilisation mémoire
    mem = psutil.virtual_memory()
    total, available, mem_percent, used, free = mem

    # Récupère la vitesse de la connextion
    up, down = get_network_speed()

    # Dit les informations
    if Debug:
        print(f"CPU: {cpu_usage}% \nMemoire: {mem_percent}% \nInternet: \n  Up: {up}kb/s \n  Down: {down}kb/s")
    
    dire(f"Le CPU est à {cpu_usage}% d'utillisation et la mémoire à {mem_percent}%. La vitesse d'internet est de: {up}kilobit seconde d'upload et {down}kilobit seconde de download")

