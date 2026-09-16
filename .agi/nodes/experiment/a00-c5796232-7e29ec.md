---
id: experiment:a00-c5796232-7e29ec
mint_id: 2c8777e43ab241f0889a1437e29e5e56
type: experiment
parents:
  - hypothesis:l4-sm48b-a-spawned-agent-stamps-its-own-id-never-the-inherited-seat-so-a-kid-act-cannot-stale-the-director
next_edges: []
confidence: 0.7
edited_by: a00-1d0ac11a
evidence_runs:
  - experiment:a00-c5796232-7e29ec
line_ceiling: 10
loop: hypothesis:l4-sm48b-a-spawned-agent-stamps-its-own-id-never-the-inherited-seat-so-a-kid-act-cannot-stale-the-director@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "env AGI_AGENT_ID=a00-probe AGI_SEAT=sensei-director AGI_ACTOR=a00-probe USER=sensei-director python3 extensions/agi/bin/write.py goal:g17.1 \"note probe1\" --root <tmp>/.agi", "expected": "a00-probe.last-act written, sensei-director.last-act absent", "observed": "a00-probe.last-act only; sensei-director.last-act absent", "result": "held"}
  - {"conjunct": 3, "class": "auth", "cmd": "same env + write.py goal:g17.1 \"note probe3\" --actor sensei-director", "expected": "the explicit flag wins: sensei-director.last-act written, a00-probe.last-act absent", "observed": "sensei-director.last-act only", "result": "held"}
  - {"conjunct": 4, "class": "gate", "cmd": "env -i PATH HOME USER=sensei-director python3 extensions/agi/bin/write.py goal:g17.1 \"note probe2\" --root <tmp>/.agi", "expected": "no seat named -> NO stamp written (the falsifier 'USER ever producing a stamp')", "observed": "0 *.last-act files under the graph root; write succeeded", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "director env (AGI_AGENT_ID=dry00-x AGI_ACTOR=dry00-x AGI_SEAT=sensei-director) -> last_act.touch_env(root) (EXACTLY cli.py:2623 / write.py:2590 un-flagged) -> last_act.card_stale(root,'sensei-director',card); A/B against 3d470d88c bytes", "expected": "the director's OWN act stales its own card (conjunct 2 clause 2)", "observed": "POST bytes: env_seat()='dry00-x', card STALE=False, sensei-director.last-act absent; PRE bytes 3d470d88c: env_seat()='sensei-director', card STALE=True", "result": "falsified"}
production_lines: 8
profile: balanced
role: kid
scaffold_hash: 68ed3af2c576408a
season: 2
title: A00 c5796232 7e29ec
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-c5796232-7e29ec

Built conjuncts 1-5 of the SM.48b claim in `extensions/agi/bin/last_act.py` and
proved them on the built bytes. Parent's resolution of the conjunct-1 ambiguity
holds: `explicit` first, then `AGI_AGENT_ID`, then `AGI_SEAT`/`AGI_ACTOR`;
`USER` dropped; `env_seat`'s loop untouched.

## What changed (8 production lines added, 4 removed — `git diff --numstat`)

`extensions/agi/bin/last_act.py`:

```python
SEAT_ENV = ("AGI_AGENT_ID", "AGI_SEAT", "AGI_ACTOR")
```

plus the `env_seat` docstring, now quoted from the file:

```
    """The seat a verb acts as: the caller's `explicit` flag first (--actor,
    --seat, --from), else AGI_AGENT_ID (a spawned agent stamps its OWN id,
    never the seat it inherited), else AGI_SEAT, AGI_ACTOR. '' when nothing
    names a seat, and then NO stamp is written."""
```

`extensions/agi/tests/test_bin_help_smoke.py`: ONE `NO_HELP` dict line —
`"last_act.py": "library module (the seat's own last-act clock); no --help",`.

`extensions/agi/tests/test_last_act.py`: 3 new env-fixture tests (no spawn) and
`monkeypatch.delenv("AGI_AGENT_ID"/"AGI_ACTOR")` on the existing closeout test.

## Pre-fix state (measured, not re-derived)

    $ python3 -c "... last_act.env_seat()"   # in this kid's own env:
    PRE-FIX env_seat() -> 'sensei-director'      # AGI_AGENT_ID=a00-c5796232 ignored
    PRE-FIX SEAT_ENV = ('AGI_SEAT', 'AGI_ACTOR', 'AGI_AGENT_ID', 'USER')

    $ python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q -k last_act
    FAILED test_help_smoke[last_act.py]
    E  AssertionError: last_act.py --help produced empty stdout (exit 0 though)
    1 failed, 68 deselected

## Post-fix state (the same two probes)

    $ python3 -c "... last_act.env_seat()"   # same kid env:
    POST-FIX env_seat() -> 'a00-c5796232'
    POST-FIX SEAT_ENV = ('AGI_AGENT_ID', 'AGI_SEAT', 'AGI_ACTOR')

    $ python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q
    65 passed, 4 skipped        # last_act.py now one of the 4 skips

## Suite runs (named files, never a bare directory)

    $ python3 -m pytest extensions/agi/tests/test_last_act.py \
        extensions/agi/tests/test_bin_help_smoke.py -q
    73 passed, 4 skipped in 8.80s

    $ python3 -m pytest extensions/agi/tests/test_cli.py \
        extensions/agi/tests/test_send.py \
        extensions/agi/tests/test_rotate_prepare.py -q
    409 passed, 48 warnings in 10.61s

## Hermeticity probe (the trap the parent named)

A spawned kid's ambient env carries the hazard keys, so the suite must pass in
BOTH configurations:

    $ python3 -m pytest extensions/agi/tests/test_last_act.py -q          # ambient
    8 passed
    $ env -u AGI_AGENT_ID -u AGI_ACTOR -u AGI_SEAT \
        python3 -m pytest extensions/agi/tests/test_last_act.py -q
    8 passed

No test reads the ambient agent id: the closeout test's seat assertions are
preceded by `delenv` on AGI_AGENT_ID/AGI_ACTOR, and every new test sets or
deletes every key its assertion depends on.

## Conjunct coverage

1. `test_spawned_agent_stamps_its_own_id_never_the_inherited_seat` —
   `AGI_AGENT_ID=a00-x` + inherited `AGI_SEAT=sensei-director` → `a00-x` stamped,
   `<director>.last-act` ABSENT.
2. `test_only_a_seat_env_stamps_that_seat_itself` — only `AGI_SEAT` → the seat's
   own stamp, and not `a00-x`'s.
3. `test_explicit_actor_beats_the_agent_id_env` — `--actor master-sensei` with
   `AGI_AGENT_ID` set → the flag wins.
4. folded into test 1: only `USER=sensei-director` → `env_seat() == ""` and
   `touch_env()` writes nothing.
5. `last_act.py` in `NO_HELP`; help smoke green.

Call sites were NOT touched: `cli.py:2623` (`touch_env(root)`) and
`write.py:2590` (`touch_env(root, args.actor)`) now resolve the kid's own id;
`send.py`, `rotate.py:4144`, `dispatch.py:2739` all pass an explicit seat and
are unchanged in behaviour.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
why this version differs from the last one

The previous version was the kid's own record of its build: it claimed conjuncts 1-5 proved and reported verdict proved at confidence 0.9.

This version is the parent's review, and it changes what the node asserts in one place: conjunct 2 clause 2 is FALSIFIED, not proved. The kid's bytes raise AGI_AGENT_ID above AGI_SEAT for everyone, and a director is itself a spawned agent with both keys set (I read that off the real spawn by running dispatch.py --tier director --seat sensei-director --dry-run, rather than reading the source order). So the director's own cli.py done / write.py act stopped staling its own card, which conjunct 2 forbids. The A/B is in probes: conjunct 2, and the review note carries the commands.

The version also records the falsifier runs I did myself (wire on the real write.py call site, auth on --actor, gate on USER-alone) so the parts that DO hold are evidenced by a probe rather than by the kid's suite.

I did not edit the kid's body claims about conjuncts 1/3/4/5: my probes agree with them. I added probes: and this note, and left the node's verdict field alone -- cli.py done owns that field and the round's final verdict is recorded by me, not by editing this file.
<!-- THOUGHT:END -->

## Agent Notes
SEAT_ENV reordered to (AGI_AGENT_ID, AGI_SEAT, AGI_ACTOR) with explicit still first; USER dropped; last_act.py added to NO_HELP. 8 production lines. Kid env now resolves a00-c5796232 instead of sensei-director; test_last_act+test_bin_help_smoke 73 passed, test_cli/test_send/test_rotate_prepare 409 passed, test_rotation_alert(s) 61 passed; hermetic both with and without ambient AGI_AGENT_ID.

PARENT REVIEW (a00-1d0ac11a, SM.49). VERDICT: lean_proved on conjuncts 1/3/4/5, FALSIFIED on conjunct 2 clause 2 -> the round is NOT accepted as final; kid 2 is re-briefed against it (see the sibling experiment node).

PROBES I RAN (not the kid's suite). See the probes: frontmatter field for the exact commands.

(1) WIRE, conjunct 1 — HELD. With a spawned-agent env (AGI_AGENT_ID=a00-probe, inherited AGI_SEAT=sensei-director, AGI_ACTOR=a00-probe) the REAL call site write.py:2590 (no --actor) stamps a00-probe.last-act and leaves sensei-director.last-act ABSENT. The changed bytes are reached live, from the real entry point, not from a stub.

(2) AUTH, conjunct 3 — HELD. Same env plus --actor sensei-director: the flag wins, sensei-director.last-act is written, a00-probe.last-act is absent. The explicit flag still beats the agent id, so write.py --actor <post> is intact.

(3) GATE, conjunct 4 — HELD. env -i with ONLY USER=sensei-director: no seat is named, zero *.last-act files are written. The target's falsifier 'USER ever producing a stamp' does not fire.

(4) GATE, conjunct 2 clause 2 — FALSIFIED, and this is the finding. The target requires 'the director own acts (its harvest, its sends, its notes) still do [stale the card]'. A director is ITSELF a spawned agent: I built and ran dispatch.py --tier director --role director --seat sensei-director --dry-run and read argument N of the real spawn, which prints env AGI_AGENT_ID=dry00-4414dcb9 AGI_ACTOR=dry00-4414dcb9 AGI_SEAT=sensei-director. So a director carries BOTH keys, exactly like a kid. Raising AGI_AGENT_ID above AGI_SEAT therefore re-pointed the DIRECTOR'S own clock at its agent id. A/B, same env, same call (last_act.touch_env(root), which IS cli.py:2623 and write.py:2590 un-flagged), only the bytes differing: PRE-change 3d470d88c -> env_seat()='sensei-director', card STALE=True; POST-change -> env_seat()='dry00-x', card STALE=False, sensei-director.last-act absent. The gate (rotate.py:15181 last_act.card_stale(root, seat, card); hooks/rotation_alert.py:880) reads <post>.last-act, which the director now never writes. Net: the kid no longer stales the director (fixed) and the director no longer stales ITSELF (new regression, forbidden by conjunct 2).

WHY THIS IS A SCOPE DEFECT, NOT A KID MISREAD. The target's own preamble measured the disease as 'dispatch.py:1245-1250 lets the dispatching seat inherited AGI_SEAT survive into every kid/parent env', then scoped the fix to last_act.py alone. env_seat cannot separate an OWNED seat from an INHERITED one: both land as AGI_SEAT=<post> next to AGI_AGENT_ID=<agent>. The near miss that satisfies the instruction and loses the mechanism is exactly what landed — a global reorder of one tuple, which is symmetric in the two cases and so cannot be right in both. The discriminator that IS in the env is AGI_TIER (director tiers own the seat; kid/parent tiers inherited it), which is what kid 2 is ordered to use.

EVIDENCE I TRUST: the child's own suite is not my evidence. I re-ran it in MY ambient env (which carries AGI_AGENT_ID) to test the hermeticity claim, and it holds: extensions/agi/tests/test_last_act.py + test_bin_help_smoke.py = 73 passed, 4 skipped, and the help-smoke red is green. Conjunct 5 (last_act.py in NO_HELP) is accepted.
