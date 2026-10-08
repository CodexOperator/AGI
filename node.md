---
id: experiment:a00-1eb71fd9-ce56f9
mint_id: 7cf5debf4eb342b59b36c30a2303ca68
type: experiment
parents:
  - hypothesis:pb3-agi-post-stream-registered-and-current
next_edges: []
confidence: 0.9
edited_by: a00-06814999
evidence_runs:
  - experiment:a00-1eb71fd9-ce56f9
loop: hypothesis:pb3-agi-post-stream-registered-and-current@s2
model: stealth/space-bunny-alpha
production_lines: 6
profile: balanced
role: kid
scaffold_hash: f43355200372da09
season: 2
title: agi-post SKILL.md cites engine code by function name
town: core
verdict: proved
---
# experiment:a00-1eb71fd9-ce56f9

## Experiment

Conjunct (2) of `hypothesis:pb3-agi-post-stream-registered-and-current`: make
`skills/agi-post/SKILL.md` cite engine code by NAME, never by line number.
PROSE ONLY, 6 production lines changed (`git diff --numstat` = 6 6).

### Method — name resolved by AST over the live file, not by the briefed number

| skill cite (was) | live enclosing def (`ast`, depth 0) | now cited as |
|---|---|---|
| heal.py:3470-3527, 3597-3602 | `heal._recover_seat` (3428-3627) | `heal.py _recover_seat` |
| heal.py:3541-3556 | `heal._recover_seat` (NOT `_watch_one_seat` as briefed) | `heal.py _recover_seat` (same function) |
| heal.py:3463-3465 | `heal._recover_seat` | `heal.py _recover_seat` |
| heal.py:2862-2887 | `heal._pin_table` (2846-2892) | `heal.py _pin_table` |
| rotate.py:1935-2459 | `rotate._cmd_spawn` (2376-2815) / `spawn_window` (2042-2216) | `rotate.py spawn_window` |
| rotate.py:4915-5017 | `rotate.cmd_merge_up` / `_load_templates` — the SEATS-LAUNCH body is `cmd_seats_launch` (5272) | `rotate.py cmd_seats_launch` |
| send.py:4733-5251 | `send.whois` (5188-5266) | `send.py whois` |
| line 12 `rotate.py spawn` | `rotate.cmd_spawn` (2307) | `rotate.py cmd_spawn` |

Two briefed numbers were STALE and would have propagated a lie: the seats-launch
cite (4915-5017) lands in `cmd_merge_up`/`_load_templates`, nowhere near
`cmd_seats_launch`; the 3541-3556 cite lands inside `_recover_seat`, not
`_watch_one_seat`. I read the regions live and named the function that OWNS the
claim. No caveat was deleted to make a grep pass — the meaning of every bullet
is unchanged, only its anchor.

## Falsifiers run

```
$ grep -nE '(heal|rotate|send)\.py:[0-9]' skills/agi-post/SKILL.md
(no output, exit 1)                                   PASS

$ <ast name check over the three real files>
heal _watch_seats True   heal _recover_seat True  True   heal _pin_table True
rotate cmd_spawn True    rotate spawn_window True       rotate cmd_seats_launch True
send whois True                                    PASS for every CODE cite

$ python3 -m pytest extensions/agi/tests/test_rotate_templates.py -q --basetemp /tmp/pb3ps2
36 passed, 1 xfailed, 1 warning in 50.05s            PASS
```

### Known non-pass, stated rather than hidden

The same ast probe prints four False hits: `rotate stand` (x2, from
`rotate.py stand-up --post <p>`), `rotate spawn` (from `rotate.py spawn --seat`)
and `rotate migrate` (from `rotate.py migrate --post`). These are **argparse
subcommand spellings inside runnable shell commands**, not function cites — the
handlers are `cmd_stand_up` (2319), `cmd_spawn` (2307) and `cmd_migrate`. I did
NOT rewrite a command into a name that does not run: that would make the skill
wrong to make a probe green. The probe as briefed cannot distinguish a verb from
a cite; the file is correct and the probe is over-broad. Siblings hitting the
same shape on agi-stream should expect it.

## Scope held

Only `skills/agi-post/SKILL.md` was touched. `config:rotations`, `skills/agi-stream/`,
`.agi/config.json`, locations.py untouched. Conjunct (1) stays RED and is not mine.

## Agent Notes
agi-post SKILL.md now cites heal/rotate/send by function name (AST-resolved, two briefed line numbers were stale); grep 0 hits, every code name resolves True, 6 production lines, pytest 36 passed

REVIEW a00-06814999 (parent): ACCEPTED, verdict proved stands. PROBES RUN BY ME, not the kid: (gate) `grep -nE (heal|rotate|send).py skills/agi-post/SKILL.md` — the file now carries only NAME-form cites (lines 12, 23, 25, 37, 41, 43), and `grep -nE (heal|rotate|send).py:[0-9]` prints nothing; the line-cite surface is gone. (wire) I re-ran the ast name probe over the LIVE extensions/agi/bin/{heal,rotate,send}.py: _watch_seats True, _recover_seat True (x2), _pin_table True, cmd_spawn True, spawn_window True, cmd_seats_launch True, whois True — every CODE cite resolves to a real top-level def. (auth) the four False hits are argparse VERBS inside runnable shell commands (`rotate.py stand-up`, `rotate.py spawn`, `rotate.py migrate`), the kid disclosed them unprompted; I checked rotate.py:5272 and the docstring there is exactly the claim the skill makes (starts EVERY non-fire-and-forget row, writes no row/key/commit), so cmd_seats_launch owns the claim the old number 4915-5017 did not. The kid also corrected two STALE briefed numbers rather than transcribing them — that is the opposite of the near miss. No demotion.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW, rewriting. (1) WHAT THE BRIEF SAID, quoted: "skills/agi-post/SKILL.md cites code by NAME (heal.py _watch_seats / _watch_one_seat / _live_seat_row, rotate.py _cmd_spawn / cmd_seats_launch, send.py whois), no (heal|rotate|send).py:<n> line cite remains, and every underscored name it cites is a top-level def or constant in that file." (2) WHAT THE MACHINE DOES: I re-ran both falsifiers on the live bytes, not on the report — grep for the line-cite pattern returns nothing, and an ast walk of the three real bin files resolves every name-form cite to a top-level def (_watch_seats, _recover_seat x2, _pin_table, cmd_spawn, spawn_window, cmd_seats_launch, whois). Two of the numbers I BRIEFED were stale: 4915-5017 lands in cmd_merge_up/_load_templates, and 3541-3556 lands inside _recover_seat, not the _watch_one_seat my brief named. (3) NEAR MISS: a kid that greps the region and transcribes the enclosing def mechanically would have written cmd_merge_up — a real def, satisfying the words, and citing the wrong function; the ast-ownership check is what separates the two, and it is why the node says _recover_seat where the brief said _watch_one_seat. The second near miss is the tempting inverse: rewriting `rotate.py spawn` into `cmd_spawn` to make the probe print True, which would have made a runnable command unrunnable. (4) NO DEVIATION: I judged the four False probe hits against the claim text, which asks that every underscored NAME resolve — argparse verbs are not citations, and the kid disclosed them rather than hiding them. The claim conjunct is met; proved, evidence this node.
<!-- THOUGHT:END -->
