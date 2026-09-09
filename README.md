# Advanced PC Assistant

A powerful voice-controlled desktop assistant for Windows that can perform various tasks using natural language commands.

## Features

### Core Capabilities
- **Voice Recognition**: Listen to your commands through microphone
- **Text-to-Speech**: Talk back with natural voice responses
- **Browser Automation**: Control Chrome browser for web tasks
- **Application Management**: Open and manage Windows applications

### Supported Commands

#### General
- "Hello", "Hi", "Hey" - Greeting responses
- "Who are you" - Assistant identity
- "Exit", "Quit", "Bye", "Stop" - Close the assistant

#### Application Control
- "Open Chrome/Firefox/Notepad/Calculator/Paint/Word/Excel"
- "Open Spotify/Discord/VSCode"
- "Close browser"

#### Web Operations
- "Search for [query]"
- "Google [query]"

#### YouTube Downloads
- "Download music from YouTube [song name]"
- "Download from YouTube [video name]"
- "Download YouTube song [song name]"

#### Software Installation
- "Install NodeJS/Python/Chrome/[any software]"
  - Searches for official download page
  - Opens browser to download location
  - Can run downloaded installers

#### File Management
- "Run installer"
- "Run downloaded exe"
- "Open downloads"
- "Open documents"

#### System Information
- "What time is it"
- "What's the date"
- "Current weather"

#### System Control
- "Shutdown computer"
- "Restart computer"
- "Lock screen"
- "Sleep mode"

## Installation

### Prerequisites
1. **Windows OS** (designed for Windows 10/11)
2. **Python 3.8+** installed
3. **Google Chrome** browser installed
4. **Microphone** for voice input
5. **Speakers** for voice output

### Setup Steps

1. **Clone or download this repository**
   ```bash
   cd pc-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Test the assistant**
   ```bash
   python pc_assistant.py
   ```

4. **Build as .exe (Optional)**
   ```bash
   python build_exe.py
   ```
   
   The executable will be created in the `dist` folder as `PC_Assistant.exe`

## Usage Examples

### Example 1: Install NodeJS
```
You: "Install NodeJS"
Assistant: "Searching for NodeJS installer"
[Opens Chrome with search results for NodeJS download]
Assistant: "I've opened search results for NodeJS. Please review and click the official download link."
[After download completes]
You: "Run installer"
Assistant: "About to run nodejs-installer.exe. Running the installer. Follow the installation wizard."
```

### Example 2: Download YouTube Music
```
You: "Download music from YouTube Bohemian Rhapsody"
Assistant: "Searching for Bohemian Rhapsody on YouTube"
[Opens YouTube, finds video, navigates to downloader]
Assistant: "Downloading audio from YouTube. Check your downloads folder."
```

### Example 3: Open Applications
```
You: "Open Chrome"
Assistant: "Opening Chrome"

You: "Open Spotify"
Assistant: "Opening Spotify"
```

### Example 4: Web Search
```
You: "Search for Python tutorials"
Assistant: "Searching for Python tutorials"
[Opens Chrome with Google search results]
```

## Important Notes

### Security Considerations
- The assistant will ask for confirmation before running executable files
- For software installation, it opens official websites but requires manual verification
- Never share sensitive information through voice commands
- Review all downloads before running them

### Limitations
- Voice recognition requires internet connection (uses Google Speech API)
- Browser automation may break if website layouts change
- Some applications may require specific paths to be configured
- YouTube downloaders may change their structure frequently
- Windows UAC prompts still require manual approval

### Troubleshooting

**Microphone not working:**
- Check Windows sound settings
- Ensure microphone permissions are granted to Python
- Test microphone in Windows Sound Control Panel

**Browser won't open:**
- Make sure Google Chrome is installed
- Update ChromeDriver if needed
- Check antivirus isn't blocking Selenium

**Voice not recognized:**
- Speak clearly and at moderate pace
- Reduce background noise
- Check internet connection

**Build fails:**
- Run as Administrator
- Ensure all dependencies are installed
- Use consistent Python architecture (all 64-bit or all 32-bit)

## Dependencies

- `SpeechRecognition` - Voice input
- `pyttsx3` - Text-to-speech output
- `selenium` - Browser automation
- `requests` - HTTP requests
- `webdriver-manager` - ChromeDriver management
- `PyInstaller` - EXE compilation (for building)

## Customization

### Add New Applications
Edit the `self.apps` dictionary in `pc_assistant.py`:
```python
self.apps = {
    'yourapp': r'C:\\Path\\To\\YourApp.exe',
    # ... more apps
}
```

### Change Voice Settings
Modify `setup_voice()` method:
```python
self.engine.setProperty('rate', 175)  # Speed
self.engine.setProperty('volume', 0.9)  # Volume
```

### Add New Commands
Extend the `process_command()` method with new command patterns.

## Building for Distribution

To create a standalone Windows executable:

```bash
# Install PyInstaller
pip install pyinstaller

# Build with console (for debugging)
pyinstaller --onefile --name PC_Assistant pc_assistant.py

# Build without console (release version)
pyinstaller --onefile --windowed --name PC_Assistant pc_assistant.py
```

The executable will be in the `dist` folder.

## License

This project is provided as-is for educational purposes. Use responsibly and respect website terms of service when using automation features.

## Disclaimer

- This tool should be used responsibly and legally
- Respect copyright when downloading content from YouTube
- Only download software from official sources
- The author is not responsible for any misuse or damages

## Support

For issues or questions:
1. Check the troubleshooting section
2. Ensure all dependencies are properly installed
3. Verify microphone and speaker permissions
4. Make sure Chrome browser is up to date

Enjoy your personal PC assistant!
