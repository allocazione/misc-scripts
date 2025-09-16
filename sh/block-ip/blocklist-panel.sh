#!/bin/bash

# Set working directory to current path + /block-ip
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKDIR="${SCRIPT_DIR%/}/block-ip"

# Create directory if it doesn't exist
if [ ! -d "$WORKDIR" ]; then
    mkdir -p "$WORKDIR"
    echo "[INFO] Created working directory: $WORKDIR"
fi

UPDATE_SCRIPT="$WORKDIR/update-ipblacklist.sh"

while true; do
    echo "==============================="
    echo " Gestione Blacklist IP"
    echo "==============================="
    echo "1) Aggiungi un IP manualmente (iptables)"
    echo "2) Aggiorna blacklist da GitHub"
    echo "99) Esci"
    echo -n "Scelta [1-2, 99]: "
    read choice

    case "$choice" in
        1)
            echo -n "Inserisci l'IP da bloccare: "
            read ip
            if [[ $ip =~ ^[0-9]{1,3}(\.[0-9]{1,3}){3}$ ]]; then
                sudo iptables -A INPUT -s "$ip" -j DROP
                echo "[INFO] IP $ip aggiunto e bloccato con iptables."
                # Salvataggio per persistenza
                sudo netfilter-persistent save
            else
                echo "[ERRORE] Formato IP non valido."
            fi
            ;;
        2)
            echo "[INFO] Avvio script aggiornamento blacklist..."
            sudo bash "$UPDATE_SCRIPT"
            ;;
        99)
            echo "[INFO] Uscita dal programma."
            break
            ;;
        *)
            echo "[ERRORE] Scelta non valida."
            ;;
    esac

    echo ""  # riga vuota per leggibilità
done

