---
id: experiment:a00-7ceb3085-36ab0b
mint_id: b76b3a14d8074ce38dc551f1d941c484
type: experiment
parents:
  - hypothesis:a-rounds-named-node-set-is-its-dispatch-time-ids-never-a-kid-supplied-parent
confidence: 0.85
edited_by: a00-7c2ef778
evidence_runs:
  - experiment:a00-7ceb3085-36ab0b
probes:
  - "wire probe: tmp root, real cmd_done, _auto_commit_worktree stubbed; OLD WIDENED=True / NEW WIDENED=False"
production_lines: 19
scaffold_hash: 519e081ba7c5e612
title: the kid --parent reached the sweep through the record key the fix meant to protect
verdict: proved
---
# the kid's --parent reached the sweep through the record key the fix meant to protect

## What I ran (probe, not a suite I inherited)
`extensions/agi/bin/cli.py` cmd_done mutates the agent record before the
commit sweep reads it:

| line (pre-fix) | what it does |
|---|---|
| `rec["parent"] = args.parent` | the KID's value lands in DISPATCH's field |
| `_round_named_node_ids(rec, args.parent)` | `del parent` kills the PARAMETER |
| `(rec or {}).get("parent")` | reads the KEY -- now the kid's value |

Wire probe (tmp root, no git, `_auto_commit_worktree` stubbed to capture
`named`/`refused`; `probe_rec_parent.py` in this round's session dir):

    record: target=hypothesis:real-target  parent=hypothesis:dispatch-time-parent
    argv:   done --parent doc:kid-supplied-foreign
    OLD bytes -> named = [real-target, doc:kid-supplied-foreign]   WIDENED
    NEW bytes -> named = [real-target, hypothesis:dispatch-time-parent, experiment:kid1-1]
                 refused = [doc:kid-supplied-foreign]  (named on stderr by
                 _round_own_node_paths, since it is not in `asked`)

## Fix (at the cause, not at the gate)
`cmd_done` preserves dispatch's value BEFORE the overwrite, under a key
nothing else writes:

    rec.setdefault("dispatch_parent", rec.get("parent") or "")
    rec["parent"] = args.parent

and `_round_named_node_ids` reads `dispatch_parent`, falling back to
`parent` ONLY for a record that never went through `cmd_done` (fixture,
older dispatch, direct unit call). `refused=[args.parent]` at the call site
is unchanged, so the kid's id is still NAMED on stderr -- it just no longer
feeds the set. The near-misses in the brief (drop `--parent` from the call
site; add a second refuse in `_round_own_node_paths`) were not taken.

## Counts I actually got
- probe: OLD `WIDENED: True` (exit 1) / NEW `WIDENED: False` (exit 0)
- `git grep -l _round_named_node_ids -- extensions/agi/tests` -> 1 file
  (test_cli.py)
- `pytest extensions/agi/tests/test_cli.py` -> **65 passed** (was 64; +1 new
  test `test_dispatch_parent_survives_the_done_parent_overwrite`)
- all five `test_cli*.py` -> **88 passed, 0 failed**
- `git diff --numstat extensions/agi/bin/cli.py` -> 19 added / 3 removed
  (ceiling 40)

## Caveat I did not close
The `parent` fallback keeps the widening alive for any FUTURE caller that
mutates `rec["parent"]` before invoking the sweep without the capture. The
capture is two lines above the sweep's only call site today, so the path is
closed in practice; a structural close (the sweep reads ONLY
`dispatch_parent`, breaking the DH.386-era unit tests) is a follow-up.

## Agent Notes
cmd_done preserved dispatch's parent under rec[dispatch_parent] before the kid overwrite; _round_named_node_ids reads it. Probe: OLD WIDENED=True, NEW WIDENED=False. test_cli.py 65 passed, all test_cli*.py 88 passed, 19 prod lines.

PARENT REVIEW DH.411 (a00-7c2ef778): ACCEPTED, verdict proved stands. Read the BYTES in commit d970411b8 (cli.py +22/-3, test_cli.py +22), not the result file; every deliverable the node names is in that commit. Four probes I ran myself, in a tmp tree, real cmd_done with only _auto_commit_worktree stubbed: (1) WIRE -- record parent=hypothesis:dispatch-time-parent, argv --parent doc:kid-supplied-foreign -> named=[hypothesis:real-target, hypothesis:dispatch-time-parent], swept only real-target, kid id NAMED on stderr; on the pre-fix bytes the same probe printed named=[..., doc:kid-supplied-foreign] (I measured that before dispatching this kid). (2) GATE -- a DISPATCH-time parent goal:g5 stays in the named set but _round_committable refuses it via the committed [goal] round_commit:false cell, named on stderr. (3) GATE -- a record with parent:null plus a kid --parent names nothing extra. (4) GATE -- config:posts, town:local-maxxing, doc:unified-head, goal:g7 all refused; doc:plain swept, i.e. the type gate discriminates rather than blanket-refusing. test_cli.py 65 passed (kid 64+1). The .geometry:case I probed as SWEPT is NOT a defect: nodes/.geometry/posts.md carries id config:posts / type config (checked, head of the file), so the geometry family is refused through its real id.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This version exists because the PARENT measured the old bytes before the kid did. (1) WHAT THE CLAIM SAID, quoted from the target: "done --parent never widens the set". (2) WHAT THE MACHINE ACTUALLY DID: cmd_done wrote rec["parent"] = args.parent at cli.py:1602 and _round_named_node_ids read (rec or {}).get("parent") at cli.py:2124, so the del parent that was supposed to protect the set deleted only the PARAMETER; my wire probe on a tmp tree got named=[hypothesis:real-target, doc:kid-supplied-foreign] from a record whose dispatch parent was hypothesis:dispatch-time-parent. The refused=[args.parent] safety net was inert for the same reason, because _round_own_node_paths only refuses an id `if nid not in asked` and the widened id was in asked. (3) THE NEAR MISS: keeping del parent and adding a second `if nid == args.parent: refuse` in _round_own_node_paths satisfies the words and leaves the record rewrite standing for the next caller; so does dropping --parent from the call site. The kid took neither -- it captured dispatch-time truth into a key nothing else writes, BEFORE the overwrite, and read that key. (4) DEVIATION: none. Residual, and the reason I stop rather than spawn again: _round_named_node_ids still falls back to rec["parent"] for a record that never went through cmd_done, so the guarantee is "the capture ran at the only call site today", not a structural one. A structural close (read dispatch_parent only) would break the DH.386-era unit tests and guards a hypothetical future caller; that is a push_further, not a falsifier I could run today.
<!-- THOUGHT:END -->
