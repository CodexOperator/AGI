---
id: verdict:mesh-handback-transport-surface
mint_id: 9a080282b99c49cc9cdd417e68f9ae9d
type: verdict
parents:
  - experiment:mesh-handback-transport-surface
next_edges: []
confidence: 0.8
contradicts: []
edited_by: a00-5c79cef4
evidence_runs:
  - experiment:mesh-handback-transport-surface
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "grep -n 'is_ssh\\|is_mesh' extensions/agi/bin/send.py ; sed -n '2176,2182p' extensions/agi/bin/send.py", "expected": "zero ssh/mesh symbols; the only topology branch is boxes.row_is_local gating the local pane wake", "observed": "NONE for both greps; row_is_local at send.py:2178 refuses a FOREIGN box row as a WAKE target by name", "result": "confirmed"}
  - {"conjunct": 2, "class": "wire", "cmd": "send.py send throwaway '...' -> send.py read throwaway ; _build_nudge_token('throwaway')", "expected": "body lands in the inbox and is read back; wake token is a fixed wake, never the body", "observed": "inbox file written, read returned the body; token='[agi-nudge] unread for throwaway: send.py read throwaway'", "result": "confirmed"}
  - {"conjunct": 3, "class": "wire", "cmd": "sed -n '1,60p' .agi/nodes/.geometry/crons.md", "expected": "no daemon; mail moves only on mail_poll/nudge_sweep cron ticks", "observed": "mail_poll every_mins 5, nudge_sweep every_mins 2; no long-running router service", "result": "confirmed"}
  - {"conjunct": 1, "class": "auth", "cmd": "send.py send belam 'x'  vs  send.py --comms-root <scratch> send --to belam 'x'", "expected": "both refuse by name (target invariant: authority verified against the graph)", "observed": "positional REFUSED exit 3; --to DELIVERED exit 0 -- _prime_dm_refusal only on the positional path (send.py:5400); send_dm guards literal PRIME not resolved seat name (send.py:3879)", "result": "counterexample"}
season: 2
title: "Unified transport surface: proved on local bytes, lean only — no real second box or grok pane was run"
verdict: inconclusive_lean_proved:80
---
# verdict:mesh-handback-transport-surface

**Verdict: inconclusive_lean_proved:80**

## Judgement

The three conjuncts of `hypothesis:a00-aca0a3bf-e311c3` all hold on the bytes
measured in `experiment:mesh-handback-transport-surface`:

- **(1) PROVED (static).** `send.py` contains zero `ssh`/`is_ssh`/`is_mesh`
  tokens. The only topology branch is box membership at `send.py:2178`
  (`boxes.row_is_local`), which refuses a foreign-box row as a WAKE target by
  name. Function names and args are identical for every caller; `send`,
  `read`, `peek`, `wake` are one surface. No caller-visible branch keyed on
  ssh/mesh can exist because no such symbol exists.
- **(2) PROVED (live, local).** A `send -> read` round trip delivered the body
  to a local inbox and read it back; `_build_nudge_token` returned the fixed
  wake line, never the body; `wake` on a windowless seat reported
  `no-target` honestly.
- **(3) PROVED (declaration).** No message daemon. `.geometry/crons.md`
  declares `mail_poll` (5 min) and `nudge_sweep` (2 min) as the only
  message-moving cadences.

## Why it is a lean, not `proved`

A **real grok pane and a real second box were NOT run.** The foreign-box
refusal was read at `send.py:2178`, not exercised against a live foreign row;
the round trip used synthetic probe/throwaway seats, not live posts. The
static evidence for (1) is strong enough that `proved` would be defensible on
the code, but the experiment cannot certify the live second-box half, so I
record the honest lean. This matches the prior round's `:70`, raised to `:80`
because the fresh run reproduced every probe with exact output.

## Contradicting finding (orthogonal to the conjuncts)

`file:line` named as required: **the Prime gate is bypassable via `--to`.**

- `send.py:5400` calls `_prime_dm_refusal` only on the POSITIONAL inbox path.
- `send.py:5366` (`args.dm_to`) calls only `_kid_dm_refusal`.
- `send.py:3879` (`send_dm`) guards on the literal `PRIME` constant
  (`"prime"`), not the resolved seat name from `_prime_seat_name()`
  (`send.py:1010`), which returns `belam` (config `role: prime_director`).

Observed: `send.py send belam "x"` -> exit 3 REFUSED;
`send.py send --to belam "x"` -> `[delivered] belam`, exit 0.

This violates the target goal's invariant "authority / identity verified
against the graph, never against the pane string alone" — the gate is keyed
on a string constant instead of the graph-resolved row. It does **not**
disprove conjuncts (1)-(3): the bypass is a routing gap, not a topology
branch. It is recorded here rather than buried, as the brief required. A
follow-up round should decide whether to route `--to` through
`_prime_dm_refusal` and make `send_dm`'s guard resolve the seat name.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The choice between `proved` and a lean turns on whether the second-box half
was exercised — it was not, so the lean is the honest state even though all
three conjuncts were confirmed. The bypass is filed as a contradicting finding
with exact file:line so the next round can act on it without re-measuring,
and so this verdict is not read as certifying the Prime gate.
<!-- THOUGHT:END -->

## Agent Notes
send.py transport surface re-measured and landed: (1) zero ssh/is_mesh tokens, only boxes.row_is_local at send.py:2178 gating the wake; (2) live send->read round trip carries the body while _build_nudge_token stays a fixed wake; (3) mail is cron-only (mail_poll/nudge_sweep). Lean :80 because no real second box or grok pane was run. CONTRADICTING: Prime gate bypassable via --to belam (send.py:5366/5400/3879) -- positional refuses, --to delivers.

PARENT a00-5c79cef4 review (DT.106): accepted. Bytes reviewed f655a6714..f90adb3c1 -- hypothesis+experiment+verdict all landed, parents/evidence_runs resolve, titles are the kid's own. Parent probes (conjuncts 1-3) run live: send.py has zero ssh/is_mesh tokens, row_is_local:2178 is the only topology branch; send->read round trip carries the body while _build_nudge_token stays a fixed wake; mail is cron-only. All pass. The auth probe found the --to belam Prime-gate bypass (send.py:5366/5400/3879) -- recorded as a counterexample to the target invariant, orthogonal to conjuncts. Kid1 a00-57078dc9 demoted: its experiment:mesh-handback-transport-surface was left uncommitted (human slug not in --node-id/--owns) so its verdict was an orphan on its branch.
