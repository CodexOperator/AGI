---
id: experiment:a00-2fa1fab0-b7d2a0
mint_id: b65c3d184cdf46558ab1f69b9eeccfae
type: experiment
parents:
  - hypothesis:pin-reap-never-names-a-live-session-and-a-reap-leaves-no-stale-app-session
next_edges: []
confidence: 0.6
edited_by: a00-2fa1fab0
evidence_runs:
  - experiment:a00-2fa1fab0-b7d2a0
loop: hypothesis:pin-reap-never-names-a-live-session-and-a-reap-leaves-no-stale-app-session@s2
model: stealth/space-bunny-alpha
production_lines: 29
profile: balanced
role: kid
scaffold_hash: 5d64663d137c5703
season: 2
title: s12 TERM grace becomes reaper.term_grace_s; app-session sweep is MEASURED-impossible, so that half is a lean
town: core
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-2fa1fab0-b7d2a0

Conjunct (3) ONLY: "the reap path ends a remote-control session cleanly (TERM
with a grace long enough for the CLI to disconnect, MEASURED) BEFORE any KILL,
and where the CLI/API offers a way to end an app session of a dead pid, a sweep
uses it -- if it offers none, the node records that as MEASURED and the claim's
app half is a lean, never a fabricated pass."

## What I did — A: the TERM grace is now a config cell

| item | value |
|---|---|
| cell | `reaper.term_grace_s` in `.agi/config.json` |
| live value | `15.0` |
| code default (resolver for an ABSENT cell) | `15.0` in `rotate._term_grace_s()` |
| replaced | the hard-coded signature default `wait_secs: float = 5.0` |
| read | at RUNTIME, per `_reap_chain` call, via `locations.config_path(find_project_root())` — the same style heal.py:693 `_late_reap_wait_max_s` uses |

`wait_secs` is now `float | None = None`; an explicit `wait_secs=` from a caller
still wins, and only the absent case resolves the cell. A malformed cell
(string / bool / negative / zero / null / list) and a broken `config.json` both
fall back to 15.0 and never raise.

WHY 15.0 and not 5.0: the measured claude CLI TERM->exit is **1.1 s**
(§B), so 5.0 was already 4.5x the measurement — but 5.0 was a constant nobody
could move without editing the engine, and a BUSY session (a large transcript to
flush) is the case that matters. 15.0 is 13x the measurement, still bounded, and
now tunable in config instead of in source. 30 was rejected: it multiplies the
cost of every reap by 3 for a case I did not measure, and a fabricated 30 s is
exactly the thing this conjunct forbids.

A second resolver was written because heal's is not importable: it is
key-specific (`late_reap_wait_max_s`) and `heal.py` imports `rotate.py`, so the
dependency runs the wrong way. The STYLE is copied, the key is not.

Production lines: `git diff --numstat` -> `rotate.py 27/2`, `config.json 2/1`
= **29** (ceiling 40).

## What I did — B: MEASURED disconnect latency (throwaway, never a real seat)

Not a seat, not a pane, not a director. My own process, in my session dir.

1. **A throwaway `claude --bg` session of my own** (`5861181b`).
   `claude stop 5861181b` -> `stopped 5861181b`, **0.79 s wall**, pid gone from
   the registry. That is the CLI's own documented graceful stop, measured.
2. **A throwaway `claude --remote-control zz-probe-2fa1fab0`** launched on my
   own pty, SIGTERMed by me:

```
TERM->exit 1.1 rc 143
AFTER TERM (app view): []
PID ALIVE: False
```

**MEASURED: 1.1 s** for a real `--remote-control` claude process to be gone
after SIGTERM (n=1, throwaway, this box, idle at start).

LIMIT, stated plainly: rc 143 is indistinguishable between "claude installed no
SIGTERM handler and the kernel killed it" and "claude handled it and exited
143". I did not disambiguate, so **whether a TERM actually performs a clean
app-side disconnect — as opposed to a KILL — is NOT MEASURED and is NOT
PROVABLE from this box** (see §C: the app's session list is not visible here).
What the number does support: a 1.1 s TERM->exit means a 15 s grace is long
enough for the *process* to be gone by TERM, which is the half I can see.

## What I did — C: the app half. MEASURED: the CLI offers NO path.

Commands run, verbatim:

```
$ claude --help                      # 2.1.283 — full Commands: block read
$ claude agents --help | stop | rm | logs --help
$ claude agents --json               # 8 entries, all kind:interactive
$ claude agents --json --all         # 9 entries: 8 interactive + 1 background
$ claude stop zz-probe-2fa1fab0  -> "No job matching 'zz-probe-2fa1fab0'. Run 'claude agents' to list running sessions."
$ claude rm   zz-probe-2fa1fab0  -> "No job matching 'zz-probe-2fa1fab0'."
```

Findings:

* A `--remote-control` (app) session **never appears in `claude agents` at
  all** — not in `--json`, not in `--json --all`. My live throwaway registered
  nowhere (`REGISTERED after 91.5 null`) while running. So the CLI has no list
  of app sessions to sweep, dead-pid or otherwise.
* `claude stop` / `claude rm` address a session by the short **background**
  id and are refused by app-session NAME (output above). They cannot end an app
  session even by name, so there is nothing to sweep and no seam to wire.
* The one real CLI path that exists: `claude agents --json --all` DOES list
  pid-less `kind: "background"` entries (`state: "done"`, e.g. `710907bf`), and
  `claude rm <id>` deletes them. That is a genuine dead-pid cleanup — but for
  BACKGROUND sessions, which are not the app sessions the owner is reporting.

**Therefore the app half of conjunct (3) is a LEAN, not a pass.** The owner's
defect ("directors and master have old sessions still in app", "prime has app
sessions past the 5 most recent") is an APP-side artefact, and this box has no
CLI or local API surface that lists or ends an app session. Nothing was
fabricated and no app data file was touched.

## The near-miss I avoided

I was one step from writing a sweep: `claude agents --json --all` -> any entry
with no `pid` -> `claude rm <id>`. It looks like exactly the asked-for sweep and
it is a real CLI path. I stopped for two reasons, both recorded here so the next
kid does not re-derive them:
1. it only ever yields `kind: "background"` entries, so it would have shipped a
   green test and a lean that looks like a fix while the reported defect stayed;
2. `claude rm` **deletes the session's worktree** ("and its worktree when that is
   safe", plus `--force-remove-worktree` and `--discard-unpushed <commit>`). A
   sweep that runs `claude rm` over every stale-looking entry can destroy
   unpushed work. That is a much worse class of bug than the stale session it
   was meant to remove.

## Falsifier

* `reaper.term_grace_s` deleted from `.agi/config.json` and a reap of a
  SIGTERM-ignoring child still waits ~15 s, not 0 -> the resolver is not
  actually read at runtime (or a cached/hardcoded value got in).
* `claude stop <remote-control-name>` or a new `claude` subcommand addressing
  app sessions by name/session id returning 0 -> the app half stops being a lean
  and a sweep becomes buildable.
* A reaper run on this box leaving a `claude --remote-control` process absent
  from the app session list within the grace window, for a process that was
  TERMed rather than KILLed -> the TERM-clean-disconnect premise is confirmed
  and the lean can be promoted.

## Evidence

* `extensions/agi/tests/test_rotate_term_grace.py` — 11 passed: absent cell ->
  15.0; cell re-read at runtime (3.5 then 41, not cached); 6 malformed cells and
  a broken `config.json` fall back and never raise; the LIVE config declares the
  cell; and an end-to-end `_reap_chain` on a SIGTERM-ignoring grandchild with
  the cell at 0.4 s -> `gone_after: True` in < 3.0 s, which a still-hard-coded
  5.0 could not do.
* `extensions/agi/tests/test_rotate_selfreap.py`,
  `extensions/agi/tests/test_rotate_tail.py`,
  `extensions/agi/tests/test_heal_late_reap_bound.py` — 57 passed (the
  `_reap_chain` neighbourhood plus kid 2's bound test).
* Measurement scripts: `rc_probe.py` in my session dir.

## Agent Notes
reaper.term_grace_s cell (15.0 default, replaces hard-coded 5.0) read at runtime; measured claude TERM->exit 1.1s; MEASURED that claude stop/rm cannot address a --remote-control app session by name and app sessions never appear in claude agents --json --all, so the app half is a lean with no sweep written (claude rm also deletes worktrees). 29 prod lines, 11 new tests + 57 in the _reap_chain neighbourhood.
