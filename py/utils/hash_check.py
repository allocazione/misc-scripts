import hashlib
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore

logo = (fr"""{Fore.WHITE}
  $$\   $$\                     $$\              $$$$$$\  $$\                           $$\
  $$ |  $$ |                    $$ |            $$  __$$\ $$ |                          $$ |
  $$ |  $$ | $$$$$$\   $$$$$$$\ $$$$$$$\        $$ /  \__|$$$$$$$\   $$$$$$\   $$$$$$$\ $$ |  $$\  $$$$$$\   $$$$$$\
  $$$$$$$$ | \____$$\ $$  _____|$$  __$$\       $$ |      $$  __$$\ $$  __$$\ $$  _____|$$ | $$  |$$  __$$\ $$  __$$\
  $$  __$$ | $$$$$$$ |\$$$$$$\  $$ |  $$ |      $$ |      $$ |  $$ |$$$$$$$$ |$$ /      $$$$$$  / $$$$$$$$ |$$ |  \__|
  $$ |  $$ |$$  __$$ | \____$$\ $$ |  $$ |      $$ |  $$\ $$ |  $$ |$$   ____|$$ |      $$  _$$<  $$   ____|$$ |
  $$ |  $$ |\$$$$$$$ |$$$$$$$  |$$ |  $$ |      \$$$$$$  |$$ |  $$ |\$$$$$$$\ \$$$$$$$\ $$ | \$$\ \$$$$$$$\ $$ |
  \__|  \__| \_______|\_______/ \__|  \__|$$$$$$\\______/ \__|  \__| \_______| \_______|\__|  \__| \_______|\__|
                                        \______|
""")


def calculate_hash(file_path):
    """Calculates the SHA-256 hash of the given file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        print(f"{Fore.RED}[!] Error: This shouldn't happen, how tf did it get past the first check?")
        return None


def search_file_in_directory(directory, filename):
    """Searches for a file in the given directory and its subdirectories."""
    for root, _, files in os.walk(directory):
        if filename in files:
            return os.path.join(root, filename)
    return None


def find_file(filename):
    """Searches for the file across multiple directories using multithreading."""
    # Common directories to search on a Windows machine
    search_directories = [
        "C:\\",
        os.path.expanduser("~"),  # User's home directory
        "C:\\Program Files",
        "C:\\Program Files (x86)",
        "C:\\Windows"
    ]

    with ThreadPoolExecutor() as executor:
        future_to_dir = {executor.submit(search_file_in_directory, directory, filename): directory for directory in
                         search_directories}

        for future in as_completed(future_to_dir):
            file_path = future.result()
            if file_path:
                return file_path

    # If not found in common directories, return None
    return None


def main(file1, file2):
    print(f"{Fore.WHITE}[?] Initialising query...")

    file1_path = find_file(file1)
    if file1_path:
        print(f"{Fore.GREEN}[+] Found '{file1}' at: {file1_path}")
    else:
        print(f"{Fore.RED}[-] Error: '{file1}' not found.")
        return

    file2_path = find_file(file2)
    if file2_path:
        print(f"{Fore.GREEN}[+] Found '{file2}' at: {file2_path}")
    else:
        print(f"{Fore.RED}[-] Error: '{file2}' not found.")
        return

    print(f"{Fore.WHITE}[+] Found both files! Calculating hashes...\n")

    hash1 = calculate_hash(file1_path)
    hash2 = calculate_hash(file2_path)

    if hash1 and hash2:
        print(f"{Fore.WHITE}[!] Hash of '{file1}': {hash1}")
        print(f"{Fore.WHITE}[!] Hash of '{file2}': {hash2}")

        if hash1 == hash2:
            print(f"{Fore.WHITE}[!]The files have the same hash. {Fore.GREEN}They are identical.")
        else:
            print(f"{Fore.WHITE}[!]The files have different hashes. {Fore.YELLOW}They are not identical.")


def setup_console() -> None:
    os.system("cls")   # Width   Height
    os.system("mode con: cols=119 lines=40")
    print(logo)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: py hash_check.py <file1> <file2>")
    else:
        setup_console()
        main(sys.argv[1], sys.argv[2])
