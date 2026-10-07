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
