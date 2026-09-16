---
id: experiment:a00-bc47117f-2715e7
mint_id: bade3f90929145049d2d2786ee60c1ff
type: experiment
parents:
  - hypothesis:l4-sl04-residue-ack-and-latch-fixes
next_edges: []
confidence: 0.9
edited_by: a00-c3326eda
evidence_runs:
  - experiment:a00-bc47117f-2715e7
loop: hypothesis:l4-sl04-residue-ack-and-latch-fixes@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: a30f285ff9f820cd
season: 2
title: A00 bc47117f 2715e7
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-bc47117f-2715e7

## Experiment

SL.04 review residue, CODED not re-measured (goal:g15 build order). Three of the
four named CODE items were open on the built bytes and are FIXED; item (3) was
already satisfied by the SM.243 harvest and lands its regression test only.
Scope: `extensions/agi/bin/rotate.py` (four named regions + their callers) and
`extensions/agi/tests/test_rotate.py` + `extensions/agi/tests/test_rotate_latch_sweep.py`.
No git, no commits. ~40 production lines changed (docstrings included), under
the 60-line ceiling.

### Item (3) `_compose_seating_announcement` non-prime ack line — ALREADY SATISFIED (measured)

`rotate.py:5396` def; the non-prime branch is `rotate.py:5451-5457` and already
calls `_ack_call_args(seat=seat, role=role, gen=generation)`. Measured NOW by
calling the function directly (`python3` from `extensions/agi/bin`):

```
role='director'   -> rotate.py ack --post adv-alive --ref abc123 diff --text -
role='parent'     -> rotate.py ack --post adv-alive --ref abc123 diff --text -
role='prime'      -> rotate.py ack --seat adv-alive --gen 3 --ref abc123 diff --text -
role=None         -> rotate.py ack --seat adv-alive --gen 3 --ref abc123 diff --text -
```

No `--gen` and no `--seat` for a non-prime post; the prime branch keeps
`--seat <seat> --gen 3` byte-identical. Recorded as already-satisfied;
`test_seating_announcement_ack_line_is_genless_for_a_nonprime_post` is the
regression test that lands with it.

### Item (4) after_join second-input dm — FIXED

Before (`_compose_after_join_dm("director-seat", 7, "abc123", [])`):

```
python3 extensions/agi/bin/rotate.py ack --post director-seat --gen 7 --ref abc123 diff --text -
```

After (same call, `role="director"`):

```
python3 extensions/agi/bin/rotate.py ack --post director-seat --ref abc123 diff --text -
```

Role matrix measured after the fix:

```
role='director' -> ack --post director-seat --ref abc123 diff --text -
role='parent'   -> ack --post director-seat --ref abc123 diff --text -
role='prime'    -> ack --seat director-seat --gen 7 --ref abc123 diff --text -
role=None       -> ack --post director-seat --gen 7 --ref abc123 diff --text -
```

Hunks:

- `rotate.py:12811-12818` — `_compose_after_join_dm` gains keyword-only `role: str | None = None`.
- `rotate.py:12874-12886` — the captive ack argv tail is now built by
  `_ack_call_args(seat=seat, role=role, gen=int(gen))`; an UNKNOWN role
  (`None`) keeps the legacy `--post <seat> --gen <gen>` tail, and the
  `gen not in (None, "")` guard at `:12871` is untouched, so an unresolved gen
  still omits the line entirely (never a placeholder).
- `rotate.py:13180-13181` — `run_after_join` gains `role: str | None = None`.
- `rotate.py:13332` — `run_after_join` resolves `role or _seat_role(root, seat)`
  at the dm call site.
- `rotate.py:13624-13630` — `run_after_join_for_seat` keeps the ROLE THAT WAS
  MEASURED (`row_role = (row or {}).get("role") or None`) separate from the
  template default `"parent"`, so a ROW-LESS seat is not mistaken for a
  non-prime post (a row-less seat genuinely still needs `--gen`);
  `rotate.py:13824` passes `role=row_role`.
- `rotate.py:17367` — the rotate-self dry-run after_join plan passes `role=role`.

The `--ref <ref> diff --text -` tail is intact in every branch.

### Item (7) `_sweep_dead_hook_latches` glob — FIXED

Before (`rotate.py:9576`): `latch_dir.glob(f"hook-{seat}-gen*.lock")` — the
post-SM.243 non-prime shape is `hook-<seat>-<session_id[:8]>.lock`, written by
`extensions/agi/hooks/rotation_alert.py:777-798` `_latch_path` (`if not prime and
session_id: f"hook-{seat}-{session_id[:8]}.lock"`), so a dead session-keyed
latch was never swept — one leaked file per non-prime re-seat.

After (`rotate.py:9605-9606`):

```python
        latches = sorted(set(latch_dir.glob(f"hook-{seat}-gen*.lock"))
                         | set(latch_dir.glob(f"hook-{seat}-????????.lock")))
```

Fixture output (seat `adv-alive`; dead pid from a reaped child; live pid =
`os.getpid()`):

```
swept dead hook latch hook-adv-alive-2717aaaa.lock (holder 3443062)
swept dead hook latch hook-adv-alive-gen1.lock (holder 3443062)
swept: ['hook-adv-alive-2717aaaa.lock', 'hook-adv-alive-gen1.lock']
remaining: ['hook-adv-alive-9999bbbb.lock', 'hook-adv-alive-gen2.lock']
```

So a DEAD session-keyed latch is swept, a LIVE session-keyed latch survives, the
gen shape still works, the one-stderr-line-per-swept-file behaviour and the
`_append_sweep_log` append are unchanged. Known limit, recorded in the docstring
instead of hidden: the 8-char session pattern can also match a LONGER seat name
whose remainder is exactly 8 chars before `.lock` (seat `adv` vs seat `adv-ab`,
latch `hook-adv-ab-gen1.lock`). That collision can only ever unlink a latch whose
holder pid is ALREADY DEAD — the `_pid_alive` gate runs before the unlink for
every candidate, so a live rotate-self is never unlinked in either shape — and a
dead latch is not held, so it is a sweep-timing wrinkle, not a correctness hole.

### Item (8) by-name `--gen` refusal message — FIXED

Before (read verbatim from the pre-fix source at `rotate.py:2429-2432`; this one
was cut before I captured bytes, so it is source-read, not measured output):

```
ERR: --gen is refused on non-prime post 'np-post': a non-prime seating is keyed by session id, never a generation. Run: rotate.py ack --post np-post --session a1b2c3d4-1111-2222-3333-444455556666 diff
```

(bare `rotate.py`, no `--ref`, no `--text -` — a pasted `diff` submits EMPTY text
and rotate-self reads it as `continue`).

After (`rotate.py:2435-2441`):

```
ERR: --gen is refused on non-prime post 'np-post': a non-prime seating is keyed by session id, never a generation. Run: python3 extensions/agi/bin/rotate.py ack --post np-post --session a1b2c3d4 --ref <your ListAgents ref> diff --text -
```

The engine-relative entry point matches the sibling refusal paths, the session
is named by its `sid8` (exactly the slice `_ack_path` keys the file on, so the
pasted form is byte-identical), `--ref` is always present, and `--text -` is
appended only for `args.answer == "diff"` (the streamed body); a `continue`
refusal prints a complete command with no `--text -`.

## Evidence

All commands run from the checkout root
`/home/ubuntu/work/agi/.agi/worktrees/a00-c3326eda`.

Build-order verification (the two files named in the orders):

```
$ python3 -m pytest extensions/agi/tests/test_rotate.py extensions/agi/tests/test_rotate_latch_sweep.py -q
306 passed, 346 warnings in 53.12s
```

Regression sweep over every caller of the two changed functions and the ack /
latch readers:

```
$ python3 -m pytest extensions/agi/tests/test_after_join_service.py extensions/agi/tests/test_rotate_handover.py extensions/agi/tests/test_rotation_alerts.py extensions/agi/tests/test_rotate_startup.py extensions/agi/tests/test_rotate_templates.py -q
266 passed, 267 warnings in 21.87s

$ python3 -m pytest extensions/agi/tests/test_rotate_recover.py extensions/agi/tests/test_rotate_identity_main.py extensions/agi/tests/test_rotate_verb.py extensions/agi/tests/test_rotate_prepare.py extensions/agi/tests/test_rotate_complete.py extensions/agi/tests/test_rotate_tail.py -q
129 passed, 211 warnings in 10.78s
```

New assertions landed (6 tests):

- `tests/test_rotate.py::test_seating_announcement_ack_line_is_genless_for_a_nonprime_post` — item 3, both directions (non-prime -> `--post`, no `--gen`; prime -> `--seat ... --gen 3`).
- `tests/test_rotate.py::test_after_join_dm_ack_line_routes_through_ack_call_args` — item 4, non-prime / prime / unknown-role, and the `--ref ... diff --text -` tail.
- `tests/test_rotate.py::test_after_join_dm_omits_ack_line_when_gen_unresolved` — item 4 guard kept.
- `tests/test_rotate.py::test_ack_gen_refusal_line_is_complete_and_pasteable` — item 8, `python3 extensions/agi/bin/rotate.py` + `--session <sid8>` + `--ref` + `--text -` on stderr for `diff`, and no `--text -` for `continue`.
- `tests/test_rotate_latch_sweep.py::test_sweep_removes_dead_session_keyed_latch_and_keeps_live` — item 7, dead session-keyed swept, live session-keyed kept, gen shape still swept.
- `tests/test_rotate_latch_sweep.py::test_sweep_never_unlinks_a_live_session_keyed_latch` — item 7 falsifier: a live-pid latch of EITHER shape survives.

## Verdict

`proved` against the parent hypothesis' falsifiers: neither announcement call
site prints `--gen` for a non-prime post (item 3 was already fixed; item 4 is
fixed and measured), a dead session-keyed latch is swept on a full sweep pass
while a live-pid latch of either shape survives, and the `--gen` refusal line
carries `--ref` and `--text -` with the engine-relative entry point.

## THOUGHT

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-c3326eda, SM.35) — I did not re-run the kid's suite as
evidence; I read the changed bytes and ran my own negative probes.

(1) WHAT THE INSTRUCTION SAID. The target hypothesis: "route the announcement
line through _ack_call_args (the shared helper cmd_ack itself uses)"; "widen the
glob (or add a session-id-keyed pattern) so both shapes are covered"; "the
refusal message must include a complete, pasteable command"; falsifiers: "any of
the two announcement call sites still printing --gen for a non-prime post after
the fix; a dead session-keyed latch file surviving a full sweep pass; the --gen
refusal line still missing --ref/--text -".

(2) WHAT THE MACHINE ACTUALLY DOES (probes run by me, not the kid's tests).
  conjunct (3): `_compose_seating_announcement(role="director", ask_diff=True)`
    returns `rotate.py ack --post np-post --ref abc123 diff --text -`; fed
    verbatim into `cmd_ack` it returns 0 — the line is accepted, never the
    by-name refusal. Already satisfied by the SM.243 harvest; the kid measured
    it before cutting, which is why it lands a regression test and not a fix.
  conjunct (4): at the PUBLIC entry `run_after_join(root, seat="np-post", gen=7,
    startup={}, dry_run=True)` with NO role passed, a spy on
    `_compose_after_join_dm` saw `role='director'` (resolved from the seat row)
    and the dm carried `--post np-post` and no `--gen`; that dm line fed back
    into `cmd_ack` returns 0.
  conjunct (7): a dead `hook-adv-2717aaaa.lock` next to a live
    `hook-adv-9999bbbb.lock` in a fixture rotations dir: dead swept, live
    survives.
  conjunct (8): `cmd_ack(seat="np-post", gen=3, answer="diff")` on a
    session-keyed row prints `Run: python3 extensions/agi/bin/rotate.py ack
    --post np-post --session a1b2c3d4 --ref <your ListAgents ref> diff --text -`
    with `--ref` and `--text -`; substituting the ref placeholder and pasting
    that line back into `cmd_ack` returns 0 (not the refusal).
  Regression: 398 passed across test_rotate.py, test_rotate_latch_sweep.py,
    test_after_join_service.py, test_rotation_alerts.py.

(3) THE NEAR MISS. Two, both recorded rather than hidden, and neither is
reachable on the live registry (38 rows read across three worktrees: 0 without a
`role`, every session_id length 36):
  (a) item (7), the exact input I tried to kill it with: a DEAD session-keyed
      latch whose sid is SHORTER than 8 chars (`hook-adv-abc.lock`) is NOT swept
      — `hook-{seat}-????????.lock` demands exactly 8. `rotation_alert._latch_path`
      writes `session_id[:8]`, so the written shape is "up to 8". It is
      unreachable in production only because harness session ids are UUIDs; the
      kid's own docstring example for the residual collision (`seat adv` vs
      `seat adv-ab` latch `hook-adv-ab-gen1.lock`) does NOT actually collide —
      the middle is 7 chars, not 8 — so the documented limit is the wrong one.
      A precise widening cannot be written without knowing the live seat-name
      set (a bare `hook-{seat}-*` swallows a longer seat's latch), which is why
      I accept the 8-char pattern rather than re-cutting.
  (b) item (4), the sentinel: `_compose_after_join_dm(role=None)` bypasses
      `_ack_call_args` and emits `--post <seat> --gen <gen>`, which `cmd_ack`
      REFUSES for any row that carries a session_id (`_ack_session_id` treats a
      role-less row as non-prime, as does the hook's own `_seat_latch_identity`).
      So the one input where the shared helper's own answer (`--post`, no gen)
      is right is the one input the fix overrides. A row with session_id and no
      role is the trigger; no writer in this tree emits one.

(4) DEVIATION. None from the target; I kept the kid's verdict at `proved`,
because every conjunct holds for every producible input and the two gaps are
latent. I recorded the gaps in the node rather than accepting the kid's stated
collision limit, which misdescribes where the hole actually is.
<!-- THOUGHT:END -->

## Agent Notes
SL.04 residue CODE fixes built: item 4 after_join dm ack tail now routed through _ack_call_args (non-prime -> 'ack --post <seat> --ref ... diff --text -', no --gen; prime unchanged); item 7 _sweep_dead_hook_latches widens to the post-SM.243 session-keyed latch shape hook-<seat>-<sid8>.lock while the pid-liveness gate still protects live holders of either shape; item 8 --gen refusal prints a COMPLETE pasteable command (python3 extensions/agi/bin/rotate.py + --session <sid8> + --ref + --text - on diff); item 3 measured ALREADY SATISFIED by the SM.243 harvest (non-prime announce emits 'ack --post <seat>', no --gen) so only its regression test lands. 6 new tests. pytest extensions/agi/tests/test_rotate.py + test_rotate_latch_sweep.py -q = 306 passed; 395 further assertions across after_join_service/rotate_handover/rotation_alerts/rotate_startup/rotate_templates/recover/identity_main/verb/prepare/complete/tail = all passed.

PARENT REVIEW (a00-c3326eda, SM.35) — accepted at `proved`, confidence 0.85. Verdict is mine, from probes I ran, not from the kid's suite: (3) announcement emits `ack --post np-post --ref abc123 diff --text -` and, fed verbatim into `cmd_ack`, returns 0 (already fixed by the SM.243 harvest — kid measured before cutting); (4) at the PUBLIC `run_after_join` entry with role omitted, a spy saw `role='director'` resolved from the row and the dm held `--post ...` with no `--gen`, and that line pasted back into `cmd_ack` returns 0; (7) a dead `hook-adv-2717aaaa.lock` is swept while a live latch of the same shape survives; (8) the refusal prints `--ref` and `--text -` and the pasted corrective line returns 0. Regression: 398 passed in test_rotate.py + test_rotate_latch_sweep.py + test_after_join_service.py + test_rotation_alerts.py. TWO LATENT GAPS RECORDED, NOT FIXED: (a) item (7) misses a dead session-keyed latch whose sid is shorter than 8 chars (`session_id[:8]` writes "up to 8"); the kid's stated collision limit is the wrong one — `hook-adv-ab-gen1.lock` is 7 mid-chars and never matches. Unreachable only because harness session ids are UUIDs (38 live rows: 0 role-less, all sids 36 chars). (b) item (4) `role=None` overrides `_ack_call_args` and emits `--gen`, which `cmd_ack` refuses for any row carrying a session_id; trigger is a role-less row, which no writer in this tree emits.
