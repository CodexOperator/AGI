---
name: agi-corrective
description: >
  Turn a merge-up-review residue into a corrective round, or into a node update: read the mur verdict
  files, triage every residue (corrective · demote · goal leaf · red · findings row), write the orders
  ONTO the hypothesis node as a `## CORRECTIVE DH.<N>` section (the graph holds them, never a scratch
  file), cut from the round's loop tip, dispatch, re-mur. Use whenever a mur verdict reads
  accept_with_residue or demote, a conjunct is NOT_MET, or a harvest turns up a red on a loop branch.
---

# agi-corrective — residue ▸ triage ▸ node update ▸ corrective round ▸ re-mur

Owner 2026-09-27 05:3xZ (director-engine pane): "You should have a goal corrective or goal update skill."
Standing rule it serves: the director template §2 "mur residues close in-loop". Dispatch flags: skill `agi-dispatch` §2.

## 1 · The loop
```
mur run ──▶ READ verdicts (§2) ──▶ TRIAGE each defect / missed item (§3)
                                      │
      ┌──────────────┬───────────────┼──────────────────┬───────────────────┐
  corrective      demote         goal leaf            [red]            findings row
  (§4-§5)      (measured why   (skill agi-goal §5:   (MAJOR: rule,     (engine/process defect
               in the merge    a residue big enough  design, cost,      not in this round's
               commit + card)  for its OWN round)    Prime/owner call)  claim: goal:g7.33.19)
      │
      └─▶ re-mur the corrective's loop branch ──▶ residues 0 ──▶ merge the chain (template §1) ──▶ ONE [merge-up]
```

## 2 · Read the verdict files — never the log's summary line
`/data/work/agi/.agi/sessions/workflows/runs/<mur-key>/{review,verify}_<label>.json`
| stage | fields |
|---|---|
| review | `verdict_recommendation` · `conjuncts[].status` (MET · NOT_MET · UNVERIFIED) · `defects[]` {title, file, line, detail, severity: residue \| note} · `config_max` · `template_max` |
| verify | `final_recommendation` (accept · accept_with_residue · demote) · `verdicts[]` {defect, refuted, reason} rules on the review's defects · `missed[]` = new residues |
| `{"unstructured": …}` | read the prose; the stage did not return the schema |
Verify WINS over review. A verify that died (memory-cap rc=-9, timed out) leaves the review's defects standing: triage them,
never re-run the whole mur just to get a verify the corrective will supersede.

## 3 · Triage — one row per defect
| the defect is | do |
|---|---|
| a `residue` in THIS round's claim, bytes or nodes | corrective (§4) — batch every residue of the round into ONE corrective |
| a NOT_MET conjunct | corrective; or split: the conjunct becomes a goal leaf when it needs a new claim / >1 round |
| `config_max` / `template_max` = yes | corrective naming the EXACT cell or line (never accepted as code) |
| a `note`, or a refuted defect | demote: the measured reason (command + number) in the merge commit and the card's chain line |
| a ceiling breach alone (kids, lines) | not a corrective: a findings row (the parent ignored the CEILING) |
| rule-changing · design above the node · cost/model · Prime/owner-only | `[red]` to your master, named MAJOR — never a corrective |

## 4 · The node update (the orders live in the graph)
Write the orders ONCE to a scratch file, then append it to the hypothesis node's body; the same file is `--orders`.
```bash
N=$(python3 extensions/agi/bin/write.py hypothesis:<id> 'read body 1:9999' | wc -l)   # body length L
# file = line L verbatim, a blank line, then the section below  (append = replace body L:L; there is no END keyword)
# body ENDS in a THOUGHT block (L = '<!-- THOUGHT:END -->')? the paragraph guard refuses L:L -> N = the last one-line
# paragraph ABOVE THOUGHT:BEGIN (read the body numbered first); the section goes before the block, never inside it
python3 extensions/agi/bin/write.py hypothesis:<id> "replace body $N:$N <file>" --actor <post> --role director
python3 extensions/agi/bin/write.py hypothesis:<id> 'thought corrective DH.<N>: <mur key> <labels>: <residues in one line>' --actor <post> --role director
# order: node section FIRST, verify it landed (read the range), THEN dispatch -- a refused write does not stop a chained dispatch
git commit <exact node path>      # a real commit before dispatch (grid history)
```
Section shape, every line explicit:
```
## CORRECTIVE DH.<N> -- closes <mur key> <label> (<recommendation>)
BASE      CUT FROM <loop branch> tip <sha> (worktree <path>). No merge. Never rebase.
1. <residue title> -- <file>:<line> -- <what is true when fixed> (re-run the command, paste the output; never type a number)
2. …
ANON      no user name, home or repo path value, host or IP; patterns write <user>
FILE SCOPE <the files named in 1..n + the kid's own node>
CEILING   HARD CAP: <k> kid(s) · <n> production lines · <t> test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit
```

## 5 · Cut + dispatch + close
```bash
git worktree add -b de-base-<N> .agi/worktrees/de-base-<N> <loop tip>
cd .agi/worktrees/de-base-<N> && python3 extensions/agi/bin/dispatch.py . DH.<N> --target hypothesis:<id> --level small \
  --tier parent --role parent --ladder-tier 0 --branch --detach --orders <file> --from <post> --allow-stale-base "<reason>"
```
The card's chain row gets the new tip (`<chain> <N> LIVE`). On harvest: agi-dispatch §5 traps → mur over `<prev tip>..<new tip>` only
(skill agi-workflow) → back to §2. A chain merges only at its LAST cleared tip, in the order the card names.
