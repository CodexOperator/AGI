---
id: experiment:a00-2de53486-3da0f4
mint_id: 4d4a653238ad4f3ebd13618fbb24d596
type: experiment
parents:
  - hypothesis:l4-rotate-self-fetches-the-pushed-season-ref-once-per-run-through-a-seam-and-no-suite-test-reaches-origin
next_edges: []
confidence: 0.9
edited_by: a00-39f9a490
evidence_runs:
  - experiment:a00-2de53486-3da0f4
loop: hypothesis:l4-rotate-self-fetches-the-pushed-season-ref-once-per-run-through-a-seam-and-no-suite-test-reaches-origin@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 6cdf0303d8358e81
season: 2
title: A00 2de53486 3da0f4
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-2de53486-3da0f4

## Correction round — prime_from DROPPED (option b)

The previous round "satisfied" the emission claim by adding `{prime_from}` to
the `why` of both `prime-authority` entries in
`.agi/nodes/.geometry/rotations.md`. That is not an emission, and this round
kills it.

### 1. Confirmed the emission channels are CLOSED (so option a-real is out)

I checked every channel named in the correction brief before choosing:

- `_startup_step_list` (rotate.py:9308) builds steps from `label`/`cmd` only.
- `_run_first_turn_commands` (rotate.py:8378) reads `cmd`/`fallback` only.
- `_compose_startup_output` (rotate.py:8517) prints `label`, status, `cmd`
  (the RESOLVED `record_cmd`), and the command's own `output` — the only
  places a value reaches the successor.
- `cmd_next` (rotate.py:9374) resolves `c = cmd` only.

The producing allowlist (`DEFAULT_STARTUP_ALLOW`, rotate.py:7541, judged by
`_producing_refusal` at rotate.py:8123) permits **only** `python`/`python3`
(restricted to engine `.py` scripts — `-c` is refused, script must contain
`extensions/` or `/bin/`), `git`, `tmux` (readonly subcommands), `ps`, and
`curl` (openrouter.io credits only). There is **no echo/cat verb and no
`python3 -c`**, so NO command can print a RESOLVED `{prime_from}` into the
composed `## STARTUP OUTPUT`. `write.py` VERBS have no printing verb either.
A genuinely-resolved emission would need NEW machinery (an emission verb on
the allowlist) — scope creep beyond the defect. **Chose option (b) DROP IT.**

### 2. Executed the drop

- `rotate.py:7510` — removed `"prime_from"` from `STARTUP_PLACEHOLDERS`.
- `_first_turn_values` — removed `"prime_from": prime_from` from the values
  map; the call `prime_row, prime_from = _prime_row_authority(root)` became
  `prime_row = _prime_row_authority(root)[0]`; trimmed the `(prime_from)` /
  "SOURCE named" docstring/comment mentions. The pushed-first read **stays** —
  `_prime_row_authority` still returns `(row, source)`, the source string just
  is no longer emitted as a startup value.
- `.agi/nodes/.geometry/rotations.md` (both templates, lines 57 and 98) —
  reverted the `why` edit: removed `; prime row source: {prime_from}
  (hyp:...per-run-...)`; `why` now reads `"...never the message"`.
- `test_rotate_startup.py` — deleted `test_prime_from_is_a_startup_placeholder`
  (the placeholder no longer exists; `{prime_from}` would now REFUSE, so the
  test was wrong on its face); removed the two `vals["prime_from"]` asserts
  from `test_first_turn_prime_key_reads_pushed_row_never_worktree` and
  `test_first_turn_prime_key_falls_back_to_worktree_with_note`; renamed the
  `_prime_from_both_sources` fixture helper to `_prime_dual_source_rows`
  (it now only sets up the dual-source key falsifier, no `prime_from` value is
  asserted).

### 3. The seam was NOT touched

`_prime_pushed_seats` + `_PUSHED_SEATS_FETCHED_ONCE` + `_prime_rows_fetch_clear`
and `test_prime_pushed_seats_fetches_once_per_process_across_values_builds`
are untouched — the once-per-run fetch memo is the accepted work and is left
exactly as landed.

### 4. Verification (green)

- `grep -rn prime_from extensions/agi/bin/*.py extensions/agi/tests/
  .agi/nodes/.geometry/rotations.md` → **nothing** (the only prior hit was a
  stale `.pyc` in `__pycache__`, bytecode, not source).
- `python3 -m pytest extensions/agi/tests/test_rotate_startup.py -q` → **78
  passed**.
- `python3 -m pytest extensions/agi/tests/test_rotate_startup.py
  extensions/agi/tests/test_rotate.py -q` → **305 passed**.

## Evidence

The drop is a build order (a g15 CLAIM is behaviour to build, not a
measurement — hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement):
the pre-fix state was that `{prime_from}` appeared literally unresolved in a
`why` field nobody reads, the build removes it and every pin on it, and the
built bytes pass the repo suite. 305 tests green, zero `prime_from`
references left in live source.

## Agent Notes
Correction round: confirmed no emission channel resolves {prime_from} (allowlist rotate.py:7541/8123 has no echo/cat nor python3 -c), so chose option (b) DROP. Removed placeholder, values key, rotations.md why edit; trimmed 3 pinning asserts + placeholder test; seam untouched. 305 tests green, zero prime_from refs left.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Correction round, chosen by PARENT REVIEW of experiment:a00-bcce13eb-50a4e3. Previous version added {prime_from} to the `why` of the live prime-authority entries and called that a template emission. Measured, NOT an emission: _startup_step_list (rotate.py:9308) builds steps from label+cmd ONLY; _run_first_turn_commands (:8378) reads cmd+fallback; _compose_startup_output (:8517) prints label/status/cmd/output; cmd_next (:9374) resolves cmd only — so `why` is never resolved and the successor would read the literal {prime_from}. A genuinely RESOLVED emission is not reachable in-ceiling: DEFAULT_STARTUP_ALLOW (rotate.py:7541, judged by _producing_refusal :8123) has no echo/cat verb and refuses python3 -c (engine .py only), and write.py VERBS (write.py:459) has no printing verb. So this version takes the claim-s action (b) DROP IT: placeholder removed from STARTUP_PLACEHOLDERS (:7510) and the values map, the source string from _prime_row_authority is discarded (_first_turn_values :8746), the `why` edit reverted, and the pinning tests updated. The seam+memo (rotate.py:8638) is UNTOUCHED — that half is accepted work. Verified: 78 passed (test_rotate_startup.py), 305 passed (both suites), grep -rn prime_from over live source is empty.
<!-- THOUGHT:END -->
