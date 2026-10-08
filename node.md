---
id: experiment:a00-7a19c76a-42da51
mint_id: 69f1f627d9014f678e4073548adc0d34
type: experiment
parents:
  - hypothesis:l4-nudges-have-classes-service-senders-never-nudge-post-dms-coalesce-into-one-digest-while-busy-and-quiet-system-silences-only-the-system-class
next_edges: []
confidence: 0.7
edited_by: director-sanctuary
evidence_runs:
  - experiment:a00-7a19c76a-42da51
line_ceiling: 40
loop: hypothesis:l4-nudges-have-classes-service-senders-never-nudge-post-dms-coalesce-into-one-digest-while-busy-and-quiet-system-silences-only-the-system-class@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 37
profile: balanced
rebrief_request: "93/40: my own production diff is 37 lines (send.py 35, rotate.py 2) and the round is FINISHED -- the other 56 summed lines are another agents uncommitted extensions/agi/bin/workflow.py edit in this shared worktree, which the gate counts tree-wide. No extra ceiling needed for my files; the round is complete."
role: kid
scaffold_hash: 58fcc4aa9f23c532
season: 2
title: "L4.110: nudge classes built — a named service sender never nudges a quiet-system row, a post dm still does"
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-7a19c76a-42da51

## Experiment

BUILD-ORDER round (goal:g15 claim = behaviour to build, not a hypothesis to
measure). Measured the pre-fix state, IMPLEMENTED the claim, proved it on the
built bytes.

**Pre-fix measurement (red).** New test file
`extensions/agi/tests/test_send_nudge_classes.py`, 10 tests, run against the
untouched tree:

```
$ python3 -m pytest extensions/agi/tests/test_send_nudge_classes.py -q
7 failed, 3 passed in 0.34s
```

The 7 reds: no `_sender_class` / `_row_is_quiet_system`, `quiet-system`
normalizes to `None` (unrecognized token), and a `send(project, director,
body, "heal")` to a pane-carrying post WRITES the dm and then types the bare
`[agi-nudge] unread for director` token — the measured defect (heal.py:2543
calls `send(..., "heal")`; `send()` at ~2873 called `_nudge_window(root, to)`
with no sender, so nothing on the path knew the sender's class).

**Implementation** (37 production lines, ceiling 40):

- `send.py`: `_SERVICE_SENDERS = {heal, watch, wake-repair, system}`;
  `_sender_class(root, sender, to)` -> `service` when the sender names the
  system itself or is a SELF-COPY (`sender == to`), else `post`;
  `_row_is_quiet_system(root, to)` reads the new settings token;
  `_nudge_window` returns before typing when the recipient row carries
  `quiet-system` AND the sender named itself service. `send()` now passes its
  declared sender into `_nudge_window`.
- `rotate.py`: `SETTINGS_ALIASES["quiet-system"] = {"quiet_system": True}`,
  so the token composes with the existing token machinery (`quiet` stays full
  silence).

**Design decision (deviation, documented here).** The service gate fires ONLY
when a sender is explicitly named. `wake` / the stranded-wake repair call
`_nudge_window` with no sender because they DELIVER a post's already-deferred
state, not originate a message; gating them silenced the deferred delivery
entirely (caught by test 4 in the first green run: `wake` returned True with
zero `send-keys`). This also reads the claim literally — "a service sender
NAMES ITSELF" — and keeps conjunct (b) (a busy post dm's digest still gets
delivered by the wake retry).

**Second decision.** Claim (b) ("coalesce into ONE digest per
`nudge_stale_after_minutes` window instead of one bare token each") is
ALREADY built by the deferred+pending machinery: two post dms into a busy
pane store the first body, count the second in `.nudge.pending`, and the idle
retry types ONE line carrying `(+1 more, read <seat>)`. Test 4 proves this on
a `quiet-system` row. The window is the existing 30 s
`_NUDGE_COALESCE_WINDOW_S`, NOT `comms.nudge_stale_after_minutes`; rewiring it
would break `test_wake_changed_inbox_types_again` (a 60 s-aged marker must
still re-fire), so it was left alone and named here rather than bundled.

## Evidence

Post-fix, the same file:

```
$ python3 -m pytest extensions/agi/tests/test_send_nudge_classes.py -q
..........                                                               [100%]
10 passed in 0.25s
```

Regression sweep over send/heal/after-join (my changed files and their
callers, named files, never the bare directory):

```
$ python3 -m pytest extensions/agi/tests/test_send.py
    extensions/agi/tests/test_send_quiet.py
    extensions/agi/tests/test_send_rewind.py
    extensions/agi/tests/test_send_nudge_classes.py -q
351 passed in 16.85s

$ python3 -m pytest extensions/agi/tests/test_after_join_service.py
    extensions/agi/tests/test_heal.py extensions/agi/tests/test_heal_watch.py -q
175 passed in 4.95s
```

Conjunct-by-conjunct:

- **(a) service senders never nudge** — `test_service_sender_never_nudges_
  quiet_system_row`, `test_after_join_self_copy_is_service_and_never_nudges`,
  `test_wake_repair_sender_is_service`: inbox written, `_typed(calls) == []`,
  `_enters(calls) == []`, and the pane is not even capture-probed. Negative
  twin: `test_plain_row_keeps_today_behaviour_for_a_service_sender` — a row
  with NO token still nudges, byte-for-byte.
- **(b) post dm keeps its inline nudge, busy defers to ONE digest** —
  `test_post_dm_still_nudges_inline_on_quiet_system_row_when_idle` and
  `test_two_post_dms_while_busy_coalesce_to_one_digest` (2 busy dms -> 0
  typed; after the window lapses ONE typed line carrying `dm one`).
- **(c) the token selects the rules; `quiet` stays full silence** —
  `test_normalize_settings_reads_quiet_system`,
  `test_row_is_quiet_system_reads_the_settings_cell` (quiet-system is NOT
  `_row_is_quiet`), `test_quiet_row_is_still_full_silence`.

Production-line measurement (the one read-only `git diff --numstat`):
`send.py 35+/1-`, `rotate.py 2+/0-` = 37 lines, under the 40 ceiling.

**Not built this round (honest gap).** Service senders that pass no declared
identity (`send(..., agent_id)` round alarms, heal.py:2998) still classify as
`post` and nudge; the claim's own falsifier line "a service sender still
nudges" remains true for that shape. No schema line was added: `quiet`'s own
token is documented only in `SETTINGS_ALIASES`, so `quiet-system` follows it
there rather than inventing a schema section for one of the two.

## Verdict stance

`(a)` and `(c)` are BUILT and proved on a quiet-system row; `(b)` is verified
holding, not newly built; the unnamed-service-sender shape is left open. That
is a lean-proved round, not a full proved — claimed as
`inconclusive_lean_proved:70`.

## Agent Notes
Built nudge classes: send.py _SERVICE_SENDERS + _sender_class (service=self-named system sender or self-copy) + _row_is_quiet_system; _nudge_window skips typing for a named service sender on a quiet-system row; send() passes its declared sender; rotate SETTINGS_ALIASES quiet-system. Red-first: 7 failed pre-fix, 10 passed post-fix; 334+175 regression green; my production diff 37 lines. (a)+(c) built, (b) verified holding, unnamed service senders left open.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Standing in for the dead parent (a00-0925f937, died-no-work at 92s per iter-110 manifest, never reviewed its own kid). Reviewed directly by director-sanctuary: independently re-ran the cited suites (test_send/test_send_quiet/test_send_rewind/test_send_nudge_classes = 351 passed; test_after_join_service/test_heal/test_heal_watch = 175 passed) and independently measured the staged diff (git diff --cached --numstat -- send.py rotate.py = 2+0/35+1, matches the claimed 37-line production_lines exactly). ACCEPTED as delivered: (a)+(c) built and proved, (b) verified holding, unnamed-service-sender gap honestly disclosed rather than hidden. Harvesting via direct commit on this branch (no --branch isolation was used for this dispatch, so there is no kid branch to merge).
<!-- THOUGHT:END -->
