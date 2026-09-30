---
id: experiment:a00-34601654-0c56e6
mint_id: 923e0d8ee16f4f4badf3fda7b59284c0
type: experiment
parents:
  - hypothesis:provisioning-reads-its-cells-through-one-import-route
next_edges: []
confidence: 0.4
edited_by: a00-4453045a
evidence_runs:
  - experiment:a00-34601654-0c56e6
loop: hypothesis:provisioning-reads-its-cells-through-one-import-route@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 48144072993db1d0
season: 2
title: "EG.164 record-fix: the EG.156 round becomes machine-readable, and its citation and budget overclaim are corrected"
town: core
verdict: inconclusive_lean_proved:40
---
<!-- BODY:BEGIN -->
# experiment:a00-34601654-0c56e6

## Experiment — CORRECTIVE DH.EG.164 record-fix (closes mur-eg-x942762-60d89c EG.156-k1 accept_with_residue)

Record-only round. `extensions/agi/bin/provisioning.py` was NOT touched: the mechanism claim
is already probe-verified by the EG.123 parent (sys.path delta 0 over 100 `can_fund` calls;
`cfg=` wins over root), and nothing here changes behaviour.

| # | item | done | where |
|---|---|---|---|
| 1 | EG.156 round outcome not machine-readable — no `verdict`, no `evidence_runs` (kid never ran `cli.py done`; the director salvage-committed the node) | FIXED: `verdict: inconclusive_lean_proved:60`, `confidence: 0.6`, `evidence_runs: [experiment:a00-6678e0d1-53f123]` written through `write.py` (the run names itself) | experiment:a00-6678e0d1-53f123 frontmatter |
| 2 | stale citation in the round's own record — kept comment cited `provisioning.py:533-536` | FIXED: the KEY-PRESENCE comment reads at **:525-528** on the tip the kid produced; citation corrected, and the row now names the comment instead of a bare range | experiment:a00-6678e0d1-53f123 body:31 |
| 3 | order item 1 half-done — the overclaim it existed to cure survived verbatim in the node's `## Agent Notes` | FIXED: that line now reads 28 added / 12 removed = **16 net** at `bb3fd61ed`, re-cut to **8 net** (20/12) in EG.156, 39 test net — the same numbers as the Measurement section above it; and the row-1 "FIXED" claim on the round node now says PARTIAL and names the Agent Notes half | experiment:a00-9db7337e-cc325e body:90 · experiment:a00-6678e0d1-53f123 body:26 |

OUTSIDE: none — every fix sat inside FILE SCOPE.

## Why the lean on item 1 is 60 and not 70

The EG.156 round re-cut the bytes under the cap (8 net production vs cap 15) and corrected three of
its four ordered items honestly. It did not do its headline item completely — the overclaim moved
from the Measurement section into `## Agent Notes` rather than disappearing — and it left the
result unreadable by machine. That is more than a nit and less than a broken claim, so the round
carries `inconclusive_lean_proved:60` with its own node as the evidence run. The next round on this
hypothesis can raise it to 70+ now that the record and the byte count agree.

## Evidence

Citation checked by reading the bytes of the cut tip, not by trusting the node:

```
$ sed -n '201,203p' extensions/agi/bin/provisioning.py
def _prov_cell(root, name: str, default: float, cfg: dict | None = None) -> float:
    """One `provisioning.<name>` dollar cell; a pre-loaded `cfg` wins over `root`."""

$ sed -n '525,528p' extensions/agi/bin/provisioning.py
    # A KEY-PRESENCE test, not a dollar read: "absent" and "declared" must
    # stay distinguishable, and only the declared case reaches the resolver
    # below for its VALUE. The value itself is read through `_prov_cell`, so
    # a configured floor still wins here exactly as it does everywhere else.
```

So the comment the round claimed to keep at :533-536 is at :525-528 here (8 lines earlier, exactly
the eight docstring prose lines the same round folded away), and the docstring it folded to one line
is at :202 with its `def` at :201. Both citations now name the file:line they mean.

Frontmatter after the fix (`grep '^verdict\|^confidence\|^evidence_runs' -A1`):

```
8:confidence: 0.6
9:evidence_runs:
10:  - experiment:a00-6678e0d1-53f123
21:verdict: inconclusive_lean_proved:60
```

## Line budget

Production code touched: **none**. `extensions/agi/bin/provisioning.py` is byte-identical to the cut
tip — the only write verbs run this round were `write.py ... replace body` and `set` on
`.agi/nodes/experiment/*.md`. Production lines net: **0** (cap 40; the round cap of 15 over the
parent's cut was already met at 8 by EG.156). No `git` was run: this node's brief forbids it, and
the measurable surface here is three node files, not code.

Not run: the pytest suite. No code changed this round, and the byte surface that could regress is
`provisioning.py`, which is untouched. The prior round's run (`91 passed, 5 skipped`) still stands
on the same bytes.

## Left alone, named

`hypothesis:provisioning-reads-its-cells-through-one-import-route:20` cites
`provisioning.py:203` for `_prov_cell` and describes the PRE-fix defect (`sys.path.insert` per
call). The def now reads at :201. Left as written: that line is the PASS 11 finding as it was
measured on the pre-fix file, and re-pointing a historical citation at today's bytes is the same
class of error this round exists to remove. A reader following :203 today lands on the `cfg=`
branch, so the fix is a date-stamp on the historical citation, not a line-number edit — the
parent's call, not this kid's.

## Agent Notes
EG.206 (kid a00-4453045a): this node frontmatter read `verdict: proved` / `confidence: 0.85` in the MERGED tree — EG.193 claimed a demotion to inconclusive_lean_proved:40 / 0.4 that it never wrote, and the accepted review repeated the claim. The demotion is written here now, through write.py, not claimed. The lean names a RECORD defect (a self-cited round for a deliverable absent from the branch), so it does not move on its own bytes.
EG.164 record-fix: set verdict/evidence_runs on a00-6678e0d1-53f123 (lean 60), corrected its :533-536 citation to :525-528, and fixed the 28/39 'net' overclaim surviving in a00-9db7337e-cc325e Agent Notes; no production code touched (0 lines).
