WITH CHATGPT API:
import os
import datetime
import webbrowser
import speech_recognition as sr
import pyttsx3
from openai import OpenAI
import threading
import tkinter as tk
import time
import psutil
import pyautogui
import requests
# ==========================================
# 1. SYSTEM CONFIGURATION & API SETUP
# ==========================================
os.environ['PYWHATKIT_NO_INTERNET_CHECK'] = 'True'
# Securely load the OpenAI API Key
try:
 with open("key.txt", "r") as f:
 API_KEY = f.read().strip()
except:
 API_KEY = "YOUR_OPENAI_API_KEY_HERE"
# Initialize the Brain and the Memory Array
try:
 client = OpenAI(api_key=API_KEY)
 ai_status = "Connected (GPT-3.5)"
 # This array acts as Jarvis's short-term memory
chat_history = [
 {"role": "system", "content": "You are Jarvis, a highly efficient AI assistant. Keep
answers concise."}
 ]
except Exception as e:
 client = None
 ai_status = "Offline"
 chat_history = []
# ==========================================
# 2. LOCAL APPLICATION DICTIONARY
# ==========================================
APP_MAP = {
 "notepad": "notepad.exe",
 "calculator": "calc.exe",
 "chrome": "chrome.exe",
 "cmd": "cmd.exe",
 "explorer": "explorer.exe",
 "settings": "start ms-settings:",
 "task manager": "taskmgr.exe"
}
# ==========================================
# 3. GRAPHICAL USER INTERFACE (GUI)
# ==========================================
root = tk.Tk()
root.title(f"Jarvis Ultimate ({ai_status})")
root.geometry("450x200")
root.attributes("-topmost", True)
root.configure(bg="#050505")
# Main Status Text
status_label = tk.Label(root, text="SYSTEM BOOTING", font=("Impact", 18),
fg="#00ffcc", bg="#050505")
status_label.pack(pady=10)
# Activity Log
log_label = tk.Label(root, text="Initializing subroutines...", font=("Consolas", 10),
fg="#aaaaaa", bg="#050505")
log_label.pack()
# Hardware Stats Bar (Bottom)
stats_label = tk.Label(root, text="CPU: --% | BAT: --%", font=("Consolas", 9),
fg="#555555", bg="#050505")
stats_label.pack(side="bottom", pady=10)
def update_ui(status, log):
 status_label.config(text=status)
 log_label.config(text=log)
 root.update()
def update_hardware_stats():
 """Background loop to check PC health every 3 seconds"""
 while True:
 try:
 cpu = psutil.cpu_percent(interval=None)
 battery = psutil.sensors_battery()
 bat_txt = f"{battery.percent}%" if battery else "AC Power"
 stats_label.config(text=f"CPU: {cpu}% | BAT: {bat_txt}")
 except:
 pass
 time.sleep(3)
# Start hardware monitor in the background
threading.Thread(target=update_hardware_stats, daemon=True).start()
# ==========================================
# 4. VOCAL OUTPUT ENGINE
# ==========================================
def speak(text):
 """Handles text-to-speech without locking the system"""
 print(f"Jarvis: {text}")
 try:
 engine = pyttsx3.init('sapi5')
 engine.setProperty('rate', 175) # Slightly faster, more robotic
 # Change voice to male if available
 voices = engine.getProperty('voices')
 if len(voices) > 0:
 engine.setProperty('voice', voices[0].id)

 engine.say(text)
 engine.runAndWait()
 engine.stop()
 except Exception as e:
 print(f"Audio Error: {e}")
# ==========================================
# 5. EXTERNAL MODULES (Weather & Net)
# ==========================================
def get_weather():
 """Pulls live weather data without needing an API key"""
 try:
 res = requests.get("https://wttr.in/?format=%C+%t", timeout=3)
 return res.text.strip()
 except:
 return "I cannot reach the weather satellite at this time."
# ==========================================
# 6. MAIN INTELLIGENCE LOOP
# ==========================================
def run_jarvis():
 r = sr.Recognizer()
r.dynamic_energy_threshold = True
 speak("All systems are operational. I am listening.")
 while True:
 try:
 with sr.Microphone() as source:
 update_ui("LISTENING...", "Awaiting command")
 r.adjust_for_ambient_noise(source, duration=0.5)
 audio = r.listen(source, timeout=None, phrase_time_limit=10)
 update_ui("PROCESSING...", "Analyzing audio")
 try:
 raw = r.recognize_google(audio).lower()
 except:
 continue # Ignore silence
 # Clean the command
 cmd = raw.replace("jarvis", "").strip()
 if not cmd:
 continue

 update_ui("EXECUTING", f"> {cmd}")
 # --- 6A. SYSTEM OVERRIDES (Instant Execution) ---
 if "exit" in cmd or "shut down" in cmd:
 speak("Powering down. Goodbye, Sir.")
 os._exit(0)
 elif "time" in cmd:
 now = datetime.datetime.now().strftime("%I:%M %p")
 speak(f"The current time is {now}")
 continue

 elif "weather" in cmd:
speak("Checking local sensors.")
 conditions = get_weather()
 speak(f"It is currently {conditions}")
 continue
 # --- 6B. HARDWARE CONTROL (PyAutoGUI) ---
 elif "volume up" in cmd:
 pyautogui.press("volumeup", presses=5)
 speak("Volume increased.")
 continue

 elif "volume down" in cmd:
 pyautogui.press("volumedown", presses=5)
 speak("Volume decreased.")
 continue

 elif "pause" in cmd or "play music" in cmd:
 pyautogui.press("playpause")
 speak("Media toggled.")
 continue
 # --- 6C. APPLICATION LAUNCHER ---
 elif "open" in cmd and "google" not in cmd and "youtube" not in cmd:
 app = cmd.replace("open", "").replace("launch", "").strip()
 if app in APP_MAP:
 speak(f"Launching {app}")
 os.system(f"start {APP_MAP[app]}")
 continue
 # --- 6D. BROWSER NAVIGATION ---
 elif "search" in cmd or "find" in cmd or "look up" in cmd:
 topic = cmd.replace("search for", "").replace("search", "")\
 .replace("find", "").replace("look up", "")\
 .replace("in google", "").replace("on google", "").strip()
if topic:
 speak(f"Searching the web for {topic}")
 webbrowser.open(f"https://www.google.com/search?q={topic}")
 else:
 speak("Please specify what you want to search for.")
 continue
 elif "open google" in cmd:
 speak("Opening Google Chrome")
 webbrowser.open("https://www.google.com")
 continue

 elif "open youtube" in cmd:
 speak("Opening YouTube")
 webbrowser.open("https://www.youtube.com")
 continue
 # --- 6E. AI NEURAL NET (ChatGPT with Memory) ---
 else:
 if client:
 try:
 # Append user question to memory
 chat_history.append({"role": "user", "content": cmd})

 # Ensure memory doesn't get too large (Keep last 10 messages)
 if len(chat_history) > 11:
 chat_history.pop(1) # Remove oldest user message
 chat_history.pop(1) # Remove oldest AI reply
 # Ask the AI
 response = client.chat.completions.create(
 model="gpt-3.5-turbo",
 messages=chat_history,
 max_tokens=150,
temperature=0.7
 )

 answer = response.choices[0].message.content

 # Append AI answer to memory so it remembers for next time
 chat_history.append({"role": "assistant", "content": answer})

 speak(answer)
 except Exception as e:
 print(f"Brain Error: {e}")
 speak("I am having trouble connecting to the OpenAI servers.")
 else:
 speak("My neural net is offline. Please verify the API key.")
 except Exception as e:
 # Catch all other errors to prevent crashes
 print(f"System Error: {e}")
 continue
# ==========================================
# 7. MULTITHREADING LAUNCH
# ==========================================
# Run the voice engine in a background thread so the GUI doesn't freeze
threading.Thread(target=run_jarvis, daemon=True).start()
# Keep the GUI window open
root.mainloop()