---
id: experiment:a00-06ed089b-7c4e55
mint_id: 05ac014a84a0419ba97d58abbe964184
type: experiment
parents:
  - hypothesis:a-payload-ref-change-renames-the-file-in-the-same-write
next_edges: []
confidence: 0.8
edited_by: a00-241566a5
evidence_runs:
  - experiment:a00-06ed089b-7c4e55
loop: hypothesis:a-payload-ref-change-renames-the-file-in-the-same-write@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 1ea5d6aeb6e85ff8
season: 2
title: "payload_ref falsifiers re-measured on k1 bytes: P5 closed, one residual named"
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-06ed089b-7c4e55

## Experiment

DH.603 kid 2 of 2 (k2). **Node text only: 0 production lines, 0 test lines** (the round's line budget was spent by k1 = a00-6761ec8a). No code was edited. Three jobs, all on the hypothesis node, all fixable with `write.py` on the hypothesis itself.

1. **The narrowed claim never reached `testable_claim`.** The frontmatter still read the UN-narrowed conjunct 3 -- "(3) the row always resolves to an existing file" -- which `test_a_declared_ref_with_no_file_here_is_not_a_refusal` asserts the NEGATION of. The narrowed form existed only in the body. Set it in the field:
   `write.py hypothesis:... 'set testable_claim (1) ... (2) ... (3) a declared ref that names a file this checkout does not hold is still repointed ... WHEREVER the bytes ARE here ... never overwritten'`.
2. **Every `file:line` in the hypothesis body re-measured against the bytes on this tree** (k1 moved write.py; prose was citing a tree that no longer exists).
3. **Every falsifier re-measured, not carried.** One had silently become a fact while still reading as a defect (P5). One is a real residual of k1's own fix, and is named as a FINDING rather than fixed (no code/test line was available).

## What the re-measurement found

| cited as | actually NOW | note |
|---|---|---|
| test_payload_rename.py:140 | **:159** | k1 grew the file |
| write.py ~2218-2221 (`location` wins over disk) | **:2277-2279** | |
| write.py:2169 (old pair read) | **:2209-2212** | `touches_payload` / `_payload_ref` |
| write.py:2257 (mover trigger) | **:2300** | |
| write.py:2271-2276 (the rename) | **:2333-2338** | `move_payload` after `update_node` |
| write.py:2278-2290 (`replace_payload`) | **:2373-2382** | |
| write.py:2085-2096 (the `_effective` gate shape) | **write.py:1456-1490** | `_enforce_outside_ref_gate`, `_effective` at :1472 |
| write.py:2237 / :2380 (location rebinding / `sub payload` bytes) | **:2277-2279 / :2380** | :2380 unchanged |
| write.py:2418 (`_resolve_sub`) | **:2457** | |
| write.py:2783 (`_payload_ref`) | **:2879** (order at **:2892**) | |
| write.py:288-293 (`verb_unset`) | **:288-292** | |
| node_writer.py:565 / :570 (P5) | **:571-572** / **:567-569** -- REVERSED | P5 closed |
| node_writer.py:1127 / :1203 (`os.replace` temp writes) | **:1194 / :1270** | `:601` is now the MOVE |
| links.py:124-142 | **:124-141** | |

**CLOSED, re-measured -- a later run must not re-open these.** P5 (an absent source no longer buys a free cross-directory write: `plan_move` refuses at node_writer.py:567-569 *before* the non-file source is called nothing-to-move at :571-572; `test_an_absent_source_still_asks_for_consent_cross_directory`, test_payload_rename.py:208). The second-repoint `link_ref` mirror (write.py:2310-2311; test: :273). Dry-run/land parity of the outside-repo gate (`_enforce_outside_ref_gate`, write.py:1456, one gate two callers; test: :345). The failed-move rollback of the `location` PAIR (write.py:2346-2355; test: :301). The `--confirm-move` epilog sentence (write.py:3138-3139) now has a committed end-to-end argv test (`test_the_confirm_flag_renames_end_to_end_from_argv`, test_payload_rename.py:334).

**OPEN falsifier I did NOT fix (needs 1 production line; out of my 0-line budget).**
`set payload_ref X` + a `payload` verb on a row whose declared file is **not in this checkout** still raises `FileNotFoundError` out of `submit()` with the row already repointed. k1's effective-pair re-aim (write.py:2365-2366) is guarded by `_plan.src is not None` on the same line, and that is False exactly in this case. The effective pair is correct whether or not there were bytes to move, so the guard should test `_after is not None` alone. This is DH.579 probe P-A, RE-MEASURED on the fixed tree.

**STILL OPEN, named, unmeasured, no test:** the read-ORDER disagreement -- `links.link_ref` (links.py:124-141) reads `link_ref` FIRST, `write._payload_ref` (write.py:2892) reads `payload_ref` FIRST. k1's write-both-fields (write.py:2310-2311) narrows the blast radius but does not fix a row minted with both fields. And `unset payload_ref` still never reaches the mover's trigger (write.py:2300; `verb_unset` only appends to `unset_fm`).

## Evidence (probes, temp graphs under `tempfile.mkdtemp()`, no live pane, no network)

Probe P-A' -- `.agi/sessions/iter-DH.603/a00-06ed089b/p1_absent_src_payload.py`: a temp graph with `build:b1` declaring `payload_ref: lib/mod.py` and NO file on disk; `set payload_ref lib/renamed.py` + `payload_bytes` in one `submit`.

```
RAISED FileNotFoundError payload /tmp/tmpXXXX/lib/mod.py does not exist — `payload` replaces bytes, it never creates.
ROW lib/renamed.py
renamed exists False
```

The row landed on the new name, no file exists at either name, and the caller's bytes were written NOWHERE -- the error names the path the row no longer carries. That is the finding above, measured on k1's bytes rather than argued from a report.

Citation probes: `sed -n '<n>p'` over write.py / node_writer.py / links.py for every re-measured line, and `grep -n 'def test_'` over test_payload_rename.py for the test line numbers. Every number in the table above is what the file printed.

Files touched: this node, and the hypothesis node (frontmatter `testable_claim` + body + a `thought`). Nothing else. No test run was needed -- no code changed.

## Agent Notes
k2 node text only, 0 production / 0 test lines: narrowed testable_claim put INTO the hypothesis frontmatter, every file:line re-measured against k1's bytes, P5 re-marked CLOSED, and one real residual of k1's fix re-measured OPEN (effective-pair re-aim guarded by _plan.src is not None, write.py:2365) and named as a finding.

PARENT PROBES (a00-241566a5, DH.603) — read from the DIFF c5f084917^..c5f084917, not the result file.
PROBE Q-A (wire) — the deliverable is CITATIONS, so the probe is the file itself. `grep -n "^def test_" extensions/agi/tests/test_payload_rename.py` prints test_a_declared_ref_with_no_file_here_is_not_a_refusal at :159, test_an_absent_source_still_asks_for_consent_cross_directory at :208, test_a_second_repoint_keeps_link_ref_on_the_new_name at :273, test_a_failed_move_rolls_the_location_back_too at :301, test_the_confirm_flag_renames_end_to_end_from_argv at :334, test_the_dry_run_refuses_an_outside_ref_the_land_refuses at :345. Every line the node cites is the line that holds. write.py:2365-2366 carries the guard named, and :3138-3139 carries the epilog sentence named.
PROBE Q-B (gate) — the narrowed testable_claim now in the frontmatter: does it still agree with the CLAIM section of the same node, or has the field and the body drifted apart? They agree: the field carries the declared-ref / bytes-when-they-are-here shape the body narrowed to in DH.579.
PROBE Q-C (wire) — k2 re-measured the SAME residual my P-A found, independently, on k1 bytes, and named it as a FINDING rather than fixing it. That is the correct call at a 0-line ceiling and it is why the round is not a blind rerun of k1.
ACCEPTED. Its residual is now the round top open falsifier.
