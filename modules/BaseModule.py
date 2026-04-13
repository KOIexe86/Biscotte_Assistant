# ---------------------------------------------------------- #
#                    Base Module by KOIexe                   #
# ---------------------------------------------------------- #
#  Description: Base class for all modules                   #
#  Available functions: detecter(), executer()                #
# ---------------------------------------------------------- #


# --------------------------
#          Imports
# --------------------------

from config import Debug


# --------------------------
#           Class
# --------------------------

class Modules:
    def __init__(self, keywords):
        self.keywords = keywords
    
    def detecte(self, text_diviser):
        # Goes through the divided text and checks for keywords
        for i in text_diviser:
            for j in self.keywords:
                if i == j:
                    # Here, the module is detected, we return True to execute the command
                    if Debug:
                        print(f"Module {self.__class__.__name__} detected with keyword: {j}")

                    return True
                
    def execute(self, text):
        # Execute the module's command (has to be defined in each module)
        pass