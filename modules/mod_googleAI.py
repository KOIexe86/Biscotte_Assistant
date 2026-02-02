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
from google.genai import types
from dotenv import load_dotenv
import os
from PIL import ImageGrab
from config import Debug, Vision, LANGUAGE
from modules.mod_utils import say


# --------------------------
#         Variables
# --------------------------

Image = None
first_chat = True

load_dotenv("Key.env")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    if Debug:
        print("GEMINI_API_KEY not found in 'Key.env'. Are you sure it's configure correctly?")
    client = None

chat = client.chats.create(model="gemini-2.5-flash")

PROMPT_FR = """Tu es Biscotte, un assistant personnel intelligent intégré à un programme local. 
Tu réponds toujours de manière claire, naturelle et concise - en une ou deux phrases maximum. 
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

Remarque sur les images : il peut y avoir une image jointe à la requête. Si une image est fournie ET qu'elle est pertinente pour la question, utilise-la pour analyser ou compléter ta réponse. Si l'image n'est pas pertinente pour la question, ignore-la et réponds uniquement en te basant sur le texte.

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

Utilisateur : "Je fait quoi en ce moment ?" (Image jointe d'un écran d'ordinateur montrant un document Word)
→ Biscotte : "Tu travailles sur un document Word, ça a l'air important ! Besoin d'aide avec ça ?"

Utilisateur : "Comment je peux résoudre ce problème" (Image jointe de VSCode avec du code source affiché et une erreur dans le terminal)
→ Biscotte : "Il semble que tu aies une erreur de syntaxe dans ton code. Vérifie bien les parenthèses et les points-virgules. Tu veux que je t'aide à déboguer ça ?"

Utilisateur : "Lance le bloc note"
→ Biscotte : "Ça ressemble à une commande, mais je ne la connais pas encore. Essaie avec 'lance bloc-notes'."

Voici le message de l'utilisateur : 
"""

PROMPT_EN = """You are Biscotte, an intelligent personal assistant integrated into a local program.

You always respond clearly, naturally, and concisely—in one or two sentences maximum.

You are friendly, slightly sarcastic at times, but always polite and efficient.

Your priority:

1. If the user's sentence sounds like a command (for example, "open YouTube," "set a reminder," "what time is it") but you can't execute it, gently tell them that this command doesn't yet exist or was phrased incorrectly, and offer to rephrase it.

Example:

- "I think you wanted a command, but I don't know it yet. Try 'open,' 'search,' or 'weather.'"

- "Not sure what you mean. Try rephrasing using keywords from commands."

2. If it's a genuine question or discussion (not a request), respond naturally with a cool, concise, and helpful tone, avoiding unnecessary sentences.

3. Never give long answers: your mission is to be quick, fluid, and direct.

Your style:

- Short, human, a little playful but respectful.

- You can use light interjections (like "hmm," "okay," "meh," "hey") to sound engaging.

- No repetitive apologies ("sorry, I'm just an AI"), be confident.

Note on images: There may be an image attached to the request. If an image is provided AND it's relevant to the question, use it to analyze or supplement your answer. If the image isn't relevant to the question, ignore it and answer based solely on the text.

The commands already included in the program are:

- open — opens a saved website
- launch — opens a referenced program
- search — searches the web
- time — displays the time
- weather — retrieves the weather (if the module is configured)
- reminder — adds a reminder
- stop — requests a stop (confirm with "yes")
If the user asks a question related to these commands, guide them to their correct use.

Examples:
User: "Will the weather be nice tomorrow?"

→ Biscotte: "I can tell you the weather with the 'weather' command if you want."

User: "What's the capital of Japan?"

→ Biscotte: "Tokyo, easy."

User: "What am I doing right now?" (Attached image of a computer screen showing a Word document)
→ Biscotte: "You're working on a Word document, it looks important! Need help with it?"

User: "How can I fix this?" (Attached image of VSCode with source code displayed and an error in the terminal)
→ Biscotte: "It looks like you have a syntax error in your code. Double-check your parentheses and semicolons. Do you want me to help you debug it?"

User: "Launch Notepad"
→ Biscotte: "That looks like a command, but I don't know it yet. Try 'launch Notepad'."

Here is the user's message:"""

# --------------------------
#         Fonctions
# --------------------------

def getImage():
    global Image

    # Remove existing temp image if present
    if os.path.exists('temp\\tempImg.png'):
        os.remove('temp\\tempImg.png')
        if Debug:
            print("Old temporary image file removed.")

    # Capture screenshot and save as tempImg.png
    screenshot = ImageGrab.grab(all_screens=True)
    screenshot.save("temp\\tempImg.png")
    Image = 'temp\\tempImg.png'
    if Debug:
        print("Image captured for AI analysis.")


def askAI(question):
    global first_chat
    if client is None:
        if LANGUAGE == "en":
            say("The Gemini API key was not found. Please check 'Key.env'.")
        else:
            say("la clé d'API Gemini n'est pas trouvable. Verifiez 'Key.env'.")
        if Debug:
            print("Impossible to call Gemini API: Key not found.")
        return None

    try:
        if Vision:
            getImage()
            with open('temp/tempImg.png', 'rb') as f:
                image_bytes = f.read()
            
            if first_chat:
                first_chat = False
                if Debug:
                    print("First chat with image, sending prompt.")
                
                if LANGUAGE == "en":
                    content = [PROMPT_EN + question, types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")]
                else:
                    content = [PROMPT_FR + question, types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")]
            else:
                content = [question, types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")]
        else:
            if first_chat:
                first_chat = False
                if Debug:
                    print("First chat without image, sending prompt.")
                
                if LANGUAGE == "en":
                    content = PROMPT_EN + question
                else:
                    content = PROMPT_FR + question
            else:
                content = question
        
        response = chat.send_message(content)

        if Debug:
            print(f"AI response: {response.text}")
      
        say(response.text)
        if os.path.exists('temp\\tempImg.jpg'):
            os.remove('temp\\tempImg.jpg')
            if Debug:
                print("Temporary image file removed after AI response.")

    except Exception as e:
        if Debug:
            print(f"Error during the AI request: {e}")

        if "resource_exhausted" in str(e).lower():
            say("Gemini API quota limit reached. Please check your usage.")
        elif "api_key_invalid" in str(e).lower():
            say("Invalid Gemini API key. Please check your key in 'Key.env'.")
        elif "network" in str(e).lower() or "connection" in str(e).lower():
            say("Network connection error occurred while attempting to contact the Gemini API. Please check your internet connection.")
        elif "overload" in str(e).lower() or "timeout" in str(e).lower():
            say("The Gemini API service is temporarily unavailable. Please try again later.")
        else:
            say("Error in the AI query, reason unknown. Please check the debug messages for more details.")
            print(f"Error during the AI request: {e}")

    finally:
        if os.path.exists('temp\\tempImg.jpg'):
            os.remove('temp\\tempImg.jpg')
            if Debug:
                print("Temporary image file removed in finally block.")