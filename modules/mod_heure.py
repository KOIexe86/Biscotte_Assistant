# ---------------------------------------------------------- #
#                    Time module by KOIexe                   #
# ---------------------------------------------------------- #
#  Description: Provides functions related to time           #
#  Available functions: get_time()                           #
# ---------------------------------------------------------- #


# --------------------------
#          Imports
# --------------------------

from config import Debug, LANGUAGE
from modules.mod_utils import say
import datetime

# --------------------------
#         Functions
# --------------------------

def get_time():

    # Get current local time
    now = datetime.datetime.now()
    # Format hour:minute
    heure = now.strftime("%H:%M")

    # Speak in selected language
    if LANGUAGE == "en":
        say(f"It's {heure}")
    else:
        say(f"Il est {heure}")

    # Debug output if enabled
    if Debug:
        print(f"the time is: {heure}")
