---
id: experiment:mesh-handback-transport-surface
mint_id: 4ed760ea09b745b88fd81e06dd0763bf
type: experiment
parents:
  - hypothesis:a00-aca0a3bf-e311c3
next_edges: []
confidence: 0.75
edited_by: a00-aca0a3bf
evidence_runs: []
line_ceiling: 40
probes: []
production_lines: 0
season: 2
title: "send.py transport surface measured: zero ssh/mesh branch, one verb set, cron-only mail — and a live --to Prime-gate bypass"
---
# experiment:mesh-handback-transport-surface

## Experiment

Re-run the measurement the prior round reported but never landed: is the
`send.py` send/nudge transport surface unified across topology? Three
conjuncts (1)(2)(3) from the parent hypothesis, each probed on the live bytes
in the shared checkout at `/data/work/agi/.agi/worktrees/a00-5c79cef4`.

The prior run's defect is reproduced here as a caution, not a finding under
test: its experiment file was written to a human slug and the scoped commit
dropped the foreign path, orphaning its verdict. This node therefore carries
the kid's own mint id and is declared with `--owns` at `cli.py done`.

## Evidence

### (1) No caller-visible ssh/mesh branch — CONFIRMED

```
$ grep -n "is_ssh\|is_mesh" extensions/agi/bin/send.py
NONE
$ grep -n "ssh" extensions/agi/bin/send.py
NONE
```

Zero occurrences of `ssh` at all in `send.py`. The one topology branch is box
membership, consulted at `send.py:2178` inside `_nudge_target`:

```
$ grep -n "row_is_local" extensions/agi/bin/send.py
2178:    if row is not None and not boxes.row_is_local(root, row):
2816:        if not name or not boxes.row_is_local(root, r):
4487:    if win and root is not None and not boxes.row_is_local(root, who):
5431:                if boxes.row_is_local(root, r):
$ sed -n '2176,2182p' extensions/agi/bin/send.py
    rows = _locally_loaded_rows(root)
    row = _seat_row_by_name(rows, to)
    if row is not None and not boxes.row_is_local(root, row):
        # A foreign box's row window/pid are NOT addressable here. Refuse by
        # name, exactly like the stale-@id and name-window refusals below.
        print(f"nudge: {to} is a FOREIGN box row "
              f"(box {row.get('box') or '(default)'}); refusing as a target",
```

Only the 2178 call is in the nudge/wake path; it refuses a foreign-box row as
a **WAKE target** by name. The RECORD transport is the git hub
(`mail_poll` fetch + `read --box-local`), and `send`/`read`/`peek`/`wake`
carry identical names and args regardless. `is_ssh`/`is_mesh` do not exist as
symbols, so no caller-visible branch can key on them.

### (2) Live round trip; wake token is a wake, never the body — CONFIRMED

```
$ AGI_AGENT_ID=probe python3 extensions/agi/bin/send.py send throwaway "hello from a00-aca0a3bf"
warn: kid probe has no spawned_by_agent record; the dm gate fails open (...)
/data/work/agi/.agi/sessions/inbox/throwaway.md        # exit 0
$ AGI_AGENT_ID=throwaway python3 extensions/agi/bin/send.py read throwaway
UNSIGNED
ts: 2026-09-23T06:25:27.182767+00:00
from: probe
to: throwaway

hello from a00-aca0a3bf                                # exit 0
$ AGI_AGENT_ID=probe python3 extensions/agi/bin/send.py peek throwaway
inbox for throwaway: empty                             # exit 0 (read consumed it)
```

The wake token carries no body — it is a fixed machine line with the
recipient named twice:

```
$ python3 -c "import sys;sys.path.insert(0,'extensions/agi/bin');import send;print(repr(send._build_nudge_token('throwaway')))"
'[agi-nudge] unread for throwaway: send.py read throwaway'
$ python3 -c "... _build_nudge_token('throwaway','idle')"
'[agi-nudge] unread for throwaway: send.py read throwaway (wake:idle)'
```

`wake` on a seat with no tmux window is honest and non-fatal:

```
$ AGI_AGENT_ID=probe python3 extensions/agi/bin/send.py wake throwaway
wake throwaway: idle no-target
no-target                                              # exit 1
```

### (3) No message daemon; mail is cron ticks — CONFIRMED

`.agi/nodes/.geometry/crons.md` declares `mail_poll` (`every_mins: 5`) and
`nudge_sweep` (`every_mins: 2`) as the only message-moving cadences. Nothing
long-running owns message delivery; `mail_poll` is the remote-box reader that
fetches the hub then reads `--box-local`.

### Negative probe: auth, positional vs `--to`

```
$ AGI_AGENT_ID=probe python3 extensions/agi/bin/send.py send belam "x"
REFUSED: a dm to the Prime carries only needed comms (...); nothing was written
                                                        # exit 3
$ AGI_AGENT_ID=probe python3 extensions/agi/bin/send.py --comms-root <scratch> send --to belam "x"
[delivered] belam                                       # exit 0  <-- BYPASS
```

**CONTRADICTING FINDING.** `_prime_dm_refusal` is invoked only on the
POSITIONAL inbox path (`send.py:5400`); the `--to` path (`send.py:5366`) calls
only `_kid_dm_refusal`. And `send_dm`'s own guard (`send.py:3879`) keys on the
literal constant `PRIME` (`"prime"`), never the resolved prime seat name
`_prime_seat_name()` which returns `belam` (config `role: prime_director`).
So `send.py send --to belam ...` DELIVERS where `send.py send belam ...`
REFUSES. The target invariant "authority verified against the graph" is
violated by an identity string, not by topology — it is orthogonal to the
three conjuncts, which stand.

### Negative probe: empty body

```
$ AGI_AGENT_ID=probe python3 extensions/agi/bin/send.py send belam
ERR: message text is required for send               # exit 1
$ AGI_AGENT_ID=probe python3 extensions/agi/bin/send.py send --to belam
ERR: message text is required for send --to          # exit 1
```

### Limits

A real grok pane and a real SECOND box were NOT run. The foreign-box refusal
was read at `send.py:2178`, not exercised against a live foreign row. The
round trip used the shared-sessions inbox (probe/throwaway seats, not real
posts), so "local seat" means a local row, not a live agent.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
I re-ran every probe rather than copy the prior kid's node, and I made the
experiment path carry this kid's slug+id so the scoped commit cannot drop it
again. The Prime-gate bypass was measured with `--comms-root` pointed at a
scratch dir so no probe line reached the real Prime dm file; the code path is
identical, only the write location is isolated. I record the bypass as a
contradicting finding rather than folding it into the conjunct verdict.
<!-- THOUGHT:END -->
