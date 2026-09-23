---
id: experiment:a00-baa8e365-a4a8cb
mint_id: 74e5d08651f14ecba74ef1d18c9e09e9
type: experiment
parents:
  - hypothesis:mur-0921-engine-residues-dispositioned-and-corrected
next_edges: []
confidence: 0.75
edited_by: a00-baa8e365
evidence_runs:
  - experiment:a00-baa8e365-a4a8cb
line_ceiling: 40
loop: hypothesis:mur-0921-engine-residues-dispositioned-and-corrected@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "verdict-intact", "class": "gate", "cmd": "re-read the `verdict:` frontmatter of all 13 changed nodes and compare to the pre-round values captured before any write", "expected": "byte-identical for every node -- no correction changes a verdict/lean/confidence field", "observed": "all 13 identical: 6 proved, 5 inconclusive_lean_* :N, unchanged; PASS", "result": "pass"}
  - {"conjunct": "probes-are-lists", "class": "gate", "cmd": "load frontmatter.probes for the five converted nodes and assert isinstance(list)", "expected": "five YAML lists, not quoted scalars, with every probe string preserved", "observed": "a00-794503d4 list2, a00-09d5b982 list4, a00-f0f7f404 list4, a00-3a04e059 list1, a00-931b52d8 list1; PASS", "result": "pass"}
  - {"conjunct": "no-broken-links", "class": "wire", "cmd": "python3 extensions/agi/bin/links.py links on this worktree after every write", "expected": "0 broken", "observed": "3980 resolved, 0 broken; PASS", "result": "pass"}
  - {"conjunct": "false-detached-unit-line-gone", "class": "gate", "cmd": "grep the a00-3a04e059 body for the literal `Ladder cells added live` outside the THOUGHT, and grep rotate.py for `_run_alarms_unit`/`--detach`", "expected": "the false body line gone; both identifiers absent from the engine bytes", "observed": "`Ladder cells added live` appears only inside the new THOUGHT that names it; `grep -n '_run_alarms_unit\\|--detach' extensions/agi/bin/rotate.py` = 0 hits; PASS", "result": "pass"}
  - {"conjunct": "last-kid-edits-present", "class": "gate", "cmd": "one grep per file for each of the nine last-kid edits", "expected": "all nine present and coherent", "observed": "all nine matched: path_max NOT DELIVERED; Boundary DEFERRED BY NAME; KEPT by design; MORAL region; no systemd-run; 4 tracked files; holds ZERO ampersand pairs; nudge_sweep; is public; PASS", "result": "pass"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 30d43c0430f9f934
season: 2
title: "The 11 experiment-node C residues of the 0921 engine batch corrected in place: probes lifted to real lists, stale counts and detached-unit claims dropped, nine last-kid edits verified"
town: core
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-baa8e365-a4a8cb

## Experiment

Round EF.23 scope: the ELEVEN experiment-node C items of
hypothesis:mur-0921-engine-residues-dispositioned-and-corrected. The seven
hypothesis-node C items plus the two file C items were the previous kid's
scope (agent a00-11797ce4, experiment:a00-11797ce4-ddb8cb); its nine edits are
verified still present below. Every item here was re-checked against the bytes
in this worktree and applied IN PLACE through the sanctioned writer
(`python3 extensions/agi/bin/write.py`, verbs `set`, `body_patch`, `thought`).
No verdict, lean or confidence field was changed, and no engine file was
touched.

### Item ledger (one line per item)

1. `exp:a00-c2bcfc6a-03c123` -- APPLIED. The body read as a clean build while
   the verdict is `inconclusive_lean_disproved:60`; the Experiment section and
   Agent Notes now name the cause -- a pid-null kid counted live because
   `_rec_pid` maps null/0 to 0 and the production pi adapter answers
   `is_alive(0) == True` (`adapters/pi_adapter.py:224` `os.kill(0,0)`
   fallback), the `pid > 0` guard the rest of the reaper keeps
   (dispatch.py:3083/3119, heal.py:472) having been dropped in this helper.
   File `.agi/nodes/experiment/a00-c2bcfc6a-03c123.md`.
2. `exp:a00-794503d4-628fb0` -- APPLIED + VERDICT-QUESTION. Restored the
   truncated second (refusal-atomic) probe from the body Evidence, and
   narrowed the title and Experiment text from "agrees in every reachable
   state" to a DECLARED-LOCATION base (the location-only-edit bypass survives:
   write.py:1912-1922 reads only `edit.set_fm`, never `unset_fm`). The node's
   own THOUGHT already says `-- FALSE`, so `inconclusive_lean_proved:70`
   overclaims and the honest class is `lean_disproved`; recorded in the
   THOUGHT and in the report, field NOT changed. File
   `.agi/nodes/experiment/a00-794503d4-628fb0.md`.
3. Probe-field shape -- APPLIED (five nodes). `probes:` was a quoted scalar
   (`cli._parse_probes` returns None for it) where `[experiment].md:18` wants a
   YAML list. Converted to a real list with every probe string verbatim:
   `a00-794503d4-628fb0`, `a00-09d5b982-1fe871`, `a00-f0f7f404-aceba1`,
   `a00-3a04e059-da77bd`, `a00-931b52d8-2c24f6`.
4. `exp:a00-dab18263-f2f8c4` -- APPLIED. The node had no `probes:` field;
   Probes A (parser), B (harvest resolution, with its REUSE_SCAFFOLD caveat)
   and C (wire) were lifted verbatim from the THOUGHT (:109-127) into a real
   list. File `.agi/nodes/experiment/a00-dab18263-f2f8c4.md`.
5. `exp:a00-2e6aafdb-b5acf1` -- APPLIED. The node last committed a41b65791,
   before re-scope 3626f0eb3; its four probes (conjuncts 2/2/3/4) and its
   parent review restate the PRE-RE-SCOPE pending-key claim, while the current
   conjuncts are (2) read tree, (3) key_history never authorizes, (4)
   `.key.pending` stays out. The probes are now labelled `pre-re-scope <n>`
   and the THOUGHT says so.
6. `exp:a00-3a04e059-da77bd` -- APPLIED. `production_lines` 81 -> 78 (kid
   commit a63959d87 carries rotation_alert.py 78/3 only), the false "Ladder
   cells added live" line dropped (the cells landed later, in ceaa79618), and
   the body notes its `proved` rests on a deliverable the round's diff lacks.
7. `exp:a00-81fb6a5d-63f6f9` -- APPLIED. `production_lines` 77 -> 62 (kid
   commit 8ca78e04c carries rotate.py 62/6 only; the crons.md 11 + ladder.md 4
   counted into 77 were never in it). The title and body claimed an alarms dm
   and a detached user unit; neither exists (`cmd_alarms` rotate.py:7237 calls
   `_master_rotate` and sends no dm; `_run_alarms_unit`/`--detach` deleted in
   20e848493).
8. `exp:a00-d7588719-d59894` -- APPLIED. Title and body marked SUPERSEDED:
   `_run_alarms_unit` and `alarms --detach` were deleted in 20e848493 and
   `grep` finds neither in `extensions/agi/bin/rotate.py`.
9. `exp:a00-39a8276d-9dfd67` -- APPLIED. The conjunct-3 probe and the THOUGHT
   said the post-change grep returns "12 residual lines"; corrected to 7 (12
   was the PRE-change count, and the node's own title already says 7 non-self
   residuals / 4 files / 7 lines).
10. `exp:a00-dd617306-ee4cd1` -- APPLIED. Four internal contradictions
    reconciled against its own lines, no number invented: 18/18 -> 16 of 18;
    "18 parent-dead rounds" vs the committed probe's "17 rows" (both stated,
    17 named as the committed-probe figure; row 18 has no `death` key);
    `death.evidence null on all 18` -> the 17 rows that carry a `death` key;
    `dispatch.py never calls systemd-run` -> dispatch.py:2668 ->
    `mem_cap.wrap_argv` -> mem_cap.py:67-75 wraps the spawn in
    `systemd-run --user --scope`, and only the parent's unit NAME stays
    UNKNOWN.
11. `exp:a00-b0575ad8-e27a4c` -- APPLIED. "closes the last clause-(2) hole"
    -> the VERB-ONLY half of clause (2) is closed; clause (2a) -- a prose
    argument quoting a verb-led command literally -- is STILL OPEN, pinned by
    `extensions/agi/tests/test_write.py:2039`.
12. `hypothesis:lm-research-review-why-brainstorm-mint-by-default` and
    `experiment:a00-2ec3b4a6-b531ae` -- SKIPPED (excluded by the dispatch
    order; thought-side nodes, TM decides).

No item was `already-correct` or `stale-citation` in the residual sense: each
named a genuinely stale line, and each cited engine file was re-read (never
edited) so the correction cites what the bytes say now. `l4-quick-migrate`,
which the last kid touched, was already left correct.

### The nine last-kid edits -- verified present, no repair needed

One grep per file confirms all nine: `path_max` NOT DELIVERED in
`hypothesis:l4-config-max-and-template-max-are-required-verdict-fields-of-every-merge-up-review-and-a-named-line-of-every-dispatch-order.md`;
`## Boundary` DEFERRED BY NAME in
`hypothesis:l4-quick-migrate-...`; `KEPT by design` in
`hypothesis:l5-a-message-...`; `MORAL region` in
`hypothesis:l5-moral-one-...`; `no systemd-run` in
`hypothesis:l5-the-meter-...`; `4 tracked files` in
`hypothesis:l5-tracked-files-...`; `holds ZERO ampersand pairs` + authored
body in `hypothesis:l5-write-py-splits-...`; `nudge_sweep` in
`.agi/context/schemas/[cron].md`; `is **public**` in `QUICKSTART.md`.

## Evidence

Node ids changed, all via `write.py`, all under `.agi/nodes/experiment/`:
`a00-c2bcfc6a-03c123`, `a00-794503d4-628fb0`, `a00-09d5b982-1fe871`,
`a00-f0f7f404-aceba1`, `a00-931b52d8-2c24f6`, `a00-dab18263-f2f8c4`,
`a00-2e6aafdb-b5acf1`, `a00-3a04e059-da77bd`, `a00-81fb6a5d-63f6f9`,
`a00-d7588719-d59894`, `a00-39a8276d-9dfd67`, `a00-dd617306-ee4cd1`,
`a00-b0575ad8-e27a4c`.

Read-only checks, run on this worktree:

```
$ python3 extensions/agi/bin/links.py links
links: 3980 resolved, 0 broken (18 retired payload(s), not damage)

$ # every changed node re-read: verdict field byte-identical to its pre-round value
a00-c2bcfc6a-03c123  inconclusive_lean_disproved:60  OK
a00-794503d4-628fb0  inconclusive_lean_proved:70     OK
a00-09d5b982-1fe871  inconclusive_lean_disproved:35  OK
a00-f0f7f404-aceba1  proved                          OK
a00-931b52d8-2c24f6  proved                          OK
a00-dab18263-f2f8c4  proved                          OK
a00-2e6aafdb-b5acf1  proved                          OK
a00-39a8276d-9dfd67  inconclusive_lean_proved:65     OK
a00-3a04e059-da77bd  proved                          OK
a00-81fb6a5d-63f6f9  inconclusive_lean_disproved:55  OK
a00-d7588719-d59894  proved                          OK
a00-b0575ad8-e27a4c  inconclusive_lean_proved:80     OK
a00-dd617306-ee4cd1  proved                          OK

$ # all five converted probe fields, re-read from frontmatter
a00-794503d4-628fb0 list 2  a00-09d5b982-1fe871 list 4
a00-f0f7f404-aceba1 list 4  a00-3a04e059-da77bd list 1
a00-931b52d8-2c24f6 list 1  a00-dab18263-f2f8c4 list 3
```

Production lines: 0 engine/test lines. The round edits node text only; the
`probes:`/`production_lines:` fields are graph metadata, and no file under
`extensions/`, `skills/` or `src/` was touched. `line_ceiling` 40 (the
dispatch default) is recorded in frontmatter.

## Verdict

`inconclusive_lean_proved:75`. Eleven of eleven in-scope items were re-checked
against the bytes and corrected in place; the nine last-kid edits are present
and coherent; verdicts are intact; `links.py` reports 0 broken. It is NOT
`proved` because this round's own probes are verification of the edits, not
independent witnesses to the parents' claims -- the truths corrected here rest
on the cited engine bytes, and one item (a00-794503d4) carries an unresolved
verdict question the parent owns.

## Agent Notes
Applied the 11 experiment-node C items of
hypothesis:mur-0921-engine-residues-dispositioned-and-corrected (the previous
kid took the 7 hypothesis + 2 file items, all nine verified still present). Two
verdict questions surfaced and were recorded, not resolved:
`exp:a00-794503d4` should read `inconclusive_lean_disproved` (its own THOUGHT
says FALSE), and `exp:a00-dd617306`'s tree-wide count is 16 of 18 with the
committed probe's 17 vs the tabulated 18 reconciled by name. No verdict, lean
or confidence field was changed; no engine file was touched; 0 production
lines. `skipped`: hypothesis:lm-research-review-why-brainstorm-mint-by-default
and experiment:a00-2ec3b4a6-b531ae (thought-side, excluded by the order).

DONE experiment:a00-baa8e365-a4a8cb
caveats: a00-794503d4's `inconclusive_lean_proved:70` and a00-dd617306's
  verdict header remain as their authors set them -- this round corrected the
  text around them but left every verdict field untouched by rule.
struggles: the `write.py` script parser still splits a verb's free-text
  argument at an ampersand pair followed by a verb name, so each THOUGHT had to
  be hand-sanitised (ampersand pairs spelled out) before `thought` would take
  it -- the same defect write.py's own open clause (2a) names.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
EF.23 round on hypothesis:mur-0921-engine-residues-dispositioned-and-corrected, experiment-node C scope (the eleven experiment-node items, disjoint from the previous kid's seven hypothesis plus two file items). Eleven of eleven items applied in place through write.py; no verdict, lean or confidence field changed; no engine file touched. Why each: item 1 hid a pid-null falsifier behind a clean-build body; items 2 and 9 carried stale overclaims ("every reachable state", "12 residual lines") that the nodes' own lines contradict; items 3 and 4 were probe-shape defects that made cli._parse_probes read None, so the probes were evidence no reader could collect; item 5's probes tested a claim the parent hypothesis had since re-scoped; items 6, 7 and 8 proved deliverables whose bytes the round's own diff (or a later delete) does not carry; item 10 held four self-contradictions; item 11 claimed the last clause-(2) hole closed while clause (2a) is pinned open. Two verdict questions were recorded rather than resolved: a00-794503d4 should read lean_disproved, and a00-dd617306's tree-wide count reconciles to 16 of 18 with 17 the committed-probe figure. The nine last-kid edits were verified present by one grep each; links.py reports 0 broken. This node carries its own probes as a real list and a 0 production-line count (node text only).
<!-- THOUGHT:END -->

## Agent Notes
Applied the 11 experiment-node C items of hypothesis:mur-0921-engine-residues-dispositioned-and-corrected; the nine last-kid edits verified present; 0 broken links; no verdict/lean/confidence field changed; 0 production lines (node text only).
