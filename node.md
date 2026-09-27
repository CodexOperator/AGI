---
id: hypothesis:one-mint-route-answers-file-validated-row-by-row
mint_id: 0b847b08000f419ab87e1594f21c1f41
type: hypothesis
parents:
  - goal:g4.18.1.1
next_edges: []
confidence: 0.7
edited_by: director-engine
scaffold_hash: 1d5d4a7e5db1cdc4
season: 2
tags:
  - engine
  - write
  - mint
testable_claim: "(1) write.py create --answers <file> mints a node from ONE answers file with no field value passing through a shell-quoted argv (2) every row is checked by ONE row validator built on _schema_field_refusal, and a missing REQUIRED row or a bad row refuses naming the row and the rule and writes nothing (3) actor, role, town, season and thought_session are stamped from the calling post config:posts row when the file does not set them (assigned: director-engine)"
title: "one mint route (1): write.py create --answers <file> -- every row checked by ONE validator, required rows refused by name, the caller stamped from config:posts"
town: core
---
# hypothesis:one-mint-route-answers-file-validated-row-by-row

# hypothesis:one-mint-route-answers-file-validated-row-by-row

## Measured
- `write.py create` (extensions/agi/bin/write.py:2866) takes every field as a shell argv: `--set k=v` pairs parsed at :3046, the body from `--body-file` at :3088. A value with an apostrophe, a backtick or `$(` must be shell-escaped by the model; the predecessor dropped an owner quote's apostrophes to get it through (goal:g4.18.1 Evidence).
- Field checks run once, on the finished dict: `_enforce_create_schema_gate` (write.py:1860) over `set_fm`, with the per-field rule in `_schema_field_refusal` (write.py:1800). Required fields that are absent are only a SCHEMA-WARNING at scaffold: director-engine minted goal:g4.18.1.1-.5 at 02:1xZ 09-27 and all five printed "scaffolded without confidence, origin, seeds, tags" and were written anyway; `snapshot-goals.py --render` then refused on a missing heading_level.
- actor / role / seat are resolved from flags and config rows (`_resolve_role` write.py:767, `_resolve_seat` :811), but town, season and thought_session are not stamped at create: the five leaves above carry none of them.

## CLAIM
(1) `write.py create --answers <file>` mints a node from ONE answers file (type, slug, parents, every frontmatter row, body, optional payload) with no field value passing through a shell-quoted argv; (2) every row is checked by ONE row validator built on `_schema_field_refusal` (never a second copy of a schema rule), and a missing REQUIRED row or a bad row refuses naming the row and the rule and writes nothing; (3) actor, role, town, season and thought_session are stamped from the calling post's config:posts row when the file does not set them.

## Dispatch line
config-max: none new -- the rows and their rules already live in `.agi/context/schemas/[<type>].md`; the stamp sources already live in `config:posts` / `config:ladder`. template-max: none in this round (the role templates that teach `create` change via the master once this lands, goal:g4.18.1 refinement (e)). code: the answers-file reader + the one row validator + the caller stamp -- the resolver that does not exist.

## FALSIFIERS
- An answers file whose body quotes a line with an apostrophe, a backtick and `$(` does not round-trip byte-identically (`write.py <id> 'read body 1:N'`).
- An answers file missing one required row (e.g. a goal without `origin`) mints anyway, or mints with a warning.
- A bad row (e.g. `goal_kind: sometimes`) refuses without naming the row, or leaves a file on disk.
- A second schema-rule table appears in the new code (grep: a required-field list or a regex literal copied from a schema).

## TESTS
New: `extensions/agi/tests/test_write_answers_file.py` -- round-trip (quote/backtick/dollar-paren body), missing required row refused by name + no file, bad regex row refused by name + no file, stamp rows filled from a temp config:posts row, `--set`/`--body-file` path unchanged. Neighbourhood: `test_write*.py test_spawn_gate*.py test_bin_help_smoke.py`. Every test runs against a temp graph under tmp_path, never the live `.agi/nodes`.

## FILE SCOPE
extensions/agi/bin/write.py · extensions/agi/tests/test_write_answers_file.py (new). Nothing else.

## CEILING
2 kids · <= 36 production lines · pi-free tier-0 · 0 USD. No test spawns pytest; kids never launch real claude; no test writes the live graph.

## CORRECTIVE DH.521 -- closes mur-director-engine-17 DH.502-k1 (verify: DEMOTE)
BASE      CUT FROM season2/loops/hypothesis-one-mint-route-answer-a00-06858031 tip 5d92fc78d (worktree de-m502). No merge. Never rebase.
1. write.py:3200 -- the rank-1 post_rows re-stamp runs after node_writer's env stamp and never passes _ceiling_refusal (write.py:749): `--answers f --set role=owner` on a parent seat writes role=owner -> every re-stamped role goes through _ceiling_refusal; one test: a parent seat asking role=owner via --answers is refused by name.
2. write.py:3159 -- `list(answers.get("parents"))` char-splits a JSON string and raises TypeError on 5/true/an object -> _read_answers_file type-checks parents (a list of str ids) and refuses by name with exit 2; tests for the string and the non-iterable case.
3. write.py:1866 _ANSWERS_IDENTITY hardcodes the minted-key set node_writer.write_node builds (node_writer.py:758-768) -> derive it from node_writer's one definition (expose a tuple there if none exists).
4. experiment:a00-9086ec16-e5b481 misquotes numstat ('45 3'; the range a6d513eb7..tip is 42/3) -> RE-RUN, paste, fix production_lines.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_write_answers_file.py + test_write*.py neighbourhood + test_bin_help_smoke.py once (timeout 600, --basetemp under /tmp)
FILE SCOPE extensions/agi/bin/write.py (the answers route only) · extensions/agi/bin/node_writer.py (one exposed tuple) · extensions/agi/tests/test_write_answers_file.py · experiment:a00-9086ec16-e5b481 (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · net <= 12 production lines · <= 60 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.521: mur-17 DH.502-k1 DEMOTE -- the rank-1 role re-stamp bypasses the seat ceiling (write.py:3200, confirmed by verify), parents char-split / TypeError, a second copy of the minted-key set, a misquoted numstat. Refuted and dropped: the argv precedence wording, the pre-existing SystemExit.
<!-- THOUGHT:END -->
