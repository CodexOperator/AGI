#!/bin/bash
# env-get.sh — print one value out of the project's `.env`, and nothing else.
#
# Exists for pi's auth.json indirection (goal:g1.8). `~/.pi/agent/auth.json`
# supports a `"!command"` key form, so:
#
#   "openrouter": { "type": "api_key",
#                   "key": "!/home/ubuntu/work/agi/extensions/agi/bin/env-get.sh OPENROUTER_API_KEY" }
#
# makes pi resolve the secret from the SAME single file `driver.sh` sources,
# instead of holding a second copy that can drift from it. One value, one file,
# two readers.
#
# Resolution is deliberately anchored to THIS SCRIPT's location, not to cwd:
# pi is launched from wherever the user happens to be standing, and a key
# lookup that silently resolves a different project's `.env` depending on cwd
# is the kind of quiet wrong answer this repo exists to not ship.
#
# Prints the value with no trailing newline, on stdout, and nothing else ever.
# Every diagnostic goes to stderr so a caller can capture stdout blind.
#
# 🔴 THE ENVIRONMENT WINS OVER THE FILE, and that ordering is goal:g1.11's
# whole mechanism rather than a convenience (fixed 2026-09-03, L1.02).
#
# `dispatch.py` mints a capped, expiring key per spawn and injects it into the
# child's environment as OPENROUTER_API_KEY. pi does not read that variable:
# its auth.json points at THIS SCRIPT, and this script used to read `.env`
# unconditionally. So every kid authenticated with the shared long-lived key
# while a minted key sat unused beside it -- the engine minted 2 keys in the
# first live run and both ended at `usage=0` while spend landed on the shared
# key. Per-spawn credentials were, end to end, decorative.
#
# It was invisible because the mechanism was proved against a stub that dumps
# its environment. A stub that reads $OPENROUTER_API_KEY proves injection; it
# cannot prove the harness READS what was injected, and pi does not.
set -euo pipefail

VAR="${1:?usage: env-get.sh VAR_NAME [ENV_FILE]}"

# Injected wins. Checked before the env file is even resolved, because a
# spawned agent's credential must not depend on a file lookup succeeding.
if [[ -n "${!VAR-}" ]]; then
  printf '%s' "${!VAR}"
  exit 0
fi

SCRIPT_REAL="$(readlink -f "${BASH_SOURCE[0]}")"
PLUGIN_ROOT="$(cd "$(dirname "$SCRIPT_REAL")/.." && pwd)"

ENV_FILE="${2:-}"
if [[ -z "$ENV_FILE" ]]; then
  # The path is graph content: `nodes/.geometry/secrets.md` declares it and
  # `envfile.py` resolves it (goal:g10.2). Asked for rather than written here,
  # so this script and driver.sh cannot disagree about where the file is.
  ENV_FILE="$(python3 "$PLUGIN_ROOT/bin/envfile.py" "$PLUGIN_ROOT" --what env-file 2>/dev/null || true)"
fi

if [[ -z "$ENV_FILE" ]]; then
  echo "ERR: could not resolve an env file from $PLUGIN_ROOT" >&2
  exit 1
fi

if [[ ! -f "$ENV_FILE" ]]; then
  echo "ERR: no env file at $ENV_FILE — copy .env.example and fill it in" >&2
  exit 1
fi

value="$(set -a; . "$ENV_FILE"; set +a; printf '%s' "${!VAR-}")"

if [[ -z "$value" ]]; then
  echo "ERR: $VAR is unset or empty in $ENV_FILE" >&2
  exit 1
fi

printf '%s' "$value"
