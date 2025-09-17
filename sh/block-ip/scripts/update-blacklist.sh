#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKDIR="$SCRIPT_DIR"

if [ ! -d "$WORKDIR" ]; then
    mkdir -p "$WORKDIR"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Created working directory: $WORKDIR"
fi

FILE="$WORKDIR/ipblacklist.txt"
URL="https://raw.githubusercontent.com/LittleJake/ip-blacklist/main/all_blacklist.txt"
LOG="$WORKDIR/log/update-ipblacklist.log"
SETNAME="ipblacklist"
IPTABLES_RULE_COMMENT="ipblacklist_drop"

mkdir -p "$WORKDIR"

{
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Starting IP blacklist update..."

  if wget -q "$URL" -O "$FILE"; then
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Blacklist downloaded successfully."
  else
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] Blacklist download failed!"
      exit 1
  fi

  if ! ipset list "$SETNAME" &>/dev/null; then
      ipset create "$SETNAME" hash:net
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] ipset $SETNAME created."
  else
      ipset flush "$SETNAME"
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] ipset $SETNAME flushed."
  fi

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

  if ! iptables -C INPUT -m set --match-set "$SETNAME" src -j DROP &>/dev/null; then
      iptables -I INPUT -m set --match-set "$SETNAME" src -j DROP
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] iptables rule added for ipset $SETNAME."
  else
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] iptables rule already present."
  fi

  echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Update complete. IPs loaded: $count, errors: $error_count"

  sudo netfilter-persistent save
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Rules saved for persistence after reboot."

} 2>&1 | tee -a "$LOG"
