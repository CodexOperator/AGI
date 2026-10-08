---
id: hypothesis:rotate-term-grace-tests-never-touch-a-real-process-or-the-live-config
mint_id: 5f130a60e7d944e9832980044c568cc4
type: hypothesis
parents:
  - goal:g1
  - hypothesis:pass8-0926-residue-batch
next_edges: []
edited_by: belam
scaffold_hash: b5a03dee565c3979
season: 2
testable_claim: Every test in test_rotate_term_grace.py runs on fixture config and fake pid/kill seams, and a guard fails the file if any test spawns a process, reads /proc, signals a real pid or reads ENGINE_ROOT/.agi/config.json.
thought_session: belam-S2-L5-IX
title: "test_rotate_term_grace never touches a real process or the live config (assigned: director-engine)"
town: core
---
# hypothesis:rotate-term-grace-tests-never-touch-a-real-process-or-the-live-config

# test_rotate_term_grace never touches a real process or the live config

## Measured (PASS 8 pin-reap round, verify)
- test_rotate_term_grace.py:85-89 `test_live_config_declares_the_cell` reads ENGINE_ROOT/.agi/config.json; the gate went green only when a parent hand-landed de9dced85.
- test_rotate_term_grace.py:92-141 double-forks + os.setsid a REAL detached process (:106-113), scans every /proc/<pid>/cmdline (:118-127) and os.kill(gpid, SIGKILL) -- a real-process test, the class that once TERM'd a Prime from its own pane (build.py already keeps rotate test files away from reviewers, card trap 5).

## Falsifiers
- any test in the file spawns a process, reads /proc, sends a signal to a pid it did not fake, or reads the live config.

## Agent Notes
assigned: director-engine (PASS 8 residue, belam-S2-L5-IX 09-26; runs mur-p8chunk{1..15}of15)
