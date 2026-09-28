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

## CORRECTIVE DH.555 -- closes mur-director-engine-23 DH.521-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-one-mint-route-answer-a00-11b193da tip 31d121f4f (branch de-base-555; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. DRY-RUN BYPASS of the new ceiling guard (CONFIRMED on the bytes, runtime UNVERIFIED). write.py:3231 `if args.dry_run:` prints and `return 0` at write.py:3241 -- the new guard is write.py:3252-3258, AFTER that return, so `--answers f --set role=owner --actor post-a --dry-run` prints `set role = 'owner'` and exits 0 while the real mint refuses with exit 2. This contradicts the invariant the same function states twice (write.py:3220-3226 'a dry run simulates the mint, so it refuses what the real mint would refuse'; write.py:3200-3201 for the answers row validator) and is precisely what the file's own committed test `test_a_bad_row_refuses_in_dry_run_too` enforces for the row validator. No committed test passes `--dry-run` with a role row, so no test covers it. Probe I WOULD run (not run, per instruction): `cd <archive-of-31d121f4f> && python3 -c "import sys;sys.path.insert(0,'extensions/agi/bin');import write,json,tempfile,pathlib;p=pathlib.Path(tempfile.mkdtemp())/'.agi';(p/'nodes/goal').mkdir(parents=True);(p/'context/schemas').mkdir(parents=True);(p/'config.json').write_text('{}');(p/'nodes/.geometry').mkdir(parents=True);(p/'nodes/.geometry/posts.md').write_text('---\nid: \"config:posts\"\ntype: config\nposts:\n - name: post-a\n role: parent\n---\n');f=p/'a.json';f.write_text(json.dumps({'type':'goal','slug':'g9.9.9','goal_id':'G9','goal_kind':'subgoal','status':'active','origin':'x','seeds':[],'confidence':.5,'tags':[],'title':'t'}));print(write.main(['create','--answers',str(f),'--root',str(p),'--actor','post-a','--set','role=owner','--dry-run']))"` -- expected under the bytes: 0 with `role = 'owner'` on stdout.
2. A TEST THAT REQUIRES AN EXACT SPELLING (confirmed, test_write_answers_file.py:591-596). Line 591 already asserts the behaviour that matters (`write._ANSWERS_IDENTITY == frozenset(node_writer.MINTED_IDENTITY)`), and 595-596 only check the token exists. Line 593 then pins the literal source line `'"_ANSWERS_IDENTITY = frozenset(node_writer.MINTED_IDENTITY)"'` in write.py, so an equally one-source derivation written as a wrap, a local alias, or a different frozenset spelling fails green -> the test would require the wording, not the mechanism. Mechanism-level, and it is the one defect here the round's own node does not disclose.
3. INHERITED FAIL-OPEN ON AN UNSEATED ACTOR, now on a third call site (confirmed, write.py:757 reached from write.py:3254). `_ceiling_refusal` returns None when `seat_role not in _LADDER`, and `_resolve_seats_role` returns None for an empty actor (write.py:727). So `--answers f --set role=owner` with NO `--actor` still mints `role: owner`: `post_rows` is fed by `post_rows.update({k: set_fm[k] for k in _STAMP_ROWS if k in set_fm})` (write.py:3213-3214, and `role` IS in `_STAMP_ROWS` at write.py:1876), but the seat is unresolvable. This is the same documented policy as the `--role`/`AGI_ROLE` routes (write.py:754-756), so it is not a new hole -- but the node's Caveats name only the argv-route `--set` gap and not this one, and it is a third call site of the same guard.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_write_answers_file.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/node_writer.py · extensions/agi/bin/write.py · extensions/agi/tests/test_write_answers_file.py · .agi/nodes/experiment/a00-b0bf124f-4b8eb4.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 31d121f4f · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.570 -- closes mur-director-engine-27 DH.555-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-one-mint-route-answer-a00-0cdc4614 tip 83d964956 (branch de-base-570; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. Parent caveat addendum unlanded — the 'THIRD call site' the round says it recorded is absent from 83d964956
2. Test cap breached — 54/3 numstat = 51 net added against a declared cap of 40
3. Wording-coupled assertion — test_write_answers_file.py:609 hard-codes the six-space pad of the dry-run `set` print
4. The first reviewer's own citation is wrong on defect 1: a00-b0bf124f-4b8eb4.md:72 is inside the ``` evidence fence (the ERR message text), not the Caveats list; the Caveats header is :83. A citation that does not point at the thing it indicts should not be relayed upward as-is.
5. The round's node under-reports itself in TWO places the first reviewer did not flag: (a) the test-line overrun is absent from its Caveats entirely (its only budget sentence is '(file scope + the 15-line cap)' about the argv route, a00-949eaa34-76f733.md), and (b) the item-3 provenance line claims a parent-node edit that was never made. The graph is the memory; a node whose cost and whose cross-references are both understated fails 'residues = 0' independently of the mechanism being right.
6. UNVERIFIED (not run, by rule): the node's evidence block claims '113 passed, 6 skipped' for test_write_answers_file.py + test_bin_help_smoke.py and '11 passed' for test_rotate_first_decision.py. I ran only the single in-scope file (41 passed) because test_rotate_first_decision drives rotate.py and I will not execute rotate-family code inside the Prime's own tmux pane (2026-09-11 17:45Z precedent, belam.log:58240-58290, goal:g15.20). Probe I WOULD run, in a throwaway detached worktree of 83d964956: `cd <that-worktree> && env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_write_answers_file.py extensions/agi/tests/test_bin_help_smoke.py extensions/agi/tests/test_rotate_first_decision.py -q -p no:cacheprovider --basetemp=/tmp/dh555v`
7. The node's own reload caveat is OVER-stated, so it should not be relayed upward as an open risk: the new mutation test calls importlib.reload(write) (test_write_answers_file.py:637-646), which the node calls 'heavier than a source assert and the one thing a future write.py with import-time side effects would break'. I checked the concrete cross-module risk instead: `grep -rn '^from write import|^from node_writer import' extensions/agi/tests/*.py` returns NOTHING, so no sibling module holds a stale function binding across the in-place reload, and I ran the reload test FIRST followed by two mint tests — 3 passed. The real residual is narrower than the node states: only a future import-time side effect in write.py, not present today.
8. A green-test/real-resource sweep came back clean and is worth recording as a negative result, since the first reviewer did not report one: the `project` fixture is entirely under tmp_path (test_write_answers_file.py:91-100), `_geometry` writes only inside that temp graph (:133-139), the diff touches no tmux/systemd/crontab/process, no verification or gate file (conftest/verification.py/commands.py) was edited so the round did not fix the gate it must pass through, and `git diff --numstat` shows zero deletions anywhere — no demotion under .agi/nodes.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_write_answers_file.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/write.py · extensions/agi/tests/test_write_answers_file.py · .agi/nodes/experiment/a00-949eaa34-76f733.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 83d964956 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.587 -- closes mur-director-engine-30 DH.570-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-one-mint-route-answer-a00-e8ed6f32 tip 4b007ebab (branch de-base-587; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. DH.570's own test-ceiling claim is false and is copied into the parent node's Caveats — a00-ff788172-12084f.md:216 'BREACHED by 18 net / 58 net against a 40 cap' where the measured DH.570 delta is 8/1 = 7 net; same claim at a00-949eaa34-76f733.md:105
2. 2. the false parent-edit claim DH.570 struck survives at two sites in the same node — a00-949eaa34-76f733.md:127 (Agent Notes) and THOUGHT :138 still say the parent's Caveats bullet was recorded by DH.555, which it was not
3. a00-ff788172-12084f.md:227-229 undercounts its own rule: 'The unseated fail-open is now recorded in TWO places (the parent's Caveats, added here, and the docstring at the call site).' It is stated in at least FOUR: .agi/nodes/experiment/a00-b0bf124f-4b8eb4.md:95-104 (the Caveats bullet DH.570 added), .agi/nodes/experiment/a00-949eaa34-76f733.md:92-96 (its own Caveats, which already carry the same content in the same words — 'that is `_ceiling_refusal`'s fail-open, identical to `--role`/`AGI_ROLE` … A ladder decision for the director' — and DH.570 did not touch it), the write.py call-site comment at extensions/agi/bin/write.py:3237-3242, and hypothesis:one-mint-route-answers-file-validated-row-by-row.md:67. The caveat is load-bearing precisely because it issues a strike order — 'If a later kid hardens `_ceiling_refusal`, both must be struck together' — and striking 'both' would leave two stale copies live. This is the one-source-per-rule violation, in the very rule the caveat is about, and the first reviewer did not count the sites.
4. DH.570's own completeness claim is false in the same way it corrected: a00-ff788172-12084f.md:62 ('5 | TWO SELF-UNDERSTATEMENTS | both fixed on the round's own node') and :126-130 ('Both are now on the round's own node, struck through at the claim site and stated in its Caveats'). The claim survives UN-struck at a00-949eaa34-76f733.md:127, so item 5(b) is not 'both fixed'. The corrective asserted a completeness it did not have — the same class of error the round exists to remove.
5. a00-ff788172-12084f.md:103-110 pastes a code fence whose content is NOT what the file says: it carries the OLD literal `set role = 'kid'` with an inline `<- actually r"set\s+role = 'kid'"` annotation. The disclosure at :112-113 ('the real line uses r"set\s+role = 'kid'"') is honest, but a reader skimming the fence — or any future miner copying it — gets the spelling DH.570 removed. On a node whose declared Question is 'Did experiment:a00-949eaa34 say true things about itself? … every number a pasted command and not a typed one', a node that pastes bytes that are not the bytes is a small self-inflicted instance of its own subject.
6. The weakened assertion is looser than the node claims but not decoupled, and the note should say so: a00-ff788172-12084f.md:106-107 and the THOUGHT's 'never the column layout' describe de-wiring, and the live test at extensions/agi/tests/test_write_answers_file.py:614 (`re.search(r"set\s+role = 'kid'", out)`) does drop the column padding — but it still pins the single-space `{k} = {v!r}` row format of extensions/agi/bin/write.py:3260. That is acceptable (the claim is only about column layout) and the assertion is NOT vacuous: it still binds on the value 'kid', and the added `assert not (project / 'nodes' / 'goal' / 'g9.9.9.md').exists()` at :615-616 is a strict strengthening the old line did not carry (the create dry run returns at write.py:3261 before any write), matching the existing pattern at :199, :559, :598. UNVERIFIED, not run: that the new assertion FAILS if the dry-run short-circuit is removed — I did not patch the source, and a committed test does not answer it; the probe I would run is a scratch copy of write.py with `if args.dry_run:` at :3251 flipped to fall through, then this one test file, expecting exactly the :615 assert to fail.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_write_answers_file.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_write_answers_file.py · .agi/nodes/experiment/a00-949eaa34-76f733.md · .agi/nodes/experiment/a00-b0bf124f-4b8eb4.md · .agi/nodes/experiment/a00-ff788172-12084f.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 4b007ebab · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.610 -- closes mur-director-engine-32 DH.587-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-one-mint-route-answer-a00-21eb7514 tip 697247787 (branch de-base-610; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. Strike order cites a fifth copy that does not exist (.agi/nodes/experiment/a00-ff788172-12084f.md:255, mirrored at a00-b0bf124f-4b8eb4.md:108)
2. 3. Site-count arithmetic wrong in both directions (.agi/nodes/experiment/a00-b0bf124f-4b8eb4.md:105 and a00-ff788172-12084f.md:250)
3. 4. No grid version for any of the four changed nodes (.agi/nodes/experiment/a00-62dbecb1-6ed405.md:1)
4. 62dbecb1:137-139 asserts a READER behaviour about a copy that does not exist: 'the fifth copy of the unseated fail-open rule, and the copy a reader reaches FIRST, since it is the hypothesis this whole chain hangs from'. The hypothesis node is 48 lines with zero matches for the rule (verified at 697247787), so this is a claim about a reader of a file that was never read -- and it sits in 'Findings for the director', the section the director reads first.
5. The wrong count is carried in the two regions a reader reaches FIRST: the What-I-did table row at 62dbecb1:37 ('recounted: FIVE live copies, all named') and the Agent Notes at 62dbecb1:179 ('TWO->FIVE call sites'), both presenting the count as re-derived evidence, while its refutation sits 160 lines below at 62dbecb1:196. A reader who takes the summary as the round's answer gets five.
6. ff788172:250 counts 'this node's Caveats bullet' among the places the rule is recorded, but that bullet is the pointer performing the count and states none of the mechanism; the node's other 'unseated/fail-open' hits (:80, :296) are a grep transcript and a THOUGHT, not a statement of the rule. So even the surviving 'four' is one too many counted as copies.
7. No demotion and no hand-landed gate: git diff --name-status 4b007ebab 697247787 = 1 A + 3 M, all under .agi/nodes/experiment/ -- nothing under extensions/ or skills/, so the round could not have fixed the gate it passes through, and no node file was deleted.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS      + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE  · .agi/nodes/experiment/a00-62dbecb1-6ed405.md · .agi/nodes/experiment/a00-949eaa34-76f733.md · .agi/nodes/experiment/a00-b0bf124f-4b8eb4.md · .agi/nodes/experiment/a00-ff788172-12084f.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 697247787 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.621 -- closes mur-director-engine-35 DH.610-k1 demote
BASE      CUT FROM season2/loops/hypothesis-one-mint-route-answer-a00-52167e83 tip df5fe19b0 (branch de-base-621; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
NOTE      DH.610's four node edits never committed: its parent left them unlogged in its own worktree (never hand-landed, TMM.268). Re-apply every ordered node edit THROUGH write.py on this branch and commit.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. Corrective claims four node edits landed; none of the four in-scope nodes changed at this tip (items 2/4/5/6 written as done while the diff is 1 A)
2. 2. PARENT PROBES gate probe quotes a sentence that does not exist ('DH.587 read FIVE, DH.610 corrected it to THREE' has 0 hits)
3. 3. Decisive verdict 'proved' on claims the bytes refute; needs inconclusive_lean_proved:N
4. 4. Evidence numstat not reproducible from any commit; omits the node its own name-status shows as M
5. 5. Two ranges pasted as one; DH.587's landing commit presented as this round's delta
6. 6. Item 6's rule has no home at this tip (reading correct, destination write unlanded)
7. The dead citation the round exists to refute is STILL LIVE in the graph at the tip. `hypothesis:one-mint-route-answers-file-validated-row-by-row.md` is 48 lines with 0 `_ceiling_refusal` hits, yet it is cited as site #4 at a00-ff788172-12084f.md:254, and a `row-by-row.md:67` citation survives in a00-62dbecb1-6ed405.md and a00-b0bf124f-4b8eb4.md (1 hit each, measured at df5fe19b0). The node's own thesis at :77-78 — 'the strike order that sent a later striker there had a fifth site that does not exist' — is therefore still true of the graph, and the strikers are still being sent.
8. The gate probe's count under-reports by one even on its own search string: a00-2e615bb5-234c16.md:186 says 'returns ONE hit, 62dbecb1:37'; `grep -n 'all five\|FIVE live'` over the four in-scope nodes returns TWO (a00-62dbecb1-6ed405.md:37 'all named, the strike order rewritten to "all five"' and a00-b0bf124f-4b8eb4.md:110 'strike all five'). A gate that miscounts the survivors it is clearing is the same defect class as the five-vs-three arithmetic it is certifying.
9. Self-contradiction on 949eaa34 inside the node: :97 pastes it as `M` in the name-status, :39 and :60 treat it as a live third copy needing no edit, and :153 states '949eaa34 is unmodified' — while the node's own name-status says it was modified. A reader cannot tell whether the file is in scope and unchanged or out of the delta.
10. An unread reader: .agi/context/schemas/[experiment].md says 'the decisive judgement belongs in a child `verdict` node'. a00-2e615bb5-234c16.md:23 carries a decisive `verdict: proved` inline with `next_edges: []` (:7) and no child verdict node. The viewport rule that proved/disproved need `evidence_runs >= 1` is satisfied only by the self-reference at :10-11, so no gate in the chain could have caught this round.
11. template_max: the counting rule authored at a00-2e615bb5-234c16.md:47-51 ('A copy is a place that states the mechanism ... a mention, a count, a grep transcript and a THOUGHT do not state it') is a standing rule for every future reviewer, written on a single experiment node with no home in a template or schema (`git grep -ln 'one source per rule' df5fe19b0 -- skills/` returns nothing), and the node's claim that it landed on the ff788172 Caveats (:137-138) is false (ff788172:250 still reads FOUR). The next kid re-derives it from a node instead of reading a rule.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS      + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE  · .agi/nodes/experiment/a00-2e615bb5-234c16.md · .agi/nodes/experiment/a00-62dbecb1-6ed405.md · .agi/nodes/experiment/a00-b0bf124f-4b8eb4.md · .agi/nodes/experiment/a00-ff788172-12084f.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over df5fe19b0 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## OPEN at the 2026-09-28 merge-up (director-engine; belam [decision] 00:0xZ: in-progress included)
STATUS    IN PROGRESS, not landed: DH.660 QUEUED (not yet dispatched); round work so far on loop branch season2/loops/hypothesis-one-mint-route-answer-a00-31004c15 tip 1e74cea4b.
ROUNDS    this post's rounds on this node: DH.610 DH.621 DH.660; the open round's bytes live on its loop branch, never on the post branch, until its mur clears.


## CORRECTIVE DH.660 -- closes mur-director-engine-41 DH.621-k1 demote
BASE      CUT FROM season2/loops/hypothesis-one-mint-route-answer-a00-31004c15 tip 1e74cea4b (branch de-base-660; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. Item 3 not landed -- the self-evidenced `proved` on 2e615bb5 is still verdict: proved with evidence_runs=[itself] while the round's title, table, Agent Notes and THOUGHT report the demotion as done
2. Item 7 not landed -- the dead `hypothesis:...md:67` citation is still live at b0bf124f:108, 62dbecb1:137 and ff788172:255, a file that is 48 lines with 0 hits
3. Item 8 not landed -- 2e615bb5:186 still asserts the grep returns ONE hit; it returns three
4. Item 11 not landed -- ff788172:250 still reads FOUR and :260 'still stated in five places'
5. The round reports its own other-node writes as landed while its committed delta is one added file -- the class ff788172's own THOUGHT names ('the writer logs the write; it does not put the write on the branch')
6. The round's own ceiling arithmetic is false in the very round about miscounts: a00-e0efd9fc-a8cf4c.md:108 states 'I wrote net +65 production lines against a 15-line net clause (40 as the dispatch default) ... It is under the 2x stop threshold'. The 2x stop is 2x the operative clause (GOALS.md:13035, '66 production lines vs 35 ceiling, under the 2x stop gate of 70'), so against the 15-line clause the gate is 30 and 65 is 4.3x OVER; only against the 40 default (gate 80) is 1.6x. The node names the clause it exceeds and then declares itself under the gate it names. Self-disclosed, but the disclosed number is the wrong arithmetic.
7. The corrective round creates the one-source-per-rule violation it declares homeless: a00-e0efd9fc-a8cf4c.md:49-52 and :109 state that the counting rule ('a copy is a place that STATES the mechanism') has NO home -- verified, `git grep -ln 'one source per rule' 1e74cea4b -- skills/ .agi/context/` exits 1 -- and then spends 112 lines restating that rule and the strike order in node prose (:33-41 table, :49-52, :86-93). The fix it names (one line in a skill or schema) was not made; a fourth copy was written instead. TEMPLATE_MAX violation, created by the corrective.
8. The round proposes 'A `proved` whose only evidence is itself passed every gate in the chain ... Worth a gate, not a note' (:55-56) and does not apply that observation to its own node, whose frontmatter is the same shape: a00-e0efd9fc-a8cf4c.md:10-11 `evidence_runs: - experiment:a00-e0efd9fc-a8cf4c` with :21 the verdict. The taxonomy is already satisfied (a lean, not a proved), so this is residue, not a demote -- but the round names the smell in a neighbour and carries it.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS      + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE  · .agi/nodes/experiment/a00-2e615bb5-234c16.md · .agi/nodes/experiment/a00-62dbecb1-6ed405.md · .agi/nodes/experiment/a00-b0bf124f-4b8eb4.md · .agi/nodes/experiment/a00-e0efd9fc-a8cf4c.md · .agi/nodes/experiment/a00-ff788172-12084f.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 1e74cea4b · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## CORRECTIVE EG.62 -- closes mur-eg-14 EG.39-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-one-mint-route-answer-a00-ae77e8be tip eef31410a (branch de-base-EG.62; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. THOUGHT not rewritten with the demotion — a00-d85ae42b-bf72d8.md:135 still 'The claim is PROVED' against frontmatter :21 inconclusive_lean_disproved:65
2. '[rule] BANKED' claim unbacked at eef31410a — a00-d85ae42b-bf72d8.md:46 (also a00-e0efd9fc-a8cf4c.md:54)
3. The missing-THOUGHT defect covers ALL THREE edited nodes, not just the one: e0efd9fc:49-54 changes a factual claim (the rule's home, from ff788172's Caveats to 2e615bb5:47) and ff788172:253 adds a new on-this-tip claim ('the command also returns b0bf124f:106'), and neither node's THOUGHT (e0efd9fc:115, ff788172:296+) records that its version changed. The diff has no THOUGHT hunk anywhere (git diff f0f5a36e6 eef31410a touches only :5-8, :18-21, :35-81 of d85ae42b; :6-9, :49-54 of e0efd9fc; :253 of ff788172).
4. The demotion's REASON is unrecorded inside the merge range, not merely its THOUGHT: `git grep -n 'EG.39' eef31410a -- .agi/nodes/doc/card-director-engine.md` returns no match, and the parent hypothesis one-mint-route-answers-file-validated-row-by-row.md never names a00-d85ae42b. A reader of the merged tip sees proved -> inconclusive_lean_disproved:65 with no stated cause anywhere in the tree; the only trace is 72aff26ec, outside the range.
5. The version-delta was pasted into the BODY instead of the authored region: d85ae42b:44-46 ('EG.39 (the director's pure-text fix of mur-eg-11 DH.660-k1) corrected this line: it named ff788172's Caveats, which never held it. The rule's skill home is BANKED by the director as a [rule]') sits in the 'The one number' body section while the THOUGHT at :134-136 still carries the DH.660 delta — a note in two homes, neither of them the version's delta region.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_bin_help_smoke.py once (timeout 900, TMPDIR + --basetemp under /dev/shm, env -u TMUX -u TMUX_PANE -u AGI_POST -u AGI_SEAT (TMM.322)); TEXT-ONLY round: node text only
FILE SCOPE .agi/nodes/experiment/a00-d85ae42b-bf72d8.md · .agi/nodes/experiment/a00-e0efd9fc-a8cf4c.md · .agi/nodes/experiment/a00-ff788172-12084f.md (write.py) · the kid's own node
CEILING   HARD CAP: this kid only (claude-code text-fix, skill agi-corrective §3a) · 0 production lines · 0 test lines · node text only · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat eef31410a <your final tip>` on your node (an empty range is not a measurement)
KID       you ARE the round: commit every edit on your loop branch (cli.py done) before you exit; a version delta goes in the node THOUGHT (write.py), never the body


## CORRECTIVE DH.EG.89 -- closes mur-eg-19 EG.62-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-one-mint-route-answer-a00-0c20ee50 tip 11a2fd3ce (branch de-base-EG.89; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. THOUGHT points at a grid version that does not exist (x3) - d85ae42b:134 'Prior DH.660 reasoning lives in the grid version before this one'; same clause at e0efd9fc:114 and ff788172:297
2. Re-runnable ONCE probe no longer reproduces and the round doubled its hits - d85ae42b:43 'Re-run on this tip, pasted, not typed' over the paste at :49-52
3. Stale typed count left live in the node whose THOUGHT was rewritten - d85ae42b:140 'returns TWO sites, not one'
4. Evidence row PROVED=0 where the file holds 1 - 0c20ee50:54
5. 0c20ee50:67 'test_bin_help_smoke.py: 72 passed, 6 skipped' pasted as a bare number, no command; measured 72 passed, 7 skipped
6. CAUSE of defect 1, which the first reviewer reported as a symptom only: NEITHER commit in the range ran `grid.py commit` - 056aac2ce (the kid's done commit, 1 file) and 11a2fd3ce (the director's landing, 3 files) are plain git commits. AGENTS.md pairs the two ('git commit · python3 extensions/agi/bin/grid.py commit --all'). That is why all four mints have 0 grid versions, so 'the grid version before this one' is empty; it also means 0c20ee50 (a3fd3d8a) joins the 11-node anomaly set that has no grid history at all. Fixing the landing without the grid commit is what manufactures the false pointer.
7. Low: the numstat paste at 0c20ee50:60-65 (4/5, 5/6, 2/16) omits the round's own 80-line minted node, so read as the round's scope it reports 11 insertions where the range holds 91. It is labelled 'Measured on the worktree before `cli.py done` commits', so it is scoped rather than wrong - but the block is not ordered against :52 ('After the edits'), which is why the miscount at :54 escaped.
8. DEMOTED by the director: the TMM.268 'bytes == last write-log sha' custody item -- the harvest matched against the KID worktree's own write-log (per-root, node_writer.py:127; findings row); do not rewrite a landing commit.
9. Every number or line you write is measured at YOUR final tip after your last edit and PASTED with its command (two-operand git diff); a claim you cannot re-run is narrowed or removed, never retyped.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees (belam [red] 06:56Z: two such searches held io PSI at 84)
TESTS     test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE .agi/nodes/experiment/a00-0c20ee50-c7717f.md · .agi/nodes/experiment/a00-d85ae42b-bf72d8.md · .agi/nodes/experiment/a00-e0efd9fc-a8cf4c.md · .agi/nodes/experiment/a00-ff788172-12084f.md (write.py) · the kid's own node
CEILING   HARD CAP: this kid only (claude-code text-fix, skill agi-corrective §3a) · 0 production lines · 0 test lines (text, comments, docstrings, briefs and skill rows only) · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat 11a2fd3ce <your final tip>` on your node (an empty range is not a measurement)
COMMIT    every edit on your loop branch before you exit (cli.py done; g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective EG.89: mur-eg-19 EG.62-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
