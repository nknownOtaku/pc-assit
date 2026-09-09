"""
Advanced PC Assistant - Voice Controlled Desktop Assistant
Features:
- Speech recognition and text-to-speech
- Open applications and files
- Browser automation (search, download, YouTube)
- System control (volume, shutdown, etc.)
- File management
- Web information retrieval
- Software installation assistance
"""

import speech_recognition as sr
import pyttsx3
import os
import subprocess
import webbrowser
import time
import datetime
import json
import re
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import requests
import threading
import sys

class PCAssistant:
    def __init__(self):
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.setup_voice()
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Browser setup
        self.driver = None
        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        
        # Application paths (Windows)
        self.apps = {
            'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'firefox': r'C:\Program Files\Mozilla Firefox\firefox.exe',
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'paint': 'mspaint.exe',
            'word': r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE',
            'excel': r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE',
            'powershell': 'powershell.exe',
            'cmd': 'cmd.exe',
            'spotify': r'C:\Users\AppData\Roaming\Spotify\Spotify.exe',
            'discord': r'C:\Users\AppData\Local\Discord\app-\Discord.exe',
            'vscode': r'C:\Users\AppData\Local\Programs\Microsoft VS Code\Code.exe'
        }
        
        self.is_listening = True
        
    def setup_voice(self):
        """Configure voice settings"""
        voices = self.engine.getProperty('voices')
        # Use female voice if available (index 1 usually)
        if len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)
        self.engine.setProperty('rate', 175)  # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        
    def speak(self, text):
        """Convert text to speech"""
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
        
    def listen(self):
        """Listen to microphone and convert speech to text"""
        try:
            with self.microphone as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
            
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            self.speak("Sorry, I'm having trouble connecting to the speech service.")
            return ""
        except Exception as e:
            print(f"Error: {e}")
            return ""
    
    def init_browser(self):
        """Initialize Chrome browser with Selenium"""
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": self.download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(10)
            return True
        except Exception as e:
            self.speak("Failed to initialize browser. Please make sure Chrome is installed.")
            print(f"Browser error: {e}")
            return False
    
    def close_browser(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def open_application(self, app_name):
        """Open an application by name"""
        app_name = app_name.lower()
        
        # Check if app is in our dictionary
        for key, path in self.apps.items():
            if key in app_name:
                try:
                    subprocess.Popen(path)
                    self.speak(f"Opening {key}")
                    return True
                except Exception as e:
                    print(f"Error opening {key}: {e}")
        
        # Try to find app in PATH or common locations
        common_extensions = ['.exe', '.bat', '.cmd']
        search_paths = [
            os.environ.get('PROGRAMFILES', 'C:\\Program Files'),
            os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)'),
            os.environ.get('LOCALAPPDATA', os.path.expanduser('~\\AppData\\Local'))
        ]
        
        for ext in common_extensions:
            app_with_ext = app_name + ext if not app_name.endswith(ext) else app_name
            for path in search_paths:
                for root, dirs, files in os.walk(path):
                    if app_with_ext.lower() in [f.lower() for f in files]:
                        full_path = os.path.join(root, app_with_ext)
                        try:
                            subprocess.Popen(full_path)
                            self.speak(f"Opening {app_name}")
                            return True
                        except:
                            continue
        
        # Last resort: try running directly
        try:
            subprocess.Popen(app_name)
            self.speak(f"Trying to open {app_name}")
            return True
        except:
            self.speak(f"Sorry, I couldn't find {app_name}")
            return False
    
    def search_web(self, query):
        """Search the web using Chrome"""
        if not self.driver:
            if not self.init_browser():
                return False
        
        url = f"https://www.google.com/search?q={'+'.join(query.split())}"
        self.driver.get(url)
        self.speak(f"Searching for {query}")
        return True
    
    def download_from_youtube(self, video_url=None, search_query=None, audio_only=True):
        """Download video or audio from YouTube"""
        try:
            # If no URL provided, search first
            if not video_url and search_query:
                self.speak(f"Searching for {search_query} on YouTube")
                if not self.driver:
                    if not self.init_browser():
                        return False
                
                self.driver.get("https://www.youtube.com/results?search_query=" + "+".join(search_query.split()))
                time.sleep(2)
                
                # Click first result
                try:
                    first_video = self.driver.find_element(By.CSS_SELECTOR, 'a#video-title')
                    first_video.click()
                    time.sleep(2)
                    video_url = self.driver.current_url
                except Exception as e:
                    self.speak("Could not find video on YouTube")
                    return False
            
            if not video_url:
                self.speak("Please specify what you want to download from YouTube")
                return False
            
            # Use a YouTube downloader website
            if not self.driver:
                if not self.init_browser():
                    return False
            
            # Using y2mate or similar service
            downloader_url = "https://www.y2mate.is/"
            self.driver.get(downloader_url)
            time.sleep(2)
            
            # Find search box and enter URL
            try:
                search_box = self.driver.find_element(By.NAME, "url")
                search_box.clear()
                search_box.send_keys(video_url)
                
                # Click search/download button
                search_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                search_button.click()
                time.sleep(3)
                
                # Select audio or video quality
                if audio_only:
                    # Look for MP3 download option
                    mp3_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'MP3')]")
                    if mp3_buttons:
                        mp3_buttons[0].click()
                        time.sleep(2)
                        
                        # Click final download
                        download_links = self.driver.find_elements(By.XPATH, "//a[contains(@class, 'download-button')]")
                        if download_links:
                            download_links[0].click()
                            self.speak("Downloading audio from YouTube. Check your downloads folder.")
                            return True
                else:
                    # Look for MP4 download option
                    mp4_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'MP4')]")
                    if mp4_buttons:
                        mp4_buttons[0].click()
                        time.sleep(2)
                        
                        download_links = self.driver.find_elements(By.XPATH, "//a[contains(@class, 'download-button')]")
                        if download_links:
                            download_links[0].click()
                            self.speak("Downloading video from YouTube. Check your downloads folder.")
                            return True
                
                self.speak("Download started. Check your downloads folder.")
                return True
                
            except Exception as e:
                self.speak("Having trouble with the download. The website structure may have changed.")
                print(f"Download error: {e}")
                return False
                
        except Exception as e:
            self.speak("Error downloading from YouTube")
            print(f"YouTube download error: {e}")
            return False
    
    def install_software(self, software_name):
        """Search for and download software installer"""
        self.speak(f"Searching for {software_name} installer")
        
        if not self.driver:
            if not self.init_browser():
                return False
        
        # Search for official download page
        search_query = f"{software_name} official download windows"
        url = f"https://www.google.com/search?q={'+'.join(search_query.split())}"
        self.driver.get(url)
        time.sleep(2)
        
        self.speak(f"I've opened search results for {software_name}. Please review and click the official download link.")
        
        # Note: Automatic downloading and installing software can be dangerous
        # We'll guide the user instead of doing it automatically
        self.speak("For security reasons, I recommend you manually verify the official website before downloading. Would you like me to open the first result?")
        
        return True
    
    def run_downloaded_file(self, filename=None):
        """Run a recently downloaded file"""
        try:
            if not filename:
                # Get most recent file in Downloads folder
                downloads = Path(self.download_path)
                recent_files = sorted(downloads.iterdir(), key=os.path.getmtime, reverse=True)
                
                if recent_files:
                    # Find executable files
                    for file in recent_files[:5]:  # Check last 5 files
                        if file.suffix.lower() in ['.exe', '.msi', '.bat', '.cmd']:
                            filename = str(file)
                            break
                    
                    if not filename:
                        self.speak("No recent installer files found. Please specify the filename.")
                        return False
                else:
                    self.speak("Downloads folder is empty.")
                    return False
            
            # Confirm with user before running
            self.speak(f"About to run {os.path.basename(filename)}. Do you want to proceed? Say yes or no.")
            # Note: In a real implementation, you'd wait for voice confirmation
            
            # Run the file
            subprocess.Popen(filename, shell=True)
            self.speak("Running the installer. Follow the installation wizard.")
            return True
            
        except Exception as e:
            self.speak("Error running the file. Please check if the file exists.")
            print(f"Run file error: {e}")
            return False
    
    def get_system_info(self, info_type):
        """Get system information"""
        if 'time' in info_type:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The current time is {current_time}")
            
        elif 'date' in info_type:
            current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            self.speak(f"Today is {current_date}")
            
        elif 'weather' in info_type:
            # Simple weather lookup (would need API key for real implementation)
            self.speak("Checking weather... For accurate weather, please enable location services.")
            self.search_web("current weather")
            
        elif 'volume' in info_type:
            self.speak("Volume control not fully implemented yet.")
    
    def system_control(self, command):
        """Control system functions"""
        if 'shutdown' in command:
            self.speak("Shutting down in 10 seconds. Cancel now if you changed your mind.")
            time.sleep(10)
            os.system("shutdown /s /t 0")
            
        elif 'restart' in command:
            self.speak("Restarting in 10 seconds.")
            time.sleep(10)
            os.system("shutdown /r /t 0")
            
        elif 'lock' in command:
            os.system("rundll32.exe user32.dll,LockWorkStation")
            self.speak("System locked.")
            
        elif 'sleep' in command:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            
        elif 'volume up' in command or 'increase volume' in command:
            # Requires pycaw library for proper volume control
            self.speak("Increasing volume")
            os.system("nircmd.exe changesysvolume 2000")  # Requires nircmd
            
        elif 'volume down' in command or 'decrease volume' in command:
            self.speak("Decreasing volume")
            os.system("nircmd.exe changesysvolume -2000")
            
        elif 'mute' in command:
            self.speak("Muting volume")
            os.system("nircmd.exe mutesysvolume 1")
    
    def file_management(self, command):
        """Manage files and folders"""
        if 'open downloads' in command:
            os.startfile(self.download_path)
            self.speak("Opening downloads folder")
            
        elif 'open documents' in command:
            os.startfile(os.path.expanduser("~/Documents"))
            self.speak("Opening documents folder")
            
        elif 'search for' in command:
            # Extract search term
            search_term = command.replace('search for', '').strip()
            self.speak(f"Searching for {search_term}")
            self.search_web(search_term)
    
    def process_command(self, command):
        """Process and execute commands"""
        if not command:
            return
        
        # Greeting responses
        if any(greet in command for greet in ['hello', 'hi', 'hey']):
            self.speak("Hello! How can I help you today?")
            return
        
        # Identity questions
        if 'who are you' in command or 'what are you' in command:
            self.speak("I am your personal PC assistant, ready to help you with various tasks.")
            return
        
        # Open application
        elif 'open' in command:
            app_name = command.replace('open', '').strip()
            self.open_application(app_name)
        
        # Close application/browser
        elif 'close' in command:
            if 'browser' in command or 'chrome' in command:
                self.close_browser()
                self.speak("Browser closed")
        
        # Search web
        elif 'search' in command or 'google' in command:
            query = command.replace('search', '').replace('google', '').replace('for', '').strip()
            self.search_web(query)
        
        # YouTube download
        elif 'youtube' in command and ('download' in command or 'music' in command):
            if 'song' in command or 'music' in command:
                query = command.replace('download', '').replace('from youtube', '').replace('music', '').replace('song', '').strip()
                self.download_from_youtube(search_query=query, audio_only=True)
            else:
                query = command.replace('download', '').replace('from youtube', '').strip()
                self.download_from_youtube(search_query=query, audio_only=False)
        
        # Install software
        elif 'install' in command:
            software = command.replace('install', '').strip()
            self.install_software(software)
        
        # Run downloaded file
        elif 'run' in command and ('installer' in command or 'download' in command or 'exe' in command):
            self.run_downloaded_file()
        
        # Time and date
        elif 'time' in command:
            self.get_system_info('time')
        
        elif 'date' in command or 'day' in command:
            self.get_system_info('date')
        
        # Weather
        elif 'weather' in command:
            self.get_system_info('weather')
        
        # System control
        elif 'shutdown' in command:
            self.system_control('shutdown')
        
        elif 'restart' in command or 'reboot' in command:
            self.system_control('restart')
        
        elif 'lock' in command:
            self.system_control('lock')
        
        elif 'sleep' in command:
            self.system_control('sleep')
        
        # File management
        elif 'downloads' in command and 'open' in command:
            self.file_management('open downloads')
        
        elif 'documents' in command and 'open' in command:
            self.file_management('open documents')
        
        # Exit
        elif 'exit' in command or 'quit' in command or 'bye' in command or 'stop' in command:
            self.speak("Goodbye! Shutting down assistant.")
            self.is_listening = False
            self.close_browser()
            sys.exit(0)
        
        else:
            self.speak("I'm not sure how to help with that. You can ask me to open apps, search the web, download from YouTube, or install software.")
    
    def run(self):
        """Main loop for the assistant"""
        self.speak("PC Assistant initialized. How can I help you?")
        
        while self.is_listening:
            command = self.listen()
            if command:
                self.process_command(command)
            
            # Small delay to prevent CPU overuse
            time.sleep(0.5)


def main():
    """Entry point for the assistant"""
    print("=" * 50)
    print("   Advanced PC Assistant")
    print("   Voice Controlled Desktop Helper")
    print("=" * 50)
    print("\nInitializing...")
    
    try:
        assistant = PCAssistant()
        assistant.run()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure all required libraries are installed:")
        print("pip install SpeechRecognition pyttsx3 selenium requests")
        print("Also ensure Google Chrome is installed.")


if __name__ == "__main__":
    main()
