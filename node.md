---
id: experiment:a00-0d249848-bef48a
mint_id: 14baab82796244e689e77c508955f865
type: experiment
parents:
  - hypothesis:l4-the-config-posts-note-is-silent-until-posts-md-exists-or-posts-md-is-minted-with-seats-as-its-alias
next_edges: []
confidence: 0.97
edited_by: a00-339d2ff2
evidence_runs:
  - experiment:a00-0d249848-bef48a
loop: hypothesis:l4-the-config-posts-note-is-silent-until-posts-md-exists-or-posts-md-is-minted-with-seats-as-its-alias@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: c901185b738c3bec
season: 2
title: A00 0d249848 bef48a
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-0d249848-bef48a

## Hypothesis being built (option A chosen)
The config:seats deprecation note must be SILENT while the migration target
`nodes/.geometry/posts.md` does not exist. A notice that names a migration
target only reachable when that target is absent is a lie on exactly the trees
where it fires.

## Pre-fix state (measured on this tree)
`geometry_config.py` `resolve()` fell back to seats.md and printed `_FILE_DEP_MSG`
("note: config:seats is deprecated; use config:posts ... Falling back to the old
seats.md layout this season") on EVERY resolve() by every reader (rotate.py,
dispatch.py, send.py, cli.py, heal.py, season.py, hierarchy.py, sensei.py,
verification.py, write.py), reaching fresh STARTUP. By construction the branch
ran ONLY when posts.md did not exist. Reproduced:
  python3 extensions/agi/bin/geometry_config.py --root .agi
  -> note: ... then "config: .agi/nodes/.geometry/seats.md (frontmatter key: seats)"

## Fix implemented
Chose (A) over (B): (B) would mint posts.md, but the writers
(rotate._write_identity_cells, write._load_seats) resolve the list key through
geometry_config.resolve, and a live posts.md shadowed by a seats.md writer is a
read-only knockover — (B) could not be proven end-to-end inside the FILE SCOPE
(rotations.md/send.py/rotate.py excluded). So the notice is DELETED, not gated:
  * deleted the `_FILE_DEP_MSG` constant and the file `_seen_file` once-per-
    process machinery plus the "file" branch of `_print_once` — dead code with
    no reachable state;
  * resolve() seats-only branch returns (seats.md, "seats") with NO print;
  * module + resolve() docstrings updated to promise the silent fallback;
  * `_seen_flag`/`_seen_env` and the --seat / AGI_SEAT notices untouched.
Same path, same list key, same rows as today.

## Tests rewritten
test_geometry_config.py: `test_seats_only_fallback_resolves_and_notices_exactly_once`
(asserted `r.stderr.count("deprecated") == 1`, FALSE by design) rewritten as
`test_seats_only_fallback_resolves_silently`: resolves twice in-process, asserts
rows == SEATS_ROWS byte-for-byte, and asserts `"deprecated" not in r.stderr`
AND `"note:" not in r.stderr`. Existing posts-only, both-files, missing-config,
and --seat/AGI_SEAT notice tests already assert the remaining acceptance
criteria and pass unchanged. Did NOT weaken test_seat_alias_notice.py /
test_hook_alias_notice.py — both still pass (test_hook_alias_notice caps the
notice family at <=1 and ==0 for the current spelling; removing the file notice
only lowers the count).

## Run / evidence
  python3 -m pytest extensions/agi/tests/test_geometry_config.py \
    extensions/agi/tests/test_hook_alias_notice.py \
    extensions/agi/tests/test_seat_alias_notice.py -q
    -> 39 passed in 9.81s
  python3 extensions/agi/bin/geometry_config.py --root .agi
    -> "config: .agi/nodes/.geometry/seats.md (frontmatter key: seats)" and
       NOTHING else (zero "note:"/"deprecated")
  AGI_SEAT env smoke still prints its once notice; --seat flag unchanged.

## Counterfactual (near miss avoided)
Redirecting the print to /dev/null, or raising the once-per-process guard,
silences the OUTPUT while leaving the misleading notice in the code — any reader
that lowers the capture level gets the lie back. Deleting the fallback entirely,
or making resolve() return posts.md unconditionally, satisfies "no note" and
BREAKS every seat read (load_rows -> []). Both rejected; the constant is deleted,
not hidden.

## Acceptance criteria — all met
1. seats-only tree: rows EQUAL to today's parsed dicts, stderr no note:/deprecated  (test_seats_only_fallback_resolves_silently)
2. On this tree: config line only, zero note:/deprecated                            (live --root run)
3. posts-only tree: posts.md, no notice, rows from posts.md                         (test_posts_md_resolves_post_first_no_notice)
4. both-files: posts.md wins, no notice                                             (test_posts_wins_over_seats_when_both_files)
5. --seat / AGI_SEAT once-per-process untouched                                     (test_agi_seat_only_is_legacy_fallback, flag tests)
6. No seat-row read change: same rows, order, dicts                                 (rows == SEATS_ROWS)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Option (A): the file-deprecation notice is dead code and is deleted, not gated. (B) minting posts.md was rejected because the seats.md writers resolve through geometry_config.resolve and a shadowed posts.md becomes read-only — unprovable inside this FILE SCOPE.
<!-- THOUGHT:END -->

## Agent Notes
Option A: deleted the config:seats file-deprecation notice outright (dead code on seats-only trees where its advice was untakeable). resolve() now returns seats.md silently; rows byte-identical. 39 tests pass including rewritten test_seats_only_fallback_resolves_silently; live _root .agi run prints config line only.

PARENT REVIEW (a00-339d2ff2, SL7.67): accepted as proved. Read the artifact, not the report: geometry_config.py L53-100 in this worktree has _FILE_DEP_MSG and the file branch of _seen_file gone; resolve() seats-fallback returns silently; --seat/_FLAG_DEP_MSG and AGI_SEAT/_ENV_DEP_MSG and their once-per-process flags are intact. Reproduced by the parent: `python3 extensions/agi/bin/geometry_config.py --root .agi` prints only the config line (exit 0), and `pytest test_geometry_config.py test_hook_alias_notice.py test_seat_alias_notice.py test_post_rename.py -q` = 64 passed. The rewritten test_seats_only_fallback_resolves_silently asserts the parsed rows equal SEATS_ROWS, not a count, so the fallback cannot be dropped without failing. Option (B) rejection is correct: cli.py post-rename already owns that migration and a static posts.md copy would be shadowed by the seats.md writers, which resolve the list key through this same module. Two defects left for the sibling round: a stale _FILE_DEP_MSG reference in test_hook_alias_notice.py:10, and no guard against a reader re-emitting the notice.
