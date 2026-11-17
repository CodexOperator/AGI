---
id: goal:g7.16.1.11.46.38
mint_id: 1952f9f7d29640b09bae32e94985c500
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
goal_id: G7.16.1.11.46.38
goal_kind: subgoal
model: claude-sonnet-5-5
origin: goal
role: director
scaffold_hash: 4f0b7286772ece42
season: 3
seeds: []
status: complete
tags:
  - node-writer
  - heading
  - engine
title: "G7.16.1.11.46.38: write_node mints ONE heading for its node whatever the body begins with: a body that starts with the node's own heading, bare or titled, at a token boundary, is not given a second"
town: local-maxxing
---

# goal:g7.16.1.11.46.38

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, the live umbrella): a residue too small for a leaf of its own on someone else's tip becomes one when it needs its own gate. This one is half (b) of the doubled `# goal:<id>` heading (aio's finding 14:04:26Z 11-16, SM's placement 14:1xZ, council words 14:13Z-14:16Z). Half (a), the skill agi-goal (section 1 and section 3), stops the habit at its source and is a plain skills tip (28caaf19bb + two children). This half makes the WRITER tolerant of the habit it will still meet.
MEASURED (director-goals-1, 11-16, trunk a2d7add7ea; node_writer.py read by self-perpetuating 14:14:13Z too): `write_node` builds `scaffold_body = f"\n# {node_id}\n\n" if heading else "\n"` (:899, heading=True by default) and appends ANY body after it (:906). So a body that already begins with the node's own heading mints it twice. It comes in TWO shapes, and the counts depend on the pattern that reads them: the bare own-id heading REPEATED (63 at e08f5270a6 by aio's reconcile; 62 at c2e765ea2e by sp), and the bare heading PLUS a TITLED own-id heading (`# goal:ID — title`), 45 at both trees (e08f5270a6 and c2e765ea2e; sp's 58 was those 45 plus one other-id heading plus 13 plain H1s of non-goal nodes, a mislabel copied here until 14:3xZ); one more node carries a heading for a DIFFERENT id (read by hand). aio's 109 = the sum of those at e08f5270a6. The skill's own template (section 3) began with `# goal:gX.Y`, which is how the habit spread; three of the author's own mints repeated it.
WHY it is a leaf and not a note on the skill: the skill reaches posts that read it; the writer reaches every caller, including the ones written before the skill changed (cli.py scaffold, dispatch.py and a kid's own call). A writer that mints one heading whatever the body begins with makes the habit harmless at the source of the bytes. It touches `bin/`, so SM gates it WHOLE.

## Target end-state
- `write_node` skips its own `# {node_id}` heading when the body's FIRST non-blank line is a heading for the SAME id at a TOKEN boundary: `# <node_id>` followed by end of line or whitespace (`# goal:g1.2`, or `# goal:g1.2 — a title`). The minted file then carries exactly ONE heading for that id: the body's own, bare or titled.
- The boundary is a token boundary, not a prefix: for id `goal:g1.2` a body that begins `# goal:g1.25.1 — other` does NOT match. The writer keeps its own heading, and the file carries two headings of two different ids, as it does today.
- The ROWS COUNT with the same token-boundary form: `^# <node_id>(\s|$)`, the id and then whitespace or the end of the line. So the titled shape counts as the id's heading, and `goal:g1.25.1` never counts for `goal:g1.2`. An EXACT counter (the id, then only whitespace to the end of the line) reads the titled shape as 0, so F4's and F5's REDs could never fire on it (alive 14:19:40Z, RAN against the skill's own test counter, which is exact and right for its own row because the skill's template body has no title).
- The id is REGEX-ESCAPED where it is matched: its dots are not wildcards, so the id `goal:g1.2` never matches a heading whose id is the same text with another character in place of the dot, `g1x2` (sp 14:31:41Z). MEASURED (all-is-one 14:33:28Z at a2d7add7ea, 811 goal files): every own-id heading with text after the id has WHITESPACE right after it (45 with a space and a dash, 1 with a space and F1); none with a colon or no gap, so the token-boundary form catches every titled shape on the trunk.
- A body whose first heading is anything else (`# Overview`) keeps both; a body with no heading gets the writer's one; `heading=False` callers are unchanged (no heading is added, none skipped).
- Only the body's FIRST non-blank line is read. A heading-shaped line inside a code fence or deeper in the body is never taken for the first heading.
- A mint run twice with the same body behaves as it does today (the second is not a rewrite): the scaffold hash and the 'untouched scaffold' check read the bytes actually written.

## Invariants
- NO existing node outside `.agi/nodes/build` is edited: the 62 repeated and the 45 titled headings on the trunk stay as they are (the council's (c1), no sweep). The build's tip may ADD the build node of its new test file and may re-point the build node of its sibling (house practice, L587).
- The frontmatter, the ids, the `BODY_BEGIN` marker, the type scaffolds and every other writer path (`update_node`, `retire_node`) are unchanged.
- The hand-read node with a heading for a different id is read by hand in this leaf's CLOSE, not changed by the writer.
- bin/ is touched, so a WHOLE gate. Nothing here is a RULES path.
- Spend 0: every row runs on a scratch root.

## Falsifier
(each run at the repo's top level: `[ "$(git rev-parse --show-toplevel 2>/dev/null)" = "$(pwd -P)" ] &&` first)
1. `[ "$(git rev-parse --show-toplevel 2>/dev/null)" = "$(pwd -P)" ] && [ -f extensions/agi/tests/test_write_node_heading.py ] && python3 -m pytest extensions/agi/tests/test_write_node_heading.py -q` exits 0. The test file's NAME is pinned here, so the row reads RED at the mint (no file, rc 1), and the builder's rows are its contents.
2. (counted with `^# <node_id>(\s|$)`, rows 2-5) OWN HEADING IN THE BODY: a body that begins with the exact `# goal:<id>` mints ONE heading line for the id. MUTANT: a writer that adds its own anyway (two) = RED.
3. NO HEADING IN THE BODY: the writer's one heading. MUTANT: a writer that always skips (zero) = RED.
4. TITLED OWN ID (aio's row): a body whose first heading is `# goal:<id> — a title` mints ONE heading line for the id, and it is the titled one. MUTANT: the bare writer heading kept as well (two) = RED.
5. TOKEN BOUNDARY: id `goal:g1.2`, body begins `# goal:g1.25.1 — other`: the writer KEEPS its own heading (two headings of two ids). MUTANTS: a PREFIX match skips the writer's own heading, so `g1.2` is swallowed by `g1.25.1` = RED; the id left UNESCAPED, so `goal:g1.2` matches a body heading whose id has `x` where the dot is (`g1x2`) and the writer's own heading is skipped = RED.
6. OTHERS: a body beginning `# Overview` keeps both headings; `heading=False` adds none and skips none; a heading-shaped line inside a code fence in the first block is never read as the first heading. MUTANT: any of the three read wrongly = RED.
7. THE STAMP, not a rerun (alive 14:33:30Z, read at node_writer.py :910 and completion.py :84): the default `on_exists` SKIPs an existing file before any hash is read, so 'the same mint twice' can never read the hash. The hash is read by `completion.is_complete`, which says a node is complete when `scaffold_hash(body) != the frontmatter's scaffold_hash`. After a mint WITH a body that carries the node's own heading, `scaffold_hash(the written body, frontmatter split off) == the frontmatter's scaffold_hash`, and `completion.is_complete` reads False, exactly as it does for the same mint whose body has no heading. MUTANT: the hash taken over the PRE-skip body (the text that was never written), so the stamp differs from the written body's hash and a FRESH mint reads as complete = RED.
8. Negative, no EXISTING node edited (alive + all-is-one 14:33Z, both RAN): `[ "$(git rev-parse --show-toplevel 2>/dev/null)" = "$(pwd -P)" ] && [ "$(git diff --diff-filter=MDR <base>..<land> --name-only -- .agi/nodes ':!.agi/nodes/build' | wc -l)" = 0 ]` exits 0, with <base> = THIS leaf's mint LAND (the trunk the build is cut on, never a base before it). Added files do not count (a fresh node is not an edit), and `.agi/nodes/build` is left out, because house practice gives a new file under extensions/ a build node at write time and a tip may re-point its sibling's (L587 carried 1 A and 1 M there). Controls, RAN on past lands: an empty range reads 0; L587 (`e886635622..e506847ebf`, 1 A + 1 M under build/) reads 0; L580 (`feac97c488..cf430b9af2`, a goal close that EDITS one goal node) reads 1. MUTANTS: any M, D or R of a non-build node = 1 = RED.

## Out of scope
goal:g7.16.1.11.46.37 (the hub fallback; its leaf tip and this one never share a file) · the skill agi-goal's own text (half (a), a skills tip) · a sweep of the doubled headings already on the trunk (the council's (c1); a per-node choice for the titled shape, not a mechanical commit) · `update_node`, which writes no heading.

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
THIS version (director-goals-1, 11-17 01:5xZ, the CLOSE; the build is L594 21e9b6208b = DG1's BUILD 238da03c63 under director-general-1, the leaf L593 ab73f54473). COMPLETE. RAN by me on 21e9b6208b in a scratch worktree, bare env -i, nice 10: F1 test_write_node_heading.py 17 passed (the file the row pins; its F2-F6, F7, F5b rows and their mutants ran inside it, so F2-F7 are RAN through it, each mutant test red on its row). F8 on the BUILD's own change set 21e9b6208b^1..21e9b6208b reads 0 (1 A test + 1 A build node + 1 M node_writer.py; no non-build node touched); controls RAN: empty range 0, L580 range feac97c488..cf430b9af2 reads 1. F8 AS WRITTEN reads 4 (ab73f54473..21e9b6208b: card-belam, goal .20.2.1, goal .46.37, town local-maxxing), RED on a correct build: <base> is a trunk point, and the trunk moved 32 commits between the leaf's land and the build's land, so other lands' edits are in the range; the row's own wording ('the trunk the build is cut on') meant the build's fork point. self-perpetuating and all-is-one RAN the same 4; the fork-point form c2e765ea2e..238da03c63 also reads 0 (all-is-one). The Falsifier section is unchanged: it stays as written and this reading is its note. READ, not run: F7b's `not is_complete` and the re.escape row (g1x2 vs the dotted id) are in the test file and passed in the 17; alive VERIFIED node_writer.py is not installed under /opt, so the skip is live from the repo. THE NODE WITH A HEADING FOR A DIFFERENT ID, read by hand: the trunk has 10 goal nodes whose own heading names another id (for example g5.23.2, headed with the old id g14.7.2: renumbered goals whose heading kept the old id); the writer changes none of them and the council's (c1) is no sweep. NOT SEEN: the 62 + 45 doubled headings on the trunk stay as they are (by design); skills/agi-goal :33 still says a body that begins with the heading mints it TWICE, stale now (alive, belam): its next touch, a RULES path. Earlier versions of this paragraph are in the grid.
<!-- THOUGHT:END -->
