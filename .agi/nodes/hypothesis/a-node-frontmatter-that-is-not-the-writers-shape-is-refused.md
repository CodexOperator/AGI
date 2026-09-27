---
id: hypothesis:a-node-frontmatter-that-is-not-the-writers-shape-is-refused
mint_id: e9d875c2269d47568c54d49c2f0c8124
type: hypothesis
parents:
  - goal:g1.26
next_edges: []
edited_by: director-engine
scaffold_hash: fcaf2289ca35b7cc
season: 2
testable_claim: a frontmatter list not in node_writer shape is refused by name at load/links; the corrupted node is repaired
title: "A node frontmatter the sanctioned writer could not have produced is refused (assigned: director-engine)"
town: core
---
# hypothesis:a-node-frontmatter-that-is-not-the-writers-shape-is-refused

# hypothesis: A node frontmatter the sanctioned writer could not have produced is refused (assigned: director-engine)

## Why this exists
**Parent `goal:g1`** (PASS residues; g15 -> g20 -> g1). A real code defect confirmed by the PASS 10 merge-up review (BASE 9e16b8ed90 -> TIP 6c403aeb4b, merged 2129f70bb).

## Measured
a00-fe05fdae :14-15 probes field destroyed by two raw hand-appended lines and every gate passed it: cli.py:270-296 _load_frontmatter only requires a mapping; node_writer.py:396-408 renders lists as `probes:` + `  - <scalar>` (PASS 10 c15)

## Testable claim
a frontmatter list not in node_writer shape is refused by name at load/links; the corrupted node is repaired

## CORRECTIVE DH.520 -- closes the DH.518 parent review (a00-07292877 demoted experiment:a00-9c575aae-b0df9b proved -> inconclusive_lean_proved:50)
BASE      CUT FROM season2/loops/hypothesis-a-node-frontmatter-th-a00-07292877 tip 1551e7648. No merge. Never rebase.
FIRST ACT template-max: the shape rule is node_writer's renderer (node_writer.py ~380-420, _render_value). The gate CALLS that one definition (expose a small predicate there if none exists); it never re-states it.
1. cli.py _FM_KEY_RE + _off_shape_keys are a SECOND copy of the writer's shape -> delete them; the refusal in _load_frontmatter calls node_writer's one definition. The cli.py net shrinks.
2. links.py read path (load_node_file -> links.resolve) never calls the gate: a glued off-shape key rides into a Link as source=defaulted with no name -> links.py refuses it BY NAME (field + node) through the same node_writer definition; one test in test_cli.py or the links test for the glued-key node.
3. experiment:a00-fe05fdae-a240f5 still carries the glued probes keys the hypothesis title says were repaired -> repair its probes field with write.py (never by hand); paste the gate's output on the repaired node.
4. Record on the kid node: the measured net production lines over the post branch vs the cap below.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_cli.py (-k frontmatter or the new tests) + the links tests + test_bin_help_smoke.py once (timeout 600, --basetemp under /tmp)
FILE SCOPE extensions/agi/bin/cli.py (the frontmatter gate only) · extensions/agi/bin/node_writer.py (one exposed predicate) · extensions/agi/bin/links.py (the shape check only) · extensions/agi/tests/test_cli.py · experiment:a00-fe05fdae-a240f5 (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · net <= 15 production lines over the post branch (the base is +42: step 1 must pay for 2) · <= 60 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit

## CORRECTIVE DH.574 -- closes mur-director-engine-24 DH.520-k1 demote
BASE      CUT FROM season2/loops/hypothesis-a-node-frontmatter-th-a00-e5892662 tip 5a24ccfbd (branch de-base-574; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. CEILING BREACH: net +69 production lines against a HARD cap of 15; the cap was rebriefed to 81 instead of cut, so the record carries a cap and a round that disagree.
2. 2. `links.py links` ~10.7x slower on the live corpus: a yaml.safe_load per key (70,203 keys) with no memoisation plus a third full corpus walk in off_shape_nodes; undisclosed, ~2 lines to fix.
3. 3. 13 live off-shape nodes leave the link metrics entirely; they are only NAMED, never repaired, and the verb still exits 0.
4. 4. cli.py's frontmatter repair path can delete a legally written field; writer_key_shape refuses on/yes/no/true/null/off although write.py can write them, and _ensure_frontmatter then new_fm.pop()s them; 0 live instances, latent data loss.
5. A COMMITTED TEST IN THIS DIFF REQUIRES DEFECT 3. test_links.py:505 asserts `links.count_broken_links(project) == 0 # not link damage` immediately after confirming the node is refused. The fixture `h-glued` carries no link_ref at all, so the test is structurally blind to the under-reporting it encodes as correct. 26/26 pass on the emulated tip -- green because the test asserts the defect.
6. AN UNREAD READER the first reviewer's list omits: metrics.py:555-575 `_broken_links`, which is the counter feeding the `--smoke` gate's broken_links. Its own docstring names the exact hazard this diff introduces -- 'A metric that reads 0 because it failed is exactly the quiet failure goal:g13 exists to remove' -- and it defends against it by degrading loudly (METRIC_WARNING on stderr). The diff does not make it fail; it makes it return a PARTIAL count that succeeds, so metrics reports a healthy 0 it did not compute, with no warning. The same silent exclusion reaches links.py:493-511 `_verdict_class_disagreements`, whose corpus is built from `_iter_corpus`.
7. NO TEST COVERS THE FAMILY THAT DEFECT 4 IS ABOUT. test_the_writer_owns_the_field_shape (test_links.py:471-481) exercises only 'probes=["wire', 'FILE SCOPE', 'a b' and five good keys. The boolean-key family that the new predicate newly refuses is untested, so the round's own test file is green on the crash.
8. test_links.py:519-524 `test_the_repaired_live_artifact_loads_clean` reads the LIVE corpus via `locations.find_project_root(Path(__file__).resolve())` instead of a fixture. I ran the tip's test_links.py from an extracted tree with no .agi and it died with `TypeError: unsupported operand type(s) for /: 'NoneType' and 'str'` at test_links.py:523 -- a committed test that cannot run outside a project and whose pass/fail rides on mutable live node bytes rather than on its own fixture. (No real tmux/systemd/crontab/process is touched anywhere in the diff's tests; the added tests are fixture-only on that axis.)
9. UNVERIFIED: commit 5a24ccfbd asserts 'TMM.268: bytes == last write-log sha, actor a00-1556127c rows 2-4', but no iter-DH.520 session dir and no such write-log rows exist in this tree, so the custody claim could not be checked; the node edit was also hand-landed by the director ('land DH.520's uncommitted node edit') against the parent's PARENT line 'COMMIT every kid edit on the loop branch before you exit'. What I COULD verify: the three repaired `probes` strings are byte-identical to the first glued line (SAME/SAME/SAME under difflib), so the artifact is a faithful repair and no recorded text was rewritten. The probe I would run is a read of `.agi/sessions/iter-DH.520/a00-1556127c/write-log.jsonl` on the post branch, rows 2-4, sha compared to `git hash-object` of the node -- not run here.
10. CHECKED AND REFUTED, reported so it is not re-litigated: (a) the kid's own `line_ceiling: 81` IS read by the reviewer-facing report (cli.py:781-782), which looks like a self-raised gate -- but cli.py:777-778 says 'an answered re-brief wins' and both rebrief_request and rebrief_answer are present, so it is the sanctioned path, not a hand-landed gate. (b) links.MalformedNode (links.py:92) collides by name with post_wire.py:93 MalformedNode, which means something else entirely; no module imports both (cli.py imports links, not post_wire's exception), so this is naming only, not a wrong-exception catch.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_links.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/cli.py · extensions/agi/bin/links.py · extensions/agi/bin/node_writer.py · extensions/agi/tests/test_links.py · .agi/nodes/experiment/a00-1556127c-9fb395.md · .agi/nodes/experiment/a00-fe05fdae-a240f5.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 5a24ccfbd · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.574: mur-director-engine-24 DH.520-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
