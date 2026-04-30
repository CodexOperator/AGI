#!/bin/bash
# start.sh — launch pi-autoresearch in ~/.hermes/agi
# Continuous loop. maxIterations=48 (12hrs @ 15min/iter) as ceiling.
# Tell Shael to message to stop.

cd ~/.hermes/agi

exec pi \
  --session-dir ~/.pi/agent/sessions \
  --skill ~/.pi/agent/git/github.com/davebcn87/pi-autoresearch/skills/autoresearch-create \
  "Goal: investigate DB-augmented directed code generation via unified graph memory.
   Metric: graph_build_time_ms (lower is better).
   Files in scope: ~/.hermes/agi/ schema, Python modules, and the belam-codex source (~/.hermes/belam-codex/).
   Context: the belam-codex workspace uses GitNexus for code intelligence (symbol graphs, impact analysis).
   pi session dir: ~/.hermes/agi/ — write all output files there.
   Init the experiment, run baseline, then loop until Shael says stop."
