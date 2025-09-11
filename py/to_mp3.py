import os
import subprocess
import sys
import argparse
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from moviepy import VideoFileClip
from pathlib import Path
from colorama import Fore, init
import webbrowser

# Initialize colorama
init(autoreset=True)

logo = (fr"""{Fore.WHITE}
                     __                           ________                    
                   _/  |_  ____       _____ ______\_____  \     ______ ___.__.
                   \   __\/  _ \     /     \\____ \ _(__  <     \____ <   |  |
                    |  | (  <_> )   |  Y Y  \  |_> >       \    |  |_> >___  |
                    |__|  \____/____|__|_|  /   __/______  / /\ |   __// ____|
                              /_____/     \/|__|         \/  \/ |__|   \/     

{Fore.RESET}""")


def setup_console(length: int = 0, width: int = 0) -> None:
    if os.name == 'nt':  # For Windows
        os.system("cls")
        os.system(f"mode con: cols={length} lines={width}")  # Set the console size
    else:  # For Linux and other Unix-like systems
        os.system("clear")
        os.system(f"stty rows {width} columns {length}")  # Set the console size


# Function to convert video to mp3
def convert_video_to_mp3(input_video_path: str, output_mp3_path: str) -> None:
    try:
        video = VideoFileClip(input_video_path)
        video.audio.write_audiofile(output_mp3_path)
        video.close()
        print(f"{Fore.GREEN}Conversion complete: {Fore.WHITE}{output_mp3_path}")

    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Fore.RESET}")


# Function to open the converted MP3 file using VLC
def open_with_vlc(file_path: str) -> None:
    # Determine VLC installation path based on the operating system
    match sys.platform:
        case "win32":  # Windows
            vlc_path = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
        case "darwin":  # macOS
            vlc_path = "/Applications/VLC.app/Contents/MacOS/VLC"
        case _:  # Linux and other Unix-like systems
            possible_paths = [
                "/usr/bin/vlc",
                "/usr/local/bin/vlc",
                "/usr/share/vlc/vlc",
                "/snap/bin/vlc",  # If installed via Snap
                "/usr/lib/vlc/vlc"  # Another common installation path
            ]
            vlc_path = next((path for path in possible_paths if os.path.exists(path)), None)

    if not check_vlc_installation(vlc_path):  # Check if VLC is installed
        return

    try:
        # Construct the VLC command with the full file path
        vlc_command = [vlc_path, os.path.abspath(file_path)]

        # Create startupinfo to suppress console window
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW  # Suppress the window

        # Use subprocess.Popen with startupinfo to suppress the console window
        print(f"\n{Fore.CYAN}Opening the file with VLC...{Fore.RESET}\n")
        subprocess.Popen(vlc_command, startupinfo=startupinfo, shell=True)
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}VLC failed to open the file. Please install VLC before opening the file.{Fore.RESET}")


# Function to check if VLC is installed and prompt for installation if not
def check_vlc_installation(vlc_path: str) -> bool:
    if not os.path.exists(vlc_path):
        print(f"{Fore.RED}VLC is not found at {vlc_path}. Please install VLC before opening the file.{Fore.RESET}")
        install_vlc_prompt()  # Prompt for installation
        return False
    return True


# Function to prompt user to install VLC
def install_vlc_prompt() -> None:
    print(f"{Fore.YELLOW}You can download VLC from: {Fore.CYAN}https://www.videolan.org/vlc/{Fore.RESET}")
    open_link = input(f"{Fore.YELLOW}Would you like to open the VLC download page? (y/n): {Fore.RESET}")
    if open_link.lower() == 'y':
        webbrowser.open("https://www.videolan.org/vlc/")  # Open the VLC download page in the browser


# Function to get default download directory
def get_default_download_dir() -> str:
    if sys.platform == 'nt':
        return os.path.join(os.path.expanduser('~'), 'Downloads')
    else:
        return os.path.join(Path.home(), 'Downloads')


# Tkinter file chooser for video
def choose_file() -> str:
    root = Tk()

    # Set window title and icon
    root.title("Select a Video File")

    root.withdraw()  # Hide the root window initially
    file_path = askopenfilename(filetypes=[("Video files", "*.mp4 *.mkv *.avi *.mov *.flv")])
    root.destroy()  # Close the Tkinter window after the file selection

    if file_path:  # Check if a file is selected
        # Get absolute path without file name and the file name
        absolute_path = Path(file_path).resolve().parent
        file_name = Path(file_path).name

        # Print the absolute path without the file name and the file name separated by a hyphen
        print(f"{Fore.CYAN}Selected file: {Fore.WHITE}{absolute_path} - {file_name}{Fore.RESET}")

    return file_path


# Function to print help message
def print_help() -> None:
    print(f"{Fore.YELLOW}Usage: py to_mp3.py <flag> <argument>\n{Fore.RESET}")
    print(f"{Fore.CYAN}Flags:")
    print(f"{Fore.WHITE} └── {Fore.CYAN}-d    Specify the video file directory")
    print(f"{Fore.WHITE} │   └── {Fore.CYAN}-dp   Use a file dialog to choose the video file")
    print(f"{Fore.WHITE} └── {Fore.CYAN}-o    Specify the output directory for the MP3 file (default: Downloads)")
    print(f"{Fore.WHITE} └── {Fore.CYAN}-v    Open the converted MP3 file using VLC (requires VLC installation)")
    print(f"{Fore.WHITE} └── {Fore.CYAN}-h    Print the help page")


# Main function to handle arguments and convert video
def main() -> int:
    setup_console(length=100, width=30)
    print(logo)

    # Default to -h if no arguments are provided
    if len(sys.argv) == 1:
        sys.argv.append("-h")

    # Argument parsing with custom -h argument
    parser = argparse.ArgumentParser(description="Convert video to MP3 format", add_help=False)
    parser.add_argument('-d', '--directory', help="Specify the video file directory")
    parser.add_argument('-dp', '--dialog', action='store_true', help="Use a file dialog to choose the video file")
    parser.add_argument('-o', '--output', help="Specify the output directory for the MP3 file")
    parser.add_argument('-v', '--view', action='store_true', help="Open the converted MP3 file using VLC")
    parser.add_argument('-h', '--help', action='store_true', help="Print the help message")

    args = parser.parse_args()

    # Handle custom help flag
    if args.help:
        print_help()
        return 0

    # Initialize input_video and error flag
    input_video = None
    error_flag = False

    # Pattern matching with match-case
    match sys.argv[1] if len(sys.argv) > 1 else None:
        case "-d":
            input_video = args.directory
            if not input_video or not os.path.isfile(input_video):
                print(f"{Fore.RED}error: invalid or missing video file path.{Fore.RESET}")
                error_flag = True
        case "-dp":
            input_video = choose_file()
            if not input_video:
                print(f"{Fore.RED}error: no file selected.{Fore.RESET}")
                error_flag = True
        case _:
            print(f"{Fore.RED}error: invalid flag provided.{Fore.RESET}")
            error_flag = True

    # Check for any errors
    if error_flag:
        return 1

    # Determine output path for MP3
    output_dir = args.output if args.output else get_default_download_dir()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_mp3 = os.path.join(output_dir, f"{Path(input_video).stem}.mp3")

    # Convert video to MP3
    convert_video_to_mp3(input_video, output_mp3)

    # Only open VLC if the -v flag is specified
    if args.view:
        open_with_vlc(output_mp3)

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
