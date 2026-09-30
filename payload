#!/usr/bin/env bash
# session-sweep.sh -- goal:g7.16.1.5.2 (owner 2026-09-30 01:3xZ: "auto-sweep old sessions into the standard session
# directory for Claude in /data"). Moves IDLE session dirs to their /data homes and leaves a symlink behind:
#   MAIN/.agi/sessions/iter-*   -> GUARD_AGI_SESSIONS_ARCHIVE_<box>
#   ~/.claude/projects/<dir>    -> GUARD_CLAUDE_PROJECTS_ARCHIVE_<box>   (the 09-28 claude-projects convention)
# Idle = no file written within the idle age AND no live process with its cwd or an open file inside.
# Under tmpfs pressure (MAIN up on the RAM disk and use >= GUARD_SWEEP_PRESSURE_PCT) the agi sweep uses the shorter
# GUARD_SWEEP_PRESSURE_IDLE_MIN, oldest first, and stops 10 points under the line.
# Usage: session-sweep.sh [--dry-run]
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
NODE=${GUARD_ENV_NODE:-$HERE/../../../.agi/nodes/.geometry/guard.md}
box=${GUARD_BOX:-$(cat /etc/sanctuary-guard/box 2>/dev/null || hostname -s)}; key=$(printf %s "$box" | tr -c 'A-Za-z0-9' '_')
[ -f "$NODE" ] && eval "$(awk '/^```sh guard.env$/{f=1;next} f&&/^```$/{exit} f' "$NODE")"
cell() { local v="GUARD_${1}_${key}"; eval "printf '%s' \"${!v:-${2:-}}\""; }
DRY=0; [ "${1:-}" = --dry-run ] && DRY=1

MAIN=$(cell RAM_MAIN); RAM_DIR=$(cell RAM_DIR /mnt/agi-ram)
AGI_ARCH=$(cell AGI_SESSIONS_ARCHIVE); CC_ARCH=$(cell CLAUDE_PROJECTS_ARCHIVE)
IDLE=$(cell SWEEP_IDLE_MIN 120); PCT=$(cell SWEEP_PRESSURE_PCT 60); PIDLE=$(cell SWEEP_PRESSURE_IDLE_MIN 20)
CC_IDLE=$(cell SWEEP_CLAUDE_IDLE_MIN 1440)
[ -n "$MAIN" ] && [ -n "$AGI_ARCH" ] || { echo "session-sweep: cells unset for box $key -- off"; exit 0; }
DISK="$(dirname "$MAIN")/.$(basename "$MAIN")-disk"
up() { [ "$(findmnt -rn --mountpoint "$MAIN" -o FSTYPE 2>/dev/null | head -1)" = tmpfs ]; }
pct() { df --output=pcent "$RAM_DIR" | tail -1 | tr -dc 0-9; }
log() { echo "$(date -u +%FT%TZ) $*"; }

# every path a live process of this user holds (cwd + open fds), read ONCE
LIVE=$(mktemp); trap 'rm -f "$LIVE"' EXIT
for p in /proc/[0-9]*; do [ -O "$p" ] || continue
  readlink "$p/cwd" 2>/dev/null || true; ls -l "$p/fd" 2>/dev/null | awk -F' -> ' 'NF==2{print $2}' || true
done | grep '^/' | sort -u > "$LIVE"
held() { grep -qF -- "$1/" "$LIVE" || grep -qxF -- "$1" "$LIVE"; }
recent() { [ -n "$(find "$1" -newermt "-$2 min" -print -quit 2>/dev/null)" ]; }

# move a real dir to dest (same fs: rename; else copy, verify byte count, remove), then symlink back
move() { local src=$1 dest=$2
  [ -e "$dest" ] && dest="$dest.$(date +%s)"
  [ "$DRY" = 1 ] && { log "DRY move $src -> $dest"; return 0; }
  mkdir -p "$(dirname "$dest")"
  if [ "$(stat -c %d "$src")" = "$(stat -c %d "$(dirname "$dest")")" ]; then mv "$src" "$dest"
  else ionice -c3 cp -a "$src" "$dest.part"
       [ "$(du -sb --apparent-size "$src" | cut -f1)" = "$(du -sb --apparent-size "$dest.part" | cut -f1)" ] || { log "VERIFY FAILED $src (kept)"; rm -rf "$dest.part"; return 1; }
       mv "$dest.part" "$dest"; rm -rf "$src"; fi
  ln -s "$dest" "$src"; log "moved $src -> $dest"; }

# 1. agi iter-* session dirs (live tree = MAIN, which is the RAM tree when up)
idle=$IDLE; stop_at=0
if up && [ "$(pct)" -ge "$PCT" ]; then idle=$PIDLE; stop_at=$((PCT - 10)); log "pressure: tmpfs $(pct)% >= $PCT% -> idle ${PIDLE} min"; fi
n=0
while read -r d; do
  [ "$stop_at" -gt 0 ] && [ "$(pct)" -lt "$stop_at" ] && break
  recent "$d" "$idle" && continue; held "$d" && continue
  name=$(basename "$d")
  move "$d" "$AGI_ARCH/$name" || continue; n=$((n+1))
  # MAIN up: DISK holds a stale copy of the same dir -- it becomes the same symlink
  if up && [ "$DRY" = 0 ] && [ -d "$DISK/.agi/sessions/$name" ] && [ ! -L "$DISK/.agi/sessions/$name" ]; then
    rm -rf "${DISK:?}/.agi/sessions/$name"; ln -s "$(readlink "$d")" "$DISK/.agi/sessions/$name"; fi
done < <(find "$MAIN/.agi/sessions" -maxdepth 1 -name 'iter-*' -type d -printf '%T@ %p\n' | sort -n | cut -d' ' -f2-)
log "agi: $n moved (idle ${idle} min)"

# 2. Claude Code project dirs
m=0
if [ -n "$CC_ARCH" ] && [ -d "$HOME/.claude/projects" ]; then
  while read -r d; do
    recent "$d" "$CC_IDLE" && continue; held "$d" && continue
    move "$d" "$CC_ARCH/$(basename "$d")" || continue; m=$((m+1))
  done < <(find "$HOME/.claude/projects" -mindepth 1 -maxdepth 1 -type d)
fi
log "claude: $m moved (idle ${CC_IDLE} min)"
