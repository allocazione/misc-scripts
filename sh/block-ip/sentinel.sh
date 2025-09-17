#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKDIR="$SCRIPT_DIR"

UPDATE_SCRIPT="$WORKDIR/scripts/update-blacklist.sh"
BLOCK_COUNTRY_SCRIPT="$WORKDIR/scripts/block-country.sh"
UPDATE_SCRIPT_URL="https://raw.githubusercontent.com/allocazione/seloris-toolkit/production/sh/block-ip/scripts/update-blacklist.sh"
BLOCK_COUNTRY_SCRIPT_URL="https://raw.githubusercontent.com/allocazione/seloris-toolkit/production/sh/block-ip/scripts/block-country.sh"

download_script() {
    local script_path=$1
    local script_url=$2
    if [ ! -f "$script_path" ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Script $script_path does not exist. Downloading..."
        mkdir -p "$(dirname "$script_path")"
        if curl -o "$script_path" "$script_url"; then
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Script downloaded successfully."
            chmod +x "$script_path"
        else
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] Unable to download script $script_url."
            exit 1
        fi
    fi
}

download_script "$UPDATE_SCRIPT" "$UPDATE_SCRIPT_URL"
download_script "$BLOCK_COUNTRY_SCRIPT" "$BLOCK_COUNTRY_SCRIPT_URL"

while true; do
    echo "===================================================="
    echo "               Sentinel - IP Management             "
    echo "                      by Selene                     "
    echo "  https://github.com/exterpolation/seloris-toolkit  "
    echo "              https://t.me/selorisdev               "
    echo "===================================================="
    echo ""
    echo "1) Manually blacklist an IP (iptables)"
    echo "2) Update blacklist from GitHub"
    echo "3) Block IPs from a country"
    echo "99) Exit"
    echo -n "Choice [1-3, 99]: "
    read choice

    case "$choice" in
        1)
            echo -n "[?] Enter the IP to block: "
            read ip
            if [[ $ip =~ ^[0-9]{1,3}(\.[0-9]{1,3}){3}$ ]]; then
                sudo iptables -A INPUT -s "$ip" -j DROP
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] IP $ip added and blocked with iptables."
                sudo netfilter-persistent save
            else
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] Invalid IP format."
            fi
            ;;
        2)
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Starting blacklist update script..."
            sudo bash "$UPDATE_SCRIPT"
            ;;
        3)
            sudo bash "$BLOCK_COUNTRY_SCRIPT"
            ;;
        99)
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Exiting the program."
            break
            ;;
        *)
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] Invalid choice."
            ;;
    esac

    echo ""
done

