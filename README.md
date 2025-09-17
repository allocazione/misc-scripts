<div align="center">

# Seloris' Toolkit

A collection of various scripts to automate tasks and simplify workflows.

## 📜 Description

This repository contains a set of utility scripts written in AutoHotkey, Python, and Shell script. Each script is designed to perform a specific task, from adding special characters and launching terminals to converting media files and managing IP blacklists.

## 🌳 Repository Structure

```
.
├── README.md
├── ahk
│   ├── add_chars
│   │   ├── tilde_it.ahk
│   │   └── tilde_it_altgr.ahk
│   └── shortcuts
│       └── winf_terminal.ahk
├── py
│   ├── misc
│   │   ├── colorizer.py
│   │   ├── to_mp3.py
│   │   └── word_counter.py
│   ├── requirements.txt
│   └── utils
│       ├── hash_check.py
│       └── spam.py
└── sh
    └── block-ip
        ├── sentinel.sh
        └── scripts
            ├── block-country.sh
            └── update-blacklist.sh
```

---

## 🚀 Scripts Overview

### AutoHotkey (`.ahk`)
- **`tilde_it.ahk` / `tilde_it_altgr.ahk`**: Scripts for easily typing the tilde (~) character.
- **`winf_terminal.ahk`**: A shortcut to quickly open a terminal window.

### Python (`.py`)
- **`colorizer.py`**: A script to help colorize text for specific platforms.
- **`to_mp3.py`**: Converts video files to MP3 format.
- **`word_counter.py`**: Counts words from text input or a file.
- **`hash_check.py`**: Calculates and compares the SHA-256 hashes of two files to check for identity.
- **`spam.py`**: A simple script to automate sending multiple messages.

### Shell (`.sh`)
- **`sentinel.sh`**: A panel to manage IP blacklisting.
- **`block-country.sh`**: Script to block IPs from a specific country.
- **`update-blacklist.sh`**: Updates the IP blacklist from a source.

---

## 📊 Star Graph

<a href="https://www.star-history.com/#allocazione/seloris-toolkit&Timeline">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=allocazione/seloris-toolkit&type=Timeline&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=allocazione/seloris-toolkit&type=Timeline" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=allocazione/seloris-toolkit&type=Timeline" />
 </picture>
</a>

---

## 🖼️ Script Previews

<details>
<summary>Click to expand script previews</summary>

| Script                | Preview                                                              |
| --------------------- | -------------------------------------------------------------------- |
| **`colorizer.py`**    | ![Colorizer]() |
| **`word_counter.py`** | ![Word Counter]() |
| **`hash_check.py`**   | ![Hash Check]() |
| **`spam.py`**         | ![Spam]() |
| **`blacklist-panel.sh`**| ![Blacklist Panel]() |

</details>

---

## ⚙️ Installation & Usage

### Python Scripts
1.  Navigate to the `py` directory.
2.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run a script using Python:
    ```bash
    python <script_name>.py
    ```

### AutoHotkey Scripts
1.  Ensure you have [AutoHotkey](https://www.autohotkey.com/) installed.
2.  Double-click any `.ahk` file to run it.

### Shell Scripts
1.  Navigate to the `sh` directory or its subdirectories.
2.  Make the script executable:
    ```bash
    chmod +x <script_name>.sh
    ```
3.  Run the script:
    ```bash
    ./<script_name>.sh
    ```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have suggestions for improvements.

---
<p align="center">Made with ❤️ by Selene</p>

</div>