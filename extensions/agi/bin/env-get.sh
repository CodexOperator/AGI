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
set -euo pipefail

VAR="${1:?usage: env-get.sh VAR_NAME [ENV_FILE]}"

SCRIPT_REAL="$(readlink -f "${BASH_SOURCE[0]}")"
PLUGIN_ROOT="$(cd "$(dirname "$SCRIPT_REAL")/.." && pwd)"

ENV_FILE="${2:-}"
if [[ -z "$ENV_FILE" ]]; then
  # Same resolver every other entry point calls; `--what source` is the repo
  # enclosing `.agi/` under the g11 layout, which is where `.env` lives.
  SOURCE_ROOT="$(python3 "$PLUGIN_ROOT/bin/locations.py" "$PLUGIN_ROOT" --what source 2>/dev/null || true)"
  ENV_FILE="${SOURCE_ROOT:-$PLUGIN_ROOT}/.env"
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
