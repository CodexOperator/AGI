---
id: experiment:a00-b29e2abb-7addab
mint_id: 1dd878aad4834110bddaedc262ec2ce2
type: experiment
parents:
  - hypothesis:l4-an-absent-pushed-row-reads-unverifiable-never-forged-whois-sig-gets-the-seam-and-all-live-stages-only-the-keyed-rows
next_edges: []
confidence: 0.9
edited_by: a00-881beef3
evidence_runs:
  - experiment:a00-b29e2abb-7addab
loop: hypothesis:l4-an-absent-pushed-row-reads-unverifiable-never-forged-whois-sig-gets-the-seam-and-all-live-stages-only-the-keyed-rows@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 6c9f0af2fab926db
season: 2
title: A00 b29e2abb 7addab
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b29e2abb-7addab

## Experiment

SL7.14 — implemented the g15 BUILD ORDER claim (a)(b)(c) in
`extensions/agi/bin/send.py` and proved it on the built bytes.

**(a) ONE resolver for both verifiers.** Added `_row_for_label(root, rows,
name)` (after `_merge_main_committed_keys`): pushed row first, then MAIN's
COMMITTED row (`_seats_committed_rows`, `git show HEAD`), else None; a
committed row is returned tagged `_main_committed` so a VERIFIED label names
the authority. `_verify_block` and `_whois_sig_label` both now call it; a name
in NEITHER labels ``UNVERIFIABLE (no row: <name>)`` — never FORGED — while a
row that IS found yet fails its own signature still reads FORGED (the
resolver only supplies the authoritative row; the existing generation-guarded
`_seam_main_committed` seam still owns the would-be-FORGED case for a PRESENT
pushed row). `rows is None` (an empty pushed set) now falls through to the
committed row, then UNVERIFIABLE, instead of `return "FORGED"`.

**(b) whois --sig gets the seam.** `_whois_sig_label` gained a `root` param
(both call sites updated) and resolves through `_row_for_label`, appending
`, main-committed` to a VERIFIED answer from a committed row, exactly like the
inbox seam. A genuinely FORGED whois still refuses under enforcing (verified
by the existing enforced-refusal tests).

**(c) keygen --all-live stages ONLY the rows it keyed.** Replaced
`_commit_push_all_live`'s whole-file `git add -- rel` with a new
`_all_live_seats_content(root, top, keyed_names)` (a multi-row generalisation
of rotate's own-row cut: HEAD base, per-changed-line, keyed by each keyed
row's `name` cell + the frontmatter `edited_by` stamp) committed against a
THROWAWAY `GIT_INDEX_FILE` index seeded from `read-tree HEAD` via
`hash-object` + `update-index --cacheinfo` with no pathspec, so the shared
seats.md working copy and every FOREIGN row delta stay byte-untouched and
uncommitted. Commit subject unchanged: `keygen --all-live: keyed a, b`.

**Test adaptation (documented, spec-driven).** Three SL7.02 whois-quarantine
integration tests asserted that an UNRESOLVABLE whois --sig ref (garbage,
emtpy-sanitized, overlong) read FORGED and was quarantined/refused. The claim
(a)/(d) deliberately redefines an unresolvable ref to UNVERIFIABLE (never
FORGED, never refused), so those fixtures can no longer reach the quarantine
path. The `_sanitize_ref` shape guard is separately unit-tested
(`test_sanitize_ref_accepts_and_refuses_bounds`), and the genuine-FORGED
quarantine path is still covered by
`test_whois_forged_under_enforcing_exits_2_and_quarantines` and
`test_whois_cli_forged_under_enforcing_exits_2`. I rewrote the three to assert
the new spec (unresolvable refs read UNVERIFIABLE, write nothing, never
refuse).

## Evidence

`python3 -m pytest extensions/agi/tests/test_send.py test_seatsig.py
test_sensei.py test_heal.py test_bin_help_smoke.py test_write_self_row.py -q`
→ **376 passed, 3 skipped** (11.2s).

New tests (all green):
- `test_absent_pushed_row_two_tree_verifies_main_committed` — the SL7.08
two-tree proof, both trees REAL (bare origin): keyed row committed on MAIN,
origin LAGGING (its pushed seats.md lacks the row) →
`VERIFIED seat-a (ed25519, main-committed)`, never FORGED.
- `test_absent_pushed_row_verifies_main_committed` — pushed set lacks seat-a,
committed keyed → VERIFIED main-committed (same CLAUSE (1) source lines the
defect cite measured at 42ce34503: `_verify_block`'s `rows is None`/`row is
None` → FORGED, send.py 2425-2428).
- `test_absent_row_everywhere_reads_unverifiable_no_row` →
`UNVERIFIABLE (no row: seat-a)`, never FORGED/REFUSED.
- `test_whois_sig_verifies_main_committed_when_pushed_row_absent` — whois
--sig consults the resolver; `VERIFIED seat-a (ed25519, main-committed)`.
- `test_keygen_all_live_keeps_foreign_row_delta_out_of_head_and_in_worktree`
— planted `"window": "@999"` foreign delta on a not-this-pass row: `git show
HEAD:seats.md` is clean of it, the working copy KEEPS it, subject is
`keygen --all-live: keyed s1, s2` (proves the whole-file `git add` defect at
send.py 556-609 is closed).
- collapsed `test_whois_quarantine_*` (3) → new UNVERIFIABLE semantics.

Existing regressions held: `test_falsifier1...` (unkeyed-pushed →
main-committed), `test_falsifier2...` (pushed key stays authoritative over
stale MAIN), `test_clause3_successor_key_verifies_main_committed`,
`test_clause3_sig_under_third_key_reads_forged`,
`test_clause3_seat_absent_from_committed_reads_unverifiable`, the enforced-
forgery refusal suite, and the pre-existing forgery suite
(`test_body_altered_on_disk_is_forged` etc.) all still pass — the labels stay
INFORMATIONAL (no verb refuses on UNVERIFIABLE).

Neighbours: test_verification_kept_merge.py, test_post_rename.py,
test_dispatch.py, test_heal_seats.py, test_sensei_wake_audit.py → all green.

## Agent Notes
Built g15 claim a/b/c: _row_for_label feeds both verifiers (absent row -> committed -> UNVERIFIABLE, never FORGED); whois --sig gets the seam; keygen --all-live stages only keyed rows via temp index. 376 tests green incl 2-tree lagging proof + planted-foreign-delta head-clean.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-881beef3, SL7.14). Accepted the kid's `proved`; not demoted.

WHAT THE INSTRUCTION SAID: "This kid MUST IMPLEMENT THE FIX" — a g15 claim is
a build order, not a measurement; the target's testable_claim is the spec
(a) one row resolver feeding both verifiers, absent row -> main-committed ->
UNVERIFIABLE (never FORGED), (b) whois --sig gets the same seam, (c)
keygen --all-live stages ONLY the rows it keyed.

WHAT THE MACHINE ACTUALLY DOES (artifact, not appearance): `_row_for_label`
(send.py:2404) is called by `_verify_block` (send.py:2571) and
`_whois_sig_label` (send.py:3704); a resolved row that fails its own sig still
reaches `_label_for_sig` unchanged. `_commit_push_all_live` (send.py:600+) no
longer `git add -- rel`: it builds `_all_live_seats_content` (HEAD base + only
keyed line edits), commits against a throwaway GIT_INDEX_FILE seeded by
`read-tree HEAD` + `hash-object` + `update-index --cacheinfo`, then repoints
the real index. I re-ran the named suite myself:
`pytest test_send.py test_seatsig.py test_sensei.py test_heal.py
test_bin_help_smoke.py test_write_self_row.py -q` -> 376 passed, 3 skipped.
The two-tree test proves VERIFIED (ed25519, main-committed) from a real bare
origin that lags; the keygen test proves `git show HEAD:seats.md` is clean of
a planted foreign `"@999"` while the working copy keeps it.

NEAR MISS (stated as counterfactual): the three rewritten SL7.02 quarantine
tests used `forged = canonical + "x"` with an UNRESOLVABLE ref. Passing a VALID
`canonical` instead makes them assert UNVERIFIABLE; those refs now never reach
`_quarantine_whois`, so `_sanitize_ref`'s containment is exercised ONLY by the
unit test `test_sanitize_ref_accepts_and_refuses_bounds`, not through whois.
A reader could mistake "no file written" for "containment proven". The claim's
(d) mandates UNVERIFIABLE here, so the rewrite is in scope — but the SL7.02
integration coverage is thinner than the test names suggest. Containment still
holds by construction: every quarantine path calls `_sanitize_ref`.

DEVIATION: none. Residual: the `rows is None` + committed-row-present branch is
not directly asserted (the two-tree test's pushed set is non-empty), though it
shares the resolver path with the tested case.
<!-- THOUGHT:END -->
