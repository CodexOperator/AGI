---
id: experiment:a00-3b353d15-da3cef
mint_id: 3078010490b84ff5b6a67994c276a2a6
type: experiment
parents:
  - hypothesis:l4-sm48b-a-spawned-agent-stamps-its-own-id-never-the-inherited-seat-so-a-kid-act-cannot-stale-the-director
next_edges: []
confidence: 0.9
edited_by: a00-1d0ac11a
evidence_runs:
  - experiment:a00-3b353d15-da3cef
line_ceiling: 10
loop: hypothesis:l4-sm48b-a-spawned-agent-stamps-its-own-id-never-the-inherited-seat-so-a-kid-act-cannot-stale-the-director@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "env AGI_TIER=kid AGI_AGENT_ID=a00-probe AGI_SEAT=sensei-director AGI_ACTOR=a00-probe python3 extensions/agi/bin/write.py goal:g7.16 \"note probeB\" --root <tmp>/.agi", "expected": "a kid act stamps a00-probe.last-act; sensei-director.last-act ABSENT", "observed": "stamps: a00-probe.last-act only", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "env AGI_TIER=director AGI_AGENT_ID=dry00-x AGI_ACTOR=dry00-x AGI_SEAT=sensei-director -> last_act.touch_env(root) -> last_act.card_stale(root,'sensei-director',card); A/B against 3d470d88c bytes", "expected": "the director's OWN act stamps the seat and stales its own card, byte-identical to the pre-change behaviour", "observed": "PRE and POST both: env_seat()='sensei-director', card_stale=True (identical); kid-1 bytes gave 'dry00-x', stale=False", "result": "held"}
  - {"conjunct": 3, "class": "auth", "cmd": "env AGI_TIER=director AGI_AGENT_ID=dry00-x AGI_SEAT=sensei-director python3 extensions/agi/bin/write.py goal:g7.16 \"note probeC\" --root <tmp>/.agi --actor master-sensei", "expected": "the explicit flag wins over both the agent id and the owned seat", "observed": "master-sensei.last-act written; dry00-x.last-act absent", "result": "held"}
  - {"conjunct": 2, "class": "wire", "cmd": "for T in kid parent director: dispatch.py ... --tier $T --dry-run | grep -o 'AGI_TIER=[a-z_]*'", "expected": "the tier discriminator is present for every dispatched tier, so the OWNED/AGENT branch is always decidable", "observed": "kid->AGI_TIER=kid; parent->AGI_TIER=parent; director->AGI_TIER=director", "result": "held"}
  - {"conjunct": 4, "class": "gate", "cmd": "env -i PATH HOME USER=sensei-director python3 extensions/agi/bin/write.py goal:g7.16 \"note probeD\" --root <tmp>/.agi", "expected": "no seat named -> NO stamp written", "observed": "0 *.last-act files under the graph root", "result": "held"}
production_lines: 9
profile: balanced
role: kid
scaffold_hash: a8559004e65212be
season: 2
title: A00 3b353d15 da3cef
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-3b353d15-da3cef
Fixed the SM.49 conjunct-2 regression in `extensions/agi/bin/last_act.py` by
making the seat resolution TIER-AWARE, and proved all five conjuncts on the
built bytes. One new test; **9 production lines added** (`git diff --numstat`:
`9 4 extensions/agi/bin/last_act.py`, ceiling 10).

## What changed (9 added / 4 removed)

```python
SEAT_ENV       = ("AGI_AGENT_ID", "AGI_SEAT", "AGI_ACTOR")   # an AGENT's own id
SEAT_ENV_OWNED = ("AGI_SEAT", "AGI_AGENT_ID", "AGI_ACTOR")   # the seat IS the actor
OWNED_TIERS    = ("director", "prime_director")

    keys = SEAT_ENV_OWNED if (os.environ.get("AGI_TIER") or "").strip() in OWNED_TIERS else SEAT_ENV
    for v in (explicit, *[os.environ.get(k) for k in keys]):
```

`explicit` still FIRST (kid 1's `--actor` ruling stands); `USER` still dropped.

## Why AGI_TIER (measured, not inferred)

The discriminator the target's own preamble named — `AGI_SEAT` inherited into a
kid's env — cannot separate an OWNED seat from an INHERITED one: both land as
`AGI_SEAT=<post>` beside `AGI_AGENT_ID=<agent>`. A global reorder is symmetric
in the two cases, so it cannot be right in both. `AGI_TIER` is the signal that
IS in the env, read from the REAL spawn (not the source order):

    $ dispatch.py .agi SM.49 --tier director --role director --seat sensei-director --dry-run
      AGI_TIER=director  AGI_AGENT_ID=dry00-9848878f  AGI_ACTOR=dry00-9848878f  AGI_SEAT=sensei-director
    $ dispatch.py .agi SM.49 --tier kid --role kid --seat sensei-director --dry-run
      AGI_TIER=kid       AGI_AGENT_ID=dry00-f0def060  AGI_ACTOR=dry00-f0def060  AGI_SEAT=sensei-director

A director is itself a spawned agent carrying BOTH keys; `AGI_TIER` is what says
it OWNS the seat. Tier vocabulary read from `dispatch.py:898`
(`kid|parent|director|prime_director`), so `OWNED_TIERS` is complete.

## Post-fix probes (`.agi/sessions/iter-SM.49/a00-3b353d15/probe.py`)

```
POST bytes: SEAT_ENV=('AGI_AGENT_ID','AGI_SEAT','AGI_ACTOR') SEAT_ENV_OWNED=('AGI_SEAT','AGI_AGENT_ID','AGI_ACTOR') OWNED_TIERS=('director','prime_director')
C2 director  : env_seat=sensei-director stamped=sensei-director card_stale=True dry00-x_stamp=False
C1 kid       : env_seat=a00-kid stamped=a00-kid director_stamp=False
C3 --actor  : flag wins under both tiers; no agent/seat stamp written
C4 USER      : env_seat='' no stamp
C5 no tier   : env_seat=sensei-director (AGI_SEAT fallback)
PRE-SIM kid1 : env_seat=dry00-x stamped=dry00-x card_stale=False (director's OWN act)
PRE-SIM orig: env_seat=sensei-director stamped=sensei-director director_card_stale=True (kid's act)
POST (kid)   : env_seat=a00-kid
ALL PROBES HELD
```

The two `PRE-SIM` rows are the A/B, on the same director env, with only the
resolution differing: kid-1's bytes (agent-first for all) give `card_stale=False`
— conjunct 2 clause 2 FALSIFIED, the regression; the pre-kid-1 bytes stamp the
director for a KID's act — the original rotation loop. The built bytes give
`True` and `a00-kid` respectively: both clauses at once. `PRE-SIM` lines were
produced by rebinding the module constants in the probe, not by running git.

## Suite runs (named files, never a bare directory)

    $ python3 -m pytest extensions/agi/tests/test_last_act.py \
        extensions/agi/tests/test_bin_help_smoke.py -q
    74 passed, 4 skipped in 8.44s

    $ python3 -m pytest extensions/agi/tests/test_last_act.py \
        extensions/agi/tests/test_bin_help_smoke.py extensions/agi/tests/test_cli.py \
        extensions/agi/tests/test_send.py extensions/agi/tests/test_rotate_prepare.py -q
    483 passed, 4 skipped, 48 warnings in 17.67s

    $ python3 -m pytest extensions/agi/tests/test_rotation_alert.py \
        extensions/agi/tests/test_rotation_alerts.py extensions/agi/tests/test_rotate_alert_two_tree.py \
        extensions/agi/tests/test_heal_ack_rotation.py extensions/agi/tests/test_mail_alert.py -q
    80 passed, 1 xfailed, 28 warnings in 13.42s

## Conjunct coverage

1. agent id stamped, `<post>.last-act` ABSENT under `AGI_TIER=kid` — probe C1 and
   kid 1's `test_spawned_agent_stamps_its_own_id_never_the_inherited_seat`
   (now with `AGI_TIER` explicitly deleted, so it is hermetic).
2. NEW `test_director_tier_stamps_the_seat_it_owns`: `AGI_TIER=director` +
   `AGI_AGENT_ID` + `AGI_ACTOR` + `AGI_SEAT` → `env_seat() == 'sensei-director'`,
   `touch_env()` stamps the seat, the agent id is never stamped, and
   `card_stale(...)[0] is True` (card back-dated 10 s so `mtime < act` is
   decidable inside one test second; git is absent in the tmp fixture so the
   card's own commit is unmeasurable = `None`, the fail-open path).
3. `--actor` wins under both tiers — `test_explicit_actor_beats_the_agent_id_env`
   plus probe C3 (director tier included).
4. `USER` alone → `env_seat() == ''`, no stamp — folded into conjunct 1's test,
   probe C4.
5. `test_bin_help_smoke.py` GREEN, `last_act.py` in `NO_HELP` (kid 1's line, no
   change needed).

## Call sites untouched

`send.py:5086/5101/5129` and `rotate.py:4144`, `dispatch.py:2739` pass an
explicit seat (unchanged); `cli.py:2623` and `write.py:2590` pass `None` and now
resolve through the tier. `write.py`, `cli.py`, `send.py`, `rotate.py`, the hook
and `dispatch.py` were NOT edited.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
why this version differs from the last one

This is the SM.49 kid-2 correction child of `experiment:a00-c5796232-7e29ec`.
That node proved conjuncts 1/3/4/5 and FALSIFIED conjunct 2 clause 2: raising
AGI_AGENT_ID above AGI_SEAT for everyone also re-pointed a DIRECTOR's own clock
at its agent id, because a director is itself a spawned agent with both keys set.
The parent measured that A/B and re-briefed.

The previous version of this file was the empty scaffold. What differs now is
the resolution itself: instead of one global tuple order, `env_seat` picks the
tuple from the actor's TIER -- an agent (kid/parent) stamps its own AGI_AGENT_ID,
a seat that owns itself (director/prime_director) stamps AGI_SEAT. Both clauses
of conjunct 2 are true at once, which a single global order cannot deliver
because it is symmetric in the two cases. `explicit` stays first and `USER`
stays dropped: both prior rulings are upheld, and the entire change is 9 added
lines in one function plus two constants -- no call site touched.

I deviated from the parent's `SEAT_ENV_OWNED = ("AGI_SEAT","AGI_AGENT_ID","AGI_ACTOR")`
leading shape in NO way; I kept it. I did add an explicit `AGI_TIER` delete to
kid 1's three tests (tests are free against the ceiling) so they are hermetic
even outside the conftest strip.
<!-- THOUGHT:END -->

Raw output, screenshots, logs.

## Agent Notes
TIER-aware env_seat in last_act.py: AGI_TIER in (director,prime_director) -> SEAT_ENV_OWNED (AGI_SEAT first), else SEAT_ENV (AGI_AGENT_ID first); explicit still first, USER still dropped. 9 added/4 removed lines (ceiling 10). A/B probe: director env (AGI_TIER=director, both keys) -> env_seat=sensei-director, card_stale=True, agent stamp absent (conjunct 2 clause 2); kid env (AGI_TIER=kid, inherited seat) -> a00-kid stamped, <post>.last-act absent (conjunct 1); kid-1 bytes sim -> dry00-x, stale False (the regression, reproduced); pre-kid-1 sim -> director staled by a kid's act (the original disease). --actor wins under both tiers; USER alone no stamp. last_act.py + test_bin_help_smoke.py 74 passed 4 skipped; +test_cli/test_send/test_rotate_prepare 483 passed; rotation-alert cohort 80 passed 1 xfailed. One new test test_director_tier_stamps_the_seat_it_owns. dispatch.py/cli.py/write.py/send.py/rotate.py/hook untouched.

PARENT REVIEW (a00-1d0ac11a, SM.49) -- ACCEPTED. VERDICT: proved on conjuncts 1-4, and the SM.49 correction is confirmed by my own probes, not by your suite.

MY PROBES (exact commands in the probes: frontmatter field).

(1) GATE, conjunct 2 clause 2 -- the regression you were re-briefed to fix is GONE. Same fixture, same env, same call, only the bytes differing: PRE-change 3d470d88c -> env_seat()='sensei-director', card_stale=True. your bytes -> env_seat()='sensei-director', card_stale=True. Byte-identical behaviour restored, and kid 1's bytes in the same probe give 'dry00-x', stale=False. This is the A/B that condemned kid 1 and it now passes.

(2) WIRE, conjunct 1 -- held on the REAL call site. AGI_TIER=kid + AGI_AGENT_ID=a00-probe + inherited AGI_SEAT=sensei-director through write.py:2590 (no --actor) writes a00-probe.last-act and leaves sensei-director.last-act absent. The changed bytes are reached live from the real entry point.

(3) AUTH, conjunct 3 -- held. Under AGI_TIER=director with AGI_AGENT_ID=dry00-x and AGI_SEAT=sensei-director, write.py --actor master-sensei writes master-sensei.last-act and does NOT write dry00-x.last-act. The explicit flag wins in BOTH branches, which is what keeps write.py --actor <post> working.

(4) WIRE, the fix's load-bearing assumption -- held. I did not take 'AGI_TIER is always set' on trust: I built and ran dispatch.py --dry-run for kid, parent and director and read AGI_TIER=kid / AGI_TIER=parent / AGI_TIER=director off the real spawn env of each. The OWNED/AGENT branch is always decidable for a dispatched agent.

(5) GATE, conjunct 4 -- held. env -i with only USER=sensei-director writes zero *.last-act files.

SUITE, run by me in MY ambient env (which carries AGI_AGENT_ID and AGI_TIER=parent -- the env an un-hermetic test would fail in): test_last_act.py + test_bin_help_smoke.py + test_rotate_prepare.py + test_git_commit_guard.py = 163 passed, 4 skipped. Your hermeticity edits hold.

CEILING: 9 production lines against 10 -- I read the numstat and your node's frontmatter agrees. No re-brief owed.

WHAT I ACCEPT AS A CAVEAT RATHER THAN A DEFECT (recorded, not charged to you): the branch keys on AGI_TIER, so a director-tier actor whose env has AGI_SEAT and AGI_AGENT_ID but NO AGI_TIER falls to the AGENT branch and re-opens the regression for that one process. Every dispatch path sets AGI_TIER (probe 4), so this is unreachable from dispatch, and a hand-launched seat has no AGI_AGENT_ID either -- but it is the one shape the fix does not cover, and it should be named in the hypothesis node rather than left implicit.

You did the thing the round needed: you kept the two prior rulings (explicit first, USER dropped) that you could have been tempted to trade away, and you did not respond to the re-brief by re-raising AGI_AGENT_ID globally. dispatch.py, write.py, cli.py, send.py, rotate.py and the hook are untouched -- I checked the diff, not your report.
