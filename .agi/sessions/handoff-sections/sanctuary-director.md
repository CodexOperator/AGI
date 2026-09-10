# sanctuary-director — L4 gen I slice (ROTATING at 0.5185, cap 0.47)

**Successor: L4 gen II**, brief at `.agi/sessions/quorum/sanctuary-director.md` (replaced
wholesale — read THAT, it carries the live state and every trap). This slice is the ledger.

| | |
|---|---|
| Seat worktree | `.agi/worktrees/seat-sanctuary-director`, branch `seat/sanctuary-director@s2` @ `49d06d048` |
| Prime | `belam-S1-L4-I` = `agi-c6 [cd7648]` @232 — 🔴 L3 prime @230 still alive and idle, never address it |
| Helper | `seat-sanctuary-helper-05 [3a4ed4]`, answers to this seat only |
| Suite | **2270 passed, 1 skipped** (full, foreground, in the prime's window) |
| season/s2 | merged at `aafb4be0a` — prime verified: 1828 nodes, 1634 active, 194 deprecated, grew |
| Key | **$7.87 of $15, never billed all round** · $1.00 floor untouched |
| Live at rotation | **L4.37 mine** (parent `a00-bad8beca`); helper's L4.34, L4.36, conftest round |

## Rounds this generation

**L4.20 point slice** — 14 sub-goals, brief points B1-B12/B21/B22, under EXISTING goals, no
top-level goal added, no id renumbered. **L4.28** — 10 idea->hypothesis chains, proved; the
parent iterated, using kid 1's failure to brief kid 2 through `--prompt-file`, which rescued
the round. **L4.32** — the moral owner-only rule moved out of two `write.py` literals into
`[moral].md` as data, `lean_proved:85`. **L4.01** (earlier, pre-worktree) — the `replace`
verb: offset-free partial writes, one routine for bodies and payloads.
Helper's, reviewed and accepted by me: L4.10 (tmux fixture leak, proved), L4.11
(`--prompt-file` now refuses loudly at parent tier, proved), L4.22 (workflow run-tracking,
85), L4.26 (survival modes as declared config, proved), L4.12 (disproved, correctly — its
own parent caught the red-only overclaim before the helper saw it).

## 🔴 What this generation got WRONG, recorded so gen II does not repeat it

1. **I chained `grid` and `push` after a merge without gating on it.** The merge had
   CONFLICTED on GOALS.md, so the grid versioned `build:GOALS.md` WITH CONFLICT MARKERS as
   v69. Nothing reached origin; fixed forward by re-rendering from nodes (never rewriting
   history) and v70 is byte-identical to disk. **Gate every step on the previous one.**
2. **My L4.02 claim was self-contradictory** — it demanded the rule move into schema data AND
   that the tests pass unchanged, but the fixture carries no `written_by` at all. A $0.05 kid
   caught it. Corrected IN PLACE per G6.3, not as a second node.
3. **L4.32 sits at 85 because my bound was too tight**, and I LEFT it there. Loosening a bound
   after the fact to award a higher verdict erases the finding.
4. **I hand-minted the first 14 sub-goals and argued it was right.** The owner then ruled
   "always prefer dispatch over not / always". The precision argument did not survive "always".

## 🔴 Next action for gen II

Harvest **L4.37** (`git -C <worktree> status --porcelain` before believing a branch empty),
review, merge into the seat branch. Then wait for the helper's last round, take its tip, merge
BOTH into `season/s2` against the MERGE-BASE, run the suite ONCE in a prime-cleared window,
`grid.py commit --all` THERE (it refuses on a seat branch), push, report tips and numbers.
