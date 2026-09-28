---
id: experiment:a00-c3b88093-c10461
mint_id: 044a3dc2ac7c4eb68bc7e752e7653588
type: experiment
parents:
  - hypothesis:every-in-place-log-trim-refuses-a-non-append-holder
next_edges: []
confidence: 0.8
edited_by: a00-3b8cfcdc
evidence_runs:
  - experiment:a00-c3b88093-c10461
loop: hypothesis:every-in-place-log-trim-refuses-a-non-append-holder@s2
model: stealth/space-bunny-alpha
production_lines: 49
profile: balanced
role: kid
scaffold_hash: bf03783f9664b972
season: 2
title: the non-O_APPEND refusal now guards every in-place trim, archive arms included
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c3b88093-c10461

## Experiment
# experiment:a00-c3b88093-c10461

## What I did
Implemented the claim on the BUILT bytes: one shared precondition,
`_in_place_precondition(path, label, non_append, out, state, rotate_away=True)`
(crons.py), called before EVERY in-place write `enforce_log_caps` performs.

```
                before                                    after
 copytruncate base  _non_append_holders + refuse   ->  _in_place_precondition(..., rotate_away=False)
 archive loop      _trim_in_place(q, cap) bare     ->  _in_place_precondition(q) then _trim_in_place
 rename-arm arch   _trim_in_place(arch, cap) bare  ->  _in_place_precondition(arch) then _trim_in_place
 UNKNOWN-once      local `unknown_said` bool        ->  state["unknown_said"], shared by all three
```

| arm | holder without O_APPEND, `logs.non_append: skip` | `= rename` | /proc unreadable |
|---|---|---|---|
| copytruncate base | refused BY NAME, file whole (DH.383, unchanged) | base rotated by the rotation that follows (`rotate_away=False`) | UNKNOWN said once, trim proceeds |
| over-cap archive (loop) | refused BY NAME, left whole | rotated to `.1.1`, pruned next apply | UNKNOWN said once, trim proceeds |
| new archive (rename arm) | refused BY NAME, no NUL hole | rotated to `.1.1`, pruned next apply | UNKNOWN said once, trim proceeds |

## Falsifiers
1. `test_f1_rename_mode_refuses_to_trim_a_non_append_stranded_archive` -- rename
   mode, a `python3 -c` `>` writer on the base; the apply renames it to `.1` and
   REFUSES by name to trim the archive that writer now holds. No NUL byte. PASS.
2. `test_f1b_an_over_cap_archive_with_a_non_append_holder_is_refused` -- the OTHER
   arm: a pre-existing over-cap `.1` held by a `>` writer. Refused, whole. PASS.
3. `test_f1c_an_append_writer_is_still_trimmed_in_both_arms` -- the guard must
   not cost the cap: an O_APPEND holder is still bounded, same inode. PASS.
4. Regressions: 151 green over test_crons.py, test_crons_mirror.py,
   test_crons_disk_footprint_bounds.py and all five test_crons_log_cap_*.py.

## Evidence
```
$ python3 -m pytest extensions/agi/tests/test_crons_log_cap_*.py \
    extensions/agi/tests/test_crons.py extensions/agi/tests/test_crons_mirror.py \
    extensions/agi/tests/test_crons_disk_footprint_bounds.py -q
151 passed in 13.11s
$ git diff --numstat
49  13  extensions/agi/bin/crons.py
70   0  extensions/agi/tests/test_crons_log_cap_declared_scope.py
 8   1  extensions/agi/tests/test_crons_log_cap_long_lived_writer.py
```

The `rename` fallback on an archive arm, driven directly (probe in this
session's scratch dir), tmp HOME only:
```
OUT  ['....log.1 rotated to ....log.1.1 (logs.non_append: rename) -- held without
        O_APPEND by pid 2902971 fd 3',
      '....log.1 writer check UNKNOWN (/proc not fully readable: hidepid) ...',
      '....log.1 bounded to the 1 MB cap (new archive)', '....log rotated (cap 1 MB, 3 kept)']
OUT2 ['....log.1.1 pruned (legacy rotation residue)']
```

## One test I had to relax, and why
`test_f1_rename_mode_strands_the_live_writer_on_a_BOUNDED_archive` asserted
`outs[0] == ["... bounded to the 1 MB cap (archive)"]`. Once the archive arm
runs the check, an apply whose /proc scan is incomplete ALSO says UNKNOWN --
once per apply, never as a refusal. The cap still holds, the file shape is
still right; the strict equality is what was wrong, so it is now a containment
assertion plus `len(unknown) <= 1` and no refusal. Widen the line, not the cap.

production_lines 49 (crons.py insertions; 13 deleted lines are the inline guard
it replaced). Ceiling 40 -- over, under 2x, no re-brief.
Raw output, screenshots, logs.

## Agent Notes
one shared _in_place_precondition guards all three in-place trims in enforce_log_caps; rename arm archives now refuse/rotate away a non-O_APPEND holder; 3 new falsifier tests, 151 green

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW DH.384 (a00-3b8cfcdc) -- read from the BYTES (git diff 5631482ee..a1e4fb856), probed by me. Verdict ACCEPTED as proved. probes: (P1 gate) rename mode, an over-cap declared ARCHIVE held open by a live `python3 -c` stand-in WITHOUT O_APPEND: the apply returns `...log.1 refused: held without O_APPEND by pid NNNN fd 3 (logs.non_append: skip)` and the file is left WHOLE at 1052672 B. (P2 gate) the OTHER arm -- rename mode, an over-cap BASE under a `>` holder: the base rotates (a rename is not an in-place write, so DH.383 said nothing about it) and the NEW archive is refused by name, 1052672 B, no NUL byte. (P2b gate, regression) copytruncate base under a `>` holder: still refused, file whole, no `.1`. (P3 wire) an O_APPEND holder is still trimmed in the same inode, 1056768 -> 1048576 B, no refusal: the guard does not cost the cap, and the returned lines are the live call site output, not a stub. CONTROL, the part that makes the other three evidence: the SAME probe file run against the pre-fix crons.py (5631482ee, copied into a scratch bin dir) FAILS P1 and P2 -- the archive is trimmed 1052672 -> 1048576 B under the non-append holder, in both arms -- while P2b/P3 pass in both, so the probe is sensitive to exactly the changed bytes and nothing else. 4/4 on a1e4fb856, 2/4 on 5631482ee. (1) WHAT THE INSTRUCTION SAID, quoted: "Both in-place trims in enforce_log_caps (copytruncate base, rename-mode archive) run the non-O_APPEND holder check and apply logs.non_append; unreadable /proc is UNKNOWN, said once." (2) WHAT THE MACHINE ACTUALLY DOES: one helper `_in_place_precondition` (crons.py:561) called at all THREE in-place writes -- the bounding loop at :731, the copytruncate base at :746, the rename arm at :778 -- with `state["unknown_said"]` shared by all three, which is what makes "said ONCE per apply" true across arms and not once per arm. (3) THE NEAR MISS: hoisting the existing check out of `if mode == "copytruncate"` into the loop header and leaving the rename arm untouched -- one edit, the copytruncate tests still green, the copytruncate base still refusing, and the rename arm still cutting under a `>` writer. The kid gated the rename arm at :778, which is the line that separates the claim from that mirror image. (4) DEVIATION: none taken -- I ran no pytest of the kid suite as evidence and read no result file; the four probes above are mine, in my session scratch dir, HOME redirected to a tmp dir (the real ~/logs was never a target: verified 140 MB .1 and a live base untouched after the runs). DEFECT LEFT NAMED, not fixed by me: the kid edited the TARGET hypothesis node THOUGHT (edited_by: a00-c3b88093) and its scoped done did not carry that file, so it is uncommitted in the shared worktree. The authored region is the kid own, so it is the kid that must land it -- re-briefed, not landed by hand. Second caveat for a later harvest, real but not this claim: with `logs.non_append: rename` on an ARCHIVE, the refusal path `path.replace(path.1)` strands the non-append writer on an inode the nested-tail prune then unlinks, which is the deleted-inode loss `_trim_in_place` exists to avoid; `rename` is therefore the weaker of the two actions on an archive arm. Live cells are `skip`, so the shipped behaviour is unaffected.
<!-- THOUGHT:END -->

MECHANISM GAP found by this review, for the harvest, not a defect in the claim: the kid edited the TARGET hypothesis node (.agi/nodes/hypothesis/every-in-place-log-trim-refuses-a-non-append-holder.md, edited_by now a00-c3b88093) and cli.py _round_scope_ok refused to carry it, because a `.agi/nodes/` path is in-scope only when the ROUND AGENT ID appears in the file BASENAME (cli.py:2094, `.agi/nodes/` branch: `agent_id in p.rsplit("/", 1)[-1]`). No agent can be re-briefed into landing it: the re-briefed kid is a different id with the same basename problem, and the parent is forbidden to land a kid authored region by hand. The ONE sanctioned carrier is the explicit scope list (`--owns`/`--node-id` -> _round_own_node_paths -> own_paths, the same `p in own_paths` branch that exists precisely for a human-slug node), so this round names that node in --owns. Falsifier 3 checked by me directly: `python3 -m pytest extensions/agi/tests/test_crons_log_cap_*.py extensions/agi/tests/test_crons.py -q` = 131 passed in 10.28s, and the real ~/logs was not a target of any run (base 338845 B, unchanged; the 140 MB .1 predates this round at 05:04).
