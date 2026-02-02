# ---------------------------------------------------------- #
#                  Status module by KOIexe                   #
# ---------------------------------------------------------- #
#  Description: Provides the current machine status          #
#  Available function: status()                              #
# ---------------------------------------------------------- #


# --------------------------
#          Imports
# --------------------------

import time
import psutil
from modules.mod_utils import say
from config import Debug, LANGUAGE


# --------------------------
#         Functions
# --------------------------
# Utility to measure network speed over a short interval (returns upload, download in KB/s)
def get_network_speed(interval=1):
    net1 = psutil.net_io_counters()
    time.sleep(interval)
    net2 = psutil.net_io_counters()

    bytes_sent = net2.bytes_sent - net1.bytes_sent
    bytes_recv = net2.bytes_recv - net1.bytes_recv

    # Convert to kb/s
    upload_speed = bytes_sent / interval / 1024
    download_speed = bytes_recv / interval / 1024

    return round(upload_speed, 2), round(download_speed, 2)

# Gather CPU, memory and network information and speak or print the results
def status():
    # CPU usage percentage (sampled over 1 second)
    cpu_usage = psutil.cpu_percent(interval=1)

    # Memory usage information
    mem = psutil.virtual_memory()
    total, available, mem_percent, used, free = mem

    # Get current connection speed (upload and download)
    up, down = get_network_speed()

    # Debug output to console if enabled
    if Debug:
        print(f"CPU: {cpu_usage}% \nMemory: {mem_percent}% \nInternet: \n  Up: {up}kb/s \n  Down: {down}kb/s")

    # Speak the gathered information in the configured language
    if LANGUAGE == "en":
        say(f"The CPU is at {cpu_usage}% usage and the memory at {mem_percent}%. The internet speed is: {up} kilobit per second upload and {down} kilobit per second download")
    else:
        say(f"Le CPU est à {cpu_usage}% d'utillisation et la mémoire à {mem_percent}%. La vitesse d'internet est de: {up} kilobit seconde d'upload et {down} kilobit seconde de download")

