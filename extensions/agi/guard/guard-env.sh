# guard-env.sh -- the ONE reader of config:guard's ```sh guard.env block (goal:g1.41 C). SOURCED by guard-init.sh, ram-main.sh, ram-tier.sh, session-sweep.sh; nothing is ever eval'd.
# Accepts blank lines, # comments and GUARD_<CELL>=<value> (a CELL name: GUARD_UPPER_WORDS_<lowercase box key>, so no script-internal GUARD_DIR / GUARD_ENV_NODE / GUARD_BOX can be set from a block): bare [A-Za-z0-9._:/@%+,-]* or 'single quoted' of that set + space = > + the literal $HOME (string substitution). Anything else exits 1 naming the node and the line BEFORE the caller does anything. _GE_LINES = non-blank block lines read (0 = no block, or an empty one).
guard_env_load() {  # NODE
  local LC_ALL=C ln=0 inb=0 line name val ok; local bare='^[A-Za-z0-9._:/@%+,-]*$' quoted="^'([A-Za-z0-9._:/@%+, =>-]|[\$]HOME)*'\$"; _GE_LINES=0
  [ -f "$1" ] || return 0
  while IFS= read -r line; do ln=$((ln + 1))
    if [[ $line =~ ^\`\`\`sh\ guard\.env[[:space:]]*$ ]]; then inb=1; continue; fi
    [ $inb = 1 ] || continue; [[ $line =~ ^\`\`\`[[:space:]]*$ ]] && break; [[ $line =~ [^[:space:]] ]] && _GE_LINES=$((_GE_LINES + 1))
    [[ $line =~ ^[[:space:]]*(#.*)?$ ]] && continue
    name=${line%%=*}; val=${line#*=}; ok=
    [[ $line == *=* && $name =~ ^GUARD_[A-Z][A-Z0-9_]*_[a-z0-9][a-z0-9_]*$ ]] && { [[ $val =~ $bare ]] || { [[ $val =~ $quoted && $val != *'$HOME'[A-Za-z0-9_]* ]] && val=${val:1:-1} && val=${val//\$HOME/"$HOME"}; }; } && ok=1
    [ -n "$ok" ] || { echo "guard.env: $1 line $ln refused (not blank, # comment or GUARD_NAME=value): nothing evaluated" >&2; return 1; }
    printf -v "$name" %s "$val"
  done < "$1"
}

# Cells whose VALUE reaches a sink beyond a bash variable (a unit file, watch.env that sanctuary-watch dot-sources, a sudo/mount argv): checked for the shape that sink needs, refused BY NAME before any side effect (g1.41 C RC1/RC2).
# sinks: PEERWATCH_CLAUDE -> watch.env (dot-sourced) · RAM_DIR / RAM_WORKTREES -> unit text, mount argv · RAM_MAIN, TIER_HOT, TIER_COLD, TIER_DIRS, SWEEP_PAIRS, *_ARCHIVE -> mount / rsync / ln argv · the *_MIN / *_PCT numbers -> timer unit text, arithmetic.
declare -A _GE_KIND=([PEERWATCH_CLAUDE]=bool [RAM_SYNC_MIN]=uint [SWEEP_IDLE_MIN]=uint [SWEEP_PRESSURE_PCT]=uint [SWEEP_PRESSURE_IDLE_MIN]=uint [SWEEP_CLAUDE_IDLE_MIN]=uint [RAM_WT_HOLD_PCT]=uint [RAM_MAIN]=path [RAM_DIR]=path [RAM_WORKTREES]=path [TIER_HOT]=path [TIER_COLD]=path [AGI_SESSIONS_ARCHIVE]=path [CLAUDE_PROJECTS_ARCHIVE]=path [TIER_DIRS]=paths [SWEEP_PAIRS]=pairs)
guard_cells_check() {  # KEY
  local LC_ALL=C c n v re p='/[A-Za-z0-9._/+,:@-]*'
  for c in "${!_GE_KIND[@]}"; do n=GUARD_${c}_$1; v=${!n-}; [ -n "$v" ] || continue
    case ${_GE_KIND[$c]} in bool) re='^[01]$';; uint) re='^[0123456789]{1,9}$';; path) re="^$p\$";; paths) re="^$p( $p)*\$";; pairs) re="^$p=>$p( $p=>$p)*\$";; esac
    [[ $v =~ $re ]] || { echo "guard.env: cell $n is not a valid ${_GE_KIND[$c]} value (its sink cannot take it): refused, nothing done" >&2; return 1; }
  done
}
