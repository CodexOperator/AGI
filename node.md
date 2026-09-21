---
id: experiment:a00-f6bca347-d0bcab
mint_id: b5be8921b9f242abad86ec2bf0e71412
type: experiment
parents:
  - hypothesis:l4-the-sensei-audit-verbs-resolve-the-window-by-post-and-record-never-by-b-generation
next_edges: []
confidence: 0.9
edited_by: a00-1e495c92
evidence_runs:
  - experiment:a00-f6bca347-d0bcab
loop: hypothesis:l4-the-sensei-audit-verbs-resolve-the-window-by-post-and-record-never-by-b-generation@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "tmp project: R1 carries observations.b_generation{13,14}, the LATEST rotate-self record OUT is genless; `sensei.py --root <tmp> rotate-out-audit --post thought-master` (no flags)", "expected": "selects the GENLESS LATEST record 20260916T110753Z and its predecessor transcript pred_b.jsonl; an implementation that defaults/keys on b_generation would refuse (old bug) or pick the earlier gen-carrying record", "observed": "rc 0; header `--record 20260916T110753Z`; predecessor transcript .agi/pred_b.jsonl (the latest record's predecessor); no generation consulted", "result": "HOLD — the default is record-keyed, never b_generation"}
  - {"conjunct": 2, "class": "wire", "cmd": "same tmp project, flag through argv: `rotate-out-audit --post thought-master --record 20260916T063950Z`; then `--record nope`", "expected": "--record threads to the selector and picks the OLDER record (transcript pred_a.jsonl, source `previous record 20260916T000000Z transcript_path`); a bogus stamp refuses BY NAME, never falls back to latest", "observed": "--record 20260916T063950Z rc 0, header names that stamp, transcript .agi/pred_a.jsonl; --record nope rc 2 by name", "result": "HOLD — the flag reaches the changed bytes live"}
  - {"conjunct": 3, "class": "auth", "cmd": "same tmp project: `rotate-out-audit --post thought-master --gen 13` (R1 carries b_generation.before=13) and `--gen 99`; and `wake-audit --post thought-master --gen 14` on the after-carrying record", "expected": "--gen resolves through b_generation when present; when absent it REFUSES BY NAME naming the deprecated alias and NEVER becomes the default. wake --gen keeps its pre-existing per-verb predicate (after) AND the same session gate the old _latest_record applied", "observed": "--gen 13 rc 0 -> record 20260916T063950Z; --gen 99 rc 2 `no rotation record ... whose b_generation matches 99 (--gen is a deprecated alias ...)`; no-flag rc 0 (never needed --gen); wake --gen 14 rc 2 by the session gate, exactly as the old gen+session AND did", "result": "HOLD — alias resolves when present, refuses by name otherwise, is never the default"}
  - {"conjunct": 3, "class": "gate", "cmd": "LIVE committed records (the claim's own falsifier): `rotate-out-audit --post {thought-master,sensei-director,master-sensei}` and `wake-audit --post {..}` with no flags", "expected": "no refusal; every printed header names the RECORD stamp and contains no --gen", "observed": "rotate-out rc 0 for all three -> `--record 20260916T110753Z` / `20260916T104936Z` / `20260916T105216Z`, each resolving a real predecessor transcript; wake-audit rc 0 for all three with the same record stamp. The old `ERR: cannot default --gen` is gone", "result": "HOLD — the claim's named falsifier does not fire"}
profile: balanced
role: kid
scaffold_hash: 94fbd74d216f7bd9
season: 2
title: A00 f6bca347 d0bcab
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f6bca347-d0bcab

## Experiment

This is a BUILD round (hypothesis:l4-a-g15-claim-is-a-build-order-not-a-
measurement): measure the pre-fix state, implement the claim in
`extensions/agi/bin/sensei.py`, prove it on the built bytes.

### 1. Pre-fix state, measured on the committed bytes

Run from this checkout, before any edit:

```
$ for s in thought-master sensei-director master-sensei; do \
    python3 extensions/agi/bin/sensei.py rotate-out-audit --post $s; done
ERR: cannot default --gen: the latest record has no b_generation.before   (x3)
```

The three LIVE posts refuse. `wake-audit` ran but printed its identity as a
generation:

```
$ python3 extensions/agi/bin/sensei.py wake-audit --post thought-master
sensei.py wake-audit --seat thought-master --gen latest (role director)
...
```

Mechanism, read off the committed records: `rotate.py` writes
`b_generation` only for a prime role or role None (guard e85a1a797), and every
current rotate-self record for these posts carries NO gen key at ANY depth —
`b_generation`, `gen_before`, `gen_after` all absent, `observations` absent
entirely on thought-master.20260916T110753Z.json. Even
master-sensei.20260916T105216Z.json, which the claim expected to still carry
it, is now genless.

### 2. The claim, built

`extensions/agi/bin/sensei.py`:

- NEW `_record_stamp(path, seat)` — the `<stamp>` token of
  `<seat>.<stamp>[.seating].json`; the ONE identity both verbs print.
- NEW `_select_rotation_record(records, seat, *, record, gen, session_id,
  gen_match)` — ONE resolver: `--record <stamp>|latest` first, then the
  DEPRECATED `--gen` through a per-verb predicate, then the session gate
  (`handover.join.session_id`), then the latest record. `_latest_record` is
  now a thin wrapper over it (no second copy of the rules).
- `_resolve_wake_transcript(..., session_id, record)` uses that resolver; the
  old inline gen/session/latest ladder is gone.
- `_resolve_predecessor_transcript(root, seat, records, IDX, explicit)` —
  keyed on the SELECTED record's INDEX, not on `gen`: it walks BACK from the
  selected record to the nearest earlier record that names a transcript (the
  rotation that seated the predecessor), skipping a nearer record that names
  none rather than inventing a miss, then falls back to the selected record's
  own `s12_self_reap.chain` pids through the registry.
- `rotate_out_audit(root, seat, gen, transcript, registry_dir, record)` —
  default = the post's LATEST rotation record, never a generation. `window`
  gains `record` (the stamp) and `basis` (how it was picked); `window['gen']`
  is kept for existing readers and is the record's OWN generation or None.
- `wake_audit(..., record)` threads the same selector.
- `--record` added to both subparsers; `--gen` help text now says DEPRECATED.
- Both CLI headers print `--record <stamp>`, never `--gen <N>`.

### 3. Post-fix, on the committed LIVE records (no flags)

```
$ python3 extensions/agi/bin/sensei.py rotate-out-audit --post thought-master
sensei.py rotate-out-audit --seat thought-master --record 20260916T110753Z (role director)
predecessor transcript: /home/ubuntu/.claude/projects/-home-ubuntu-work-agi/e55ef12e-f004-400b-a40e-70713e1decad.jsonl (previous record 20260916T063950Z transcript_path)
window: [last real input 1030 2026-09-16T11:06:18.849Z -> 2026-09-16T11:08:55.989691Z] 10 calls
counts: a=1 b=3 c=1 d=5
```

All three posts resolve, each naming the record stamp:

| post | record | predecessor transcript | window |
|---|---|---|---|
| thought-master | 20260916T110753Z | `e55ef12e-...jsonl` via `previous record 20260916T063950Z transcript_path` | 10 calls |
| sensei-director | 20260916T104936Z | `d6231fa7-...jsonl` via `previous record 20260916T085434Z handover.join.transcript` | 6 calls |
| master-sensei | 20260916T105216Z | `ae570747-...jsonl` via `previous record 20260916T063514Z transcript_path` | 5 calls |

The predecessor transcripts are real files, and each one's mtime matches its
record's rotation instant (`e55ef12e-...jsonl` mtime 07:08 EDT = 11:08 UTC =
the OUT record's `recorded_at` 11:08:55Z) — the resolution found the SAME seat
that rotated out, not a neighbour.

`wake-audit --post <seat>` now prints `--record <stamp>` for all three.

Explicit and deprecated paths on the live tree:

```
$ ... rotate-out-audit --post thought-master --record 20260916T063950Z
sensei.py rotate-out-audit --seat thought-master --record 20260916T063950Z (role director)
predecessor transcript: .../8bd78ef0-....jsonl (previous record 20260914T162422Z handover.join.transcript)
$ ... rotate-out-audit --post thought-master --gen 1
ERR: no rotation record for seat 'thought-master' whose b_generation matches 1
     (--gen is a deprecated alias for the record; pass --record <stamp> or no flag at all)
```

### 4. Tests, committed

- NEW `extensions/agi/tests/test_sensei_audit_record_window.py` (11 tests):
  tmp_path copies of the two live record shapes. Genless: the fixture PROVES
  it carries no generation (`_gen_bounds == (None, None)`) — the exact
  condition the old default read — and then both verbs resolve with NO flag,
  `--gen` refuses by name, `--record <stamp>` selects an older record, `--record
  latest` selects the newest, a bogus stamp refuses, only-another-session's
  record still refuses by name. Generation-carrying: `--gen 14` and no-flag
  resolve the SAME transcript, recorded_at and record stamp (falsifier 2). CLI:
  headers name the record stamp and contain no `--gen` in the default path.
- `extensions/agi/tests/test_sensei_rotate_out_audit.py`: the 3 direct
  `_resolve_predecessor_transcript` call sites move to the index signature,
  and the expected `source` strings now name the record stamp
  (`previous record 20260911T100000Z transcript_path`) instead of
  `gen_after==14` — a generation in a printed line is what the claim retires.

```
$ python3 -m pytest extensions/agi/tests/test_failures.py \
    extensions/agi/tests/test_geometry_config.py \
    extensions/agi/tests/test_sensei.py \
    extensions/agi/tests/test_sensei_audit_record_window.py \
    extensions/agi/tests/test_sensei_rotate_out_audit.py \
    extensions/agi/tests/test_sensei_wake_audit.py \
    extensions/agi/tests/test_write_master_sensei.py -q
189 passed, 8 warnings in 3.87s
```

### 5. Falsifiers from the claim, answered

- *"`rotate-out-audit --post thought-master` with no flags on the committed
  20260916T110753Z record still refuses"* — it resolved (10 calls, source names
  the stamp). DISPROVED.
- *"the prime record resolves to a different window than the gen path did"* —
  `test_generation_record_resolves_the_same_window_as_the_gen_path` asserts the
  transcript, `recorded_at` and record stamp are IDENTICAL between `--gen 14`
  and no flag. DISPROVED.
- *"every printed line names the record stamp, never a generation"* — the CLI
  header for both verbs is `--record <stamp>`; the only remaining mention of
  `--gen` is the deprecation note, which names the stamp on the same line.
  `assert "--gen" not in out` holds on every default-path invocation.

### 6. Not touched, by the claim's own scope

`rotate.py` is untouched: the missing generations are the owner's 2026-09-13
rule (doc:l4-owner-decisions, "No generations anywhere"), not a defect. The
writer side keeps writing what it writes.

## Evidence

```
pre-fix (before any edit, this checkout):
$ python3 extensions/agi/bin/sensei.py rotate-out-audit --post thought-master
ERR: cannot default --gen: the latest record has no b_generation.before
$ python3 extensions/agi/bin/sensei.py wake-audit --post thought-master
sensei.py wake-audit --seat thought-master --gen latest (role director)

post-fix (same command, same committed records):
$ python3 extensions/agi/bin/sensei.py rotate-out-audit --post thought-master
sensei.py rotate-out-audit --seat thought-master --record 20260916T110753Z (role director)
predecessor transcript: /home/ubuntu/.claude/projects/-home-ubuntu-work-agi/e55ef12e-f004-400b-a40e-70713e1decad.jsonl (previous record 20260916T063950Z transcript_path)
window: [last real input 1030 2026-09-16T11:06:18.849Z -> 2026-09-16T11:08:55.989691Z] 10 calls
counts: a=1 b=3 c=1 d=5
$ python3 extensions/agi/bin/sensei.py wake-audit --post thought-master
sensei.py wake-audit --seat thought-master --record 20260916T110753Z (role director)

$ python3 -m pytest extensions/agi/tests/test_failures.py extensions/agi/tests/test_geometry_config.py extensions/agi/tests/test_sensei.py extensions/agi/tests/test_sensei_audit_record_window.py extensions/agi/tests/test_sensei_rotate_out_audit.py extensions/agi/tests/test_sensei_wake_audit.py extensions/agi/tests/test_write_master_sensei.py -q
189 passed, 8 warnings in 3.87s
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-1e495c92, SL7.130) of the kid's built claim — rewritten from scratch; the kid's own thought is superseded by this review version.

(1) INSTRUCTION: the target's CLAIM — 'both verbs resolve the window by RECORD — default = the post latest rotate-self record; --record <stamp> ...; --gen stays as a deprecated alias that resolves to the record whose b_generation.before matches WHEN present and refuses by name otherwise, never the default; every printed line names the record stamp, never a generation.'
(2) MECHANISM, built and run: sensei.py gains `_record_stamp` (the <seat>.<stamp>[.seating].json token) and `_select_rotation_record` (record -> deprecated gen -> session gate -> latest), `_latest_record` becomes a thin wrapper, `_resolve_predecessor_transcript` is re-keyed from `gen` to the SELECTED record INDEX and walks BACK to the nearest earlier record naming a transcript, and `--record` is added to both subparsers (`sensei.py:680-830`, CLI `:1999-2035`). Measured by me on the LIVE committed records: all three live posts resolve on both verbs and every header is `--record <stamp>` (TM 20260916T110753Z, SD 20260916T104936Z, MS 20260916T105216Z) — the old `ERR: cannot default --gen` is gone.
(3) NEAR MISS: a fix that keeps defaulting through `_gen_bounds(records[-1][1])[0]` but falls back to 'latest' on None satisfies 'no flag resolves' and still keys the WINDOW on a generation; my conjunct-1 gate probe is the counterfactual — an EARLIER record carrying b_generation beside a genless LATEST record: the certificate must pick the genless latest, and it does.
(4) DEVIATION ACCEPTED, recorded in the kid's own THOUGHT, not mine: `--gen` keeps each verb's own historical predicate (wake matches b_generation.after, not `before`) because flipping it would silently re-point every existing wake invocation at a different transcript; the alias is deprecated either way and the deviation is documented. My probe confirms wake `--gen` is also still ANDed with the session gate exactly as the OLD `_latest_record` did, so it is preserved behaviour, not a new defect.

PROBES (parent-run, per conjunct, in `probes:` above): 4 probes, all HOLD. conjunct 1 gate, conjunct 2 wire, conjunct 3 auth + gate. No probe falsified a conjunct; `proved` stands. Regression check: 141 passed in the four sensei test files; no other non-test caller of the changed signatures exists (rotate.py's `_latest_record_dict` is a different function).
<!-- THOUGHT:END -->

## Agent Notes
BUILT the claim in sensei.py: _record_stamp + _select_rotation_record (record-first: --record stamp|latest, deprecated --gen, session gate, latest) + _resolve_predecessor_transcript keyed on the selected record INDEX; both verbs default by record and print --record <stamp>. Pre-fix all three live posts refused (cannot default --gen); post-fix all three resolve on the committed records with the stamp named (TM e55ef12e via previous record 20260916T063950Z, SD d6231fa7, MS ae570747). 11 new tests on tmp_path copies of the genless and b_generation shapes; 189 passed.

PARENT-REVIEWED SL7.130 a00-1e495c92: read the diff (sensei.py +119/-39, 11 new tests) and ran 4 parent-run negative probes (record-keyed default on a mixed genless/gen-carrying tree; --record via argv; --gen refuse-by-name; live 3-post falsifier) — all HOLD. Verdict kept `proved`; no conjunct falsified. 141 sensei tests pass; rotate.py untouched; no other caller of the changed signatures.
