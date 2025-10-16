# 🎙️ Assistant Vocal (Python)

Un assistant vocal simple en **Python** utilisant :
- [Vosk](https://alphacephei.com/vosk/) pour la **reconnaissance vocale** (hors ligne),
- [edge-tts](https://github.com/rany2/edge-tts) pour la **synthèse vocale** (voix Microsoft Edge),
- et des commandes personnalisées pour ouvrir des sites ou lancer des programmes.

---

## 📂 Structure du projet
AssistantVocal/  
  ├── vosk-model-small-fr-0.22/\
  ├── AssistantVocal.py\
  ├── requirements.txt\
  ├── Start.bat\
  ├── README.md\
  ├── Oui.mp3\
  ├── Bonjour.mp3\
  ├── Pas_compris.mp3\
  └── Au_revoir.mp3\

---

## ⚙️ Installation

### 1. Cloner ou télécharger le projet
```bash
git clone https://github.com/TON_GITHUB/AssistantVocal.git
cd AssistantVocal
```

### 2. Créer et activer un environnement virtuel (recommandé)
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```
⚠️ Vérifie que requirements.txt contient bien la dernière version de edge-tts (ex. edge-tts==7.2.3).

---

## ▶️ Utilisation
Deux façons de lancer le projet :

### 1. Avec le script Python
```bash
python AssistantVocal.py
```
### 2. Avec le script Windows (start.bat)
Double-clique simplement sur start.bat, qui :
* active l’environnement virtuel,
* installe automatiquement les dépendances manquantes,
* lance l’assistant.

---

## 🎤 Commandes vocales
Active l’assistant en disant "Biscotte", puis donne une commande :
* stop → Ferme le programme
* ouvre [site] → Exemple : "ouvre YouTube"
* lance [programme] → Exemple : "lance VLC"
* non → Met l’assistant en veille

Les sites et programmes sont configurables dans le fichier AssistantVocal.py.

---

## 🛠️ Dépendances principales
* Python ≥ 3.12
* Vosk
* edge-tts
* sounddevice
* playsound3

---

## 🚀 Améliorations possibles
* Ajouter plus de commandes personnalisées
* Gérer plusieurs langues
* Intégrer une interface graphique
* Utiliser un hotword detector plus robuste (Snowboy, Porcupine, etc.)

---

👨‍💻 Auteur : KOIexe
📅 Date : 15/09/2025



