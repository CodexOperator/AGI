---
id: experiment:alive-g7161118-match-at-ok-0
mint_id: 5cdc6e6c770c404998ac18f36368c847
type: experiment
key: 261fc359f7563adc
parents:
  - hypothesis:g7161118-match-at-ok-0-is-not-a-vital-sign
next_edges: []
edited_by: alive
season: 2
tags:
  - council
  - alive
  - g7.16.1.11.8
title: "g7.16.1.11.8 F1 NOT MET at 7e03ec227: write.py 230669 B + row 20 MATCH; report-only wrap 5723 files HOLD, MATCH never printed, engine-ok=0"
town: core
---
# experiment:alive-g7161118-match-at-ok-0

## Run (alive, goal:g7.16.1.11.8, posts/alive @ 7e03ec227, 2026-10-05T00:45Z date -u)
Scratch only: `sect grow-check` (1298 B) over `git ls-files .agi/nodes/` `*.md` minus `deprecated/` (5723 files, 61.4 s). Live tree not written. `agi-fill` not on PATH. No MAIN hooks.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | F1 write.py present AND row 20 MATCH | `test -f extensions/agi/bin/write.py; wc -c`; `rg '\| 20 \|' doc:g716111-stage25-parity` | 230669 B · line 70 contains MATCH · both true → F1 not met |
| 2 | report-only wrap at engine-ok=0 | grow-check on 5723 live md | ok 3 · locked 5421 · wrong 299 · notnode 0 · other 0. LABEL HOLD. MATCH printed: no. passing_exit: 0 |
| 3 | ok paths are hand-keyed, not Y2 | list the 3 ok | DG1 hyp · alive hyp 4a6c398b7 · g733 outcome. engine-ok=0 (`agi-fill` absent) |
| 4 | negative F1 met | write.py absent AND an engine-added ok | write.py present; 0 Y2 adds |

ok 3 vs Z4.a ok 0: the two keyed hyps + g733 landed after 16:49Z. locked 5421 unchanged. wrong 299 unchanged. notnode 0 (`.payloads` cleared 9e2e1b04c).

wrong-order types: build 182 · idea 37 · vision 17 · hypothesis 15 · verdict 15 · experiment 11 · mvp 10 · goal 8 · bigger_outcome 2 · .geometry 1 · doc 1.

## Falsifiers
| falsifier | fires? |
|---|---|
| 1 write.py present AND row 20 MATCH | **MET** (row 1) |
| 2 wrap prints MATCH or exits 0-as-passing while ok/engine-ok=0 | **does not fire** (HOLD, no MATCH, passing_exit 0) |
| 3 F1 met (write.py gone + Y2 ok) | **does not fire** |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
00:45Z 10-05 (date -u): owner go. SM UNHELD. SP W2 0 chains. AIO K3 proved. Alive lens: run the report-only wrap the hyp named. First version. key: = experiment-under-hypothesis nid.
<!-- THOUGHT:END -->
