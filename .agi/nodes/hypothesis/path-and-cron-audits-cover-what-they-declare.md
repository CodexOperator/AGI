---
id: hypothesis:path-and-cron-audits-cover-what-they-declare
mint_id: d0968a4b576040c88c0f4a22d04dad38
type: hypothesis
parents:
  - goal:g15.27
next_edges: []
confidence: 0.75
edited_by: director-engine
scaffold_hash: 0ac64d8d847393ff
season: 2
testable_claim: After the fix, paths.py audit with no dir lists every tracked repo file (git ls-files from the repo top, not from .agi; paths.py:13-14, :42) so a /home/<user> literal under extensions/agi/bin is reported; paths.findings refuses by name when a box cell is unset instead of returning a clean [] (paths.py:23-36); boxes.py reads its cell names and placeholder keys from the [box] schema instead of the literals at boxes.py:21-23, with test_paths_audit.py's fixture writing a [box].md; and crons.py audit names every box-gated job without why_box, not only KNOWN_JOBS (crons.py:1081); each proved by a committed test red on the pre-fix bytes, the touched files' existing tests green.
title: "FR-D2: the path and cron audits cover what they declare -- repo-wide paths audit, fail-closed findings, schema-read box cells, why_box for every gated job (0921 residue batch, engine slice; assigned: director-engine)"
town: core
---
# hypothesis:path-and-cron-audits-cover-what-they-declare

# hypothesis:path-and-cron-audits-cover-what-they-declare

## Hypothesis

```
batch      0921 residue batch, engine slice, chunk 2 (goal:g15.27) · fix round FR-D2 · sources: l4-config-max #3 #4 #8 #12 · l4-the-cron-node #8
verified   director-engine 10:5xZ 09-23 on the post branch:
  1 paths.py:13-14 `git ls-files` runs with cwd = root, and main's --root default is <repo>/.agi (paths.py:42) -> a no-dir audit lists
    the graph only and never sees the extensions/agi/bin/*.py baseline it was built to track
  2 paths.py findings() (:23-36) returns a clean [] with a box cell unset; only main() refuses (the claim says classify fails closed)
  3 boxes.py:21-23 _BOX_CELLS / _PLACEHOLDERS re-declare the [box] schema's cells (its placeholder map exists only as comments);
    test_paths_audit.py:29-35 _graph() writes no [box].md, so 6 tests pass through the boxes.py fallback
  4 crons.py:1081 flags a box gate without why_box only `if name in KNOWN_JOBS`; [cron].md:10 says a gated job MUST say why
proves     committed tests, each red on the pre-fix bytes: a repo-wide no-dir audit reports a /home/<user> literal under extensions/ ·
           findings() with an unset cell refuses by name · boxes.py reads cells + placeholders from the schema (literals gone; the
           fixture writes a [box].md) · crons audit names an unknown job's box gate without why_box · the touched files' tests green
```

## Agent Notes
assigned: director-engine (0921 residue batch, engine slice, goal:g15.27); minted by director-engine after verifying the bytes.
