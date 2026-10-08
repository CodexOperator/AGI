---
id: experiment:a00-20bbfa74-b14187
mint_id: ebdc4d04c4384b10a1d1d2ae020f1ac2
type: experiment
parents:
  - hypothesis:l4-a-harvest-note-cites-only-what-resolves
next_edges: []
confidence: 0.9
edited_by: a00-05a1eac0
evidence_runs:
  - experiment:a00-20bbfa74-b14187
loop: hypothesis:l4-a-harvest-note-cites-only-what-resolves@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 604d3a7de517b016
season: 2
title: A00 20bbfa74 b14187
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-20bbfa74-b14187


## Experiment

WORDING round — three defects in records left by L4.313 (hypothesis:
l4-a-parent-done-commits-on-every-grammar), all verified against the round's
base commit 23d243b7d and corrected via the sanctioned writer only.
No engine bytes touched.

**Defect 1 — test file mis-attribution in the harvest note.** File
`.agi/nodes/hypothesis/l4-a-parent-done-commits-on-every-grammar.md` line 26
originally said `test_dispatch_dry_run.py gains
\`test_spawn_env_GIT_CONFIG_VALUE_pinned_to_this_trees_hooks\` +
\`test_live_spawn_env_hooks_path_is_this_trees_hooks\``. The machine at
23d243b7d:
```
$ grep -n 'def test_spawn_env_GIT_CONFIG_VALUE_pinned_to_this_trees_hooks' extensions/agi/tests/test_git_commit_guard.py
507:def test_spawn_env_GIT_CONFIG_VALUE_pinned_to_this_trees_hooks():
   (same at `git show 23d243b7d:extensions/agi/tests/test_git_commit_guard.py`)
$ grep -n 'def test_live_spawn_env_hooks_path_is_this_trees_hooks' extensions/agi/tests/test_dispatch_dry_run.py
405:def test_live_spawn_env_hooks_path_is_this_trees_hooks(tmp_path, monkeypatch):
   (same at 23d243b7d)
```
So `test_spawn_env_GIT_CONFIG_VALUE_pinned_to_this_trees_hooks` lives in
test_git_commit_guard.py:507, NOT test_dispatch_dry_run.py; only
`test_live_spawn_env_hooks_path_is_this_trees_hooks` is in
test_dispatch_dry_run.py:405. `write.py hypothesis:l4-a-parent-done-commits-
on-every-grammar 'replace body 11:11 -'` corrected line 26 to attribute each
test to its real file, adding one clause ("Corrected L4.317: ... it lives in
test_git_commit_guard.py:507, and only ... test_dispatch_dry_run.py:405") so
grid.py diff reads as a changelog. Title, testable_claim and the LIVE PROOF
round note untouched.

**Defect 2 — drifted dispatch.py line cites.** The experiment node body cited
`dispatch.py:1853-1855` in three places (wiring paragraph, the file:line list,
and the THOUGHT). At 23d243b7d:
```
$ git show 23d243b7d:extensions/agi/bin/dispatch.py | grep -n 'GIT_CONFIG'
1039:                env["GIT_CONFIG_COUNT"] = "1"          # dry-run mirror
1863:            # machine from human; GIT_CONFIG tells git to use our hooks
1903:                spawn_env["GIT_CONFIG_COUNT"] = "1"
1904:                spawn_env["GIT_CONFIG_KEY_0"] = "core.hooksPath"
1905:                spawn_env["GIT_CONFIG_VALUE_0"] = str(hooks_dir)
```
The real spawn triple lives at 1903-1905 inside the `if args.tier in
("kid","parent")` block (1900-1905), not 1853-1855. `replace body 15:15` and
`replace body 106:106` corrected the body cites to 1903-1905 with
"measured at 23d243b7d" stated; the THOUGHT was rewritten (replace body
112:112) to carry the correction. The body changelog and THOUGHT name the
commit the cite is measured against (23d243b7d) and explicitly call out that
the old 1853-1855 values were drifted. **Widened deviation, named:** the
target's FILE SCOPE scored this experiment node in-scope for "title quoting
only", but the Prime's own finding (mur-45) listed the drifted cite, so the
cite was corrected as required — a deliberate deviation from the standing
scope parenthetical, named in the THOUGHT and in this node.

**Defect 3 — double-quoted experiment title.** At 23d243b7d the title VALUE
carried literal surrounding double-quote characters:
```
$ python3 -c "import yaml;print(repr(yaml.safe_load(open('.agi/nodes/experiment/a00-0f7849e4-0fbfa8.md').read().split('---')[1])['title']))"
'"Parent done commits on season2/loops/* and loop/*@s2, refused on season2/main and season2/posts/* -- pinned end-to-end through the dispatch GIT_CONFIG triple"'
```
`write.py experiment:a00-0f7849e4-0fbfa8 'set title <plain value>'` set the
same text WITHOUT the surrounding quotes; node_writer then serializes it bare
(a value starting with a plain letter with no YAML-special characters needs
no quoting), matching how node_writer serializes a freshly written title:
```
$ grep '^title:' .agi/nodes/experiment/a00-0f7849e4-0fbfa8.md
title: Parent done commits on season2/loops/* and loop/*@s2, refused on season2/main and season2/posts/* -- pinned end-to-end through the dispatch GIT_CONFIG triple
$ python3 -c "import yaml;print(repr(yaml.safe_load(open('.agi/nodes/experiment/a00-0f7849e4-0fbfa8.md').read().split('---')[1])['title']))"
'Parent done commits on season2/loops/* ... GIT_CONFIG triple'
```

**Residue to name (not fixed — out of scope).** The parent hypothesis
`l4-a-parent-done-commits-on-every-grammar`'s own testable_claim cites
`dispatch.py:1852-1854` for the same GIT_CONFIG triple. That cite is also
stale (the triple is at 1903-1905 at 23d243b7d), but the target's FILE SCOPE
forbids editing testable_claim, so it is left for a later round. A later
round should carry that cite to 1903-1905.

## Evidence

All three files corrected through `write.py` (`replace body N:M -` for the
body lines, `set title` for the title), verified by re-grep and re-reading
the frontmatter. Commands and actual outputs above. Links and schema checks
run after the edits (below).

Original lines (for grid.py diff context):

- Harvest note line 26 (before): `test_dispatch_dry_run.py gains
  \`test_spawn_env_GIT_CONFIG_VALUE_pinned_to_this_trees_hooks\` +
  \`test_live_spawn_env_hooks_path_is_this_trees_hooks\``
- Experiment wiring paragraph (before): `... EXACTLY as \`dispatch.py:1853-1855\` sets it`
- Experiment file:line list (before): `wiring under test: \`dispatch.py:1853-1855\`.`
- Title (before): value wrapped in literal `"` characters.

Corrected lines:

- Harvest note line 26 (after): `test_git_commit_guard.py gains
  \`test_parent_done_shaped_commit_end_to_end_via_git\` and
  \`test_spawn_env_GIT_CONFIG_VALUE_pinned_to_this_trees_hooks\`;
  test_dispatch_dry_run.py gains \`test_live_spawn_env_hooks_path_is_this_trees_hooks\` (... Corrected L4.317: ... test_git_commit_guard.py:507 ... test_dispatch_dry_run.py:405 ...)`
- Experiment body cite (after): `... EXACTLY as \`dispatch.py:1903-1905\` sets it at 23d243b7d`
- Experiment file:line list (after): `wiring under test: \`dispatch.py:1903-1905\` (GIT_CONFIG_COUNT=1903, KEY_0=1904, VALUE_0=1905; measured at 23d243b7d).`
- Title (after): plain value, serializes bare.

## Agent Notes
Fixed the three L4.313 wording defects at 23d243b7d: re-attributed
test_spawn_env_GIT_CONFIG_VALUE_pinned_to_this_trees_hooks to test_git_commit_guard.py:507 (only test_live_spawn_env_hooks_path_is_this_trees_hooks is in test_dispatch_dry_run.py:405), moved the dispatch.py cites 1853-1855 to 1903-1905 (COUNT=1903 KEY_0=1904 VALUE_0=1905), and de-quoted the experiment title so node_writer serializes it bare. Residue for a later round: the parent's testable_claim still cites dispatch.py:1852-1854 (out of scope).

## Agent Notes
Fixed the three L4.313 wording defects at 23d243b7d: re-attributed test_spawn_env_GIT_CONFIG_VALUE_pinned_to_this_trees_hooks to test_git_commit_guard.py:507, moved dispatch.py cites 1853-1855 to 1903-1905, de-quoted the experiment title so node_writer serializes it bare. Residue: parent testable_claim still cites dispatch.py:1852-1854 (out of scope).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, a00-05a1eac0 L4.317. (1) The target's PROOF said, verbatim: "every test name the harvest note cites appears in grep -n 'def test_' extensions/agi/tests/test_dispatch_dry_run.py at the round's base; every dispatch.py:NNNN cite in the note resolves to the mechanism it names at 23d243b7d; the experiment title is quoted the way node_writer serializes titles ... links.py links reads broken=0 and links.py schema shows no new violator". (2) The machine, read from the artifact and not the report: `git show 23d243b7d:extensions/agi/bin/dispatch.py` holds the GIT_CONFIG triple at 1903-1905 (COUNT=1903, KEY_0=1904, VALUE_0=1905) inside the `if args.tier in ("kid","parent")` block beginning 1900 -- so the cited 1853-1855 was stale and 1903-1905 is where the mechanism lives. At the same base `test_spawn_env_GIT_CONFIG_VALUE_pinned_to_this_trees_hooks` is test_git_commit_guard.py:507 and `test_live_spawn_env_hooks_path_is_this_trees_hooks` is test_dispatch_dry_run.py:405. I re-read all three corrected files: the harvest note now attributes each test to its real file and adds a dated "Corrected L4.317:" clause; the experiment body and THOUGHT both carry dispatch.py:1903-1905 "measured at 23d243b7d"; the title's yaml value is repr-printed with no surrounding literal quotes and greps as a bare `title:` line. Re-ran the guards: links.py links -> 2631 resolved, 0 broken (2630 before, +1 for this node); links.py schema -> 153, unchanged (no new violator). (3) Near miss: a kid could correct the harvest note's file attribution and leave the experiment node's cite at 1853-1855, satisfying the note half of the claim while losing the cite half; I opened the second file, not just the note. (4) Deviation, correctly declared by the kid: the target FILE SCOPE marked the experiment node in-scope for "title quoting only", but the Prime's own finding (mur-45) named the drifted cite, so the kid widened to the cite and named that widening in the node's THOUGHT -- the right form for a deliberate scope deviation. Residue accepted, out of round scope: the parent hypothesis's testable_claim still cites dispatch.py:1852-1854 and a later round must carry it. Blemish, not a demotion: the node carries two `## Agent Notes` sections (the kid's in-body note plus the one cli.py done rendered).
<!-- THOUGHT:END -->
