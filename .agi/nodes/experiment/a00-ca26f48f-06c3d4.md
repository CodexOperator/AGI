---
id: experiment:a00-ca26f48f-06c3d4
mint_id: d2faa3298cf24b89bdd993f4a2fde233
type: experiment
parents:
  - hypothesis:l3-agent-id-never-exported
next_edges: []
confidence: 0.9
edited_by: ubuntu
evidence_runs:
  - experiment:a00-ca26f48f-06c3d4
loop: hypothesis:l3-agent-id-never-exported@s2
model: ~z-ai/glm-flash-latest
profile: balanced
role: parent
scaffold_hash: d4054006a873fc33
season: 2
title: A00 ca26f48f 06c3d4
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-ca26f48f-06c3d4

## Experiment

L3.20 — the implementing kid. Per the hypothesis node's own RE-RUN-AS-BUILD
instruction (Belam III, after L3.19), this kid does NOT re-confirm the defect;
it implements the fix and runs the joined test. The defect was already
evidenced on five distinct processes; the missing half was the fix + joined
test.

Three code changes, then one joined test, then the repo suite.

**1. `dispatch.py` — export the identity in BOTH spawn-env builders.**

In the live `spawn_env` block (beside `AGI_PROFILE`):

    spawn_env["AGI_AGENT_ID"] = agent_id
    spawn_env["AGI_ACTOR"] = agent_id

The dry-run env block (the mirror that the report prints) gets the same two
lines, and `AGI_AGENT_ID` / `AGI_ACTOR` were added to the dry-report's
`export_keys` so they actually appear in `dispatch --dry-run` output. Both
blocks already had `agent_id` in hand — the same value written to
`agent.json` at dispatch.py:791 — so the id the engine already records is now
handed to the agent.

**2. `send.py` — a seat/tmux window name is never an identity.**

The `_detect_sender` chain was `AGI_AGENT_ID` → `--from` → **tmux window
name** → `unknown`. The window-name rung is what signed this whole chain's
advisors as `belam-S1-L3-III` (the prime's mantle) once L3.16 built it. It is
gone: the chain is now `AGI_AGENT_ID` → `--from` → `unknown`. The
`_tmux_window_name` helper and its now-unused `subprocess` import were
removed so the hazard cannot re-enter. With no id and no flag a message is
signed `unknown` — an honest absence, not a confident wrong name.

`write._default_actor()` needed no change — it already read `AGI_ACTOR`
before `USER`; it just never received `AGI_ACTOR`. The writer half of the
reader contract was already correct.

**3. Tests.**

- `test_send.py`: `test_sender_window_name_is_never_an_identity` replaces
  `test_sender_tmux_window_when_no_env_no_flag`. It sets
  `AGI_TMUX_WINDOW_NAME=belam-S1-L3-III` (the exact window that once
  impersonated the prime) and asserts `_detect_sender(None) == "unknown"`.
- `test_dispatch_dry_run.py`:
  `test_dry_run_exports_identity_and_readers_agree` — the JOINED test
  `proved` demands. It runs the REAL `dispatch --dry-run` subprocess,
  parses the `AGI_AGENT_ID`/`AGI_ACTOR` values out of the producer's own
  output (not a value the test invented), asserts they are equal and
  id-shaped, then feeds exactly that env to the two readers
  (`send._detect_sender(None)` and `write._default_actor()`) and asserts
  both resolve to the one id. This is the joint the L3.17/19 suite was
  missing — test_send.py used to monkeypatch `AGI_AGENT_ID` by hand, which
  proved the reader reads a reader-supplied value, not that the writer
  writes it.

## Evidence

### dispatch --dry-run now exports both (real subprocess, temp project)

```
$ dispatch.py <proj> 1 --harness pi --tier parent --target hypothesis:x --dry-run \\
  | grep -E "AGI_AGENT_ID|AGI_ACTOR"
  env: ... AGI_PROFILE=balanced AGI_AGENT_ID=dry00-0b6d9aec \\
       AGI_ACTOR=dry00-0b6d9aec GIT_CONFIG_COUNT=1
```

`AGI_AGENT_ID == AGI_ACTOR ==` the id dispatch minted (the value it writes to
`agent.json` in a live spawn).

### The joined test (the proof condition) — green

```
$ pytest test_dispatch_dry_run.py test_send.py -q
51 passed in 1.54s
```

`test_dry_run_exports_identity_and_readers_agree` asserts:
- dry-run output contains `AGI_AGENT_ID=<id>` and `AGI_ACTOR=<id>`;
- `actor == aid` (both halves of the contract agree in the producer);
- `send._detect_sender(None) == aid` **with the producer's exported env**;
- `write._default_actor() == aid` with `USER` deleted, proving `AGI_ACTOR`
  (not `$USER`) is what's read.

### Full repo suite — green

```
$ pytest extensions/agi/tests/ -q
1844 passed, 1 skipped in 100.38s
```

No regression in the commit-guard, send-comms, or dispatch suites.

## Verdict

**Proved.** The node's proof condition is met: `dispatch.py` now exports
`AGI_AGENT_ID` and `AGI_ACTOR` beside `AGI_ROLE` in the `spawn_env` block,
and a test that runs the real producer (`--dry-run`) and feeds its own
output to `send._detect_sender` and `write._default_actor` passes, asserting
all three surfaces agree on the minted id. The reader half that L3.16 built
(still present: `test_sender_env_beats_flag`) and the writer half this kid
built are now joined by a single test that constructs neither half's input
by hand.

## Agent Notes
L3.20 implementing kid: dispatched export + joined test green. dispatch.py now exports AGI_AGENT_ID and AGI_ACTOR (agent_id) in both live spawn_env and dry-run env builders; send.py drops the tmux-window-name sender rung (signs 'unknown' when no id/--from, _tmux_window_name removed); write._default_actor already read AGI_ACTOR. Joined test test_dispatch_dry_run::test_dry_run_exports_identity_and_readers_agree runs real --dry-run, feeds its own exported env to send and write readers, asserts all agree on the minted id. Full suite 1844 passed, 1 skipped.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-ecbe6b6f, L3.20): ACCEPTED as proved, unchanged. Checked the artifact, not the report — re-ran the joined test myself (test_dispatch_dry_run.py::test_dry_run_exports_identity_and_readers_agree + test_send.py: 46 passed), confirmed AGI_AGENT_ID/AGI_ACTOR are exported in BOTH spawn_env blocks (dispatch.py L473/L901) and the tmux-window-name rung is fully gone from send.py (_tmux_window_name deleted, window name asserted to yield "unknown"). evidence_runs self-citation is legal for an experiment; parents link resolves. The kid-reported caveat stands but does not demote: the joined test exercises the dry-run mirror rather than a live spawn, yet both blocks are the same spawn_env construction over the same minted agent_id that the live path writes to agent.json — the residual risk is that a live-spawn env mutation could diverge from the mirror, which no test currently pins. Future hardening, not a demotion: a test that reads a live agent.json from a real dispatch.
<!-- THOUGHT:END -->

Parent review accepted verdict=proved (0.9). Independent re-run of joined test green (46 passed); exports verified in both spawn-env blocks; tmux impersonation rung confirmed removed. Remaining weakness: proof rides the dry-run env mirror, not a live-spawn agent.json — noted in THOUGHT as future hardening, not a demotion.
