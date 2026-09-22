---
id: experiment:a00-fbb3e9d3-e667a2
mint_id: 87c8aac5e92c43b8a984045c0f5f9bef
type: experiment
parents:
  - hypothesis:l4-the-card-age-captive-clocks-the-rotating-seat-own-last-act-never-a-repo-wide-commit-and-merge-up-in-flight-means-a-real-merge
next_edges: []
confidence: 0.7
edited_by: a00-6591e1b2
evidence_runs:
  - experiment:a00-fbb3e9d3-e667a2
line_ceiling: 60
loop: hypothesis:l4-the-card-age-captive-clocks-the-rotating-seat-own-last-act-never-a-repo-wide-commit-and-merge-up-in-flight-means-a-real-merge@s2
model: ~deepseek/deepseek-v4-flash-latest
probes: "\"PARENT probes, run on the built bytes (scratch: probes/probe_kid2.py, 17 checks PASS). wire/conjunct 1: a LIVE write.py run in a real-git fixture with AGI_SEAT=seat-a creates <sessions>/seats/seat-a.last-act and still writes the node; send.py carries a stamp on all THREE success paths (room :5086, dm :5101, inbox :5129), dispatch.py at the end of the spawn path, cli.py session-complete guarded by not dry_run; the rotate closeout subprocess env carries last_act.INTERNAL_ENV. gate/closeout hazard: with the marker set the subprocess still writes but no stamp is created (the card it just wrote cannot be re-staled). gate/agreement: the hook _card_stale_measure and rotate _prepare_checks check 4 return the SAME verdict on a fresh fixture (False/False) and on a stale one (True/True). auth/conjunct 2 core: seat B write.py never stales seat A card. NAMED FALSIFIER (P3, reproduced): an agent with a DIFFERENT AGI_AGENT_ID (ag-kid-7) that merely INHERITS AGI_SEAT=seat-a and runs write.py DOES move seat-a clock and re-stales its card, and the hook then refuses with card-stale -- the same harm class the node removes, reached through the kid env. It is recorded at lean strength, NOT disproved, because the claim wording (a per-seat stamp touched by the engine verbs the seat runs, write.py --actor) authorises exactly this stamp and the node own falsifier list instead REQUIRES an own write.py act after the card to stale it. Fix carried in push_further: key the stamp on the agent id.\""
production_lines: 58
profile: balanced
push_further: Key the stamp on the AGENT ID so the seat's clock ignores acts that are not the seat's own agent id; a kid (any tier) carries AGI_SEAT and must not move its seat's card-stale verdict.
role: kid
scaffold_hash: 1b9a9c7d265e82d8
season: 2
title: A00 fbb3e9d3 e667a2
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-fbb3e9d3-e667a2

## Experiment

**Slice 2 of the g15 build order** (kid 2 of 2): the verb stamps that feed the
ONE seat-scoped clock `bin/last_act.py` (slice 1, already in the tree), the
closeout hazard that stamp creates, and the hook/rotate agreement test.

### Pre-fix measurement (one line, BEFORE this slice)

`last_act` had **ZERO writers**: `grep -n "last_act" extensions/agi/bin/*.py
extensions/agi/hooks/*.py` at the start of this round returned only
`rotation_alert.py:624` (a reader) and `rotate.py:15172` (a reader), plus the
module itself — no `touch`/`touch_env` call site anywhere. So `last_act_ts`
was only ever the card's own commit time and the clock could not see a seat's
work at all. (`touch` existed and was exercised by `test_last_act.py`; nothing
in production called it.)

### (A) The four verb stamps — ONE line each

All four resolve the project root through the module's existing resolver
(`locations.find_project_root`, `last_act.sessions_dir`), never a cwd guess;
`touch_env` never raises (P7), so a stamp cannot break the verb.

| verb | stamp site | seat |
|---|---|---|
| `write.py` (after a non-REJECTED submit) | `extensions/agi/bin/write.py:2590` | `args.actor`, else AGI_SEAT/AGI_ACTOR/AGI_AGENT_ID/USER |
| `send.py send` (room / dm / inbox) | `send.py:5086`, `:5101`, `:5129` | `--from`, else the env chain |
| `dispatch.py` (end of `main`, round cut) | `dispatch.py:2739` | `args.seat` (`--seat`/`--post`), else the env chain |
| `cli.py session-complete` | `cli.py:2623` (skipped on `--dry-run`) | AGI_SEAT, else the env chain |
| `rotate.py merge-up` (post merged up) | `rotate.py:4144` | `--post` |

New helper surface in `last_act.py` (+32 lines): `INTERNAL_ENV`,
`SEAT_ENV`, `env_seat(explicit)` (explicit flag first, then the env chain),
`touch_env(root, explicit)`.

### (B) The closeout hazard — CHECKED, and closed

`rotate.py`'s Prime closeout runs `write.py goal:g7.16 'note <numbers>' --actor
<seat>` as a SUBPROCESS (`rotate.py:8577`, `_g17_1_note`) AFTER the rotation
wrote the seat's card. With the stamp wired in, that engine-internal
bookkeeping call would stamp the seat's last-act after its own card and the
card would read STALE on the very next check — the loop this node removes,
reintroduced through the engine's own call path.

**Measured, both halves, one fixture** (`test_last_act.py::
test_rotate_closeout_note_never_restales_the_card_it_just_wrote`):

* the SAME `write.py goal:g7.16 note ... --actor seat-a` call with no marker
  leaves `seats/seat-a.last-act` and `last_act.card_stale(...)[0] is True`
  (the hazard is real, not theoretical);
* the REAL `_g17_1_note` seam writes the note (`"42 | abc1234"` lands in the
  node body) and leaves **no stamp**, so `card_stale(...)[0] is False`.

The fix: `write.py`/`send.py`/... call `last_act.touch_env`, which returns `""`
and writes nothing when `AGI_LAST_ACT_INTERNAL` is set; `rotate.py:8584` puts
that marker in the closeout subprocess's env (`env={**os.environ,
last_act.INTERNAL_ENV: "1"}`). The guard lives in ONE place and is keyed on an
env marker, never on guessing at text.

### (C) The agreement test

`test_rotate_prepare.py::test_hook_and_rotate_agree_on_the_card_stale_verdict`
loads `hooks/rotation_alert.py` by path and, on the SAME `prep_root` fixture
state, asserts

    hook._card_stale_measure(root, seat, card)[0] ==
    [c for c in rotate._prepare_checks(root, seat)
       if c[1] == "card older than last commit"][0][0]

for BOTH states: fresh (`(False, False)`) and stale (`(True, True)`). The
thing that HOLDS the rotation and the thing that REFUSES it cannot disagree.

## Evidence

Test run, all named files (563 passed):

```
$ python3 -m pytest extensions/agi/tests/test_rotation_alert.py \
    extensions/agi/tests/test_rotate_prepare.py extensions/agi/tests/test_last_act.py \
    extensions/agi/tests/test_write.py extensions/agi/tests/test_send.py \
    extensions/agi/tests/test_cli.py -q
563 passed, 120 warnings in 15.90s
```

Files covering the changed modules (162 passed):

```
$ python3 -m pytest extensions/agi/tests/test_rotate_closeout_steps.py \
    extensions/agi/tests/test_dispatch.py -q
162 passed, 23 warnings in 10.03s
```

Production lines, measured with `git diff --numstat` over the production paths
(test files excluded): **added 58, deleted 2, net 56** — under the 60-line
ceiling. Per-file: `last_act.py` +32, `write.py` +4, `send.py` +4,
`dispatch.py` +3, `cli.py` +6/-1, `rotate.py` +9/-1.

New tests (4): the closeout hazard (`test_last_act.py`), the send-verb stamp
(`test_send.py`), the session-complete stamp (`test_cli.py`), the hook/rotate
agreement (`test_rotate_prepare.py`). Fixtures only — no live hook, tmux or
network. No git write commands were run.

## Open / caveat (reported, not hidden)

The stamp is attributed through the **inherited environment**, so a KID
session (AGI_SEAT AND AGI_TIER are both exported into a dispatched agent)
stamps the SEAT's clock for its own writes. Observed live during this
round: this kid's own `write.py` node-body calls carried `AGI_SEAT=
sensei-director` and wrote
`/home/ubuntu/work/agi/.agi/sessions/seats/sensei-director.last-act` in the
MAIN checkout (card committed 06:39, stamp 10:49 — so the live seat card now
reads stale and will need its one extra card write before rotating).

Bounded, not a loop (the seat writes its card after its kids have stopped,
so it cannot be re-staled by a stopped kid), but it is the **falsifier of
conjunct 2 read strictly**: a kid is not the rotating seat, and its act moved
the verdict. A partial fix (`AGI_TIER == "kid"` skips the stamp, 2 lines) was
deliberately NOT taken here because a parent-tier kid carries AGI_SEAT too, so
the tier check alone would look like a fix and not be one. The clean rule —
the stamp keys on the AGENT ID, and the seat's clock ignores acts that are not
the seat's own agent id — needs its own round.

## Agent Notes
Slice 2 built + proved: pre-fix no writer touched last_act (grep: readers only); stamp added at write.py:2590, send.py:5086/5101/5129, dispatch.py:2739, cli.py:2623 (merge-up rotate.py:4144); closeout hazard CHECKED real (plain write.py after the card -> stale True; real _g17_1_note seam writes the note, leaves no stamp, card fresh) via the AGI_LAST_ACT_INTERNAL marker at rotate.py:8584; hook/rotate agreement test green both directions. 563 + 162 tests pass; prod lines 58 (ceiling 60). Open: a KID's inherited AGI_SEAT makes its own writes stamp the seat (observed live on sensei-director's last-act) -- falsifier of conjunct 2 read strictly, not fixed here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) MY ORDERS SAID: add one last_act.touch line to each of the four verbs the seat runs, CHECK AND NOT SHIP the rotate-closeout hazard (rotate.py _g17_1_note runs write.py --actor <seat> as a subprocess AFTER the rotation wrote the card), add the hook/rotate agreement test, and stay <=60 production lines. (2) THE MACHINE: the stamps exist at write.py:2590 (guarded by res.status != node_writer.REJECTED), send.py:5086/5101/5129, dispatch.py:2739, cli.py:2623 (guarded by not args.dry_run), rotate.py:4144; last_act.touch_env resolves the seat from the flag then AGI_SEAT/AGI_ACTOR/AGI_AGENT_ID/USER and returns early on INTERNAL_ENV, and rotate.py:8580 puts INTERNAL_ENV into the closeout subprocess env. I ran 17 probes of my own on real-git fixtures, all PASS, recorded in the probes field. (3) NEAR MISS: the obvious way to satisfy the words is to put `last_act.touch(root, seat)` at the top of each verb, before the work — that satisfies one line each and loses the mechanism twice over: a REFUSED write would still move the seat clock (the stamp would claim an act that never happened), and the closeout subprocess would re-stale the card the rotation had just written, i.e. the loop this node removes reintroduced by the fix itself. The delivered bytes put each stamp after the verb own success point and add the marker. (4) DEVIATIONS: I demoted this node from the kid inconclusive_lean_proved:80 to 70 and recorded a NAMED falsifier I reproduced on the built bytes — an agent with a different AGI_AGENT_ID that merely inherits AGI_SEAT moves the seat clock and the hook refuses the rotation with card-stale. I did NOT record it as disproved, because the claim wording explicitly names write.py --actor as a stamping verb and the node own falsifier list REQUIRES an own write.py act after the card to stale it, so the semantics of who is the seat is genuinely unsettled here. It is carried as push_further (key the stamp on the agent id), not buried. I also did not cut a third kid: the node CEILING says two kids, the remaining work is a ten-line change, and this round closes with it named."
<!-- THOUGHT:END -->
