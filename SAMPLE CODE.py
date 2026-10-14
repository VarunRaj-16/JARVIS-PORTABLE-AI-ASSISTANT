SAMPLE CODE
import os
import datetime
import webbrowser
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import threading
import tkinter as tk
import time
os.environ['PYWHATKIT_NO_INTERNET_CHECK'] = 'True'
os.environ['http_proxy'] = ""
os.environ['https_proxy'] = ""
try:
 with open("key.txt", "r") as f:
 API_KEY = f.read().strip()
except:
 API_KEY = "YOUR_API_KEY_HERE"
def connect_brain():
 genai.configure(api_key=API_KEY)
 try:
 for m in genai.list_models():
 if 'generateContent' in m.supported_generation_methods:
 return genai.GenerativeModel(m.name), m.name
 except:
 pass
 return None, "Offline"
model, model_name = connect_brain()
APP_MAP = {
 "notepad": "notepad.exe",
 "calculator": "calc.exe",
 "chrome": "chrome.exe",
 "cmd": "cmd.exe",
 "explorer": "explorer.exe",
 "settings": "start ms-settings:"
}
root = tk.Tk()
root.title(f"Jarvis ({model_name})")
root.geometry("400x150")
root.attributes("-topmost", True)
root.configure(bg="#111")
status_label = tk.Label(root, text="ONLINE", font=("Impact", 16), fg="#0f0",
bg="#111")
status_label.pack(pady=10)
log_label = tk.Label(root, text="Waiting...", font=("Consolas", 10), fg="#888",
bg="#111")
log_label.pack()
def update_ui(status, log):
 status_label.config(text=status)
 log_label.config(text=log)
 root.update()
def speak(text):
 try:
 engine = pyttsx3.init('sapi5')
 engine.setProperty('rate', 170)
 engine.say(text)
 engine.runAndWait()
 engine.stop()
 except:
 pass
def run_jarvis():
 r = sr.Recognizer()
 r.dynamic_energy_threshold = True
 speak("System ready.")
 while True:
 try:
with sr.Microphone() as source:
 update_ui("LISTENING...", "Ready")
 r.adjust_for_ambient_noise(source, duration=0.5)
 audio = r.listen(source, timeout=None, phrase_time_limit=10)
 update_ui("THINKING...", "Processing...")
 try:
 raw = r.recognize_google(audio).lower()
 except:
 continue
 cmd = raw.replace("jarvis", "").strip()
 update_ui("EXECUTING", f"'{cmd}'")
 if "open" in cmd and "google" not in cmd and "youtube" not in cmd:
 app = cmd.replace("open", "").replace("launch", "").strip()
 if app in APP_MAP:
 speak(f"Opening {app}")
 os.system(f"start {APP_MAP[app]}")
 continue
 elif "time" in cmd:
 now = datetime.datetime.now().strftime("%I:%M %p")
 speak(f"It is {now}")
 continue
 elif "search" in cmd or "find" in cmd or "look up" in cmd:
 topic = cmd.replace("search for", "").replace("search", "")\
 .replace("find", "").replace("look up", "")\
 .replace("in google", "").replace("on google", "").strip()
 if topic:
 speak(f"Searching Google for {topic}")
 webbrowser.open(f"https://www.google.com/search?q={topic}")
 else:
speak("What would you like me to search for?")
 continue
 elif "open google" in cmd:
 speak("Opening Google")
 webbrowser.open("https://www.google.com")
 continue

 elif "open youtube" in cmd:
 speak("Opening YouTube")
 webbrowser.open("https://www.youtube.com")
 continue
 elif "exit" in cmd:
 speak("Goodbye.")
 os._exit(0)
 else:
 if model:
 try:
 res = model.generate_content(f"Be concise. User: {cmd}")
 speak(res.text)
 except:
 speak("My AI connection is currently limited.")
 else:
 speak("I am offline.")
 except Exception:
 continue
threading.Thread(target=run_jarvis, daemon=True).start()
root.mainloop()
CODE SNIPPET
@echo of
title Jarvis Launcher
color 0a
cls
echo ------------------------------------------
echo INITIALIZING JARVIS SYSTEMS...
echo ------------------------------------------
echo.
:: This command tells the script to look inside the 'windows' folder
:: regardless of what drive letter (D:, E:, F:) the USB uses.
cd /d "%~dp0windows"
:: Launch the executable
start jarvis.exe
:: Close this black window immediately
exit
KEY.TXT
# --- LOAD KEY FROM EXTERNAL FILE ---
try:
 # Looks for key.txt in the same folder as the .exe
 with open("key.txt", "r") as f:
 API_KEY = f.read().strip()
except:
 API_KEY = "YOUR_BACKUP_HARDCODED_KEY_HERE"
REQUIREMENTS.TXT
SpeechRecognition
pyttsx3
google-generativeai
pyaudio