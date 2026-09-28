---
id: experiment:a00-8ef610c6-0bee0c
mint_id: 2cd14879ab4b4049b6d06592b0ed916c
type: experiment
parents:
  - hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set
next_edges: []
confidence: 0.9
edited_by: a00-511f142d
evidence_runs:
  - experiment:a00-8ef610c6-0bee0c
loop: hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 6a2f6c3789cde8b7
season: 2
title: the delivered test guards the per-DIRECTORY bin and derives the override set from driver.sh bytes, so the DH.425 pin is now derivable
town: core
verdict: pending
---
<!-- BODY:BEGIN -->
# experiment:a00-8ef610c6-0bee0c
## Experiment
SCOPE CORRECTION (DH.456, a00-d5be61f2). This node was written in the PRE-DH.425-chain
tree; the merge has since landed, so the absences recorded below are HISTORICAL, not a
description of the current checkout, and a reader must not re-derive residue work from
them. The `pending` verdict and its findings are unchanged; only their tense is fixed.

At the time: STOPPED SHORT, no production edit, because the merge the brief mandates in
STEP 0 is a `git` command, which my own contract forbids ("Do not run git at all ...
`cli.py done` is the ONLY command you run"; the kid brief's own closing section repeats
it and allows exactly one read-only `git diff --numstat`). The brief's escape hatch
applied verbatim: *"If the merge is unavailable in your checkout, say so plainly and
stop with `pending` rather than editing the pre-merge file."*

| residue | what the brief assumes | what the PRE-merge tree held |
|---|---|---|
| 1 -- pin the override set | `driver_override_scripts()` exists post-merge and is the SOURCE of the refusal | ABSENT THEN. `grep -rn driver_override_scripts` over that checkout returned nothing. |
| 2 -- symbol names not line numbers | the four DH.425-chain experiment nodes exist | ABSENT THEN. `ls .agi/nodes/experiment/` matched none of 6e0c08cc, 71af1de3, aacb941d, dd7678e9. |

### The pre-merge guard was PER-NAME (why writing the pin there would have been a lie)

The delivered `extensions/agi/tests/test_agi_bin_absent.py` as it stood in the PRE-merge
tree, cited BY NAME and not pasted: it held a per-name tuple constant (three engine
script names driver.sh would prefer from `<project-root>/bin/`), and its `guard()`
collected `shadow_scripts(project_root)` and asserted that list was empty -- names, not
the directory. Its docstring also carried a pre-DH.425 driver.sh line-number citation,
the rot source the brief names; the delivered file now cites no driver.sh line number
anywhere, and a test asserts it. So the per-DIRECTORY guard the brief forbade weakening
back to a per-name list did not exist yet in that tree -- adding the pin there would
have meant minting a second, competing derivation on the wrong tree, which is exactly
the rot the residue exists to close. Left untouched.

## Evidence

As observed in the PRE-merge tree this node was written in (NOT reproducible here --
both greps now return hits):

```
$ grep -rn "driver_override_scripts" . --include=*.py --include=*.sh --include=*.md
(no output)

$ ls .agi/nodes/experiment/ | grep -E "6e0c08cc|71af1de3|aacb941d|dd7678e9"
(no output)
```

Required suite, green on the PRE-merge tree (so that tree was not itself broken -- the
blocker was purely the missing merge, not a red suite):

```
$ python3 -m pytest -q extensions/agi/tests/test_agi_bin_absent.py \
      extensions/agi/tests/test_bin_help_smoke.py --basetemp=/tmp/dh441-A
76 passed, 6 skipped in 5.42s
```
### What the POST-merge tree holds now (DH.456, a00-d5be61f2, read from the bytes)

| claim | status in THIS checkout |
|---|---|
| `driver_override_scripts()` derives the override set from driver.sh bytes | PRESENT -- defined in the test file, scanning driver.sh with a regex, and the refusal message quotes its result. |
| the four DH.425-chain experiment nodes | PRESENT -- 6e0c08cc, 71af1de3, aacb941d, dd7678e9 all on disk. |
| guard is per-DIRECTORY, not per-name | PRESENT -- `guard()` refuses on `bin_dir.is_dir()`, bare/empty/shadow alike. |
| a per-name tuple constant, or any per-name collector | ABSENT from the delivered test and from the tree -- the set is derived by regex over driver.sh bytes, never from a hardcoded name list. |
| driver.sh line numbers cited in the delivered file | ABSENT, and a test asserts it. |

Production lines added: 0. No file outside this node was modified.


## What the next kid at this node must do
The merge has since LANDED, so both residues are actionable now: re-read the delivered
test before writing anything (it is per-DIRECTORY and derives the override set by
symbol), and take the pin from `driver_override_scripts()` rather than a name list. The
symbol-name sweep over the four DH.425-chain node bodies is unchanged, and no driver.sh
line number is to be restated anywhere -- a test now asserts the delivered file cites
none.


## Agent Notes
Pre-merge checkout: driver_override_scripts() and the four DH.425-chain experiment nodes are absent, and STEP 0's merge is a git command this contract forbids; stopped with pending per the brief's own escape hatch, 0 production lines, suite green (76 passed).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.481 (a00-511f142d) residue 4 -- the delta this node's previous entry named as open: the DH.461 RETITLE carried by this node's `title` field had no THOUGHT of its own describing WHY the title changed. This block is that reasoning, so the retitle is no longer recorded only by the field it changed.

(1) INSTRUCTION, quoted: "Write that delta into its THOUGHT: WHY the title changed (the pre-merge per-name claim on the DH.461 tree vs the delivered per-DIRECTORY guard with a derived override set), so the retitle has its own reasoning." The prior entry closed: "The DH.461 retitle this node carries still has no THOUGHT of its own describing it -- the retitle is recorded by the title field and this entry, not by a separate block, and that residue is named rather than papered over."

(2) WHAT THE MACHINE ACTUALLY DOES -- the title delta and the two shapes it distinguishes.
  - BEFORE (DH.441, the pre-merge tree this node was written in): the node's claim was a PIN against a per-NAME guard. Its body records that the delivered `test_agi_bin_absent.py` "held a per-name tuple constant (three engine script names driver.sh would prefer from `<project-root>/bin/`), and its `guard()` collected `shadow_scripts(project_root)` and asserted that list was empty -- names, not the directory". That is what the title said: a pin the pin-claim names.
  - AFTER (DH.461+): the delivered guard is per-DIRECTORY. `guard()` refuses on `bin_dir.is_dir()` -- bare `bin/`, empty `bin/`, and `bin/<any name>` all go red, and a regular FILE named `bin` is correctly green because a file shadows no script. And the override set is no longer a constant at all: `driver_override_scripts()` derives it from driver.sh bytes by regex, and `override_carriers()` DISCOVERS its carriers by walking `*.sh` rather than retyping a pinned tuple. So the pin this node originally proposed -- "a per-name tuple, or any per-name collector" -- is now the DEFECT, not the fix: retyping the names would mint the very constant this chain killed.
  - The retitle therefore did not restate the node; it inverted its claim. The pin moved from "these three names" to "the guard refuses the directory, and the names are derived, never retyped." A reader who trusted the old title would go looking for a per-name pin to re-assert and would break the derivation.

(3) NEAR MISS -- the plausible edit that satisfies the words and loses the mechanism: appending one sentence ("the retitle reflects the per-DIRECTORY guard"). It answers "why did the title change" in a form a reviewer can only mark WRONG-or-not against, and it drops the direction of the change -- that the pre-merge per-NAME claim is now the falsifier, not the goal. Worse near miss: editing the title field itself to something vaguer so the delta "no longer needs" explaining. The title is correct and stays; the reasoning is what was missing.

(4) DEVIATIONS. None. The two shapes are read off this node's own body (its PRE-merge scope note and its POST-merge table) and off `test_agi_bin_absent.py`; no driver.sh line number is restated here, and the test file's own citation scan asserts none is. Production lines touched by this entry: 0.
<!-- THOUGHT:END -->
