# 🎙️ Assistant Vocal (Python)

## Fonctionnalités
- Reconnaissance vocale hors-ligne [Vosk](https://alphacephei.com/vosk/)
- Synthèse vocale [edge-tts](https://github.com/rany2/edge-tts)
- Commandes pour ouvrir des sites, lancer des programmes, obtenir l'heure, météo, rappels, etc.
- Configuration via `config.py`, `programmes.json` et `sites.json`

---

## ❗ Prérequis
- Windows
- Python 3.8+
- FFmpeg (utilisé par imageio-ffmpeg)
- Modèle Vosk pour le français (petit ou grand)

---

## 📥 Installation

### 1. Cloner ou télécharger le projet
```bash
git clone https://github.com/KOIexe86/Biscotte_Assistant.git
cd AssistantVocal
```
### > Remarque : le fichier `Start.bat` automatise les étapes suivante sur Windows.
### 2. Ouvrir un terminal à la racine du projet.
### 3. Créer et activer un environnement virtuel :
```bash
python -m venv venv
venv\Scripts\activate
```
### 4. Mettre à jour pip et installer les dépendances :
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## ⬇️ Téléchargement du modèle Vosk
### 1. Aller sur https://alphacephei.com/vosk/models
### 2. Télécharger un modèle français (ex. `vosk-model-small-fr-0.22` ou `vosk-model-fr-0.22`)
### 3. Décompresser le dossier du modèle à la racine du projet (même dossier que `AssistantVocal.py`).

---

## ⚙️ Configuration
- `config.py` :
  - NAME : mot d'activation (par défaut "biscotte")
  - VOICE : voix edge-tts (ex. `"fr-FR-RemyMultilingualNeural"`)
  - SMALL_MODEL_PATH / BIG_MODEL_PATH : noms des dossiers de modèle Vosk
- `programmes.json` : chemins des exécutables pour la commande "lance"
- `sites.json` : URLs pour la commande "ouvre"

---

## ▶️ Utilisation
Deux façons de lancer le projet :

### 1. Avec le script start.bat (recommander)
Double-clique simplement sur start.bat, qui :
* active l’environnement virtuel,
* installe automatiquement les dépendances manquantes,
* lance l’assistant.

### 2. Avec le script Python
```bash
python AssistantVocal.py
```
### 3. Au démarrage, choisir le modèle petit (p) ou grand (g).
### 4. Dire le mot d'activation (ex. "biscotte") pour activer l'assistant, puis prononcer une commande.

---

## 🎤 Commandes vocales
Active l’assistant en disant "Biscotte", puis donne une commande :
* ouvrez/ouvre <site> — ouvre un site enregistré
* lance <programme> — ouvre un programme référencé
* cherche / chercher <terme> — recherche sur le web
* heure — donne l'heure
* météo — récupère la météo (si module configuré)
* rappel — ajoute un rappel
* stop — demande d'arrêt (confirmer par "oui")

Les sites et programmes sont configurables dans le fichier AssistantVocal.py.

---

## 🛠️ Dépannage
- "FFmpeg introuvable via imageio-ffmpeg" :
  Installer FFmpeg ou vérifier que imageio-ffmpeg a accès à l'exécutable.
- "Veuillez télécharger le modèle..." :
  Vérifier que le dossier du modèle est bien présent et son nom correspond à `config.py`.
- Problèmes de micro :
  Vérifier les permissions et le périphérique audio par défaut.
- Si des modules manquent, réinstaller les dépendances depuis `requirements.txt`.

---

## Contribuer
- Modifier les fichiers sous `modules/` pour ajouter des fonctionnalités.
- Mettre à jour `programmes.json` et `sites.json` pour personnaliser les actions.

---

👨‍💻 Auteur : KOIexe
📅 Date : 16/10/2025



