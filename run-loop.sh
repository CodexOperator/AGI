#!/bin/bash
# run-loop.sh — bounded iteration loop for pi-autoresearch
# Each invocation: starts/continues autoresearch loop, runs ONE experiment, exits cleanly.
# External shell loop → fresh pi session each time, no context accumulation.
# Loops until maxIterations=48 or killed.
#
# Stop: kill this process (kill %% in the shell, or message Belam "stop")
# Tail log: tail -f ~/.hermes/agi/loop.log

AGI_DIR="$HOME/.hermes/agi"
LOG="$AGI_DIR/loop.log"
SESSION_DIR="$AGI_DIR/sessions"
MAX_ITERS=48
ITER_TIMEOUT=540  # 9 min per pi call (leaves 1min buffer before 15min cron slot)

mkdir -p "$SESSION_DIR"

echo "$(date) — loop starting (max $MAX_ITERS iters, ${ITER_TIMEOUT}s timeout/iter)" >> "$LOG"

ITER=0
while true; do
  # Hard stop check
  if [ -f "$AGI_DIR/autoresearch.jsonl" ]; then
    ITER=$(wc -l < "$AGI_DIR/autoresearch.jsonl" 2>/dev/null || echo 0)
    if [ "$ITER" -ge $MAX_ITERS ]; then
      echo "$(date) — maxIterations ($MAX_ITERS) reached, exiting" >> "$LOG"
      break
    fi
  fi

  # Fresh pi session. timeout kills after ITER_TIMEOUT seconds (hard stop).
  # --session-dir ensures clean session isolation per run.
  # Extension loads automatically from ~/.pi/agent/settings.json packages.
  timeout $ITER_TIMEOUT pi \
    --session-dir "$SESSION_DIR" \
    --skill ~/.pi/agent/git/github.com/davebcn87/pi-autoresearch/skills/autoresearch-create \
    "Resume the autoresearch loop in ~/.hermes/agi/.
     Read ~/.hermes/agi/autoresearch.md (current state + what's been tried).
     Run exactly ONE experiment iteration:
       1. Make one code change (small, targeted)
       2. git commit
       3. run_experiment (./autoresearch.sh)
       4. log_experiment (keep if improved, discard if not)
     After log_experiment, stop — do NOT loop again.
     Report iteration result in one line to stdout." \
    >> "$LOG" 2>&1

  EXIT_CODE=$?
  echo "$(date) — iter done, timeout exit=$EXIT_CODE" >> "$LOG"

  sleep 5  # brief pause between runs
done
