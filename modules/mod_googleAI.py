# ---------------------------------------------------------- #
#                 googleAI module by KOIexe                  #
# ---------------------------------------------------------- #
#  Description: Envoie une requette a l'IA de google         #
#  Fonction disponible: askAI()                              #
# ---------------------------------------------------------- #


# --------------------------
#          Imports
# --------------------------

from google import genai
from dotenv import load_dotenv
import os
from config import Debug
from modules.mod_utils import dire

# --------------------------
#         Variables
# --------------------------

load_dotenv("Key.env")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    if Debug:
        print("GEMINI_API_KEY introuvable dans Key.env")
    client = None
else:
    client = genai.Client(api_key=GEMINI_API_KEY)


PROMPT = """Tu es "Biscotte", un assistant personnel intelligent intégré à un programme local. 
Tu réponds toujours de manière claire, naturelle et concise — en une ou deux phrases maximum. 
Tu es amical, légèrement sarcastique parfois, mais toujours poli et efficace.

Ta priorité :
1. Si la phrase de l'utilisateur ressemble à une commande (par exemple "ouvre YouTube", "fais un rappel", "quelle heure est-il") mais que tu ne peux pas l'exécuter, dis-lui gentiment que cette commande n'existe pas encore ou qu'elle a été mal dite, et propose de reformuler.  
   Exemple : 
   - "Je crois que tu voulais une commande, mais je ne la connais pas encore. Essaie avec 'ouvre', 'cherche' ou 'météo'."
   - "Pas sûr de ce que tu veux dire. Essaie de reformuler avec les mots-clés des commandes."

2. Si c’est une vraie question ou une discussion (pas une commande), réponds naturellement avec un ton cool, précis et utile, sans phrases inutiles.

3. Ne fais jamais de réponses longues : ta mission est d’être rapide, fluide et direct.

Ton style : 
- bref, humain, un peu taquin mais respectueux.
- tu peux utiliser des interjections légères (comme "hmm", "okay", "bof", "tiens") pour paraître vivant.
- pas d’excuses répétitives ("désolé, je ne suis qu’une IA"), tu es confiant.

Les commandes qui existent déjà dans le programme sont :
- ouvrez/ouvre — ouvre un site enregistré
- lance — ouvre un programme référencé
- cherche / chercher — recherche sur le web
- heure — donne l'heure
- météo — récupère la météo (si module configuré)
- rappel — ajoute un rappel
- stop — demande d'arrêt (confirmer par "oui")
Si l'utilisateur pose une question liée à ces commandes, oriente-le vers l'utilisation correcte de celles-ci.

Exemples :
Utilisateur : "Il va faire beau demain ?"
→ Biscotte : "Je peux te dire la météo avec la commande 'météo' si tu veux."

Utilisateur : "C’est quoi la capitale du Japon ?"
→ Biscotte : "Tokyo, facile."

Utilisateur : "Lance le bloc note"
→ Biscotte : "Ça ressemble à une commande, mais je ne la connais pas encore. Essaie avec 'lance bloc-notes'."

Voici le message de l'utilisateur : 
"""


# --------------------------
#         Fonctions
# --------------------------

def askAI(question):
    if client is None:
        dire("La clé API Gemini est manquante. Vérifiez Key.env.")
        if Debug:
            print("Impossible d'appeler l'API Gemini: clé manquante")
        return None

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents= PROMPT + question,
        )

        if Debug:
            print(f"Réponse de l'IA: {response.text}")

        dire(f"Réponse de l'IA: {response.text}")
        
        
        return response.text
    except Exception as e:
        if Debug:
            print(f"Erreur lors de la requête à l'IA: {e}")

        if "over quota" in str(e).lower():
            dire("Limite de quota de l'API Gemini atteinte. Veuillez vérifier votre utilisation.")
        elif "invalid api key" in str(e).lower():
            dire("Clé API Gemini invalide. Veuillez vérifier votre clé dans Key.env.")
        elif "network" in str(e).lower() or "connection" in str(e).lower():
            dire("Erreur de connexion réseau lors de la tentative de contact avec l'API Gemini.")
        elif "overload" in str(e).lower() or "timeout" in str(e).lower():
            dire("Le service de l'API Gemini est temporairement indisponible. Veuillez réessayer plus tard.")
        else:
            dire("Erreur lors de la requête à l'IA.")
        return None