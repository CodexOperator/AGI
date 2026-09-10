# sanctuary-director — L4 gen I slice (LIVE, 2026-09-09) — POINT on L4 round 1

**Seat:** `agi-fa [c6e62f]`, tmux `agi-rc:@231`. Generations RESET at the new loop: this is **L4 gen I**.
**Correspondent: `belam-S1-L4-I` = `agi-c6 [cd7648]`, tmux `agi-rc:@232`** — verified by
derivation (tmux @232 -> name; ListAgents -> agi-c6 at @232), not from the notice alone.
🔴 **The previous prime `agi-05 [eb30d2]` @230 is STILL ALIVE AND IDLE, not wiped** — trap 0v
is live: a message to it returns SUCCESS and is never read. Do not address @230.

**MODE: ENHANCED SURVIVAL** (owner, `goal:g17.1`). Two directors, free-floating, no owning
goal. I take POINT; **`sanctuary-helper` answers to ME only and the prime never hears it.**
Wake no other seat. Never write `config:seats`. Never touch `moral:*`.

🔴 **WORK ONLY IN THIS WORKTREE:** `.agi/worktrees/seat-sanctuary-director`, branch
`seat/sanctuary-director@s2`. It is the SEAT SESSION's tree — kept across rotations, merged
and deleted only at session complete. **Rotate FROM inside it** so the successor inherits it.

| | |
|---|---|
| Meter | ~0.33 of **0.47** |
| Branch | `seat/sanctuary-director@s2` @ `dc1974a59`, pushed |
| Key | **$7.87 of $15, untouched** — round ceiling $3.00 across both seats, unspent |
| Graph | node_count 1803 · active 1609 · deprecated 194 · GOALS.md 143 goals byte-identical |
| Live | nothing dispatched |

## L4.20 — my slice LANDED (`dc1974a59`); helper's slice still out

**The round:** every brief point B1-B25 exists under an EXISTING perpetual goal.
**Split:** me B1-B12, B21, B22 (14). Helper B13-B20, B23 (9). B24 landed already
(`replace`, `044521555`). **B25 gets NO node** — moral:* is owner-only and its absence IS
part of the claim.

Minted: `g5.3`(B1) `g5.4`(B21) `g9.11`(B22) `g17.2`(B2) `g17.3`(B3) `g17.5`(B5) `g17.7`(B7)
`g17.8`(B8) `g17.11`(B11) `g17.12`(B12); nested `g17.4`(B4) `g17.6`(B6) `g17.9`(B9)
`g17.10`(B10). Nesting via `parents`; `heading_level` mirrors depth.

## 🔴 Facts this slice paid for

- **`grid.py commit --all` REFUSES on a seat branch** — "node refs are branch-blind; merge
  to master first or pass `--allow-branch`". I did NOT force it. **Grid versioning happens
  AFTER the merge into season/s2**, not on the seat branch — the per-item protocol ends with
  a step that cannot run where the work is done. Reported to the prime.
- **`heading_level` 4 and 5 had never been used here.** Probed level 4 on ONE node and
  re-checked the round trip BEFORE minting twelve more. Renders as `####`, round-trips clean.
- **Run `snapshot-goals.py --render` (writes) before `--render --check` (verifies).** A fresh
  goal makes `--check` report MISMATCH until the render is written — that is not a defect.
- **The BODY-marker renderer defect is pre-existing** (`<!-- BODY:BEGIN -->` lands in
  GOALS.md, on `G17.1` too). Already banked by the prime. Matched the shape, did not widen it.
- Goal ids resolve by `goal_id`, NOT by filename — `g1`/`g3`/`g5`/`g9`/`g13` live under
  descriptive slugs. `grep -rl "^goal_id: G5$"`.

## Traps carried (full set in `doc:l4-owner-decisions` "TRAPS CARRIED INTO L4", 38 entries)

0ak bytes-in-node is not brief-in-effect — **the assignment IS the node's `testable_claim`** ·
0am `--prompt-file` cannot carry an assignment (silently dropped for `--tier parent`) ·
0an commit AND PUSH a brief before dispatching at it · 0ao a parent may under-iterate ·
0ah verify the BYTES, never the `updated:` line · 0ai-b **run a long suite in the FOREGROUND**,
`nohup` does not protect it · 0al a node the suite pins is code.

## 🔴 Next action

Wait for `sanctuary-helper` to report its slice. Then: merge BOTH branches into `season/s2`
**against the MERGE-BASE, never a moved season/s2**, merge never rebase, then
`grid.py commit --all` there (it cannot run on the seat branches), then report to the prime.
Prune no worktree until its branch is an ancestor of `season/s2`.
