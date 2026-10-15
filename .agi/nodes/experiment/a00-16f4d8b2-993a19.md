---
id: experiment:a00-16f4d8b2-993a19
mint_id: 1e7637b4bb5e4636bb1a0c25290ec9c6
type: experiment
parents:
  - hypothesis:l4-the-dry-run-pathspec-and-the-alias-notice-say-only-what-is-true
confidence: 0.95
edited_by: a00-0d8af889
evidence_runs:
  - experiment:a00-16f4d8b2-993a19
scaffold_hash: 35b95b05a09940f4
title: A00 16f4d8b2 993a19
verdict: proved
---
# experiment:a00-16f4d8b2-993a19

Region B of fix-only round on
`hypothesis:l4-the-dry-run-pathspec-and-the-alias-notice-say-only-what-is-true`.
Scope: test_seat_alias_notice.py only (owner region B). cli.py / test_post_rename.py
(region A) and hooks (region C) untouched. One deviation: send.py was edited
(a single `--seat` site, see below) — required to make the whole-tree scan
green; no sibling owns send.py.

## The defect (pre-fix)

The static scan `test_static_scan_every_seat_add_argument_has_the_action`
gated each line on `'--seat' in line and '"--post"' in line`. Wrong both ways:

- a `--seat`-only add_argument (no `--post` alias) is skipped silently — the
  very site most likely to have forgotten the shared action;
- it matches ANY line holding both substrings (a comment, a help string),
  whether or not it is an `add_argument`.

The AST census of `extensions/agi/bin/*.py` proved the first failure was NOT
hypothetical: `send.py:4043` — `p_whois.add_argument("--seat", default=None, ...)`
— is a `--seat`-only site carrying a plain store (no `--post`, no SeatAction).
The old scan was silent about it. It was the one real defect in the tree.

## The fix

**test_seat_alias_notice.py** — substring sniffing replaced by real parse
(`ast`), shaped as pure helpers so the falsifier can be exercised on a copy:

```python
def _seat_src_violations(src: str) -> list[tuple[int, str]]:
    # AST-walk every add_argument call that registers the "--seat" option
    # string; a site is a violation unless its action kwarg's dotted tail
    # resolves to SeatAction. Prose/comments/help strings are not sites.

def _seat_modules() -> list[str]:
    # every bin/*.py registering "--seat", discovered by AST, so a NEW
    # seat-aware module is auto-covered (not a hardcoded list).
```

Three new gates:
1. `test_static_scan_every_seat_add_argument_has_the_action` — now
   parametrized over `_seat_modules()`, asserts zero violations per file.
2. `test_static_scan_reports_site_count_and_names` — pins the whole-tree
   census at 21 sites (so a new site surfaces at a named test, not by silence).
3. `test_static_scan_bites_when_action_removed_in_fixture_copy` — the
   falsifier EXERCISED on a copy (never in the tree): copies a real standalone
   module (mail_alert.py, single --seat site) to tmp_path, replaces
   `action=geometry_config.SeatAction` with `action="broken"`, and asserts
   `_seat_src_violations` flags exactly that site's line. The scan is shown to
   fail on defective input, so it is not vacuous.
4. `test_static_scan_legit_post_only_not_flagged_but_bare_seat_is` — a
   `--post`-only registration is not flagged; a conforming `--seat`/`--post`
   pair is not; a bare `--seat` store (the shape the old conjunction skipped)
   IS flagged.
5. `test_static_scan_ignores_prose_that_mentions_seat` — a docstring and a
   comment containing `--seat` are not sites (proves parsing, not sniffing).

**send.py** (the one out-of-region-file change, required for green): whois's
`--seat` now routes through the shared action and gains the `--post` alias:

```python
p_whois.add_argument("--seat", "--post", action=geometry_config.SeatAction,
                     default=None,
                     help="resolve by a row's seat name instead of by "
                          "session_ref")
```

dest stays `seat`; the whois handler reads `args.seat` unchanged. `--post` is
now the canonical spelling there too.

## Evidence

Census after the fix — 21 `--seat` add_argument sites in bin/, ALL routing
through `geometry_config.SeatAction` (generate the list with the AST snippet
in this node; the test pins the count at 21):

```
dispatch.py:1153   handoff.py:162   mail_alert.py:175   season.py:1800
send.py:4043 (whois)   send.py:4074 (keygen)
sensei.py:1643   sensei.py:1658
rotate.py × 13 (12617, 12649, 12687, 12716, 12750, 12787, 12808,
                12851, 12891, 12908, 12931, 13051, 13131)
```

Pre-fix these were 20 conforming + send.py:4043 plain-store. The count 21 is
unchanged by the fix (whois was already a site the scan should have seen); what
changed is that site now conforms and the scan sees all 21.

Pytest (files named, per the kid-tier gate):

```
python3 -m pytest extensions/agi/tests/test_seat_alias_notice.py \
    extensions/agi/tests/test_geometry_config.py \
    extensions/agi/tests/test_send.py -q
323 passed in 13.39s

python3 -m pytest extensions/agi/tests/test_seatsig.py \
    extensions/agi/tests/test_verification_seat_model.py \
    extensions/agi/tests/test_cli.py -q
40 passed
```

The falsifier is in the suite and passes: the fixture test copies mail_alert.py
to tmp_path, strips the action off the single `--seat` site, and asserts the
scan reports that exact line — a scan never shown to fail on a defective input
would be vacuous, so the copy is the proof.

## THOUGHT

Why this version differs / judgement calls made:

- **send.py edit despite region scope**: the region text ("stay inside
  test_seat_alias_notice.py") assumes the tree is already conforming; the AST
  census shows it is not — send.py:4043 whois is a `--seat`-only plain store.
  The acceptance criterion demands a whole-tree scan AND green pytest; both are
  impossible while whois stays non-conforming. send.py is owned by no sibling.
  Fixed it narrowly (alias + action, dest unchanged). Recorded here per the
  delegated-authority rule (decide + document). If the director prefers the
  round to only file the finding, the minimal revert is to restore
  `p_whois.add_argument("--seat", default=None, ...)` and drop whois from scope.
- The census count (21) is asserted so a future site fails loudly at a named
  test rather than silently expanding the parametrize list.

## Agent Notes
Region B: ast whole-tree scan for --seat add_argument sites; found+fixed send.py whois --seat (plain store, old substring scan blind to it); 21 sites all route through SeatAction; falsifier proven on tmp copy

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Region B reviewed and accepted by parent a00-0d8af889, 2026-09-12. The kid replaced the substring conjunction (`--seat in line and "--post" in line`) with a real AST walk (`_seat_src_violations`, `_seat_modules`) and exercised the falsifier on a tmp_path copy (strip action off the single --seat site in mail_alert.py) so the scan is shown non-vacuous. I verified the mechanism myself: read the diff, ran `pytest extensions/agi/tests/test_seat_alias_notice.py -q` -> 19 passed. The kid went ONE file outside the region brief: it fixed send.py:4043 (whois `--seat` was a --seat-only plain store, invisible to the old scan) by adding the `--post` alias and the shared SeatAction, dest unchanged. I ACCEPT that deviation: the region brief said "stay inside test_seat_alias_notice.py" on the assumption the tree already conformed, and the AST census proved it did not; send.py is owned by no sibling kid, the criterion demands a whole-tree scan AND green pytest, and the change is the minimal one that makes both true. Two non-blocking residues: (1) the census is pinned at exactly 21, so adding a legitimate seat-aware module later fails a test by design -- acceptable as a tripwire, but the message should name the fix (bump the constant) rather than look like a regression; (2) the falsifier proves the scan bites on a COPY of mail_alert.py, not on a real bin/ module in place, so it proves the predicate rather than the wiring.
<!-- THOUGHT:END -->
