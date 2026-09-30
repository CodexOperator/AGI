#!/usr/bin/env bash
# guard-init.sh — one run puts a mesh box behind the five layers that keep it
# REACHABLE while its userspace is burning. Idempotent: re-run after any change
# to this directory. The why, the layers and the kill switches: GUARD.md
#
# Source: the agi repo, extensions/agi/guard/ (build nodes; goal:g7.16.1.7).
# ~/work/.sanctuary/guard/{guard-init.sh,sanctuary-health,sanctuary-watch} are
# symlinks into it. The per-box settings are the ```sh guard.env block of the
# config node .agi/nodes/.geometry/guard.md (config:guard), keyed by BOX name
# (GUARD_BOX, else /etc/sanctuary-guard/box, else the hosts.json town whose
# host is this one, else hostname -s). GUARD_ENV_NODE overrides the node path;
# a legacy guard.env beside the script is read only when the node is missing.
#
#   sudo ~/work/.sanctuary/guard/guard-init.sh              apply every layer
#        ~/work/.sanctuary/guard/guard-init.sh --dry-run    print the plan, change nothing
#        ~/work/.sanctuary/guard/guard-init.sh --status     verify every layer, live values
#   sudo ~/work/.sanctuary/guard/guard-init.sh --uninstall  remove everything it installed
#
# Flags:  --user U            the user that runs the engine (default: $SUDO_USER)
#         --no-watchdog       skip layer 4 (the box never reboots itself)
#         --no-watch          skip layer 5 (no kill alerts, no peer checks)
#         --peerwatch-claude  on a new peer outage, launch ONE recovery claude (one box only)
#         --docker-budget S   memory set aside for docker containers, e.g. 8G
#         --apply-docker      cap running containers to that budget live (docker update)
#         --restart-engine    restart the running agi-agi-* scripts so they move into
#                             agi-engine.slice now instead of at their next start
set -Eeuo pipefail
# put() is fed by pipes all over (`{ hdr; cat <<EOF; } | put ...`). Without
# lastpipe the last element of a pipeline runs in a subshell and put()'s
# CHANGED=1 is lost, which broke "restart the watchdog only when changed".
shopt -s lastpipe

ARGS="$*"
# GUARD_DIR = where the script really lives (the repo, through the symlink):
# sanctuary-health and sanctuary-watch are its siblings there.
GUARD_DIR=$(cd "$(dirname "$(readlink -f "$0")")" && pwd)
# SANCTUARY = the box's sanctuary dir (hosts.json, ssh/config), which is NOT the
# repo: the directory the script was INVOKED from, one level up, when it holds
# hosts.json; else GUARD_SANCTUARY; else /data/work/.sanctuary. Its value is
# written into every installed file header and watch.env, so it must not move.
SANCTUARY=${GUARD_SANCTUARY:-}
if [ -z "$SANCTUARY" ]; then
  SANCTUARY=$(dirname "$(cd "$(dirname "$0")" && pwd -P)")
  [ -e "$SANCTUARY/hosts.json" ] || SANCTUARY=/data/work/.sanctuary
fi
MODE=apply TUSER=${SUDO_USER:-} DO_WATCHDOG=1 DO_WATCH=1 PEER_CLAUDE=''
DOCKER_BUDGET='' APPLY_DOCKER=0 RESTART_ENGINE=0

usage() { awk 'NR>1 && !/^#/{exit} NR>1' "$0" | sed 's/^# \{0,1\}//'; exit "${1:-0}"; }
while (( $# )); do
  case $1 in
    --dry-run) MODE=dry ;;
    --status) MODE=status ;;
    --uninstall) MODE=uninstall ;;
    --user) TUSER=$2; shift ;;
    --no-watchdog) DO_WATCHDOG=0 ;;
    --no-watch) DO_WATCH=0 ;;
    --peerwatch-claude) PEER_CLAUDE=1 ;;
    --docker-budget) DOCKER_BUDGET=$2; shift ;;
    --apply-docker) APPLY_DOCKER=1 ;;
    --restart-engine) RESTART_ENGINE=1 ;;
    -h|--help) usage 0 ;;
    *) echo "unknown flag: $1" >&2; usage 2 ;;
  esac
  shift
done

# --- output ------------------------------------------------------------------
B=$'\e[1m' D=$'\e[2m' R=$'\e[31m' G=$'\e[32m' Y=$'\e[33m' N=$'\e[0m'
[ -t 1 ] || { B=; D=; R=; G=; Y=; N=; }
WARNINGS=0 FAILS=0
say()  { printf '%s\n' "$*"; }
head_(){ printf '\n%s== %s ==%s\n' "$B" "$*" "$N"; }
ok()   { printf '  %sok%s    %s\n' "$G" "$N" "$*"; }
warn() { printf '  %swarn%s  %s\n' "$Y" "$N" "$*"; WARNINGS=$((WARNINGS+1)); }
bad()  { printf '  %sFAIL%s  %s\n' "$R" "$N" "$*"; FAILS=$((FAILS+1)); }
die()  { printf '%sguard-init: %s%s\n' "$R" "$*" "$N" >&2; exit 1; }
# Only the top-level shell dies: with set -E the trap is inherited by $(...)
# subshells, where an expected non-zero (systemctl is-active -> 3) would print a
# fake fatal line. A real failure inside a substitution still fails the
# assignment in the parent, which trips the trap there.
trap '(( BASH_SUBSHELL )) || die "line $LINENO: $BASH_COMMAND"' ERR

# run CMD... — execute, or under --dry-run only show it.
run() {
  if [ "$MODE" = dry ]; then printf '  %s+ %s%s\n' "$D" "$*" "$N"; return 0; fi
  "$@"
}

# put PATH MODE OWNER:GROUP [brief] — stdin becomes PATH, only if it differs.
# `brief` = under --dry-run name the file instead of printing all of it (scripts).
# Sets CHANGED=1 when it writes (or would), so a caller can skip a restart
# when nothing it depends on moved.
CHANGED=0
put() {
  local path=$1 mode=$2 owner=$3 brief=${4:-} tmp dir
  tmp=$(mktemp); cat > "$tmp"
  if [ -f "$path" ] && cmp -s "$tmp" "$path"; then
    rm -f "$tmp"; ok "unchanged      $path"; return 0
  fi
  CHANGED=1
  if [ "$MODE" = dry ]; then
    if [ -f "$path" ]; then
      say "  ${Y}would change${N}   $path"
      diff -u "$path" "$tmp" | sed -n '3,60p' | sed 's/^/        /' || true
    elif [ -n "$brief" ]; then
      say "  ${Y}would install${N}  $path  ($(wc -l < "$tmp") lines, from $brief)"
    else
      say "  ${Y}would write${N}    $path"; sed 's/^/        /' "$tmp"
    fi
    rm -f "$tmp"; return 0
  fi
  dir=$(dirname "$path")
  if [ "${owner%%:*}" = root ]; then mkdir -p "$dir"
  else runuser -u "${owner%%:*}" -- mkdir -p "$dir"; fi
  install -m "$mode" -o "${owner%%:*}" -g "${owner##*:}" "$tmp" "$path"
  rm -f "$tmp"; ok "wrote          $path"
}

# --- who and where -------------------------------------------------------------
[ -n "$TUSER" ] || TUSER=$(id -un)
[ "$TUSER" != root ] || die "run via sudo from the engine's user, or pass --user <name>"
TUID=$(id -u "$TUSER" 2>/dev/null) || die "no such user: $TUSER"
TGROUP=$(id -gn "$TUSER")
THOME=$(getent passwd "$TUSER" | cut -d: -f6)
# Guard-owned user units live in ~/.local/share/systemd/user, NOT ~/.config:
# crons.py's drift scan reports every undeclared *.service in ~/.config/systemd/user.
UGUARD=$THOME/.local/share/systemd/user
# The settings are keyed by the BOX (agi name, e.g. local-town), never by the
# host name: config:guard is committed, a host name must never be. First hit wins.
box_name() {
  local b=${GUARD_BOX:-} h
  [ -n "$b" ] || { [ -r /etc/sanctuary-guard/box ] && read -r b < /etc/sanctuary-guard/box; } || true
  if [ -z "$b" ] && [ -r "$SANCTUARY/hosts.json" ] && command -v python3 >/dev/null 2>&1; then
    h=$(hostname -s)
    b=$(python3 - "$SANCTUARY/hosts.json" "$h" 2>/dev/null <<'PY' || true
import json, sys
towns = json.load(open(sys.argv[1])).get("towns", {})
hit = [n for n, t in towns.items() if isinstance(t, dict) and "alias_of" not in t and t.get("host") == sys.argv[2]]
print(hit[0] if len(hit) == 1 else "")
PY
)
  fi
  [ -n "$b" ] || b=$(hostname -s)
  printf '%s' "$b"
}
HOST=$(box_name); HOSTKEY=${HOST//[^A-Za-z0-9]/_}

case $MODE in
  apply|uninstall) [ "$(id -u)" = 0 ] || die "needs root: sudo $0 $ARGS" ;;
esac

umgr() {  # systemctl for the target user's manager
  if [ "$(id -u)" = "$TUID" ]; then systemctl --user "$@"
  else systemctl --machine="$TUSER@.host" --user "$@"; fi
}

# --- sizing ------------------------------------------------------------------
to_mib() {  # 512M | 2G | 1.5G | 1024 (MiB) -> integer MiB
  local v=${1^^}
  case $v in
    *G) awk -v x="${v%G}" 'BEGIN{printf "%d", x*1024}' ;;
    *M) awk -v x="${v%M}" 'BEGIN{printf "%d", x}' ;;
    ''|*[!0-9.]*) die "bad size: $1" ;;
    *)  awk -v x="$v" 'BEGIN{printf "%d", x}' ;;
  esac
}
# The settings: the ```sh guard.env fenced block of config:guard, evaluated as
# bash (the same assignments guard.env held). Default node: the repo this script
# really lives in, else the main checkout.
guard_env_block() { awk '/^```sh guard\.env[[:space:]]*$/{f=1; next} f && /^```[[:space:]]*$/{exit} f' "$1"; }
GUARD_ENV_NODE=${GUARD_ENV_NODE:-}
if [ -z "$GUARD_ENV_NODE" ]; then
  GUARD_ENV_NODE=$(cd "$GUARD_DIR/../../.." 2>/dev/null && pwd)/.agi/nodes/.geometry/guard.md
  [ -f "$GUARD_ENV_NODE" ] || GUARD_ENV_NODE=/data/work/agi/.agi/nodes/.geometry/guard.md
fi
GUARD_ENV_FROM=defaults
if [ -f "$GUARD_ENV_NODE" ]; then
  GUARD_ENV_TEXT=$(guard_env_block "$GUARD_ENV_NODE")
  [ -n "$GUARD_ENV_TEXT" ] || die "$GUARD_ENV_NODE has no \`\`\`sh guard.env block"
  eval "$GUARD_ENV_TEXT"
  GUARD_ENV_FROM="config:guard ($GUARD_ENV_NODE)"
else
  for _gf in "$SANCTUARY/guard/guard.env" "$GUARD_DIR/guard.env"; do
    if [ -f "$_gf" ]; then . "$_gf"; GUARD_ENV_FROM="legacy $_gf"; break; fi
  done
fi
hostvar() { local n="GUARD_$1_$HOSTKEY"; printf '%s' "${!n:-${2:-}}"; }

RAM_M=$(( $(awk '/^MemTotal:/{print $2}' /proc/meminfo) / 1024 ))
SWAP_M=$(( $(awk '/^SwapTotal:/{print $2}' /proc/meminfo) / 1024 ))
# --- cells (goal:g7.16.1.5.5.5) ---------------------------------------------------
# Every number below is a config:guard cell whose default is the literal this
# script carried before; an unset OR EMPTY cell takes the default. A cell is
# checked as a STRING, in THIS shell, before any $(( )) reads it: bash arithmetic
# evaluates a variable's text, so a cell holding x[$(cmd)] would run cmd. The digit
# class is spelled out: under a UTF-8 locale [0-9] also matches non-ASCII digits.
num_cell() {  # VAR NAME DEFAULT LO HI -> VAR = a whole number LO..HI, else refused by name
  local v; v=$(hostvar "$2" "$3")
  [[ $v =~ ^[0123456789]{1,6}$ ]] && (( 10#$v >= $4 && 10#$v <= $5 )) \
    || die "GUARD_$2_$HOSTKEY must be a whole number $4..$5 (got '$v')"
  printf -v "$1" '%d' "$(( 10#$v ))"
}
size_cell() {  # VAR NAME DEFAULT -> VAR = whole MiB of 512M | 2G | 1.5G | bare MiB, else refused by name
  local v; v=$(hostvar "$2" "$3")
  [[ $v =~ ^[0123456789]{1,7}(\.[0123456789]{1,3})?[MG]$ || $v =~ ^[0123456789]{1,7}$ ]] \
    || die "GUARD_$2_$HOSTKEY must be a size: 512M, 2G, 1.5G or whole MiB (got '$v')"
  printf -v "$1" '%s' "$(to_mib "$v")"
}
DEF_RESERVE=$(( RAM_M * 12 / 100 > 768 ? RAM_M * 12 / 100 : 768 ))
[ -z "${DOCKER_BUDGET:-}" ] || printf -v "GUARD_DOCKER_BUDGET_$HOSTKEY" '%s' "$DOCKER_BUDGET"
size_cell RESERVE_M RESERVE "$DEF_RESERVE"; size_cell DOCKER_M DOCKER_BUDGET 0
# A non-integer PSI_FULL would make the health check's (( )) error out, which
# reads as "healthy" forever: the watchdog would silently never fire.
num_cell PSI_FULL PSI_FULL 40 5 100
num_cell OOMD_LIMIT OOMD_LIMIT 50 10 99          # oomd kill line for user@UID + its root slice, % memory pressure
num_cell USER_HIGH_PCT USER_HIGH_PCT 90 50 99    # user@UID MemoryHigh as % of its MemoryMax
num_cell GRACE_S GRACE 900 0 86400
num_cell USER_SWAP_PCT USER_SWAP_PCT 50 0 100; size_cell USER_SWAP_CAP_M USER_SWAP_CAP 2048M
num_cell AGI_MAX_PCT AGI_MAX_PCT 70 1 100; num_cell AGI_HIGH_PCT AGI_HIGH_PCT 90 1 100
num_cell ENGINE_HIGH_PCT ENGINE_HIGH_PCT 75 1 100; num_cell WORK_HIGH_PCT WORK_HIGH_PCT 90 1 100
num_cell AGI_OOMD_LIMIT AGI_OOMD_LIMIT 40 10 99
num_cell OOMD_SWAP_USED_PCT OOMD_SWAP_USED_PCT 90 1 100; num_cell OOMD_PRESSURE_PCT OOMD_PRESSURE_PCT 60 1 100
num_cell OOMD_PRESSURE_S OOMD_PRESSURE_S 20 1 3600
size_cell SYSTEM_MIN_M SYSTEM_MIN 128M; size_cell SSH_MIN_M SSH_MIN 64M
num_cell CLAUDE_LOW_DIV CLAUDE_LOW_DIV 6 1 100; size_cell CLAUDE_LOW_CAP_M CLAUDE_LOW_CAP 1024M
size_cell USER_MIN_M USER_MIN 2048M; num_cell DOCKER_CAP_HEADROOM_PCT DOCKER_CAP_HEADROOM_PCT 90 1 100
num_cell DEFER_PCT DEFER_PCT 90 1 100
size_cell ENGINE_MAX_M ENGINE_MAX 512M
size_cell ENGINE_SWAP_M ENGINE_SWAP_MAX 0; size_cell RAMDISK_SWAP_M RAMDISK_SWAP_MAX 0
# systemd reads a bare MemorySwapMax number as BYTES: write 0, or whole MiB with its unit.
ENGINE_SWAP=$( (( ENGINE_SWAP_M )) && echo "${ENGINE_SWAP_M}M" || echo 0 )
RAMDISK_SWAP=$( (( RAMDISK_SWAP_M )) && echo "${RAMDISK_SWAP_M}M" || echo 0 )
# goal:g7.16.1.5.5.1: the RAM disk's own line (ramdisk.slice). Default = the
# tmpfs size, so the slice never caps before the mount is full; 0 = no RAM disk.
RAM_DIR=$(hostvar RAM_DIR /mnt/agi-ram)
size_cell RAM_BUDGET_M RAM_BUDGET "$(findmnt -rno SIZE "$RAM_DIR" 2>/dev/null || echo 0)"
[ -n "$PEER_CLAUDE" ] || PEER_CLAUDE=$(hostvar PEERWATCH_CLAUDE 0)

USER_MAX_M=$(( RAM_M - RESERVE_M - DOCKER_M ))
USER_HIGH_M=$(( USER_MAX_M * USER_HIGH_PCT / 100 ))
USER_SWAP_M=$(( SWAP_M * USER_SWAP_PCT / 100 < USER_SWAP_CAP_M ? SWAP_M * USER_SWAP_PCT / 100 : USER_SWAP_CAP_M ))
AGI_MAX_M=$(( USER_MAX_M * AGI_MAX_PCT / 100 )); AGI_HIGH_M=$(( AGI_MAX_M * AGI_HIGH_PCT / 100 ))
ENGINE_HIGH_M=$(( ENGINE_MAX_M * ENGINE_HIGH_PCT / 100 ))
WORK_MAX_M=$(( AGI_MAX_M - ENGINE_MAX_M )); WORK_HIGH_M=$(( WORK_MAX_M * WORK_HIGH_PCT / 100 ))
CLAUDE_LOW_M=$(( USER_MAX_M / CLAUDE_LOW_DIV < CLAUDE_LOW_CAP_M ? USER_MAX_M / CLAUDE_LOW_DIV : CLAUDE_LOW_CAP_M ))
# --- cells end -----------------------------------------------------------------

SSH_UNIT=ssh.service
systemctl cat ssh.service >/dev/null 2>&1 || SSH_UNIT=sshd.service
UCG=/sys/fs/cgroup/user.slice/user-$TUID.slice/user@$TUID.service

# --- preflight -----------------------------------------------------------------
[ -r /sys/fs/cgroup/cgroup.controllers ] || die "cgroup v2 is not mounted; guard needs the unified hierarchy"
[ -r /proc/pressure/memory ] || die "no PSI at /proc/pressure/memory; oomd and the health check both need it"
SDV=$(systemctl --version | awk 'NR==1{print $2}')
(( SDV >= 250 )) || die "systemd $SDV is too old (need >= 250)"
if [ "$MODE" = apply ] || [ "$MODE" = dry ]; then
  (( USER_MAX_M >= USER_MIN_M )) || die "RAM ${RAM_M}M - reserve ${RESERVE_M}M - docker ${DOCKER_M}M leaves ${USER_MAX_M}M for $TUSER; need >= ${USER_MIN_M}M. Lower the docker budget or the reserve in config:guard."
fi

need_pkg() {
  if dpkg-query -W -f='${Status}' "$1" 2>/dev/null | grep -q "install ok installed"; then
    ok "package $1 present"; return 0
  fi
  run env DEBIAN_FRONTEND=noninteractive apt-get install -y -q "$1" \
    || { run apt-get update -q && run env DEBIAN_FRONTEND=noninteractive apt-get install -y -q "$1"; }
}

# The header text (and $SANCTUARY in it) is part of every installed file: changing
# it rewrites them all on the next apply. "guard.env" there now means config:guard.
hdr() { printf '# sanctuary guard layer %s. Written by %s/guard/guard-init.sh.\n# Edit guard.env or the script and re-run it; do not hand-edit this file. See GUARD.md.\n' "$1" "$SANCTUARY"; }

# =============================================================================
layer1() {
  head_ "1  systemd-oomd: kill the runaway on memory PRESSURE, before the box livelocks"
  # Remember whether guard is what turned oomd on, so --uninstall undoes only its own doing.
  if ! systemctl is-enabled --quiet systemd-oomd.service 2>/dev/null \
     && [ ! -e /etc/sanctuary-guard/oomd.enabled-by-guard ]; then
    run mkdir -p /etc/sanctuary-guard
    run touch /etc/sanctuary-guard/oomd.enabled-by-guard
  fi
  need_pkg systemd-oomd
  { hdr 1; cat <<EOF
# Ubuntu's package already has oomd watch user@.service at 50% pressure; these
# are the defaults any watched unit inherits unless it sets its own limit.
[OOM]
SwapUsedLimit=${OOMD_SWAP_USED_PCT}%
DefaultMemoryPressureLimit=${OOMD_PRESSURE_PCT}%
DefaultMemoryPressureDurationSec=${OOMD_PRESSURE_S}s
EOF
  } | put /etc/systemd/oomd.conf.d/50-sanctuary-guard.conf 0644 root:root
  run systemctl enable --quiet systemd-oomd.service
  run systemctl restart systemd-oomd.service

  { hdr 1; cat <<EOF
# Inside a user manager the root slice IS the user@UID.service cgroup. When this
# manager reports its units to oomd (it does once agi.slice asks to be watched),
# it reports this slice too, and the default "auto" makes oomd DROP the user@UID
# entry PID1 registered. Saying kill here keeps the 50% backstop alive.
[Slice]
ManagedOOMMemoryPressure=kill
ManagedOOMMemoryPressureLimit=${OOMD_LIMIT}%
EOF
  } | put "$UGUARD/-.slice.d/50-sanctuary-guard.conf" 0644 "$TUSER:$TGROUP"
  run umgr daemon-reload
}

# =============================================================================
layer2() {
  head_ "2  reserve the way back in: sshd + system keep ${RESERVE_M}M that user@$TUID can never take"

  # Decide live-vs-deferred BEFORE anything reloads: a daemon-reload applies a
  # resource drop-in to a running unit at once. If user@ already holds more than
  # the new high mark, pin its live limits to infinity with a --runtime override
  # first. /run outranks /etc, so the cap then really waits for the next boot
  # instead of squeezing seats mid-round.
  local cur hard deferred=0 defer=/run/systemd/system/user@$TUID.service.d/99-sanctuary-guard-defer.conf
  cur=$(( $(cat "$UCG/memory.current" 2>/dev/null || echo 0) / 1048576 ))
  # memory.current counts page cache and reclaimable slab, which a cap just trims
  # (measured on encryption-town: 6251M current, of it 385M anon). Judge by what
  # the cap would really have to take away.
  hard=$(awk '$1=="anon"||$1=="shmem"||$1=="file_mapped"||$1=="slab_unreclaimable"{s+=$2} END{printf "%d", s/1048576}' "$UCG/memory.stat" 2>/dev/null || echo 0)
  if (( hard >= USER_HIGH_M * DEFER_PCT / 100 )); then
    deferred=1
    # systemd merges drop-ins from ALL directories in filename order, last wins:
    # 99- sorts after guard's 50-sanctuary-guard.conf, and /run is emptied at
    # boot, so this means exactly "not now, from the next boot".
    printf '[Service]\nMemoryHigh=infinity\nMemoryMax=infinity\nMemorySwapMax=infinity\n' \
      | put "$defer" 0644 root:root
  elif [ -e "$defer" ]; then
    run rm -f "$defer"
  fi

  { hdr 2; cat <<EOF
# Everything $TUSER runs (Claude, its tmux seats, the agi engine, pi rounds)
# lives under user@$TUID. Capped at RAM - reserve - docker, it can thrash itself
# but it can never take the memory sshd needs to fork your login.
#   RAM ${RAM_M}M - reserve ${RESERVE_M}M - docker ${DOCKER_M}M = ${USER_MAX_M}M
# MemoryLow is one link of the chain that makes Claude's own MemoryLow real:
# cgroup v2 protection only reaches a cgroup whose every ancestor has some.
[Service]
MemoryHigh=${USER_HIGH_M}M
MemoryMax=${USER_MAX_M}M
MemorySwapMax=${USER_SWAP_M}M
MemoryLow=${CLAUDE_LOW_M}M
TasksMax=16384
ManagedOOMMemoryPressure=kill
ManagedOOMMemoryPressureLimit=${OOMD_LIMIT}%
EOF
  } | put "/etc/systemd/system/user@$TUID.service.d/50-sanctuary-guard.conf" 0644 root:root

  # The rest of Claude's protection chain: user.slice > user-UID.slice > user@ > app.slice.
  local s
  for s in user.slice "user-$TUID.slice"; do
    { hdr 2; cat <<EOF
# One link of the chain that lets claude-remote-control's MemoryLow take effect:
# a cgroup's memory.low only counts if every ancestor has protection too.
[Slice]
MemoryLow=${CLAUDE_LOW_M}M
EOF
    } | put "/etc/systemd/system/$s.d/50-sanctuary-guard.conf" 0644 root:root
  done

  # sshd's protection needs its parent protected too (system.slice's parent is
  # the root, so its own value counts; memory_recursiveprot hands it down).
  { hdr 2; cat <<EOF
# The parent link for ssh.service's MemoryMin: without it the child's is worth 0.
[Slice]
MemoryMin=${SYSTEM_MIN_M}M
EOF
  } | put /etc/systemd/system/system.slice.d/50-sanctuary-guard.conf 0644 root:root

  { hdr 2; cat <<EOF
# sshd must keep the pages it holds and win the CPU inside system.slice when
# everything else is stalled. Being unkillable alone is what failed on
# 2026-09-25: the listener lived, but forking a login stalled in reclaim.
# NOT set here: OOMScoreAdjust. sshd already puts its listener at -1000 itself
# and restores its starting value in every login child. Starting it at -1000
# would make every login shell, and anything run from it, unkillable.
# NOT set here: IOWeight. No io controller is enabled, so it would do nothing.
[Service]
MemoryMin=${SSH_MIN_M}M
CPUWeight=1000
EOF
  } | put "/etc/systemd/system/$SSH_UNIT.d/50-sanctuary-guard.conf" 0644 root:root

  run systemctl daemon-reload
  run systemctl set-property --runtime system.slice "MemoryMin=${SYSTEM_MIN_M}M"
  run systemctl set-property --runtime "$SSH_UNIT" "MemoryMin=${SSH_MIN_M}M" CPUWeight=1000
  run systemctl set-property --runtime user.slice "MemoryLow=${CLAUDE_LOW_M}M"
  run systemctl set-property --runtime "user-$TUID.slice" "MemoryLow=${CLAUDE_LOW_M}M"

  if (( deferred )); then
    run systemctl set-property --runtime "user@$TUID.service" "MemoryLow=${CLAUDE_LOW_M}M" TasksMax=16384
    warn "user@$TUID holds ${hard}M it cannot give back (${cur}M with cache), near its ${USER_HIGH_M}M high mark: memory cap DEFERRED to next boot ($defer); protection applied now"
  else
    run systemctl set-property --runtime "user@$TUID.service" \
      "MemoryHigh=${USER_HIGH_M}M" "MemoryMax=${USER_MAX_M}M" \
      "MemorySwapMax=${USER_SWAP_M}M" "MemoryLow=${CLAUDE_LOW_M}M" TasksMax=16384
    ok "live now: user@$TUID holds ${hard}M non-reclaimable (${cur}M with cache), well under its ${USER_HIGH_M}M high mark"
  fi

  { hdr 2; cat <<EOF
# The last parent link above claude-remote-control.service in the user manager.
[Slice]
MemoryLow=${CLAUDE_LOW_M}M
EOF
  } | put "$UGUARD/app.slice.d/50-sanctuary-guard.conf" 0644 "$TUSER:$TGROUP"

  if [ "$(umgr show -p LoadState --value claude-remote-control.service 2>/dev/null || true)" = loaded ]; then
    { hdr 2; cat <<EOF
# Claude and the tmux seats it spawns share this unit's cgroup. MemoryLow keeps
# its pages from being reclaimed ahead of its siblings; it only takes effect
# because every ancestor (app.slice, user@, user-UID.slice, user.slice) carries
# the same value. CPUWeight keeps it scheduled among its siblings.
# OOMScoreAdjust cannot be lowered from here: an unprivileged user manager may
# only raise it (see GUARD.md, caveats).
[Service]
MemoryLow=${CLAUDE_LOW_M}M
CPUWeight=400
EOF
    } | put "$UGUARD/claude-remote-control.service.d/50-sanctuary-guard.conf" 0644 "$TUSER:$TGROUP"
  else
    warn "no claude-remote-control.service for $TUSER: its MemoryLow is skipped (BOOTSTRAP section 4 installs it)"
  fi
  run umgr daemon-reload
  run umgr set-property --runtime app.slice "MemoryLow=${CLAUDE_LOW_M}M"
  if [ "$(umgr show -p LoadState --value claude-remote-control.service 2>/dev/null || true)" = loaded ]; then
    run umgr set-property --runtime claude-remote-control.service "MemoryLow=${CLAUDE_LOW_M}M" CPUWeight=400
  fi
}

# =============================================================================
layer3() {
  head_ "3  fence the engine: agi.slice ${AGI_MAX_M}M = agi-engine ${ENGINE_MAX_M}M (little scripts) + agi-work ${WORK_MAX_M}M (rounds)"
  { hdr 3; cat <<EOF
# Everything the agi engine starts as a unit. oomd acts here at ${AGI_OOMD_LIMIT}% pressure,
# before user@ reaches its own ${OOMD_LIMIT}%, so the engine is killed before Claude is.
[Unit]
Description=sanctuary guard: the agi engine (scripts + rounds)
[Slice]
MemoryHigh=${AGI_HIGH_M}M
MemoryMax=${AGI_MAX_M}M
MemorySwapMax=${USER_SWAP_M}M
TasksMax=4096
CPUWeight=50
ManagedOOMMemoryPressure=kill
ManagedOOMMemoryPressureLimit=${AGI_OOMD_LIMIT}%
EOF
  } | put "$UGUARD/agi.slice" 0644 "$TUSER:$TGROUP"

  { hdr 3; cat <<EOF
# The little engine scripts: heal.py watch (the reaper), rotate.py alarms,
# sanctuary-watch. The reaper runs at ~80M. If anything in here hits this cap,
# something upstream went wrong: sanctuary-watch raises an ALARM for it.
[Unit]
Description=sanctuary guard: little engine scripts (reaper, alarms, watch)
[Slice]
MemoryHigh=${ENGINE_HIGH_M}M
MemoryMax=${ENGINE_MAX_M}M
MemorySwapMax=${ENGINE_SWAP}
TasksMax=128
CPUWeight=20
EOF
  } | put "$UGUARD/agi-engine.slice" 0644 "$TUSER:$TGROUP"

  { hdr 3; cat <<EOF
# The heavy agent work: dispatch rounds, merge-up reviews, the test suite.
[Unit]
Description=sanctuary guard: agi rounds (dispatch, merge-up, suites)
[Slice]
MemoryHigh=${WORK_HIGH_M}M
MemoryMax=${WORK_MAX_M}M
TasksMax=2048
CPUWeight=50
EOF
  } | put "$UGUARD/agi-work.slice" 0644 "$TUSER:$TGROUP"

  if [ "${RAM_BUDGET_M:-0}" -gt 0 ]; then
  { hdr 3; cat <<EOF
# goal:g7.16.1.5.5.1 -- the RAM disk's OWN budget line, a sibling of agi.slice
# (never agi-ram.slice: a dash would nest it inside agi.slice's oomd domain).
# A tmpfs page stays charged to the cgroup that first wrote it and moves to
# that cgroup's parent when the writer exits; a bulk write into ${RAM_DIR}
# runs as a transient unit here (locations.ram_write_argv), so its pages park
# HERE. No ManagedOOM: a kill cannot free a tmpfs page.
[Unit]
Description=sanctuary guard: the RAM disk pages (${RAM_DIR})
[Slice]
MemoryMax=${RAM_BUDGET_M}M
MemorySwapMax=${RAMDISK_SWAP}
TasksMax=64
CPUWeight=20
EOF
  } | put "$UGUARD/ramdisk.slice" 0644 "$TUSER:$TGROUP"
  fi

  { hdr 3; cat <<EOF
# Every agi-* service the engine writes (dispatch, mur, suite seats) runs in
# agi-work.slice. The more specific agi-agi-.service.d/ file of the same name
# overrides this one for the little scripts.
[Service]
Slice=agi-work.slice
EOF
  } | put "$UGUARD/agi-.service.d/50-sanctuary-guard.conf" 0644 "$TUSER:$TGROUP"

  { hdr 3; cat <<EOF
# agi-agi-* = the engine's own scripts (heal.py watch, rotate.py alarms).
[Service]
Slice=agi-engine.slice
EOF
  } | put "$UGUARD/agi-agi-.service.d/50-sanctuary-guard.conf" 0644 "$TUSER:$TGROUP"

  run umgr daemon-reload

  # Where the RUNNING engine units are vs. where the drop-ins will put them.
  # Target is derived from the name, so this reads true under --dry-run too.
  local u target cg moved=0 later=0
  while read -r u; do
    [ -n "$u" ] || continue
    case $u in agi-agi-*) target=agi-engine.slice ;; *) target=agi-work.slice ;; esac
    cg=$(umgr show -p ControlGroup --value "$u" 2>/dev/null || true)
    if [[ $cg == */"$target"/* ]]; then moved=$((moved+1))
    else later=$((later+1)); say "  ${D}next start${N}  $u -> $target"; fi
  done < <(umgr list-units --no-legend --plain --state=running 'agi-*.service' 2>/dev/null | awk '{print $1}')
  say "  running agi-* units: $moved already fenced, $later move at their next start$( (( RESTART_ENGINE )) && echo " (agi-agi-* restarted below; rounds never are)" || echo " (nothing is restarted)")"

  if (( RESTART_ENGINE )); then
    while read -r u; do
      [ -n "$u" ] || continue
      run umgr restart "$u"
      [ "$MODE" = dry ] || ok "restarted $u into agi-engine.slice"
    done < <(umgr list-units --no-legend --plain --state=running 'agi-agi-*.service' 2>/dev/null | awk '{print $1}')
  fi
}

# =============================================================================
layer4() {
  head_ "4  watchdog: reboot if memory-stalled >= ${PSI_FULL}% for 5 min, or the check cannot even fork"
  CHANGED=0   # from here on, any write means the daemon must re-read its config
  { hdr 4; cat <<EOF
# A kernel panic reboots after 10s instead of hanging forever (Ubuntu default 0).
kernel.panic = 10
kernel.panic_on_oops = 1
EOF
  } | put /etc/sysctl.d/90-sanctuary-guard.conf 0644 root:root
  run sysctl -q -p /etc/sysctl.d/90-sanctuary-guard.conf

  { hdr 4; cat <<EOF
# Read by /usr/local/sbin/sanctuary-health (the watchdog's test-binary).
LIMIT=$PSI_FULL
GRACE=$GRACE_S
EOF
  } | put /etc/sanctuary-guard/health.env 0644 root:root
  put /usr/local/sbin/sanctuary-health 0755 root:root guard/sanctuary-health < "$GUARD_DIR/sanctuary-health"

  # The device: a real hardware watchdog if the box has one, else softdog.
  local module=softdog
  if ls /sys/class/watchdog/watchdog* >/dev/null 2>&1 && ! grep -q '^softdog ' /proc/modules; then
    module=none; ok "hardware watchdog present: $(cat /sys/class/watchdog/watchdog0/identity 2>/dev/null || true)"
  else
    printf 'softdog\n' | put /etc/modules-load.d/sanctuary-guard.conf 0644 root:root
    { hdr 4; printf 'options softdog soft_margin=60\n'; } | put /etc/modprobe.d/sanctuary-guard.conf 0644 root:root
    grep -q '^softdog ' /proc/modules || run modprobe softdog
  fi

  # Never arm a watchdog that would fire right now.
  if HEALTH_ENV=/dev/null LIMIT="$PSI_FULL" GRACE=0 bash "$GUARD_DIR/sanctuary-health" test; then
    ok "health check passes right now (memory PSI full avg60 < ${PSI_FULL}%)"
  else
    die "sanctuary-health FAILS right now: the box is under memory pressure. Refusing to arm a watchdog that would reboot it. Fix the pressure, or re-run with --no-watchdog."
  fi

  # No wd_keepalive, on purpose. The packaged watchdog.service ends every stop
  # with ExecStopPost '[ $run_wd_keepalive != 1 ] || false', so with keepalive on
  # every stop FAILS; OnFailure then starts wd_keepalive, which Conflicts= the
  # daemon and cancels the start half of any restart. That broke re-runs of this
  # script and package upgrades (invoke-rc.d restart under set -e in postinst).
  # Masking it BEFORE the install also stops postinst from ever starting it. A
  # clean daemon stop disarms softdog (no NOWAYOUT), so nothing needs to keep
  # petting the device while the daemon is down.
  run systemctl mask --quiet wd_keepalive.service
  # The package rewrites /etc/default/watchdog from debconf on every upgrade,
  # so the settings go into debconf, not just the file.
  run sh -c "printf '%s\n' 'watchdog watchdog/run boolean true' 'watchdog watchdog/run_keepalive boolean false' 'watchdog watchdog/restart boolean true' 'watchdog watchdog/module string $module' | debconf-set-selections"
  need_pkg watchdog

  if [ -f /etc/watchdog.conf ] && [ ! -f /etc/watchdog.conf.pre-sanctuary-guard ] \
     && ! grep -q 'sanctuary guard' /etc/watchdog.conf; then
    run cp -p /etc/watchdog.conf /etc/watchdog.conf.pre-sanctuary-guard
  fi
  { hdr 4; cat <<EOF
# realtime = mlockall + SCHED_RR: the daemon keeps running when nothing else can.
# Every 10s it forks the test-binary and pets the device. A failing check (or a
# check that cannot even start within test-timeout) is tolerated for
# retry-timeout = 5 min, then the box reboots. If the daemon itself stops
# petting, the kernel device resets the box after watchdog-timeout.
watchdog-device = /dev/watchdog
watchdog-timeout = 60
interval = 10
realtime = yes
priority = 1
test-binary = /usr/local/sbin/sanctuary-health
test-timeout = 60
retry-timeout = 300
repair-maximum = 1
log-dir = /var/log/watchdog
EOF
  } | put /etc/watchdog.conf 0644 root:root

  cat <<EOF | put /etc/default/watchdog 0644 root:root
run_watchdog=1
run_wd_keepalive=0
watchdog_module="$module"
watchdog_options=""
EOF
  run systemctl enable --quiet watchdog.service
  # Bounce the daemon only when something it reads changed, or it is not up.
  if (( CHANGED )) || ! systemctl is-active --quiet watchdog.service; then
    run systemctl restart watchdog.service
  else
    ok "watchdog daemon already running on this exact config: not restarted"
  fi
  if [ "$MODE" != dry ]; then
    sleep 2
    systemctl is-active --quiet watchdog.service \
      || die "watchdog.service is not active after start: journalctl -u watchdog -n 30"
    ok "watchdog daemon active; device $(cat /sys/class/watchdog/watchdog0/identity 2>/dev/null || echo '?') state=$(cat /sys/class/watchdog/watchdog0/state 2>/dev/null || echo '?')"
  fi
}

# =============================================================================
layer5() {
  head_ "5  watch: cap kills here + the other towns, every 2 min (recovery claude: $([ "$PEER_CLAUDE" = 1 ] && echo ON || echo off))"
  put "$THOME/.local/bin/sanctuary-watch" 0755 "$TUSER:$TGROUP" guard/sanctuary-watch < "$GUARD_DIR/sanctuary-watch"
  { hdr 5; cat <<EOF
SANCTUARY=$SANCTUARY
PEER_CLAUDE=$PEER_CLAUDE
FAILS=3
EOF
  } | put "$THOME/.config/sanctuary-guard/watch.env" 0644 "$TUSER:$TGROUP"

  { hdr 5; cat <<EOF
[Unit]
Description=sanctuary guard: cap-kill alerts + peer town checks
[Service]
Type=oneshot
Slice=agi-engine.slice
ExecStart=%h/.local/bin/sanctuary-watch
TimeoutStartSec=5min
EOF
  } | put "$UGUARD/sanctuary-watch.service" 0644 "$TUSER:$TGROUP"

  { hdr 5; cat <<EOF
[Unit]
Description=sanctuary guard: run sanctuary-watch every 2 min
[Timer]
OnActiveSec=1min
OnBootSec=3min
OnUnitActiveSec=2min
AccuracySec=15s
[Install]
WantedBy=timers.target
EOF
  } | put "$UGUARD/sanctuary-watch.timer" 0644 "$TUSER:$TGROUP"

  [ "$MODE" = dry ] || runuser -u "$TUSER" -- mkdir -p "$THOME/logs/sanctuary-guard"
  run umgr daemon-reload
  run umgr enable --now sanctuary-watch.timer
}

# =============================================================================
docker_section() {
  command -v docker >/dev/null 2>&1 || return 0
  head_ "docker: containers live in system.slice, OUTSIDE the user@$TUID cap"
  if (( DOCKER_M == 0 )); then
    warn "docker is here but no budget is set, so containers are neither capped nor subtracted from user@. Set GUARD_DOCKER_BUDGET_$HOSTKEY in config:guard."
  else
    ok "budget ${DOCKER_M}M is subtracted from user@$TUID's cap"
  fi
  local c name lim use
  for c in $(docker ps -q 2>/dev/null); do
    name=$(docker inspect -f '{{.Name}}' "$c" | tr -d /)
    lim=$(docker inspect -f '{{.HostConfig.Memory}}' "$c")
    use=$(docker stats --no-stream --format '{{.MemUsage}}' "$c" | cut -d/ -f1 | tr -d ' ')
    if [ "$lim" != 0 ]; then ok "$name capped at $(( lim / 1048576 ))M (using $use)"; continue; fi
    if (( APPLY_DOCKER )) && (( DOCKER_M > 0 )); then
      # docker prints e.g. 5.2GiB / 512MiB / 800KiB. Never cap a container at or
      # near what it already holds: the kernel would squeeze it at once.
      local use_m
      use_m=$(awk -v u="$use" 'BEGIN{ n=u+0; if (u ~ /GiB$/) n*=1024; else if (u ~ /KiB$/) n/=1024; else if (u ~ /[0-9]B$/) n/=1048576; printf "%d", n }')
      if (( use_m * 100 >= DOCKER_M * DOCKER_CAP_HEADROOM_PCT )); then
        warn "$name uses ${use_m}M, >= ${DOCKER_CAP_HEADROOM_PCT}% of the ${DOCKER_M}M budget: NOT capped. Raise GUARD_DOCKER_BUDGET_$HOSTKEY first."
        continue
      fi
      run docker update --memory "${DOCKER_M}m" --memory-swap "${DOCKER_M}m" "$c"
      [ "$MODE" = dry ] || ok "$name capped live at ${DOCKER_M}M (was unbounded, using ${use_m}M). Survives restarts, not re-creation."
    else
      warn "$name is UNBOUNDED (using $use). Re-run with --apply-docker to cap it live, no restart."
    fi
  done
}

# =============================================================================
fmt() { case $1 in ''|infinity|'[not set]') printf '%s' "${1:-unset}" ;; *[!0-9]*) printf '%s' "$1" ;; *) printf '%sM' "$(( $1 / 1048576 ))" ;; esac; }
prop() { local out; out=$("$@" 2>/dev/null) || true; printf '%s' "$out"; }

status() {
  head_ "guard status: $HOST, engine user $TUSER, systemd $SDV"
  say "  settings: $GUARD_ENV_FROM, key _$HOSTKEY"
  say "  RAM ${RAM_M}M  swap ${SWAP_M}M  |  memory PSI now: $(tr '\n' ' ' < /proc/pressure/memory)"
  # A layer is "expected" when guard's own file for it is on disk; only then is
  # its absence a FAIL. Otherwise it is reported as not installed.
  local v s u slice cg

  head_ "1  systemd-oomd"
  if [ -f /etc/systemd/oomd.conf.d/50-sanctuary-guard.conf ]; then
    [ "$(systemctl is-active systemd-oomd 2>/dev/null || true)" = active ] && ok "active, guard config present" || bad "guard config present but systemd-oomd is NOT active"
    local mon
    if mon=$(oomctl 2>/dev/null || sudo -n oomctl 2>/dev/null); then
      for s in "/user.slice/user-$TUID.slice/user@$TUID.service/agi.slice" "/user.slice/user-$TUID.slice/user@$TUID.service"; do
        grep -qxF "	Path: $s" <<< "$mon" && ok "oomd is watching $s" || bad "oomd is NOT watching $s"
      done
    else warn "cannot read oomctl (needs root): run --status with sudo to check what oomd watches"; fi
  else warn "not installed"; fi

  head_ "2  the way back in"
  if [ -f "/etc/systemd/system/user@$TUID.service.d/50-sanctuary-guard.conf" ]; then
    for v in MemoryHigh MemoryMax MemorySwapMax MemoryLow; do
      say "  user@$TUID  $v=$(fmt "$(prop systemctl show -p "$v" --value "user@$TUID.service")")"
    done
    say "  user@$TUID  TasksMax=$(prop systemctl show -p TasksMax --value "user@$TUID.service")"
    say "  user@$TUID  using $(( $(cat "$UCG/memory.current" 2>/dev/null || echo 0) / 1048576 ))M now"
    if [ "$(prop systemctl show -p MemoryMax --value "user@$TUID.service")" != infinity ]; then ok "user@$TUID is capped"
    elif [ -e "/run/systemd/system/user@$TUID.service.d/99-sanctuary-guard-defer.conf" ]; then warn "user@$TUID cap DEFERRED to next boot (it held too much it could not give back at install)"
    else bad "user@$TUID is UNCAPPED although guard's drop-in is present"; fi
    for s in user.slice "user-$TUID.slice" system.slice; do
      say "  $s  MemoryLow=$(fmt "$(prop systemctl show -p MemoryLow --value "$s")") MemoryMin=$(fmt "$(prop systemctl show -p MemoryMin --value "$s")")"
    done
    say "  $SSH_UNIT  MemoryMin=$(fmt "$(prop systemctl show -p MemoryMin --value "$SSH_UNIT")") CPUWeight=$(prop systemctl show -p CPUWeight --value "$SSH_UNIT")"
    say "  kernel view: ssh memory.min=$(fmt "$(cat /sys/fs/cgroup/system.slice/$SSH_UNIT/memory.min 2>/dev/null || echo 0)")  claude memory.low=$(fmt "$(cat "$UCG/app.slice/claude-remote-control.service/memory.low" 2>/dev/null || echo 0)")"
    [ "$(cat /sys/fs/cgroup/system.slice/memory.min 2>/dev/null || echo 0)" != 0 ] && ok "sshd's protection chain is live" || bad "system.slice memory.min is 0: sshd's MemoryMin is worth nothing"
    local link chain_ok=1
    for link in user.slice "user.slice/user-$TUID.slice" "user.slice/user-$TUID.slice/user@$TUID.service" \
                "user.slice/user-$TUID.slice/user@$TUID.service/app.slice"; do
      if [ "$(cat "/sys/fs/cgroup/$link/memory.low" 2>/dev/null || echo 0)" = 0 ]; then
        chain_ok=0; say "  ${Y}gap${N}  memory.low=0 on $link"
      fi
    done
    (( chain_ok )) && ok "Claude's protection chain is live (every ancestor has memory.low)" || bad "Claude's MemoryLow chain has a gap: its own memory.low is worth nothing"
  else warn "not installed"; fi

  head_ "3  engine fence"
  if [ -f "$UGUARD/agi.slice" ]; then
    for s in agi.slice agi-engine.slice agi-work.slice; do
      [ -f "$UGUARD/$s" ] && ok "$s  MemoryMax=$(fmt "$(prop umgr show -p MemoryMax --value "$s")") TasksMax=$(prop umgr show -p TasksMax --value "$s")" || bad "$s missing"
    done
    # goal:g7.16.1.5.5.1: the RAM disk's own line, written only when a RAM disk is mounted
    if [ -f "$UGUARD/ramdisk.slice" ]; then
      ok "ramdisk.slice  MemoryMax=$(fmt "$(prop umgr show -p MemoryMax --value ramdisk.slice)") (the RAM disk's own line)"
    elif [ "${RAM_BUDGET_M:-0}" -gt 0 ]; then bad "ramdisk.slice missing (RAM disk at $RAM_DIR)"
    else say "  ramdisk.slice  not installed (no RAM disk at $RAM_DIR)"; fi
    while read -r u; do
      [ -n "$u" ] || continue
      slice=$(prop umgr show -p Slice --value "$u"); cg=$(prop umgr show -p ControlGroup --value "$u")
      if [[ $cg == */"$slice"/* ]]; then say "  ${G}in${N}   $slice  $u"
      else say "  ${Y}next${N} $slice  $u  (running outside it until restarted)"; fi
    done < <(umgr list-units --no-legend --plain --state=running 'agi-*.service' 'sanctuary-*.service' 2>/dev/null | awk '{print $1}')
  else warn "not installed"; fi

  head_ "4  watchdog"
  if grep -q 'sanctuary guard' /etc/watchdog.conf 2>/dev/null; then
    [ "$(systemctl is-active watchdog 2>/dev/null || true)" = active ] && ok "watchdog daemon active" || bad "watchdog daemon NOT active: the box will not reboot itself"
    [ -x /usr/local/sbin/sanctuary-health ] && ok "health binary present" || bad "/usr/local/sbin/sanctuary-health missing: every check fails, the box WILL reboot"
    if [ -r /sys/class/watchdog/watchdog0/state ]; then
      say "  device $(cat /sys/class/watchdog/watchdog0/identity 2>/dev/null || true): state=$(cat /sys/class/watchdog/watchdog0/state) timeout=$(cat /sys/class/watchdog/watchdog0/timeout 2>/dev/null || true)s"
    else bad "no /sys/class/watchdog/watchdog0"; fi
    [ "$(systemctl is-enabled wd_keepalive 2>/dev/null || true)" = masked ] && ok "wd_keepalive masked" || warn "wd_keepalive not masked: restarts and upgrades can fight the daemon"
    say "  kernel.panic=$(cat /proc/sys/kernel/panic)  panic_on_oops=$(cat /proc/sys/kernel/panic_on_oops)"
    if [ -x /usr/local/sbin/sanctuary-health ]; then
      /usr/local/sbin/sanctuary-health test && ok "health check passes now" || bad "health check FAILS now: a reboot follows in 5 min unless it recovers"
    fi
    [ -e /etc/sanctuary-guard/watchdog.disable ] && warn "KILL SWITCH SET: /etc/sanctuary-guard/watchdog.disable (the check always passes)"
  else warn "not installed"; fi

  head_ "5  watch"
  if [ -f "$UGUARD/sanctuary-watch.timer" ]; then
    [ "$(prop umgr is-active sanctuary-watch.timer)" = active ] && ok "timer active" || bad "sanctuary-watch.timer NOT active: no alerts, no peer checks"
    umgr list-timers --no-pager sanctuary-watch.timer 2>/dev/null | head -2 | sed 's/^/    /' || true
    [ "$(prop umgr show -p Result --value sanctuary-watch.service)" = success ] && ok "last run succeeded" || bad "last watch run: $(prop umgr show -p Result --value sanctuary-watch.service)"
  else warn "not installed"; fi
  if [ -r "$THOME/logs/sanctuary-guard/alerts.log" ]; then
    say "  last alerts ($THOME/logs/sanctuary-guard/alerts.log):"; tail -n 5 "$THOME/logs/sanctuary-guard/alerts.log" | sed 's/^/    /'
  else say "  no alerts yet"; fi

  say ""
  if (( FAILS )); then say "${R}$FAILS layer check(s) FAILED${N}"; return 1; fi
  say "${G}all layer checks passed${N}"
}

# =============================================================================
uninstall() {
  head_ "uninstall on $HOST: packages stay installed, everything guard wrote goes"
  # A clean daemon stop disarms the device (magic close; softdog has no NOWAYOUT).
  systemctl stop watchdog.service 2>/dev/null || true
  systemctl disable --quiet watchdog.service 2>/dev/null || true
  systemctl stop wd_keepalive.service 2>/dev/null || true
  systemctl unmask --quiet wd_keepalive.service 2>/dev/null || true
  [ -f /etc/watchdog.conf.pre-sanctuary-guard ] && mv -f /etc/watchdog.conf.pre-sanctuary-guard /etc/watchdog.conf && ok "restored /etc/watchdog.conf"
  printf 'run_watchdog=0\nrun_wd_keepalive=0\nwatchdog_module="none"\nwatchdog_options=""\n' > /etc/default/watchdog
  printf '%s\n' 'watchdog watchdog/run boolean false' 'watchdog watchdog/run_keepalive boolean false' 'watchdog watchdog/module string none' | debconf-set-selections 2>/dev/null || true
  umgr disable --now sanctuary-watch.timer 2>/dev/null || true

  # Live values back to their defaults, then drop the runtime control files.
  systemctl set-property --runtime "user@$TUID.service" MemoryHigh=infinity MemoryMax=infinity MemorySwapMax=infinity MemoryLow=0 TasksMax=infinity 2>/dev/null || true
  systemctl set-property --runtime user.slice MemoryLow=0 2>/dev/null || true
  systemctl set-property --runtime "user-$TUID.slice" MemoryLow=0 2>/dev/null || true
  systemctl set-property --runtime system.slice MemoryMin=0 2>/dev/null || true
  systemctl set-property --runtime "$SSH_UNIT" MemoryMin=0 CPUWeight=100 2>/dev/null || true
  umgr set-property --runtime app.slice MemoryLow=0 2>/dev/null || true
  umgr set-property --runtime claude-remote-control.service MemoryLow=0 CPUWeight=100 2>/dev/null || true
  rm -f "/run/systemd/system/user@$TUID.service.d/99-sanctuary-guard-defer.conf"
  rm -f /run/systemd/system.control/"user@$TUID.service.d"/50-{MemoryHigh,MemoryMax,MemorySwapMax,MemoryLow,TasksMax}.conf \
        /run/systemd/system.control/user.slice.d/50-MemoryLow.conf \
        /run/systemd/system.control/"user-$TUID.slice.d"/50-MemoryLow.conf \
        /run/systemd/system.control/system.slice.d/50-MemoryMin.conf \
        /run/systemd/system.control/"$SSH_UNIT.d"/50-{MemoryMin,CPUWeight}.conf
  rm -f /run/user/"$TUID"/systemd/user.control/app.slice.d/50-MemoryLow.conf \
        /run/user/"$TUID"/systemd/user.control/claude-remote-control.service.d/50-{MemoryLow,CPUWeight}.conf

  local f
  for f in /etc/systemd/oomd.conf.d/50-sanctuary-guard.conf \
           "/etc/systemd/system/user@$TUID.service.d/50-sanctuary-guard.conf" \
           /etc/systemd/system/user.slice.d/50-sanctuary-guard.conf \
           "/etc/systemd/system/user-$TUID.slice.d/50-sanctuary-guard.conf" \
           /etc/systemd/system/system.slice.d/50-sanctuary-guard.conf \
           "/etc/systemd/system/$SSH_UNIT.d/50-sanctuary-guard.conf" \
           /etc/sysctl.d/90-sanctuary-guard.conf /etc/modules-load.d/sanctuary-guard.conf \
           /etc/modprobe.d/sanctuary-guard.conf /etc/sanctuary-guard/health.env \
           /usr/local/sbin/sanctuary-health \
           "$UGUARD/agi.slice" "$UGUARD/agi-engine.slice" "$UGUARD/agi-work.slice" "$UGUARD/ramdisk.slice" \
           "$UGUARD/agi-.service.d/50-sanctuary-guard.conf" "$UGUARD/agi-agi-.service.d/50-sanctuary-guard.conf" \
           "$UGUARD/app.slice.d/50-sanctuary-guard.conf" "$UGUARD/-.slice.d/50-sanctuary-guard.conf" \
           "$UGUARD/claude-remote-control.service.d/50-sanctuary-guard.conf" \
           "$UGUARD/sanctuary-watch.service" "$UGUARD/sanctuary-watch.timer" \
           "$THOME/.local/bin/sanctuary-watch" "$THOME/.config/sanctuary-guard/watch.env"; do
    [ -e "$f" ] && rm -f "$f" && ok "removed $f"
  done
  if [ -e /etc/sanctuary-guard/oomd.enabled-by-guard ]; then
    systemctl disable --now --quiet systemd-oomd.service 2>/dev/null || true
    rm -f /etc/sanctuary-guard/oomd.enabled-by-guard
    ok "systemd-oomd disabled (guard had enabled it)"
  else
    systemctl restart systemd-oomd.service 2>/dev/null || true
    ok "systemd-oomd left enabled (it was on before guard)"
  fi
  rmdir "$UGUARD/agi-.service.d" "$UGUARD/agi-agi-.service.d" "$UGUARD/app.slice.d" "$UGUARD/-.slice.d" \
        "$UGUARD/claude-remote-control.service.d" \
        "/etc/systemd/system/user@$TUID.service.d" /etc/systemd/system/user.slice.d \
        "/etc/systemd/system/user-$TUID.slice.d" /etc/systemd/system/system.slice.d \
        "/etc/systemd/system/$SSH_UNIT.d" /etc/sanctuary-guard \
        "$THOME/.config/sanctuary-guard" 2>/dev/null || true
  sysctl -q -w kernel.panic=0 kernel.panic_on_oops=0
  systemctl daemon-reload; umgr daemon-reload
  ok "done. Left installed: systemd-oomd, watchdog (disabled). softdog stays loaded until reboot, disarmed."
  say "  Engine units already running inside agi-*.slice stay there until they restart."
}

# =============================================================================
case $MODE in
  status) if status; then exit 0; else exit 1; fi ;;
  uninstall) uninstall; exit 0 ;;
esac

head_ "sanctuary guard on $HOST for $TUSER  ($([ "$MODE" = dry ] && echo "DRY RUN: nothing will change" || echo applying))"
cat <<EOF
  settings        $GUARD_ENV_FROM, key _$HOSTKEY
  RAM ${RAM_M}M   swap ${SWAP_M}M   reserve ${RESERVE_M}M   docker ${DOCKER_M}M
  user@$TUID      high ${USER_HIGH_M}M  max ${USER_MAX_M}M  swap ${USER_SWAP_M}M   (Claude MemoryLow ${CLAUDE_LOW_M}M)
    agi.slice     high ${AGI_HIGH_M}M  max ${AGI_MAX_M}M
      agi-engine  high ${ENGINE_HIGH_M}M  max ${ENGINE_MAX_M}M  (swap ${ENGINE_SWAP}, 128 tasks)
      agi-work    high ${WORK_HIGH_M}M  max ${WORK_MAX_M}M
  watchdog        $([ $DO_WATCHDOG = 1 ] && echo "reboot after 5 min at memory PSI full >= ${PSI_FULL}% (grace ${GRACE_S}s after boot)" || echo "SKIPPED (--no-watchdog)")
  watch           $([ $DO_WATCH = 1 ] && echo "every 2 min; recovery claude $([ "$PEER_CLAUDE" = 1 ] && echo ON || echo off)" || echo "SKIPPED (--no-watch)")
EOF

layer1
layer2
layer3
(( DO_WATCHDOG )) && layer4
(( DO_WATCH )) && layer5
docker_section

head_ "done"
if [ "$MODE" = dry ]; then
  say "  Dry run: nothing changed. Apply with:  sudo $0${ARGS:+ ${ARGS/--dry-run/}}"
else
  say "  Applied with $WARNINGS warning(s). Verify:  $0 --status"
fi
