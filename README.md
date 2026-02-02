# Biscotte Voice Assistant (Python)

## Features
- Offline speech recognition with Vosk: https://alphacephei.com/vosk/
- Text-to-speech using edge-tts: https://github.com/rany2/edge-tts
- Voice commands to open websites, launch programs, get the time, weather, etc.
- Optional AI (Google Gemini) integration for natural Q&A and image-aware replies.
- System `status` command to report CPU, memory and network speeds.
- Configuration via `config.py`, `programmes.json`, `sites.json` and `Key.env`.

---

## Prerequisites
- Windows
- Python 3.8+
- FFmpeg (required by imageio-ffmpeg)
- A Vosk model for your language (e.g. `vosk-model-small-fr-0.22` or `vosk-model-small-en-us-0.15`)
- Internet required for AI features (Google Gemini) and for installing Python packages

---

## Installation

1. Clone or download the repository
```powershell
git clone https://github.com/KOIexe86/Biscotte_Assistant.git
cd Biscotte_Assistant
```
> Note: `Start.bat` automates the following steps on Windows.

2. Open a terminal in the project root.
3. Create and activate a virtual environment:
```powershell
python -m venv venv
venv\Scripts\activate
```
4. Upgrade pip and install dependencies:
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## Downloading a Vosk model
1. Visit https://alphacephei.com/vosk/models
2. Download a model for your language (example: `vosk-model-small-fr-0.22`)
3. Extract the model folder into the project root (same folder as `AssistantVocal.py`).

---

## Configuration
- `config.py` controls the assistant behaviour:
  - `NAME`: wake word (default `biscuit` or `biscotte` depending on language)
  - `VOICE`: edge-tts voice identifier (example: `fr-FR-RemyMultilingualNeural`)
  - Model folder names for Vosk (small/big models)
  - `AI`: enable/disable Google Gemini integration
  - `Vision`: enable/disable image analysis for the AI module

- `programmes.json`: map program names to executable paths for the `launch` command
- `sites.json`: map site names to URLs for the `open` command

- `Key.env` (optional): store API keys used by external services. See `EXEMPLE_KEY.env` for the required variables:
  - `OWM_API_Key` — OpenWeatherMap API key (optional, used by the weather module)
  - `GEMINI_API_KEY` — Google Gemini API key (optional, used by the AI module)

To enable AI features:
- Set `AI = True` in `config.py`.
- If you want image-aware responses, set `Vision = True`.
- Add your Gemini API key to `Key.env` (or copy `EXEMPLE_KEY.env` → `Key.env` and update values).

---

## Usage
There are two main ways to start the assistant:

### 1. Using `Start.bat` (recommended on Windows)
Double-click `Start.bat` to:
- activate the virtual environment,
- install missing Python dependencies,
- launch the assistant.

### 2. Running directly
```powershell
python AssistantVocal.py
```

At startup you will be prompted to choose the small (`p`) or large (`g`) speech model.
Speak the configured wake word (for example `biscotte` or the value of `NAME` in `config.py`) to activate the assistant, then speak a command.

---

## Voice Commands
After saying the wake word, you can use commands such as:
- `open <site>` — open a saved website (uses `sites.json`)
- `launch <program>` — start a program from `programmes.json`
- `search <term>` — web search (Google or YouTube)
- `time` — report the current time
- `weather` — get weather information (requires OpenWeatherMap key in `Key.env`)
- `reminder` — add a reminder
- `status` — report CPU usage, memory usage and approximate network speeds
- `stop` — request the assistant to stop (confirm with "yes")

If AI is enabled (`AI = True`), you can also ask natural questions or have a short conversation — the Google Gemini integration can answer general questions and, if `Vision = True`, can also analyze a screen capture to provide contextual help.

---

## New Features (added)
- Google Gemini AI integration (`modules/mod_googleAI.py`) — natural language answers and short dialogs; supports image analysis when `Vision` is enabled. Requires a valid `GEMINI_API_KEY` in `Key.env`.
- `mod_web_search.py` improved to better handle Google and YouTube searches.
- Added English language support. Switch between French and English in `config.py`. Full translation of command, messages, comments, debug and prompt.

---

## Troubleshooting
- "FFmpeg not found by imageio-ffmpeg": install FFmpeg or ensure `imageio-ffmpeg` can access the executable.
- "Please download the model...": verify the model folder exists and matches the names configured in `config.py`.
- Microphone issues: check permissions and the default audio device.
- Missing modules: reinstall dependencies from `requirements.txt`.
- Gemini AI errors: check `Key.env`, set `GEMINI_API_KEY`, and ensure network access.

---

## Contributing
- Edit or add modules under `modules/` to implement new features.
- Update `programmes.json` and `sites.json` to personalize actions.

---

Author: KOIexe
Date: 2026-02-02