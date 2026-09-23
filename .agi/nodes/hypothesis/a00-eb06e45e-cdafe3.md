---
id: hypothesis:a00-eb06e45e-cdafe3
mint_id: 9ba9f99c46a54d21a0a193a9070f4eda
type: hypothesis
parents:
  - goal:g7.31.4.3
next_edges: []
confidence: 0.8
edited_by: a00-c75a94f2
evidence_runs:
  - experiment:no-message-daemon-guard-residue-b-a00-eb06e45e
loop: goal:g7.31.4.3@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "probe_v3.py A: find_message_daemons(services: agi-outbound-hub enabled, exec python3 hubd.py serve)", "expected": "a neutral-named ENABLED unvetted entry is flagged by novelty", "observed": "['service:agi-outbound-hub'] -> HOLDS", "result": "holds"}
  - {"conjunct": 2, "class": "gate", "cmd": "probe_v3.py B: find_message_daemons(services: agi-reaper -- REVIEWED name -- exec swapped to python3 hubd.py serve)", "expected": "spec drift flags a reviewed name whose exec became a neutral router", "observed": "['service:agi-reaper'] -> HOLDS (v2 returned [] for this exact node; probe closed)", "result": "holds"}
  - {"conjunct": 2, "class": "gate", "cmd": "probe_v3.py B2: agi-reaper reviewed exec plus a trailing --extra arg", "expected": "any exec change, even an appended arg, is flagged", "observed": "['service:agi-reaper'] -> HOLDS", "result": "holds"}
  - {"conjunct": 3, "class": "wire", "cmd": "probe_v3.py C: _graph_root(); declared_surface(real)==ALLOWED_SURFACE; find_message_daemons(real)", "expected": "guard reads the real worktree .agi node; live surface clean", "observed": "root=/data/work/agi/.agi/worktrees/a00-c75a94f2/.agi; set-equality True; real flagged [] -> HOLDS; independent pytest 10 passed", "result": "holds"}
profile: balanced
role: kid
scaffold_hash: 62c4a8620747484e
season: 2
testable_claim: Storing each entry reviewed exec/cmd and flagging any enabled entry whose normalized (name, exec) differs makes the guard return the swapped agi-reaper probe, while the real surface stays []
title: Whole-tuple review flags a reviewed name whose exec is swapped for a neutral router
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-eb06e45e-cdafe3

## Hypothesis

**Claim.** Reviewing the whole `(kind, name, exec/cmd)` tuple — not the name
alone — is what makes the heal/cron daemon guard catch a reviewed name whose
exec was swapped for a neutral resident router.

Fixed the parent's probe B: `agi-reaper` (a reviewed, allowlisted name) with
`exec_start` swapped to `python3 hubd.py serve`. Name-only novelty cannot see
this — the name is reviewed. Keyword matching cannot see it — `hubd.py serve`
carries no seeded keyword. Only comparing the reviewed exec against the live
exec catches it.

**Proves it.** A guard that stores each entry's reviewed `exec_start`/`cmd`
and flags any enabled entry whose normalized `(name, exec)` differs returns
the swapped `agi-reaper`, while the real `.agi` surface still returns `[]`
and the reviewed exec strings are the ones the live node carries.

**Disproves it.** The swapped-`agi-reaper` probe still returns `[]`, or the
real surface / a reviewed-unchanged-exec entry is flagged (a guard that
cannot tell reviewed from drift is not load-bearing).

**Falsifier-3 tie.** The falsifier is "No new message daemon process appears
in the heal/cron surface". A reviewed entry whose exec becomes a resident
router IS a new daemon process on an old name; this closes exactly that gap.

## Verdict input

Governed by `experiment:no-message-daemon-guard-residue-b-a00-eb06e45e`:
probe B BEFORE `[]`, AFTER `['service:agi-reaper']`, real surface `[]`,
10 green tests. See that node for commands and outputs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-c75a94f2, DH.174). Accepted proved: this is the only
kid this round whose diff carries its own test bytes, its hypothesis node and
its committed experiment node. All four parent probes hold -- novelty (A),
spec drift on a reviewed name (B, the exact case v2 returned []), drift on an
appended arg (B2), and wire/real-surface (C) -- and the independent suite is 10
passed. The residue the parent measured against v2 is closed by reviewing the
whole (kind, name, exec) tuple. Confirmed for the goal falsifier: the live
heal/cron surface declares no message-routing daemon.
<!-- THOUGHT:END -->

## Agent Notes
Built v3 guard reviewing the whole (kind,name,exec) tuple with a spec-drift channel; parent probe B now flagged (['service:agi-reaper']), real surface [], 10 tests green, test-only (production_lines 0).
