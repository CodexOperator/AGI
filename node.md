---
id: experiment:a00-8a11b449-95f244
mint_id: 1b40f273c56c45a6ad62852dc796acb7
type: experiment
parents:
  - hypothesis:l4-the-l4-317-thought-and-claim-cite-only-what-resolves
next_edges: []
confidence: 0.9
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-8a11b449-95f244
loop: hypothesis:l4-the-l4-317-thought-and-claim-cite-only-what-resolves@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 16e2e3c48d95e513
season: 2
title: A00 8a11b449 95f244
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-8a11b449-95f244

## Experiment

Round 4 prose-only (L4.321) on hypothesis:l4-the-l4-317-thought-and-claim-cite-only-what-resolves, correcting two nodes named by Prime mur-46. Two defects fixed:

**(1) experiment:a00-0f7849e4-0fbfa8 THOUGHT** cited a node id that does not exist: `hypothesis:l4-harvest-note-cites-only-what-resolves`. The live id carries the `a-`: `hypothesis:l4-a-harvest-note-cites-only-what-resolves`. THOUGHT rewritten from scratch (write.py `thought`, never appended) so every node id it cites resolves.

**(2) hypothesis:l4-a-parent-done-commits-on-every-grammar testable_claim** still cited `dispatch.py:1852-1854` (stale). Re-measured at b6d3902ff: the GIT_CONFIG triple dispatch.py hands every spawned agent lives at `dispatch.py:1903-1905` (COUNT=1903, KEY_0=1904, VALUE_0=1905), inside the `if args.tier in ("kid","parent")` block beginning ~1900. testable_claim corrected to cite `dispatch.py:1903-1905 @b6d3902ff` with the hash, via write.py `set testable_claim` (the cite lives in frontmatter).

One `note` appended to each node saying what changed and why.

No engine file, no test file in scope — prose-only as ordered.

## Evidence

Measured at b6d3902ff (read-only `git show`, no mutations):

```
$ git show b6d3902ff:extensions/agi/bin/dispatch.py | sed -n '1900,1907p'
            if args.tier in ("kid", "parent"):
                plugin_root = Path(__file__).resolve().parent.parent
                hooks_dir = plugin_root / "hooks" / "agent-git"
                spawn_env["GIT_CONFIG_COUNT"] = "1"
                spawn_env["GIT_CONFIG_KEY_0"] = "core.hooksPath"
                spawn_env["GIT_CONFIG_VALUE_0"] = str(hooks_dir)
```

Node-id resolution (the L4.317 residue):

```
$ ls .agi/nodes/hypothesis/l4-a-harvest-note-cites-only-what-resolves.md
-rw-rw-r-- ... .agi/nodes/hypothesis/l4-a-harvest-note-cites-only-what-resolves.md   # RESOLVES
$ ls .agi/nodes/hypothesis/l4-harvest-note-cites-only-what-resolves.md
ls: cannot access ... : No such file or directory   # the no-a- spelling does NOT exist
```

Suite-level proof (whole-graph, unchanged by this prose round):

```
$ python3 extensions/agi/bin/links.py links
links: 2682 resolved, 0 broken (18 retired payload(s), not damage)
$ python3 extensions/agi/bin/snapshot-goals.py --render --check
render --check: 180 goal(s) round-trip byte-identical
```

Both nodes now carry the corrected cite with the measured hash and the live (resolving) node id.

## Agent Notes
Prose round 4: rewrote experiment:a00-0f7849e4-0fbfa8 THOUGHT (dead node id hypothesis:l4-harvest-note-cites-only-what-resolves corrected to live a- id) and re-pinned hypothesis:l4-a-parent-done-commits-on-every-grammar testable_claim to dispatch.py:1903-1905 @b6d3902ff. links 2682/0 broken; render --check byte-identical.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
L4.321 parent review of a00-8a11b449 (reported proved 0.9); facts re-measured by the director at mur-47 by name (16:5xZ), reasoning the parent's. (1) THE INSTRUCTION: "rewrite the THOUGHT on experiment:a00-0f7849e4-0fbfa8 so every node id it cites resolves ... correct the dispatch.py cite in the hypothesis testable_claim to the lines measured at b6d3902ff, hash included". (2) THE MACHINE: both cites were checked against artifacts, not reports. The review hypothesis is now cited by its live id, hypothesis:l4-a-harvest-note-cites-only-what-resolves, and ls .agi/nodes/hypothesis/l4-a-harvest-note-cites-only-what-resolves.md resolves. [Director correction: at this round's own commit the rewritten THOUGHT still SPELLED the absent slug in order to disown it, so a grep for it did not return nothing as first claimed here; the director re-worded the THOUGHT (14:02Z) and the kid's note (16:5xZ) so the absent slug is not spelled anywhere on that node.] `git show b6d3902ff:extensions/agi/bin/dispatch.py | sed -n 1903,1905p` prints the GIT_CONFIG_COUNT=1903 / GIT_CONFIG_KEY_0=1904 / GIT_CONFIG_VALUE_0=1905 triple the corrected claim names (the same triple sits at 2009-2011 on the mur-47 tree 41c174c80 -- a cite is only true with its hash). (3) THE NEAR MISS, and the one the parent had to repair: the kid passed the new testable_claim value with its punctuation already stripped -- the delivered claim had 0 backticks and 0 apostrophes against the pre-round original 20 and 8, so "the hook's own message" read "the hook own message" and every code span lost its ticks. parse_script (`def parse_script` at write.py:566 @41c174c80; :572 on the seat after rung 3) splits a verb chunk by arity and never edits the value, so the loss was in how the kid built the command, not in the writer. The parent rebuilt the value from the pre-round bytes with only the cite replaced (dispatch.py:1903-1905 @b6d3902ff, plus the GIT_CONFIG_* line numbers) and re-ran write.py set: 22 backticks / 7 apostrophes restored, the single missing apostrophe being the removed "L4.311 parent's environ" phrase. A round that fixes a cite by flattening the prose is a worse record than the one it corrected. (4) DEVIATION: the parent re-wrote a node the brief scoped to the kid, because the kid's own delivered artifact carried the defect; the parent review edit uses the same sanctioned write.py path.
<!-- THOUGHT:END -->
