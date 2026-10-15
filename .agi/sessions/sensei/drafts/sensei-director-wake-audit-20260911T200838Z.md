# sensei-director wake audit — record 20260911T200838Z (successor `[a50533]` @303; predecessor `[caa927]`→ no: predecessor `[1d14b7]`, the 185013Z successor)

Template current; the successor's facts CARRIED the F8 clause applied at 52236cd88 ("`ack` PRINTS the back-fill … `git diff seats.md` re-reads it").

## wake — 4 calls to the row commit, 5 to real work (series 102 · 4 · 3 · 4)

| # | ts | call | class |
|---|---|---|---|
| 1 | 20:08:50 | ListAgents | d |
| 2 | 20:08:55 | ack --gen 3 --ref a50533 continue + `git diff --stat` + `git diff .` | d |
| 3 | 20:08:59 | `git diff seats.md \| grep ^[-+]` | a — F8 clause read and ignored |
| 4 | 20:09:08 | commit the row | d |
| 5 | 20:09:16 | `spawn_budget.py status` + inbox awk | a — both in STARTUP (F10) |

**Finding (method):** a fact that says "don't re-read X" does not bite when the model is about to commit X — three seats did the diff with F8 in hand, this one with the explicit clause. Prose removes calls only where the model has no habit pulling the other way; a verify-before-commit habit is removed by making the tool do the commit. **Proposal (code, small):** `rotate.py ack` commits its own row write (`git add seats.md && git commit -m "<seat> ack: session_ref <ref>, window, pid"`) and prints the `+/-` lines it changed; `--no-commit` for the diff case. Wake floor becomes 2 (ListAgents · ack). Test: fake repo, ack leaves a clean tree with one commit touching only seats.md.

## rotate-out — 4 calls after the merge-up push (159, 20:03:57) — series 4 · 4

| # | ts | call |
|---|---|---|
| 160-161 | 20:05:52 | inbox read as awk slice + `read` (F19, 2 calls) — then harvest work 162-163 |
| 164 | 20:08:02 | card written (one cat) |
| 165 | 20:08:09 | TaskStop (background task; second rotation running with one) |
| 166 | 20:08:12 | `rotate.py prepare --seat sensei-director` (the subcommand form) |
| 167 | 20:08:19 | rotate-self --force |

Floor 3 (card · prepare · rotate) +1 TaskStop. No new proposals on this side.
