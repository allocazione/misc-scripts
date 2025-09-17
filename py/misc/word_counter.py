import sys
import os
from colorama import Fore
from tkinter import Tk
from tkinter.filedialog import askopenfilename

logo = (fr"""{Fore.WHITE}
   █     █░ ▒█████   ██▀███  ▓█████▄     ▄████▄   ▒█████   █    ██  ███▄    █ ▄▄▄█████▓▓█████  ██▀███  
  ▓█░ █ ░█░▒██▒  ██▒▓██ ▒ ██▒▒██▀ ██▌   ▒██▀ ▀█  ▒██▒  ██▒ ██  ▓██▒ ██ ▀█   █ ▓  ██▒ ▓▒▓█   ▀ ▓██ ▒ ██▒
  ▒█░ █ ░█ ▒██░  ██▒▓██ ░▄█ ▒░██   █▌   ▒▓█    ▄ ▒██░  ██▒▓██  ▒██░▓██  ▀█ ██▒▒ ▓██░ ▒░▒███   ▓██ ░▄█ ▒
  ░█░ █ ░█ ▒██   ██░▒██▀▀█▄  ░▓█▄   ▌   ▒▓▓▄ ▄██▒▒██   ██░▓▓█  ░██░▓██▒  ▐▌██▒░ ▓██▓ ░ ▒▓█  ▄ ▒██▀▀█▄  
  ░░██▒██▓ ░ ████▓▒░░██▓ ▒██▒░▒████▓    ▒ ▓███▀ ░░ ████▓▒░▒▒█████▓ ▒██░   ▓██░  ▒██▒ ░ ░▒████▒░██▓ ▒██▒
  ░ ▓░▒ ▒  ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░ ▒▒▓  ▒    ░ ░▒ ▒  ░░ ▒░▒░▒░ ░▒▓▒ ▒ ▒ ░ ▒░   ▒ ▒   ▒ ░░   ░░ ▒░ ░░ ▒▓ ░▒▓░
    ▒ ░ ░    ░ ▒ ▒░   ░▒ ░ ▒░ ░ ▒  ▒      ░  ▒     ░ ▒ ▒░ ░░▒░ ░ ░ ░ ░░   ░ ▒░    ░     ░ ░  ░  ░▒ ░ ▒░
    ░   ░  ░ ░ ░ ▒    ░░   ░  ░ ░  ░    ░        ░ ░ ░ ▒   ░░░ ░ ░    ░   ░ ░   ░         ░     ░░   ░ 
      ░        ░ ░     ░        ░       ░ ░          ░ ░     ░              ░             ░  ░   ░     
                              ░         ░                                                              
""")


def setup_console() -> None:
    if os.name == 'nt':  # For Windows
        os.system("cls")
    else:  # For Linux and other Unix-like systems
        os.system("clear")
    os.system("mode con: cols=105 lines=30")  # Set the console size


def center_text(text: str, total_width: int = 101) -> str:
    # Calculate total spaces needed
    total_spaces = total_width - len(text)

    # Calculate left spaces and right spaces
    left_spaces = total_spaces // 2
    right_spaces = total_spaces - left_spaces  # This ensures any odd space goes to the right

    return ' ' * left_spaces + text + ' ' * right_spaces


# Constants for drawing the tree structure
PIPE = "│"
ELBOW = "└──"
TEE = "├──"


def print_help() -> None:
    print(f"{Fore.YELLOW}Usage: py word_counter.py <flag> <argument>\n")
    print(f"{Fore.CYAN}Flags:")
    print(f"{Fore.WHITE}{ELBOW} {Fore.CYAN}-t    Take the input directly from the console (works with or without arguments)")
    print(f"{Fore.WHITE}{PIPE}   {ELBOW} {Fore.CYAN}-ts    Take the input from the console and prints how many words + spaces")
    print(f"{Fore.WHITE}{TEE} {Fore.CYAN}-f    Take the input from a file (dir must be specified)")
    print(f"{Fore.WHITE}{PIPE}   {ELBOW} {Fore.CYAN}-fw    Take the input from a file (choosen from a dialogue window)")
    print(f"{Fore.WHITE}{ELBOW} {Fore.CYAN}-c    Print the credits for this tool{Fore.RESET}")
    print(f"{Fore.WHITE}{ELBOW} {Fore.CYAN}-h    Print this page\n{Fore.RESET}\n")


def count_words_from_console(text: str = None, count_spaces: bool = False) -> None:
    try:
        if text is None:
            text = input("Enter the text: ")

        words = text.split()
        if not count_spaces:
            print(f"Number of words: {len(words)}")
        else:
            spaces = text.count(' ')
            print(f"Number of words: {len(words)}")
            print(f"Number of spaces: {spaces}")
    except UnicodeDecodeError:
        print(f"{Fore.RED}Error: The file contains characters that cannot be decoded with utf-8.{Fore.RESET}")
    except FileNotFoundError:
        print(f"{Fore.RED}Error: The specified file was not found.{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}An unexpected error occurred: {e}{Fore.RESET}")


def count_words_from_file(file_path: str) -> None:
    try:
        with open(file_path, "r") as file:
            text = file.read()
            words = text.split()
            print(f"Number of words: {len(words)}")
    except UnicodeDecodeError:
        print(f"{Fore.RED}Error: The file contains characters that cannot be decoded with utf-8.{Fore.RESET}")
    except FileNotFoundError:
        print(f"{Fore.RED}Error: The specified file was not found. (Maybe the dir was invalid?){Fore.RESET}")


def count_words_from_file_dialog() -> None:
    root = Tk()
    root.withdraw()
    file_path = askopenfilename()
    root.destroy()

    if not file_path:
        print(f"{Fore.RED}No file selected.{Fore.RESET}")
        return

    count_words_from_file(file_path)


def print_credits() -> None:
    print(f"{Fore.WHITE}{center_text('Credits')}\n")
    print(f"{Fore.WHITE}{center_text('Made by: Lexia')}")
    print(f"{Fore.WHITE}{center_text('Git: github.com/exterpolation')}")
    print(f"{Fore.WHITE}{center_text('Dsc: tickflow | 659022591071223819')}")
    print(f"{Fore.WHITE}{center_text('IG: @peepyourclique | @ripbypassed')}")
    print(f"{Fore.LIGHTGREEN_EX}{center_text('Thank you for using my tool <3')}{Fore.RESET}")


def handle_no_args():
    if len(sys.argv) > 2:
        print(f"{Fore.YELLOW}Warning: Ignoring additional arguments.{Fore.RESET}")
    print_help()

def handle_t():
    if len(sys.argv) > 2:
        count_words_from_console(' '.join(sys.argv[2:]))
    else:
        count_words_from_console()

def handle_ts():
    if len(sys.argv) > 2:
        print(f"{Fore.YELLOW}Warning: Ignoring additional arguments.{Fore.RESET}")
    count_words_from_console(count_spaces=True)

def handle_f():
    if len(sys.argv) < 3:
        print(f"{Fore.RED}Error: No file path provided.{Fore.RESET}")
        return 1
    count_words_from_file(sys.argv[2])

def handle_fw():
    if len(sys.argv) > 2:
        print(f"{Fore.YELLOW}Warning: Ignoring additional arguments.{Fore.RESET}")
    count_words_from_file_dialog()

def handle_c():
    print_credits()

def handle_invalid():
    print(f"{Fore.RED}Error: Invalid flag.{Fore.RESET}")
    print_help()

def main() -> int:
    setup_console()
    print(logo)

    if len(sys.argv) == 1:
        handle_no_args()
        return 0

    match sys.argv[1]:
        case "-h":
            handle_no_args()
        case "-t":
            handle_t()
        case "-ts":
            handle_ts()
        case "-f":
            return handle_f()
        case "-fw":
            handle_fw()
        case "-c":
            handle_c()
        case _:
            handle_invalid()

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"{Fore.RED}An unexpected error occurred: {e}{Fore.RESET}")
        sys.exit(1)