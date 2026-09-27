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

## CORRECTIVE DH.605 -- closes mur-director-engine-31 DH.574-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-a-node-frontmatter-th-a00-27f38c7b tip 17d7c3dbe (branch de-base-605; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. Repair path renames a writer-legal boolean key to `True: true` (node_writer.py:465)
2. 2. False-refusal class only partly closed: '2024'/'1.5'/'2024-01-01' still refused although `set 2024 <v>` is legal; pop is a no-op and render sorted() TypeError still kills `done` (node_writer.py:459)
3. 4. The new end-to-end test never repairs; the assertion reads an untouched file (test_links.py:517)
4. 7. 56 test lines against a hard 40 cap (test_links.py:485)
5. test_links.py:521 `assert fm2[True] is True` is a green test that REQUIRES the defect, and the first reviewer read only the tautology (their item 4). The line pins the YAML-collapsed Python bool key as the blessed end state: no reader of that node ever sees the field `on` again. Combined with 514-516, which names a false mechanism (cli.py:431-432 pops str(k) = "True", never "on"; and the pre-fix path raised TypeError per the node's own PROBE2), the round's single end-to-end assertion for its headline claim is evidence for the corruption it claims to prevent.
6. Coverage went down in the OTHER direction too, unremarked. The old test_the_repaired_live_artifact_loads_clean was the only test in the file that read the REAL node a00-fe05fdae-a240f5.md -- the exact artifact the parent claim's repair conjunct is about and the one the director hand-landed at 5a24ccfbd. After test_links.py:559-573 pins a tmp fixture instead, nothing in the suite holds that repair in place, so the repair's durability is unpinned and the node's ITEM 9 custody claim ('bytes == last write-log sha, actor a00-1556127c rows 2-4') remains uncheckable in any automated pass. Pinning the live read to a fixture was right; deleting the last live pin with no replacement is a coverage loss the round did not name.
7. node_writer.py:459's `not isinstance(k, (bool, type(None)))` is DEAD in production: line 447 is `k = str(key)`, so `k` is a `str` for the remainder of the function and the guard can never be False on any real call path (`_off_shape_keys` cli.py:274-276 and `off_shape_keys` links.py:105-107 pass raw mapping keys, and the only non-str key that can arrive is a bool, which str()s to "True" before the check). The symmetric check the surrounding docstring implies does not exist, and the defect the Parent Review PROBE4 names needs a render-side guard (key the mapping by the original spelling), not a predicate-side one.
8. The forgiveness set is larger than anything the diff tests. `~` resolves to None and is forgiven by node_writer.py:459, as are the case variants `On`, `NO`, `TRUE`, `Off` (all -> bool), every one of them legal under write.py's verb_set (no key character class, write.py:247-259) and emitted bare by node_writer.py:422. BOOLEAN_KEYS (test_links.py:485) covers none of them, and includes `nil`, which is NOT a YAML 1.1 null word -- it resolves to the string 'nil' and was already in shape via node_writer.py:457 before the fix, so that entry is decoration rather than evidence. A reviewer trusting the tuple as the rule would understate the surface the round actually widened.
9. UNVERIFIED (not run -- probe of the review pane's own tree is prohibited and none of the committed tests enters the repair path for this shape): the `True: true` rename and the surviving TypeError for int/float/date keys are derived by reading cli.py:429 + cli.py:432 + cli.py:462 together with node_writer.py:422/459/465, plus the artifact's own PROBE4 measurement. The probe I WOULD run, on a tmp graph root only: build a node with `id/type/mint_id` + `on: yes` and NO `parents`, call cli._ensure_frontmatter(project, path, project/'absent.json', 'experiment:e1'), then read the bytes; repeat with `2024: v` in place of `on: yes` to see the TypeError. Neither touches tmux, systemd, crontab or any process.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_links.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/node_writer.py · extensions/agi/tests/test_links.py · .agi/nodes/experiment/a00-3e7b260e-2cce33.md (write.py) · the kid's own node
CEILING   HARD CAP: 2 kids (k1 = node_writer.py key-shape + repair path + tests, k2 = links.py exit code on off-shape nodes) · <= 15 production lines net over 17d7c3dbe · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.625 -- closes mur-director-engine-35 DH.605-k1 accept_with_residue (no verify)
BASE      CUT FROM season2/loops/hypothesis-a-node-frontmatter-th-a00-49582ae0 tip d7ead8841 (branch de-base-625; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 281k-line duplicate engine tree swept into the round's commit outside FILE SCOPE (commit 176f100b2 added 582 files under nopin/) -- the PARENT removes the whole nopin/ tree from the loop branch in ONE commit (git rm -r -q nopin; commit by that path only) and pastes `git diff --stat <base> HEAD -- nopin | tail -1` (must print nothing) on its node; never git add -A.
2. The restored live pin hard-codes one mutable node's address and ERRORS when it is retired or renamed -- extensions/agi/tests/test_links.py:606 -- `live = root/'nodes'/'experiment'/'a00-fe05fdae-a240f5.md'` then `read_text` at :607 — measured: with a .agi present and that file absent the test FAILS with FileNotFoundError, and the repo's own convention is retire = move to .agi/nodes/deprecated/<type>/ (renames are routine: test_rename_post/test_post_rename/test_rotate_boundary_rename), so a legal graph event turns the engine suite red; the skip guard only covers the no-.agi case, which is not the death mode the base round documented.
3. Verdict node cites itself as its own evidence run -- .agi/nodes/verdict/a00-35cc6f8f-a593c7.md:11 -- evidence_runs[0] = `verdict:a00-35cc6f8f-a593c7`; evidence_gate.py:316-319 states a verdict may not cite itself (normalize_evidence_runs:299 discards it), so the entry is decoration that flatters the row without backing it.
4. Parent experiment still carries the pre-corrective demotion after the corrective was accepted -- .agi/nodes/experiment/a00-879cb9e8-625883.md:22 -- verdict: inconclusive_lean_disproved:40 stands while its child verdict:a00-35cc6f8f-a593c7 (inconclusive_lean_proved:75) closed both refuted items and the parent hypothesis still has no verdict field at all, so the loop will keep re-dispatching a conjunct set this round closed; no node write is needed for the code half, only this re-raise, and it must go through write.py.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_links.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE nopin/ (REMOVAL only, by the parent) · extensions/agi/bin/node_writer.py · extensions/agi/tests/test_links.py · .agi/nodes/experiment/a00-879cb9e8-625883.md · .agi/nodes/verdict/a00-35cc6f8f-a593c7.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over d7ead8841 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.625: mur-director-engine-35 DH.605-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
