"""
Advanced PC Assistant with GUI - Voice Controlled Desktop Assistant
Features:
- Modern Dark Mode GUI with CustomTkinter
- Speech recognition and text-to-speech
- Open applications and files
- Browser automation (search, download, YouTube)
- System control (volume, shutdown, etc.)
- Software installation assistance
"""

import speech_recognition as sr
import pyttsx3
import datetime
import os
import subprocess
import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# GUI Imports
import customtkinter as ctk

# Setup CustomTkinter appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PCAssistant:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self.stop_event = threading.Event()
        
        # Browser setup
        self.chrome_options = Options()
        self.chrome_options.add_argument("--start-maximized")
        self.driver = None
        
        # GUI Setup
        self.root = ctk.CTk()
        self.root.title("🤖 AI PC Assistant")
        self.root.geometry("900x700")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Grid configuration
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Header
        self.header_frame = ctk.CTkFrame(self.root, height=60, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.header_frame.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="🤖 AI PC Assistant", 
                                         font=ctk.CTkFont(size=28, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=15)
        
        self.status_indicator = ctk.CTkLabel(self.header_frame, text="● Status: Idle", 
                                              text_color="gray", font=ctk.CTkFont(size=14))
        self.status_indicator.grid(row=0, column=1, padx=20)
        
        # Main Chat/Log Area
        self.log_frame = ctk.CTkScrollableFrame(self.root, label_text="📜 Command Log & Responses",
                                                 label_font=ctk.CTkFont(weight="bold"))
        self.log_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=10)
        self.log_frame.grid_columnconfigure(0, weight=1)
        
        # Control Panel
        self.control_frame = ctk.CTkFrame(self.root, height=80, corner_radius=10)
        self.control_frame.grid(row=2, column=0, sticky="ew", padx=15, pady=10)
        self.control_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.btn_listen = ctk.CTkButton(self.control_frame, text="🎙️ Start Listening", 
                                         command=self.toggle_listening, height=50, 
                                         font=ctk.CTkFont(size=16, weight="bold"),
                                         fg_color="#2CC985", hover_color="#25A86E")
        self.btn_listen.grid(row=0, column=0, padx=10, pady=15)
        
        self.btn_clear = ctk.CTkButton(self.control_frame, text="🗑️ Clear Log", 
                                        command=self.clear_log, height=50,
                                        font=ctk.CTkFont(size=14),
                                        fg_color="#6c757d", hover_color="#5a6268")
        self.btn_clear.grid(row=0, column=1, padx=10, pady=15)
        
        self.btn_manual = ctk.CTkButton(self.control_frame, text="⌨️ Type Command", 
                                         command=self.focus_input, height=50,
                                         font=ctk.CTkFont(size=14),
                                         fg_color="#3498db", hover_color="#2980b9")
        self.btn_manual.grid(row=0, column=2, padx=10, pady=15)
        
        # Input Box
        self.input_frame = ctk.CTkFrame(self.root)
        self.input_frame.grid(row=3, column=0, sticky="ew", padx=15, pady=(0, 15))
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        self.entry_command = ctk.CTkEntry(self.input_frame, placeholder_text="Type a command here... (e.g., 'Install NodeJS', 'Download music Bohemian Rhapsody')", 
                                           height=45, font=ctk.CTkFont(size=14))
        self.entry_command.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.entry_command.bind("<Return>", lambda e: self.process_manual_input())
        
        self.btn_send = ctk.CTkButton(self.input_frame, text="Send ➤", width=100, 
                                       command=self.process_manual_input, height=45,
                                       font=ctk.CTkFont(size=14, weight="bold"))
        self.btn_send.grid(row=0, column=1)

    def log_message(self, sender, message):
        """Add message to GUI log"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        frame = ctk.CTkFrame(self.log_frame, fg_color="transparent")
        frame.pack(fill="x", pady=8, anchor="w" if sender == "You" else "e")
        
        color = "#3498db" if sender == "You" else "#2ecc71"
        align = "w" if sender == "You" else "e"
        
        header = f"[{timestamp}] {sender}:"
        ctk.CTkLabel(frame, text=header, font=ctk.CTkFont(weight="bold", size=13), 
                     text_color=color).pack(anchor=align)
        
        ctk.CTkLabel(frame, text=message, wraplength=800, justify="left" if sender == "You" else "right",
                     font=ctk.CTkFont(size=13)).pack(anchor=align)
        
        # Auto scroll to bottom
        self.log_frame._scrollbar.set(1.0)

    def clear_log(self):
        for widget in self.log_frame.winfo_children():
            widget.destroy()

    def update_status(self, status, color="gray"):
        self.status_indicator.configure(text=f"● Status: {status}", text_color=color)
        self.root.update_idletasks()

    def toggle_listening(self):
        if self.is_listening:
            self.is_listening = False
            self.stop_event.set()
            self.btn_listen.configure(text="🎙️ Start Listening", fg_color="#2CC985")
            self.update_status("Idle", "gray")
            self.speak("Stopped listening.")
        else:
            self.is_listening = True
            self.stop_event.clear()
            self.btn_listen.configure(text="🛑 Stop Listening", fg_color="#E74C3C", 
                                       hover_color="#c0392b")
            self.update_status("Listening...", "#E74C3C")
            self.speak("Listening started. You can speak now.")
            thread = threading.Thread(target=self.listen_loop, daemon=True)
            thread.start()

    def process_manual_input(self):
        command = self.entry_command.get()
        if command.strip():
            self.entry_command.delete(0, 'end')
            self.log_message("You", command)
            self.update_status("Processing...", "#f39c12")
            self.root.after(100, lambda: self.handle_command(command))

    def focus_input(self):
        self.entry_command.focus()

    def on_closing(self):
        self.is_listening = False
        self.stop_event.set()
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
        self.root.destroy()

    def speak(self, text):
        """Text to Speech"""
        self.log_message("Assistant", text)
        self.engine.say(text)
        self.engine.runAndWait()

    def listen_loop(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            while self.is_listening and not self.stop_event.is_set():
                try:
                    self.update_status("Listening...", "#E74C3C")
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    self.update_status("Processing...", "#f39c12")
                    command = self.recognizer.recognize_google(audio)
                    self.log_message("You", command)
                    self.handle_command(command)
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    continue
                except sr.RequestError:
                    self.speak("Network error. Please check your internet connection.")
                    break
                except Exception as e:
                    print(f"Error: {e}")
                    break

    def get_driver(self):
        if self.driver is None:
            try:
                self.driver = webdriver.Chrome(options=self.chrome_options)
            except Exception as e:
                self.speak("Error initializing browser. Make sure Chrome and ChromeDriver are installed.")
                return None
        return self.driver

    def handle_command(self, command):
        cmd = command.lower()
        
        try:
            if any(greet in cmd for greet in ['hello', 'hi', 'hey']):
                self.speak("Hello! I'm your AI PC Assistant. I can open apps, search the web, download YouTube music, install software, and control your system. What would you like me to do?")
            
            elif 'time' in cmd:
                now = datetime.datetime.now().strftime("%I:%M %p")
                self.speak(f"The current time is {now}")
            
            elif 'date' in cmd:
                now = datetime.datetime.now().strftime("%A, %B %d, %Y")
                self.speak(f"Today is {now}")
            
            elif 'open' in cmd:
                app = cmd.replace('open', '').strip()
                self.speak(f"Opening {app}...")
                try:
                    subprocess.Popen([app])
                except FileNotFoundError:
                    self.speak(f"Could not find {app} directly. Searching for it...")
                    self.search_and_open(app)
            
            elif 'search' in cmd or 'google' in cmd:
                query = cmd.replace('search', '').replace('google', '').replace('for', '').strip()
                if query:
                    self.speak(f"Searching Google for {query}")
                    driver = self.get_driver()
                    if driver:
                        driver.get(f"https://www.google.com/search?q={query.replace(' ', '+')}")
                else:
                    self.speak("What would you like me to search for?")
            
            elif 'youtube' in cmd and ('download' in cmd or 'music' in cmd or 'video' in cmd):
                query = cmd.replace('download', '').replace('music', '').replace('video', '')
                query = query.replace('youtube', '').replace('from', '').strip()
                if not query: 
                    query = "latest music"
                self.speak(f"Searching YouTube for {query} and preparing download...")
                self.download_youtube_content(query)
            
            elif 'install' in cmd:
                software = cmd.replace('install', '').replace('please', '').strip()
                self.speak(f"Starting installation process for {software}. I'll search for the official downloader.")
                self.install_software(software)
            
            elif 'shutdown' in cmd:
                if 'cancel' in cmd or 'abort' in cmd:
                    os.system("shutdown /a")
                    self.speak("Shutdown cancelled.")
                else:
                    self.speak("Shutting down the system in 10 seconds. Say 'cancel shutdown' to stop.")
                    os.system("shutdown /s /t 10")
            
            elif 'restart' in cmd:
                self.speak("Restarting the system in 10 seconds.")
                os.system("shutdown /r /t 10")
            
            elif 'lock' in cmd:
                self.speak("Locking the system.")
                os.system("rundll32.exe user32.dll,LockWorkStation")
            
            elif 'stop' in cmd or 'exit' in cmd or 'quit' in cmd or 'bye' in cmd:
                self.speak("Goodbye! Have a great day!")
                self.is_listening = False
                self.stop_event.set()
                self.root.after(1500, self.root.destroy)
            
            elif 'help' in cmd:
                help_text = "I can help you with: opening applications, searching Google, downloading YouTube videos/music, installing software, checking time and date, shutting down or restarting your computer, and locking your screen. Just ask!"
                self.speak(help_text)
            
            else:
                self.speak("I'm not sure how to help with that. Try saying 'help' to see what I can do, or ask me to open an app, search something, download from YouTube, or install software.")
                
        except Exception as e:
            self.speak(f"An error occurred: {str(e)}")
            print(f"Error: {e}")

    def search_and_open(self, app_name):
        driver = self.get_driver()
        if driver:
            driver.get(f"https://www.google.com/search?q=download+{app_name.replace(' ', '+')}+for+windows")
            self.speak(f"I've opened search results for {app_name}. Please download from the official website.")

    def download_youtube_content(self, query):
        driver = self.get_driver()
        if not driver: 
            return
        
        try:
            search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            driver.get(search_url)
            self.speak(f"I've opened YouTube search results for '{query}'. To download, please copy the video URL and use a tool like yt-dlp, or I can guide you through using an online converter.")
            self.speak("Would you like me to search for a YouTube to MP3 converter?")
        except Exception as e:
            self.speak("Could not access YouTube. Please check your internet connection.")

    def install_software(self, software):
        driver = self.get_driver()
        if not driver: 
            return
        
        self.speak(f"Searching for the official installer of {software}...")
        driver.get(f"https://www.google.com/search?q={software.replace(' ', '+')}+official+download+windows")
        
        self.speak(f"I've opened search results for {software}. Please click on the official website link to download the installer. Once downloaded, run the installer and follow the setup wizard.")

def run_app():
    app = PCAssistant()
    app.root.mainloop()

if __name__ == "__main__":
    run_app()
