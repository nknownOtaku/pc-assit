"""
Build script to create Windows .exe file for PC Assistant
Run this on Windows: python build_exe.py
"""

import PyInstaller.__main__
import os

# Get the absolute path to pc_assistant.py
script_path = os.path.abspath('pc_assistant.py')

PyInstaller.__main__.run([
    '--onefile',              # Create a single executable file
    '--windowed',             # No console window (GUI app)
    '--name', 'PC_Assistant', # Name of the executable
    '--icon=NONE',            # No icon (you can add one if you have .ico file)
    '--add-data', 'requirements.txt;.',  # Include requirements.txt
    '--hidden-import', 'customtkinter',
    '--hidden-import', 'speech_recognition',
    '--hidden-import', 'pyttsx3',
    '--hidden-import', 'selenium',
    script_path,
])

print("\n✅ Build complete! Find PC_Assistant.exe in the 'dist' folder.")
print("⚠️  Note: First launch may take longer as Windows Defender scans the file.")
