#!/bin/bash
cd /data/work/agi/.agi/worktrees/a00-67c8a71a || exit 1
S=.agi/sessions/iter-OSC.11/a00-67c8a71a
echo "PROBE T0 $(date -u +%T) avail=$(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo) load=$(cut -d' ' -f1 /proc/loadavg)" >> $S/probe_run.log
docker stop llama-server >> $S/probe_run.log 2>&1
sleep 3
python3 -u $S/probe_q8.py >> $S/probe_run.log 2>&1
echo "PROBE ARMS DONE $(date -u +%T)" >> $S/probe_run.log
docker start llama-server >> $S/probe_run.log 2>&1
for i in $(seq 1 120); do curl -sf --max-time 3 127.0.0.1:8080/health >/dev/null && break; sleep 2; done
echo '{"model":"Qwen3.5-9B-Q4_K_M","messages":[{"role":"user","content":"ping"}],"max_tokens":8,"temperature":0}' > $S/probe_restore_req.json
curl -s --max-time 300 -X POST 127.0.0.1:8080/v1/chat/completions -H 'Content-Type: application/json' -d @$S/probe_restore_req.json > $S/probe_restore_completion.json
curl -s --max-time 10 127.0.0.1:8080/slots > $S/probe_restore_slots.json 2>&1
echo "PROBE RESTORED $(date -u +%T)" >> $S/probe_run.log
