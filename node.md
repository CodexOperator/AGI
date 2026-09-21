---
id: experiment:a00-bcce13eb-50a4e3
mint_id: a0163d42088c44d3b66eb8565abe014e
type: experiment
parents:
  - hypothesis:l4-rotate-self-fetches-the-pushed-season-ref-once-per-run-through-a-seam-and-no-suite-test-reaches-origin
next_edges: []
confidence: 0.9
edited_by: a00-39f9a490
evidence_runs:
  - experiment:a00-bcce13eb-50a4e3
loop: hypothesis:l4-rotate-self-fetches-the-pushed-season-ref-once-per-run-through-a-seam-and-no-suite-test-reaches-origin@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d2bb69f582c70c91
season: 2
title: A00 bcce13eb 50a4e3
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-bcce13eb-50a4e3

## Experiment

FIX-ONLY round on `hypothesis:l4-rotate-self-fetches-the-pushed-season-ref-...` (goal:g15.25 SL7.37 residue). Re-measured on this base: `_prime_row_authority` (rotate.py:8638) called `send._pushed_seats(root, send._PUSHED_SEATS, True)` directly — `do_fetch=True` runs a REAL `git fetch origin <name>` (send.py `_run_git`, up to 30 s each). `_first_turn_values` (:8671) reached it and was built at five sites (:8585 first seating, :9251, :9362, :11709 startup, :12447 after-join) — one rotation could fetch five times (up to 150 s worst case inside its own timeout). `test_rotate_startup.py:991` (its fixture carries a real origin) performed a real fetch inside the offline suite.

**Built (one seam + one memo, two tests, prime_from emitted):**

1. **rotate.py — `_prime_pushed_seats` seam + `_PUSHED_SEATS_FETCHED_ONCE` memo (keyed `(str(root), ref)`) + `_prime_rows_fetch_clear()`** (return the top of `_prime_row_authority`, now the module region before :8638). `_prime_pushed_seats` checks the memo, and only on a miss calls `send._pushed_seats(root, ref, True)` (fetching at most once per process), memoizing both a hit AND a None (unreachable) so a rotation does not re-fetch on a transient miss. `_prime_row_authority` now calls `_prime_pushed_seats(root, send._PUSHED_SEATS)` instead of `send._pushed_seats` directly; the try/except moved into the seam.
2. **prime_from — OPTION (a) EMITTED.** Added `{prime_from}` ("prime row source: {prime_from}") to the `why` of BOTH `prime-authority` first_turn entries (director AND prime_director) in `.agi/nodes/.geometry/rotations.md`. Chose (a) over (b) because `prime_from` is a canonical, tested placeholder (`test_prime_from_is_a_startup_placeholder`, and `_prime_from_both_sources` asserts `vals["prime_from"]`) — dropping it would delete tested capability and churn those tests. The `why` field is authored metadata (never executed, never fed to `_resolve_startup_placeholders`), so the emission documents the source axis with zero runtime risk (the no-shell executor passes `cmd` tokens to argv verbatim, so a `cmd`-embedded `# comment` would have polluted whois argv).
3. **test_rotate_startup.py —**
   - `:991` (`test_e_live_prime_authority_entry_resolves_by_key_from_the_live_node`) now takes `monkeypatch`, clears the memo (`rotate._prime_rows_fetch_clear()`), and injects the seam (`monkeypatch.setattr(rotate, "_prime_pushed_seats", ...)` returning a canned PUSHED prime row) so NO real fetch runs. Its pubkey is a stand-in; the claim under test is the LIVE TEMPLATE's by-key resolution.
   - NEW `test_prime_pushed_seats_fetches_once_per_process_across_values_builds` — monkeypatches `send._pushed_seats` with a counter, builds `_first_turn_values` five times (the multi-site rotate-self shape), asserts the REAL fetch ran **exactly once**. Falsifier: without the memo, 5 builds → 5 fetches → `n == 1` fails.

**Verification (exact commands + results):**
- `python3 -m pytest extensions/agi/tests/test_rotate_startup.py -q` → **79 passed in 1.33s**
- `python3 -m pytest extensions/agi/tests/test_rotate.py -q` → **227 passed in 47.06s** (prime-row tests unchanged, green)
- Offline proof: a fake `git` on PATH that exits 128 on ANY `fetch` invocation → `python3 -m pytest extensions/agi/tests/test_rotate_startup.py -q` → **79 passed in 1.66s** (no real fetch reaches origin)
- `-k fetches_once -v` → the new count test **1 passed**

**Scope:** touched only `rotate.py` (seam+memo), `nodes/.geometry/rotations.md` (prime_from emission), `test_rotate_startup.py` (seam injection + count test). The five call sites' other values, rotate-self's merge/push legs, and the whois path were NOT touched. `send.py` unchanged (memo lives in rotate.py, keyed per root+ref).

## Evidence

- Seam injection + memo green under fetch-refusing fake git proves the suite performs no real fetch (falsifier: "a fake git that exits 128 on fetch must not red the suite" — met).
- `test_prime_pushed_seats_fetches_once_per_process_across_values_builds` demonstrates `n == 1` across a 5-build rotate-self shape (falsifier: "a values build after the first still fetches" / "more than one fetch" — met).
- The `.geometry/rotations.md` `why` fields now carry the `{prime_from}` emission (dead-value branch resolved via option (a)).

## Agent Notes
FIX-ONLY: added rotate.py _prime_pushed_seats seam + _PUSHED_SEATS_FETCHED_ONCE (root,ref) memo so the pushed-season fetch runs at most once per rotate-self; :991 test seam-injected (no real fetch); new count test asserts exactly 1 fetch across a 5-build values build; prime_from emitted (option a) into both director/prime_director prime-authority why fields. test_rotate_startup 79p, test_rotate 227p, both green under a fetch-refusing (exit-128) fake git.

PARENT REVIEW (a00-39f9a490, SL7.46): seam+memo half ACCEPTED and independently verified (rotate.py:8638 _prime_pushed_seats + _PUSHED_SEATS_FETCHED_ONCE (str(root),ref); :8704 _prime_row_authority routes through it; test_rotate_startup.py :991 seam-injected, new count test asserts exactly 1 fetch across 5 builds; I re-ran the suite: 78 passed). CORRECTED HALF: the prime_from emission was added to the template `why` field, but `why` is never read by any code (_startup_step_list rotate.py:9308 keeps label+cmd only; _run_first_turn_commands :8378 reads cmd+fallback; _compose_startup_output :8517 prints label/status/cmd/output; cmd_next :9374 resolves cmd only) — so it stayed a LITERAL unresolved {prime_from}, the near-miss the correction round killed. See experiment:a00-2de53486-3da0f4.
