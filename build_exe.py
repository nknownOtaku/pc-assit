"""
Build script to compile PC Assistant to Windows .exe
Run this on Windows: python build_exe.py
"""

import subprocess
import sys
import os

def main():
    print("=" * 60)
    print("   PC Assistant - Build to EXE")
    print("=" * 60)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assistant_path = os.path.join(script_dir, "pc_assistant.py")
    
    if not os.path.exists(assistant_path):
        print(f"Error: pc_assistant.py not found at {assistant_path}")
        return
    
    print("\nBuilding executable...")
    print("This may take a few minutes...")
    
    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Create single executable
        "--windowed",                   # No console window (use --console for debug)
        "--name", "PC_Assistant",       # Name of the executable
        "--icon=NONE",                  # Add --icon=your_icon.ico if you have one
        "--add-data", "*.txt;.",        # Include text files if needed
        "--hidden-import=speech_recognition",
        "--hidden-import=pyttsx3",
        "--hidden-import=selenium",
        "--hidden-import=requests",
        assistant_path
    ]
    
    # Alternative simpler command for first build
    cmd_simple = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name", "PC_Assistant",
        "--console",  # Use console for debugging, change to --windowed for release
        assistant_path
    ]
    
    try:
        subprocess.check_call(cmd_simple)
        
        print("\n" + "=" * 60)
        print("   BUILD SUCCESSFUL!")
        print("=" * 60)
        print(f"\nExecutable created at:")
        print(f"  {os.path.join(script_dir, 'dist', 'PC_Assistant.exe')}")
        print("\nTo create a version without console window, run:")
        print("  pyinstaller --onefile --windowed --name PC_Assistant pc_assistant.py")
        print("\nNote: First launch may take longer as Windows Defender scans the file.")
        
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed with error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        print("2. Try running as Administrator")
        print("3. Check that Python and all packages are 64-bit or all 32-bit (not mixed)")


if __name__ == "__main__":
    main()
