#!/bin/bash
# OSC.11 arm runner: the box is memory-contended by parallel agents, so each arm waits for a
# window (MemAvailable >= 6000 MB) before loading the 9B, and a failed load is retried once.
cd /data/work/agi/.agi/worktrees/a00-67c8a71a || exit 1
S=.agi/sessions/iter-OSC.11/a00-3caaf6eb
ARMS="${1:-f16_512 f16_1024 f16_2048 q8_0_512 q8_0_1024 q8_0_2048 q4_0_512 q4_0_1024 q4_0_2048}"
for arm in $ARMS; do
  for attempt in 1 2; do
    for w in $(seq 1 24); do
      a=$(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo)
      if [ "$a" -ge 6000 ]; then break; fi
      sleep 20
    done
    a=$(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo)
    echo "ARM $arm attempt $attempt avail=${a}MB $(date -u +%T)" >> $S/runner.log
    python3 -u .agi/context/local-maxxing/serve/ub_prefill_round.py t1 "$arm" >> $S/runner.log 2>&1
    ok=$(python3 -c "import json;d=json.load(open('datasets/serving-sweep/2026-09-23-ub/logs/ub_${arm}.json'));print(1 if d['load_s'] is not None else 0)" 2>/dev/null || echo 0)
    [ "$ok" = 1 ] && break
  done
done
echo "RUNNER DONE $(date -u +%T)" >> $S/runner.log
