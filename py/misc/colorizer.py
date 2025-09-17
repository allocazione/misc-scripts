import sys
import os
import webbrowser
import pyperclip


def setup_console() -> None:
    os.system('title Colorizer - Made by Memai(illynne)' if os.name == 'nt' else 'printf "\033]0;Colorizer - Made by '
                                                                                 'Memai(illynne)\007"')
    os.system('cls' if os.name == 'nt' else 'clear')
    os.system('mode con: cols=130 lines=30' if os.name == 'nt' else 'resize -s 30 80')
    logo = fr"""
                   ________  ________  ___       ________  ________  ___  ________  _______   ________
                  |\   ____\|\   __  \|\  \     |\   __  \|\   __  \|\  \|\_____  \|\  ___ \ |\   __  \
                  \ \  \___|\ \  \|\  \ \  \    \ \  \|\  \ \  \|\  \ \  \\|___/  /\ \   __/|\ \  \|\  \
                   \ \  \    \ \  \\\  \ \  \    \ \  \\\  \ \   _  _\ \  \   /  / /\ \  \_|/_\ \   _  _\
                    \ \  \____\ \  \\\  \ \  \____\ \  \\\  \ \  \\  \\ \  \ /  /_/__\ \  \_|\ \ \  \\  \
                     \ \_______\ \_______\ \_______\ \_______\ \__\\ _\\ \__\\________\ \_______\ \__\\ _\
                      \|_______|\|_______|\|_______|\|_______|\|__|\|__|\|__|\|_______|\|_______|\|__|\|__|
    """
    print(logo)


def normalize_html(html_code: str) -> str:
    replacements = {
        "<span style='font-weight:bold;'>": "<b>",
        "<span style='color:": "<color=",
        "'": "",
        "</span>": "</color>",
        ";": "",
        "</span></span>": "</color></b>"
    }

    for old, new in replacements.items():
        html_code = html_code.replace(old, new)

    if "<b>" in html_code and "</b>" not in html_code:
        html_code += "</b>"
    if "<i>" in html_code and "</i>" not in html_code:
        html_code += "</i>"

    return html_code


def main(browse: bool) -> int:
    setup_console()
    print("First head to the site 'https://www.stuffbydavid.com/textcolorizer' and paste here the html code:")

    if browse:
        webbrowser.open('https://www.stuffbydavid.com/textcolorizer')

    try:
        html_code = input()
        if not html_code.strip():
            raise ValueError("No HTML code provided.")

        html_code = normalize_html(html_code)
        pyperclip.copy(html_code)

        print(f"\nYour code has been copied to the clipboard:\n{html_code}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return 0


if __name__ == '__main__':
    try:
        browser = '--no-browser' not in sys.argv and '-no-browser' not in sys.argv
        if len(sys.argv) > 2:
            print("Usage: py colorizer.py --no-browser (optional)")
        else:
            main(browser)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
