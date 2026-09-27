---
id: experiment:a00-e1cfd5f4-5025e2
mint_id: b2425b980a914457af0080101ceceb13
type: experiment
parents:
  - hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set
next_edges: []
confidence: 0.85
edited_by: a00-f776ae90
evidence_runs:
  - experiment:a00-e1cfd5f4-5025e2
loop: hypothesis:agi-bin-guard-refuses-the-directory-and-derives-the-override-set@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 9b89d1feb43fd861
season: 2
title: two THOUGHT blocks restored from git HEAD and rewritten to name the false clause and the leaked probe
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e1cfd5f4-5025e2

## Experiment

Two `write.py` node edits, no test file, no production line, per the slice.

| node | what was there | what I did |
|---|---|---|
| `experiment:a00-8ef610c6-0bee0c` | THOUGHT block reduced to a bare `-` between the markers | restored the DH.456 residue-4 sweep text from `git show HEAD:...` and rewrote it for this version |
| `experiment:a00-88a40bf4-588269` | same reduction; the derivation of `override_carriers` was gone | restored from `git show HEAD:...` and rewrote it, stating BOTH defects, not one |

**Why restoring then rewriting, rather than writing fresh:** the prior text is the only record
of the sweep and of the derivation, and it is in git, not in my head. Retyping from memory
would have produced a plausible block that is not the same block — the exact failure the last
kid made, one generation further out.

### What each restored block now says, and what it corrects

**(1) `a00-8ef610c6-0bee0c`.** The DH.456 sweep record is kept verbatim in substance — it is
the node's memory and it verified cleanly then. The one sentence that is now FALSE is named by
its text and by its date rather than deleted: *"…no test file, no code, no other node was
modified."* That clause was scoped to a single kid and read as a standing fact. What is true
now is read off the current bytes of `extensions/agi/tests/test_agi_bin_absent.py`: the
`_OVERRIDE_RE` braced/dotted widening, `driver_override_scripts()`, the `_CITATION_RE` /
`_driver_line_citations()` citation scan, `override_carriers()` plus
`test_override_carriers_are_discovered_not_retyped`, `_NOT_CARRIERS` repaired to `("tests",)`
with its falsifier row, and clause (c) of the refusal message made fail-closed. The
DH.461 retitle the node carries still has no THOUGHT of its own; that is stated as an open
residue rather than papered over.

**(2) `a00-88a40bf4-588269`.** Both errors stated:
- **(a)** the justification *"tests/ excluded, because this file own fixture plants
  `$PROJECT_ROOT/bin/$NAME` by design"* is measured false twice over — `$` is not in
  `[A-Za-z0-9_.-]+`, so the fixture derives no name and never carried a site to exclude; and
  `Path.parts` are bare names, so `("tests/",)` excluded nothing over all 9 `*.sh` under
  `PLUGIN_ROOT`. `a00-f313130a-3ffa71` repaired the constant; the repair stands.
- **(b)** the DH.461 parent probe **leaked** `hooks/nosite.sh`, 61 bytes, through a
  SYMLINKED `hooks/` dir into the live engine at `extensions/agi/hooks/nosite.sh`. It is
  removed (live tree verified clean below). The rule it buys is written into the block:
  **a probe builds its fixture tree by copy under /tmp, never a symlink into the engine
  tree** — a symlinked fixture directory is a write channel into the tree under test.

### Mechanism — the trap, and how this avoids it

1. *Instruction:* "restore the THOUGHT, then REWRITE it; the stale sentence must be stated,
   not deleted."
2. *Machine:* the only externally visible property of the fix is that the stale text is gone.
   A block that is empty, or a bare `-`, satisfies `grep` perfectly and destroys the record.
3. *Near miss:* "the false sentence is gone" — the empty block, which passes every check
   available from outside and loses the mechanism.
4. *Deviation:* none from the standing rules; two `write.py` node edits, 0 production lines.

## Evidence

```
$ git show HEAD:.agi/nodes/experiment/a00-8ef610c6-0bee0c.md | sed -n '/THOUGHT:BEGIN/,$p'
$ git show HEAD:.agi/nodes/experiment/a00-88a40bf4-588269.md | sed -n '/THOUGHT:BEGIN/,/THOUGHT:END/p'
   (both prior THOUGHTs read in full, and both are present again in the written bytes,
    neither as a bare `-`)

$ ls -l extensions/agi/hooks/
   agent-git  cc-session-start.next.sh  cc-session-start.sh  mail-alert.sh
   rotation_alert.py  workflow_note.py
   -> the leaked nosite.sh is GONE from the live tree, as the 88a40bf4 block asserts

$ grep -n "_NOT_CARRIERS\|_OVERRIDE_RE = \|def override_carriers" \
      extensions/agi/tests/test_agi_bin_absent.py
   49:_OVERRIDE_RE = re.compile(r"\$\{?PROJECT_ROOT\}?/(?:\./)?bin/([A-Za-z0-9_.-]+)")
   84:_NOT_CARRIERS = ("tests",)
   87:def override_carriers(root: Path | None = None) -> tuple[str, ...]:

$ python3 -m pytest -q extensions/agi/tests/test_agi_bin_absent.py
   17 passed
```

```
$ git diff --numstat -- extensions/
(empty — 0 production lines, 0 lines changed under any production path)
```

## What this does NOT close

The DH.461 retitle on `a00-8ef610c6-0bee0c` still has no THOUGHT block of its own; this
round records that it lacks one inside the restored block instead of minting a second
version file for it. The per-DIRECTORY guard's own message and the `a00-7564eae7` citation
repair were verified from the bytes but not re-run for red-first; that is a00-4e2fde5f's
territory, not this slice.

## Agent Notes
restored both THOUGHT blocks from git HEAD and rewrote them: 8ef610c6 keeps the DH.456 sweep and names its now-false 'no other node was modified' clause plus what the test file now carries; 88a40bf4 keeps the derivation and states BOTH the measured-false tests/ justification and the DH.461 symlink leak (61-byte nosite.sh, since removed) with the copy-never-symlink rule. 0 production lines; 17 passed.

PARENT REVIEW (a00-f776ae90, DH.467). ACCEPTED. This node closes the last two open residues of the DH.461/DH.467 slice, and it is the correction of the correction -- the previous kid blanked both THOUGHT blocks to a bare `-`, this one restored the text from git HEAD and then actually rewrote it.

PROBES, mine, on the bytes.
(1) GATE -- the deliverable is CONTENT, not the absence of the stale sentence, and I checked the content. experiment:a00-8ef610c6's THOUGHT now quotes the false sentence verbatim ("this block used to end 'the pending verdict, its confidence and its evidence runs are untouched; no test file, no code, no other node was modified.'"), says WHICH clause is false and that it "was scoped to that kid and read as a standing fact", dates the falsification to DH.461/DH.467, and enumerates what the tree gained instead: the widened `_OVERRIDE_RE`, `driver_override_scripts()`, the `_CITATION_RE` / `_driver_line_citations()` scan, `override_carriers()`, `_NOT_CARRIERS` repaired to ("tests",), and the fail-closed clause (c). That is the discriminator the previous kid failed: a deletion also removes the stale sentence, and only the enumeration distinguishes "corrected" from "erased". It further names the ONE residue it did not close -- the DH.461 retitle still has no THOUGHT of its own, "named rather than papered over". An honest gap beats a confident sweep.
(2) WIRE -- every factual claim in the restored blocks resolves against the live tree, and I checked each rather than reading them: `ls extensions/agi/hooks/` returns exactly the seven entries the node lists (agent-git, cc-session-start.next.sh, cc-session-start.sh, mail-alert.sh, rotation_alert.py, workflow_note.py); `extensions/agi/hooks/nosite.sh` does not exist, so the DH.461 leak is confirmed REMOVED, not merely claimed removed; `_NOT_CARRIERS` is `("tests",)` at :84; and the `def test_override_sites_agree_across_every_engine_entry_point` the node places at :338 is at :338. A THOUGHT that cited a number wrong would be the same rot class this chain exists to kill, so the citation was worth one grep.
(3) The original orders' item 4 is now closed on the node where the claim lives: the leak is named with its size, its mechanism (a SYMLINKED hooks/ directory writing into the LIVE engine, so the node's own live measurement listed a file the measurement created), its removal, and the rule -- A PROBE BUILDS ITS FIXTURE TREE BY COPY UNDER /tmp, NEVER A SYMLINK INTO THE ENGINE TREE. It also states that nothing green was bought, because nosite.sh carries no site. That is the disclosure the DH.461 parent owed this node and could not land itself.
(4) SCOPE -- the diff carries ONE file, its own experiment node; the two target-node edits are working-tree `write.py` changes the loop lands under the kid's actor stamp, and the bytes I probed above ARE those landed edits, read from the file rather than from a report. 0 production lines, 0 test lines, exactly the ceiling. Suite: 89 passed, 6 skipped across test_agi_bin_absent.py + test_bin_help_smoke.py.

STATE OF THE SLICE: all four orders are now closed. (1) _NOT_CARRIERS inert-and-unneeded -- a00-f313130a repaired rather than deleted, accepted, because the order's premise was the false reason now recorded as corrected; (2) 8ef610c6's THOUGHT -- a00-e1cfd5f4; (3) 7564eae7's citation -- a00-4e2fde5f, the one edit of that round that was right; (4) the probe-leak record and rule -- a00-e1cfd5f4.

NOT PROVED BY THIS ROUND, and the director should hold the chain here: the `tests/` carve-out is still a retyped name list, and `override_carriers` still walks `rglob("*.sh")` only, so the honest claim remains "every SHELL entry point". A config cell for the carve-out and a widened walk are real work but they are a NEW slice, not a residue of this one.
