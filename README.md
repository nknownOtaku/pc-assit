# 🤖 AI PC Assistant

A powerful voice-controlled desktop assistant with a modern dark-mode GUI that can control your PC, browse the web, download content, and install software.

## ✨ Features

- **🎙️ Voice Recognition** - Speak commands naturally
- **🔊 Text-to-Speech** - Assistant talks back to you
- **💻 Modern GUI** - Beautiful dark-mode interface with CustomTkinter
- **🌐 Browser Automation** - Controls Chrome for searches and downloads
- **📥 Download Manager** - Search and download from YouTube
- **🛠️ Software Installer** - Finds and helps install any software (NodeJS, Python, etc.)
- **⚡ System Control** - Shutdown, restart, lock your PC
- **⌨️ Manual Input** - Type commands if you prefer

## 📋 Requirements

- Windows 10/11
- Google Chrome installed
- Python 3.8 or higher
- Microphone for voice commands

## 🚀 Installation

1. **Clone or download this repository**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the assistant:**
```bash
python pc_assistant.py
```

## 🎯 Example Commands

### Voice or Type:
- "Hello" - Greet the assistant
- "What time is it?" - Get current time
- "What's the date?" - Get current date
- "Open Chrome" - Launch Chrome browser
- "Open Notepad" - Launch Notepad
- "Search for Python tutorials" - Google search
- "Download music Bohemian Rhapsody" - Search YouTube
- "Install NodeJS" - Find NodeJS installer
- "Install Python" - Find Python installer
- "Shutdown computer" - Shut down in 10 seconds
- "Cancel shutdown" - Abort shutdown
- "Restart computer" - Restart in 10 seconds
- "Lock screen" - Lock your PC
- "Help" - Show available commands
- "Stop" or "Exit" - Close the assistant

## 📦 Building .exe File

To create a standalone Windows executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "PC_Assistant" --icon=NONE pc_assistant.py
```

The `.exe` file will be in the `dist` folder.

## 🎨 GUI Features

- **Dark Mode Interface** - Easy on the eyes
- **Command Log** - See all interactions history
- **Status Indicator** - Real-time status updates
- **Start/Stop Listening** - Toggle voice recognition
- **Manual Input Box** - Type commands directly
- **Auto-scrolling Log** - Always shows latest messages

## ⚠️ Notes

- **Browser Automation**: Requires Chrome and ChromeDriver to be installed
- **YouTube Downloads**: The assistant opens YouTube search results; for actual downloads, use yt-dlp or online converters
- **Software Installation**: For safety, the assistant opens official download pages - always verify sources before installing
- **System Commands**: Shutdown/restart have 10-second delays for cancellation

## 🔧 Troubleshooting

**"Error initializing browser"**
- Install Google Chrome
- Install ChromeDriver matching your Chrome version

**"Network error"**
- Check internet connection for speech recognition

**Microphone not working**
- Allow microphone access in Windows settings
- Check default microphone in sound settings

## 📄 License

MIT License - Feel free to modify and distribute!

## 🙏 Credits

Built with:
- CustomTkinter - Modern GUI framework
- SpeechRecognition - Voice input
- pyttsx3 - Text-to-speech output
- Selenium - Browser automation
