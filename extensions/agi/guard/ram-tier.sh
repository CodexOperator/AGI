#!/usr/bin/env bash
# ram-tier.sh -- goal:g7.16.1.5.2 (owner 2026-09-30 01:4xZ: "symlink the session data directory into the RAM disk from
# the flash drive ... symlink all of the existing internal .claude, .pi and any other harness data dirs to that RAM disk
# to give us that batching benefit" / "just smart symlinking that gets added to init/setup/heal/reboot routes").
#
#   each harness data dir D (GUARD_TIER_DIRS_<box>, e.g. ~/.claude ~/.pi) becomes a symlink to HOT/<name> (tmpfs);
#   COLD/<name> (the flash drive) is its durable copy, written in ONE sequential rsync batch per sync pass.
#
# Usage: ram-tier.sh status | ensure | sync
#   ensure  idempotent, the ONE verb the boot unit, guard-init, and the sync timer (heal) all call:
#             D a real dir     -> copy to HOT, swap D for the symlink ATOMICALLY (renameat2 RENAME_EXCHANGE), catch the
#                                 swap window, seed COLD; the old dir stays beside D as D.pre-tier-<stamp>
#             D a symlink, HOT empty (after a reboot) -> restore HOT from COLD; no COLD = refuse, never an empty dir
#   sync    HOT -> COLD for every tiered dir
# Cells (config:guard, keyed by box): GUARD_TIER_HOT_<box>, GUARD_TIER_COLD_<box>, GUARD_TIER_DIRS_<box> (empty = off).
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
. "$HERE/ram-write.sh"   # HOT-bound writes charge the ramdisk.slice (hypothesis:g7556-fstype-root-...)
NODE=${GUARD_ENV_NODE:-$HERE/../../../.agi/nodes/.geometry/guard.md}
box=${GUARD_BOX:-$(cat /etc/sanctuary-guard/box 2>/dev/null || hostname -s)}; key=$(printf %s "$box" | tr -c 'A-Za-z0-9' '_')
[ -f "$NODE" ] && eval "$(awk '/^```sh guard.env$/{f=1;next} f&&/^```$/{exit} f' "$NODE")"
cell() { local v="GUARD_${1}_${key}"; eval "printf '%s' \"${!v:-${2:-}}\""; }
HOT=$(cell TIER_HOT); COLD=$(cell TIER_COLD); DIRS=$(cell TIER_DIRS)
[ -n "$HOT" ] && [ -n "$COLD" ] && [ -n "$DIRS" ] || { echo "ram-tier: cells unset for box $key -- off"; exit 0; }
log() { mkdir -p "$COLD"; echo "$(date -u +%FT%TZ) $*" | tee -a "$COLD/tier-events.log"; }
nm() { basename "$1" | sed 's/^\.//'; }
empty() { [ -z "$(ls -A "$1" 2>/dev/null)" ]; }
exchange() { python3 - "$1" "$2" <<'PY'
import ctypes, os, sys
libc = ctypes.CDLL(None, use_errno=True)
AT_FDCWD, RENAME_EXCHANGE = -100, 2
if libc.renameat2(AT_FDCWD, sys.argv[1].encode(), AT_FDCWD, sys.argv[2].encode(), RENAME_EXCHANGE) != 0:
    e = ctypes.get_errno(); sys.exit(f"renameat2 exchange failed: {os.strerror(e)}")
PY
}

case "${1:-status}" in
status)
  for D in $DIRS; do n=$(nm "$D")
    if [ -L "$D" ]; then printf 'TIERED  %-24s -> %s  hot=%s cold=%s\n' "$D" "$(readlink "$D")" \
      "$(du -sh "$HOT/$n" 2>/dev/null | cut -f1)" "$(du -sh "$COLD/$n" 2>/dev/null | cut -f1)"
    else printf 'DISK    %s\n' "$D"; fi; done
  { df -h --output=used,size,pcent "$HOT" 2>/dev/null || true; } | tail -1 | sed 's/^/        tmpfs /' ;;
ensure)
  findmnt -rn -T "$HOT" -o FSTYPE | grep -qx tmpfs || { ramw "$HOT" mkdir -p "$HOT" 2>/dev/null; findmnt -rn -T "$HOT" -o FSTYPE | grep -qx tmpfs || { echo "ram-tier: $HOT is not on a tmpfs -- refused"; exit 2; }; }
  ramw "$HOT" mkdir -p "$HOT"; mkdir -p "$COLD"
  for D in $DIRS; do n=$(nm "$D"); H="$HOT/$n"; C="$COLD/$n"
    if [ -L "$D" ]; then
      [ "$(readlink "$D")" = "$H" ] || log "WARN $D -> $(readlink "$D"), expected $H (left as is)"
      if empty "$H"; then
        [ -d "$C" ] && ! empty "$C" || { log "REFUSED $D: $H empty and no cold copy at $C"; exit 3; }
        ramw "$H" mkdir -p "$H"; ramw "$H/" rsync -a "$C/" "$H/"; log "restored $H from $C"; fi
    elif [ -d "$D" ]; then
      ramw "$H" mkdir -p "$H"; ramw "$H/" ionice -c3 rsync -a "$D/" "$H/"; ramw "$H/" rsync -a "$D/" "$H/"
      ln -sfn "$H" "$D.tier-link"; exchange "$D.tier-link" "$D"            # D is now the symlink; D.tier-link the old dir
      old="$D.pre-tier-$(date -u +%Y%m%dT%H%MZ)"; mv -T "$D.tier-link" "$old"
      ramw "$H/" rsync -a --update "$old/" "$H/"                                     # writes that landed during the swap window
      mkdir -p "$C"; ionice -c3 rsync -a "$H/" "$C/"
      log "tiered $D -> $H (cold $C, old dir kept at $old)"
    elif [ ! -e "$D" ] && [ -d "$C" ]; then
      ramw "$H" mkdir -p "$H"; ramw "$H/" rsync -a "$C/" "$H/"; ln -s "$H" "$D"; log "restored missing $D from $C"
    fi
  done ;;
sync)
  for D in $DIRS; do n=$(nm "$D"); [ -L "$D" ] && ! empty "$HOT/$n" || continue
    mkdir -p "$COLD/$n"; ionice -c3 nice -n19 rsync -a --delete "$HOT/$n/" "$COLD/$n/"; done ;;
*) sed -n '2,19p' "$0"; exit 1 ;;
esac
