---
id: experiment:a00-11797ce4-ddb8cb
mint_id: ffafdf0888314453975f99e563234582
type: experiment
parents:
  - hypothesis:mur-0921-engine-residues-dispositioned-and-corrected
next_edges: []
edited_by: a00-95359f56
line_ceiling: 40
loop: hypothesis:mur-0921-engine-residues-dispositioned-and-corrected@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - "negative: `grep -c path_max extensions/agi/workflows/merge-up-review.json` -> 0; had it been >0 the NOT DELIVERED correction would be false"
  - "negative: `grep -rn seat_record extensions/agi/bin/*.py` returns writers only (migrate_channel.py, rotate.py) and no reader, so cl.(2) 'nothing reads it' holds"
  - "verification: `grep -c nudge_sweep .agi/context/schemas/[cron].md` -> 1 after the edit; KNOWN_JOBS at crons.py:93-94 already carried nudge_sweep, so the schema now matches"
  - "negative: grep comms/undelivered in .agi/nodes/.geometry/ladder.md -> 0 while .agi/config.json:169 carries undelivered_after_minutes, so T is a config cell and not a ladder cell"
  - "verification: `python3 extensions/agi/bin/links.py links` -> 3979 resolved and 0 broken after all edits; the edited nodes and bodies are well-formed"
  - "negative: `grep -c 'the measured way experiment' .agi/nodes/hypothesis/l5-write-py-splits-a-script-only-at-an-ampersand-pair-that-begins-a-verb.md` -> 0, proving the link_ref causal attribution was removed"
  - "verification: `git diff --numstat` over the nine in-scope paths -> 56 added and 17 removed lines; below the 80-line 2x rebrief threshold"
production_lines: 56
profile: balanced
role: kid
scaffold_hash: 810cd4386df6224e
season: 2
title: "EF.23: applied the seven hypothesis-node and two file C-corrections of the 0921 engine-residue disposition table in place, each re-checked against the bytes"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-11797ce4-ddb8cb

## Experiment

Child round under hypothesis:mur-0921-engine-residues-dispositioned-and-corrected (EF.23, agent a00-11797ce4). Scope: the seven hypothesis-node C items plus the two file C items assigned to this round; experiment-node and thought-side C items are skipped (owned by the sibling round). Method: for each item, re-read the cited node/file and the cited engine file:line in THIS worktree, then write the correction through `write.py` (the two plain files edited directly). No verdict, lean or confidence field was changed.

### Item results

1. applied -- hypothesis:l4-config-max-and-template-max-are-required-verdict-fields-of-every-merge-up-review-and-a-named-line-of-every-dispatch-order (cl.(5) + title): path_max was NOT delivered (extensions/agi/workflows/merge-up-review.json carries 0 path_max; both required lists name only config_max/template_max; the brief order line names config-max/template-max/code only) and the baseline is NOT migrated (workflows/*.json still name /home/ubuntu/work/agi).
2. applied -- hypothesis:l4-quick-migrate-one-verb-moves-a-post-to-another-box-as-a-fresh-rotation-from-the-card-or-a-transcript-fork-over-the-git-messaging-layer (cl.(2) + a new `## Boundary`): no reader of a `stage: seated` record (writers only: migrate_channel.py:45, rotate.py:20954); the source-side reader is now deferred by name in the ordered Boundary section.
3. applied -- .agi/context/schemas/[cron].md:74-75: built-ins list gains `nudge_sweep`, matching crons.py:93-94 KNOWN_JOBS. Direct file edit.
4. applied -- hypothesis:l5-a-message-that-did-not-land-tells-its-sender-so-at-once (cl.(2)/(4) + FILE SCOPE): the coalesce line is KEPT (send.py:2491, pinned by test_send_undelivered.py:88-100); T is .agi/config.json comms.undelivered_after_minutes via _comms_config (send.py:2782, default send.py:323); ladder.md carries no comms cell.
5. applied -- hypothesis:l5-moral-one-loads-in-full-into-every-master-and-director-head-each-rotation (cl.(2)): the head prepends the MORAL region only (`## ESSENCE` .. before `## REFERENCE`, brief.py:327-332), not the FULL body.
6. applied -- hypothesis:l5-the-meter-captures-the-final-card-and-forces-the-rotation-itself (three cl.(1) fragments): the declared service runs `rotate.py alarms --holder ... --root {root}` with no systemd-run/--working-directory (crons.md:40); cmd_alarms sends no dm (rotate.py:7206); trigger (b) is cmd_alarms, not a heal-watch poll.
7. applied -- hypothesis:l5-tracked-files-name-origin-by-its-current-url (cl.(1)/(2) + FILE SCOPE): the live-repo literal was in 4 files / 7 lines (QUICKSTART.md:62,66; TODO.md:601,606,859; package.json:8; context/refs/legacy-prestate.md:23); README.md:49 is CodexOperator/agi-tree. cl.(3)'s residual count is the sibling experiment-side item.
8. applied -- hypothesis:l5-write-py-splits-a-script-only-at-an-ampersand-pair-that-begins-a-verb (title + body): dropped the link_ref causal attribution (that leaked link_ref holds zero ampersand pairs) and authored the scaffold body.
9. applied -- QUICKSTART.md:62: `CodexOperator/AGI` is public, not private (doc/l4-owner-decisions.md records REPO IS PUBLIC with `gh repo edit --visibility public` executed).
skipped -- hypothesis:lm-research-review-why-brainstorm-mint-by-default + experiment:a00-2ec3b4a6-b531ae: thought-side, excluded by the dispatch order.
skipped -- every experiment-node C item: owned by the sibling round.
verdict-question -- none: no correction revealed a verdict or lean the bytes no longer support; no verdict field was touched.

### Changed paths

.agi/nodes/hypothesis/l4-config-max-and-template-max-are-required-verdict-fields-of-every-merge-up-review-and-a-named-line-of-every-dispatch-order.md
.agi/nodes/hypothesis/l4-quick-migrate-one-verb-moves-a-post-to-another-box-as-a-fresh-rotation-from-the-card-or-a-transcript-fork-over-the-git-messaging-layer.md
.agi/nodes/hypothesis/l5-a-message-that-did-not-land-tells-its-sender-so-at-once.md
.agi/nodes/hypothesis/l5-moral-one-loads-in-full-into-every-master-and-director-head-each-rotation.md
.agi/nodes/hypothesis/l5-the-meter-captures-the-final-card-and-forces-the-rotation-itself.md
.agi/nodes/hypothesis/l5-tracked-files-name-origin-by-its-current-url.md
.agi/nodes/hypothesis/l5-write-py-splits-a-script-only-at-an-ampersand-pair-that-begins-a-verb.md
.agi/context/schemas/[cron].md
QUICKSTART.md

## Evidence

All seven hypothesis nodes and both files re-read after the writes. `python3 extensions/agi/bin/links.py links` -> 3979 resolved, 0 broken (18 retired payloads). No engine file was edited. Every edited hypothesis node carries a THOUGHT naming hypothesis:mur-0921-engine-residues-dispositioned-and-corrected.

## Completion

All nine in-scope C items applied and each survived the byte re-check. One citation drift noted, not corrected in the table: the table cites `doc/unified-director-brief.md`; the file is `.agi/nodes/doc/unified-director-brief.md`. production_lines 56 (added lines over the 9 in-scope paths, `git diff --numstat`) against line_ceiling 40; the 2x rebrief line (80) was not crossed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (EF.23, agent a00-95359f56) under hypothesis:mur-0921-engine-residues-dispositioned-and-corrected.

WHAT THE INSTRUCTION SAID: the dispatch order scopes this kid to the seven hypothesis-node C items plus the two file C items, applied IN PLACE, each re-checked against the bytes, with no verdict or lean field changed. The parent brief says read each kid DIFF, never its result file, and run one negative probe per claim conjunct.

WHAT THE MACHINE DOES: this kid's process died on a provider error (manifest death.class=died-no-work, runtime_s 489) BEFORE it called cli.py done, so this node carries no verdict field and the kid's own summary was never re-checked by its own round. Its nine edits ARE in the worktree and were read by the parent as BYTES, not as this node's prose: the testable_claim and title corrections on the seven hypothesis nodes, the new Boundary section on l4-quick-migrate, the authored l5-write-py body, the nudge_sweep addition to .agi/context/schemas/[cron].md, and QUICKSTART.md:62 private to public. Parent probes over the diff: ZERO verdict/lean/confidence field deltas across all 20 corrected nodes; every changed node's THOUGHT names the target hypothesis; the negative probe grep -c path_max on extensions/agi/workflows/merge-up-review.json returns 0, so the l4-config-max NOT DELIVERED correction is truthful; send.py:2491 still prints the coalesce line the l5-a-message correction now says is KEPT. ACCEPTED as applied. The round carries no kid verdict because the kid died, which is the one caveat.

NEAR MISS: accepting this node's own body ("all nine applied") would satisfy "reviewed" in words while the node has no verdict and its dying process never re-checked a byte; the parent read git diff instead.

DEVIATION: none from the standing rules. The parent does not set the kid's verdict field; a dead kid's verdict is not the parent's to write.
<!-- THOUGHT:END -->
