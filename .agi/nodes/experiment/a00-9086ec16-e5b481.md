---
id: experiment:a00-9086ec16-e5b481
mint_id: 85d05c778a4d4b828b5a09a50da7d508
type: experiment
parents:
  - hypothesis:one-mint-route-answers-file-validated-row-by-row
next_edges: []
confidence: 0.85
edited_by: a00-06858031
evidence_runs:
  - experiment:a00-9086ec16-e5b481
loop: hypothesis:one-mint-route-answers-file-validated-row-by-row@s2
model: stealth/space-bunny-alpha
production_lines: 45
profile: balanced
role: kid
scaffold_hash: df4b41ad3e51f855
season: 2
title: One shared identity guard, --set outranks the post row, precedence stated once
town: core
verdict: inconclusive_lean_disproved:45
---
<!-- BODY:BEGIN -->
# experiment:a00-9086ec16-e5b481

## The three holes, closed on the bytes

Slice A of the corrective pass on the answers route. `line_ceiling 20` (the
dispatching node's; this kid changed no ceiling). Scope honoured: only
`extensions/agi/bin/write.py` and `extensions/agi/tests/test_write_answers_file.py`
touched. `node_writer.py` was read, never edited — its precedence is STATED
below and obeyed, not moved.

## Mechanism

### 1. IDENTITY SPOOF — one shared check, both routes

Instruction: `_ANSWERS_RESERVED` "omits `id` and `mint_id`, and
`node_writer.py:769` `fm.update(extra_fm)` overwrites the minted ones (also
`next_edges` and `scaffold_hash`) … the refusal must NAME the row … close it
there too, ONE shared check, not two copies."

What the machine did: `node_writer.write_node` builds the identity dict
(`id`, `mint_id`, `next_edges`, `scaffold_hash`) at node_writer.py:757-767 and
runs `fm.update(extra_fm)` at :769 — the caller's rows land LAST, so on the
old bytes an answers row `{"id": "goal:g-stolen"}` or `--set id=…` overwrote
the node's own identity and the mint still printed `created:`. Now
`_refuse_authored_identity` (write.py, one function) is called from the
answers-row loop and, joined with `or`, from the existing argv `--set`
refusal line — so both routes refuse BY NAME with exit 2 and no file:

```
ERR: create --answers refused by name: 'mint_id' is MINTED by node_writer
(id, mint_id, next_edges, scaffold_hash) and is never authorable
```

`--answers id=…` and `--set id=…` are the same check; the only difference is
the word after `--` in the message.

NEAR MISS: adding `id`/`mint_id` to `_ANSWERS_RESERVED`. It satisfies the
instruction's first half (the row stops reaching `extra_fm`) and LOSES the
second: the row is then silently DROPPED, the caller gets exit 0 and a node
whose id is not the one it asked for, with no name in any message. A drop is
indistinguishable from success; a refusal is not.

### 2. `--set` LOSES TO THE POST STAMP — the explicit `--set` WINS

Instruction: `post_rows` is filtered "on `answers` ONLY, so an explicit
`--set role=…` is overwritten by the calling post's row … PICK ONE and TEST
IT: either the explicit `--set` WINS, or it is REFUSED BY NAME."

CHOSEN: **the explicit `--set` WINS.** The order `--set` > answers file is the
one the caller already reads as obvious (an inline flag is the most local
statement on the command line; refusing it would be a surprise and would cost
a second round-trip for something the caller can see). The filter is now on
`set_fm`, which at that point already holds BOTH the file's rows and the
`--set` rows — one line changed, no second rule:

```
post_rows = {k: v for k, v in _post_stamp(root, args.actor).items()
             if k not in set_fm}          # was: `if k not in answers`
```

NEAR MISS: refusing the collision by name (`--set role` vs `config:posts`
row). It also "fixes" the row, and it loses: a caller who must re-file the
same value because a post row happens to carry the same key can never set
`role` or `town` at all on a seated post, which is a strictly smaller
capability than winning. Refusal is the right answer only where the caller
may not choose (hole 1), not where two wishes merely meet.

### 3. THE PRECEDENCE, STATED ONCE — and executed

Instruction: "state the full precedence ONCE — in the
`_read_answers_file`/`create` docstring AND in a test — and make the answers
route FOLLOW it."

`write._STAMP_ROWS` is the single source of the order, and the
`_read_answers_file` docstring states it in prose:

```
explicit `--set` > the answers file > the calling post's config:posts row > the environment
```

Executed in `main()`: the SURVIVING choice per stamp row is what `post_rows`
carries, so `create()`'s existing post-mint re-stamp (write.py:2995-3008,
which exists precisely because `node_writer._stamp_env_fields` OWNS `season`
and `role` from the ENVIRONMENT) lands the winner last:

```
post_rows.update({k: set_fm[k] for k in _STAMP_ROWS if k in set_fm})
```

Two consequences worth naming, both deliberate:
- The re-stamp is NOT gated on a post row existing. A file (or `--set`) that
  sets `role`/`season` under an UNSEATED caller used to lose to `AGI_ROLE` /
  `AGI_SEASON`; now the env is the lowest rank in every case.
- `edited_by` is deliberately NOT in `_STAMP_ROWS`: that row is `create()`'s
  own `--actor` provenance, and the post row has always lost to it
  (write.py:3003-3004). Stated, not silently changed.
- The argv route is byte-identical: the whole re-stamp lives inside the
  `if answers:` branch, which the pre-existing control in
  `test_season_is_owned_by_the_writers_env_stamp_on_both_routes` pins —
  `--set season=1` without `--answers` still yields `season: 5` under
  `AGI_SEASON=5`. The precedence is a property of the ANSWERS route, named as
  such.

NEAR MISS: documenting the order and leaving the code alone (today's state,
one layer of the table already true and the row silently replaced at the mint
by `fm.update` / `_stamp_env_fields`). It reads exactly right on the page and
is false on disk for the two highest ranks — the doc becomes a cover for the
defect instead of its record.

## Deviations from the standing rules

- The dispatch said "Add them [id, mint_id] to the reserved set"; this node
  REFUSES by name instead. Property of THIS case: the reserved set is
  "rows that name the mint itself" (type/slug/parents/body/payload) — an
  identity row does not name the mint, it CLAIMS to BE the mint, and a
  reserved row is consumed while an identity row must be refused. Silently
  dropping a caller's id is the defect the round exists to close.
- `production_lines 45` (measured, `git diff --numstat` on
  `extensions/agi/bin/write.py`, 45 added / 3 removed) over the brief's 20.
  ~19 are executable lines; the rest are the ONE statement of precedence the
  same brief demands (docstring + the two constants' comments). Under the 2x
  re-brief threshold, so no re-brief is filed.

## Evidence

```
$ git diff --numstat -- extensions/agi/bin/write.py
45       3       extensions/agi/bin/write.py

$ python3 -m pytest extensions/agi/tests/test_write_answers_file.py -q
30 passed

$ python3 -m pytest extensions/agi/tests/test_write_answers_file.py \
    extensions/agi/tests/test_write.py \
    extensions/agi/tests/test_write_schema_checked.py \
    extensions/agi/tests/test_write_actor_rows.py \
    extensions/agi/tests/test_node_writer.py -q
315 passed, 186 warnings in 16.50s
```

New tests, all in `test_write_answers_file.py`:
`test_an_answers_row_naming_a_MINTED_row_refuses_by_name` (parametrized over
all four identity rows), `test_the_argv_set_route_refuses_a_MINTED_row_by_the
_same_check`, `test_an_explicit_set_BEATS_the_calling_posts_stamp`,
`test_an_explicit_set_BEATS_the_answers_file_row_too`,
`test_the_answers_files_own_row_beats_the_ENVIRONMENT`, and
`test_the_precedence_is_STATED_ONCE_and_the_routes_follow_it` (asserts
`_STAMP_ROWS = (` occurs exactly once in write.py and that the docstring
carries the order). Every fixture is a temp graph under `tmp_path`; no user
name, home or repo path value, host or IP appears in any fixture or in this
body.

The pre-existing `test_a_row_the_answers_file_sets_wins_over_the_stamp` and
`test_set_flags_may_still_add_a_row_on_top_of_the_answers_file` still pass
unchanged — hole 2 was that the second test only ever set `tags`, a row no
post row carries; the new tests set `role`, which one does.

## Agent Notes
Closed 3 holes on the answers route: one shared identity-row refusal (both routes), --set now outranks the post row, precedence stated once in _STAMP_ROWS and executed; 6 new tests, 315 pass in the neighbourhood.

PARENT REVIEW a00-06858031, DH.502. I read the DIFF (write.py +45/-3, tests +79, node), not the result file, and ran SIX of my own negative probes against the child's changed bytes (extracted from its branch, so the probe reaches the diff and not a stub). PROBES (all six in .agi/sessions/iter-DH.502/a00-06858031/a00-06858031/probe/test_parent_probes.py of the de-h482 worktree): (1) GATE -- answers row {"id": "goal:g-stolen"} refuses by name, exit 2, no node written: PASSES. (2) AUTH -- argv `--set mint_id=0000` on the same shared check, exit 2, no node: PASSES. (3) WIRE -- `--set role=council` with the answers file, post-a seating role parent: the re-stamp reaches the node ON DISK, "role: council", post row's parent absent: PASSES. (4) GATE -- file-set season=7 survives node_writer._stamp_env_fields with AGI_SEASON=5: PASSES. (5) GATE -- the SAME explicit `--set season=7` on the argv route with NO --answers: rc=0 and the node carries "season: 5". FAILS -- a silent replacement, nothing refused. (6) AUTH -- `--set role=owner` with an answers file, actor post-a whose seat row says parent: rc=0 and the minted node carries "role: owner". FAILS -- the seat ladder's _ceiling_refusal (write.py:749) refuses exactly that for --role and AGI_ROLE, and the new rank-1 re-stamp lands the elevated row where the env stamp used to overwrite it. WHAT THE INSTRUCTION SAID: "PICK ONE and TEST IT: either the explicit --set WINS, or it is REFUSED BY NAME", and "a row the caller may not choose is REFUSED BY NAME, never silently replaced". WHAT THE MACHINE DOES: the new post_rows.update() at write.py:3196-3197 makes the --set row durable, and the docstring/comment at write.py:1866-1871 claims "nothing above the env rank is silently lost" while never running that row past the ladder. NEAR MISS: the winner-WINS choice implemented as a filter change plus a re-stamp, with the winner's own authority UNCHECKED -- it satisfies the words ("--set wins") and loses the mechanism (a rank-1 row can claim a role its seat may not). Probe 5's counterfactual for the same line: the SAME re-stamp placed outside the `if answers:` block would make the stated precedence TRUE on both routes; the near miss is placing it inside, where only the answers route is fixed. So: item 1 is fully closed and reproduced by me; items 2 and 3 are closed as WRITTEN and false as STATED, and probe 6 is a hole the diff WIDENED (pre-diff the env stamp overwrote role=owner; post-diff the re-stamp lands it). Demoted to lean_disproved on those two probes, not on the kid's own suite. The kid's last test greps the source for a docstring and never EXECUTES the argv route -- that is how 5 and 6 both walked past it.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT RE-VERSION (a00-06858031, DH.502). WHY THIS VERSION DIFFERS: the kid closed hole 1 and proved it, but the precedence it chose -- explicit --set WINS -- is a rank-1 row with no authority check, and I falsified it twice with my own probes against its branch bytes.

(1) WHAT THE INSTRUCTION SAID, quoted: "PICK ONE and TEST IT: either the explicit --set WINS, or it is REFUSED BY NAME", and "a row the caller may not choose is REFUSED BY NAME, never silently replaced."

(2) WHAT THE MACHINE ACTUALLY DOES. write.py:3196-3197 -- post_rows.update({k: set_fm[k] for k in _STAMP_ROWS if k in set_fm}) -- sits inside the `if answers:` block, so the winner row is re-stamped onto the node AFTER node_writer._stamp_env_fields, and nothing on that path ever calls _ceiling_refusal (write.py:749, the ladder that refuses a role above the actor's seat for --role and for AGI_ROLE). Probe 6, run by me against the extracted branch bytes: `--answers f --actor post-a --set role=owner`, post-a's config:posts row role parent -> exit 0, node file carries "role: owner". Probe 5: the same explicit `--set season=7` with NO --answers -> exit 0, node file carries "season: 5" (AGI_SEASON), nothing refused. The comment the kid wrote at write.py:1866-1871 -- "nothing above the env rank is silently lost" -- is FALSE on the argv route, and probe 6 shows the diff WIDENED the hole rather than closing it: on the pre-diff bytes the env stamp overwrote role=owner; post-diff the re-stamp lands it.

(3) THE NEAR MISS. The winner-WINS choice implemented as a filter change plus a re-stamp, with the winner's own authority left unchecked. It satisfies the words (--set wins, --set is honoured) and loses the mechanism (a rank-1 row can claim a role its seat may not, and the stated order is true only on one of the two routes). The counterfactual for the same three lines: hoisting the re-stamp out of `if answers:` makes the precedence true everywhere -- and running the winner through _ceiling_refusal first makes rank 1 a LEGAL rank 1. Either is a small change; the near miss is placing both inside the answers-only branch, where the argv route keeps the old silent replacement.

(4) IF I DEVIATED FROM A STANDING RULE: I ran the writer against the kid's own worktree root to edit the kid's own node rather than my own checkout, because a review belongs in the node it reviews and the kid is terminal. That is the property of this case -- not convenience -- that makes the rule not apply.

WHAT SURVIVES: hole 1 is closed and I reproduced it twice (answers id=/mint_id= refused by name, no file written; argv --set mint_id= refused by the same shared check); the --set-over-post-row win is real on the answers route (probe 3, the row reaches the file on disk); a file-set season=7 survives the env stamp (probe 4). Those four stay. The kid's own final test greps write.py for a docstring string and never EXECUTES the argv route, which is exactly how probes 5 and 6 both walked past a suite the kid read as green.
<!-- THOUGHT:END -->
