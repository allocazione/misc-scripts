import pyautogui as gui
import time
import sys
import logging
import threading
import argparse
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='\n%(asctime)s - %(levelname)s - %(message)s')
usr = os.getlogin()


def spam(limit: int, message: str) -> None:
    time.sleep(2)
    for _ in range(limit):
        gui.typewrite(message)
        gui.press("enter")
    logging.info(f"Number of messages written: {limit}\nMessage written: '{message}'")


def setup_console() -> None:
    match sys.platform:
        case "win32":
            os.system("cls")
            os.system("mode con: cols=145 lines=50")
        case _:
            os.system("clear")
            os.system("stty rows 50 columns 145")


def main() -> None:
    parser = argparse.ArgumentParser(description="Lexia's Spammer")
    parser.add_argument('-l', '--limit', type=int, help="Number of messages to spam")
    parser.add_argument('-m', '--message', type=str, help="Message to spam")
    parser.add_argument('--no-logo', '--nl', action='store_true', help="Skip logo and console setup")
    args = parser.parse_args()

    if not args.no_logo:
        setup_console()

        print("""
     /$$                           /$$          /$$               /$$$$$$
    | $$                          |__/         | $/              /$$__  $$
    | $$        /$$$$$$  /$$   /$$ /$$  /$$$$$$|_//$$$$$$$      | $$  \\__/  /$$$$$$   /$$$$$$  /$$$$$$/$$$$  /$$$$$$/$$$$   /$$$$$$   /$$$$$$
    | $$       /$$__  $$|  $$ /$$/| $$ |____  $$ /$$_____/      |  $$$$$$  /$$__  $$ |____  $$| $$_  $$_  $$| $$_  $$_  $$ /$$__  $$ /$$__  $$
    | $$      | $$$$$$$$ \\  $$$$/ | $$  /$$$$$$$|  $$$$$$        \\____  $$| $$  \\ $$  /$$$$$$$| $$ \\ $$ \\ $$| $$ \\ $$ \\ $$| $$$$$$$$| $$  \\__/
    | $$      | $$_____/  >$$  $$ | $$ /$$__  $$ \\____  $$       /$$  \\ $$| $$  | $$ /$$__  $$| $$ | $$ | $$| $$ | $$ | $$| $$_____/| $$
    | $$$$$$$$|  $$$$$$$ /$$/\\  $$| $$|  $$$$$$$ /$$$$$$$/      |  $$$$$$/| $$$$$$$/|  $$$$$$$| $$ | $$ | $$| $$ | $$ | $$|  $$$$$$$| $$
    |________/ \\_______/|__/  \\__/|__/ \\_______/|_______/        \\______/ | $$____/  \\_______/|__/ |__/ |__/|__/ |__/ |__/ \\_______/|__/
                                                                          | $$
                                                                          | $$
                                                                          |__/
           """)

    if not args.limit or not args.message:
        print(f"\nWelcome to Lexia's Spammer, {usr}! (Reminder: You have two seconds to press on the field where you "
              f"want to spam the messages)\n")

    try:
        limit = args.limit or int(input("How many messages do you want to write?: ").strip())
    except ValueError:
        limit = int(input("How many messages do you want to write?: ").strip())

    message = args.message or input("What's the message you want to spam?: ").strip()

    if limit <= 0 or not message:
        logging.error("Invalid input: Messages numbers must be above 0 and no field must be empty!")
        return

    try:
        spam_thread = threading.Thread(target=spam, args=(limit, message))
        spam_thread.start()
        spam_thread.join()
    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
