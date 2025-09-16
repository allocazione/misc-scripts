#!/bin/bash

# === CONFIG ===
HOSTNAME=$(hostname)
WORKDIR="/home/$HOSTNAME/block-ip" #Intended to work for servers, otherwise it will be $HOSTNAME/home/
FILE="$WORKDIR/ipblacklist.txt"
URL="https://raw.githubusercontent.com/LittleJake/ip-blacklist/main/all_blacklist.txt"
LOG="$WORKDIR/log/update-ipblacklist.log"
SETNAME="ipblacklist"
IPTABLES_RULE_COMMENT="ipblacklist_drop"

mkdir -p "$WORKDIR"

{
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Avvio aggiornamento blacklist IP..."

  # DOWNLOAD BLACKLIST
  if wget -q "$URL" -O "$FILE"; then
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Blacklist scaricata correttamente."
  else
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERRORE] Download della blacklist fallito!"
      exit 1
  fi

  # CREAZIONE O SVUOTAMENTO IPSET
  if ! ipset list "$SETNAME" &>/dev/null; then
      ipset create "$SETNAME" hash:net
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] ipset $SETNAME creato."
  else
      ipset flush "$SETNAME"
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] ipset $SETNAME svuotato."
  fi

  # AGGIUNTA IP ALL'IPSET
  count=0
  error_count=0
  while IFS= read -r ip; do
      if [[ -n "$ip" && ! "$ip" =~ ^# ]]; then
          if ipset add "$SETNAME" "$ip" 2>/dev/null; then
              ((count++))
          else
              ((error_count++))
          fi
      fi
  done < "$FILE"

  # REGOLA IPTABLES
  if ! iptables -C INPUT -m set --match-set "$SETNAME" src -j DROP &>/dev/null; then
      iptables -I INPUT -m set --match-set "$SETNAME" src -j DROP
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Regola iptables aggiunta per ipset $SETNAME."
  else
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Regola iptables già presente."
  fi

  echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Aggiornamento completato. IP caricati: $count, errori: $error_count"

  # SALVA PER PERSISTENZA
  sudo netfilter-persistent save
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Regole salvate per persistenza dopo reboot."

} >> "$LOG" 2>&1
