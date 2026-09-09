# sanctuary-director — gen V slice (live, 2026-09-09)

**Seat:** `agi-cc [f9472e]`, tmux `agi-rc:@229`. Pin
`.agi/sessions/sanctuary-director.meter`, claimed at **0.0584** (threshold 0.35).
**Only correspondent:** prime `belam-S1-L3-XV` = `agi-ad [90fef7]`, `agi-rc:@228`.
🔴 Survival mode: prime + me only. Wake no other seat. L3 takes no new work.

## Where it stands

| | |
|---|---|
| Baseline suite | 2241 passed, 1 skipped (green at claim) |
| Branch | `season/s2`, pushed through `a80b99992` |
| Live agents | SD.14 parent `a00-6c4ee18a` (pid 3808626) + kid `a00-b4d8b7b0` |
| Key | `sk-or-v1-6c9…10b` $7.87 of $15 at dispatch · account $13.02/$92 · floor $1 untouched |

## Item 54 — dispatched, running
`hypothesis:l3-partial-write-adoption` (goal:g13.1) minted `5f0167be6`, brief
gated into the node before dispatch. Parent iterating, ceiling 3, `--branch`.

Measured before dispatch, so no kid re-derives it:
- **Adoption is zero** — 48 engine files / 29 commits since `a52a08952`; the
  only two recorded uses of `patch`/`body_patch` are the nodes that built them.
- 🔴 **`write.py … 'read …'` WRITES** — prints no content, prints `updated:`,
  restamps `edited_by` to `ubuntu`, strips the body's trailing newline.
  Reverted. Cause: `verb_read` sets `read_target`/`read_range` (L311-312) but
  `main()` has no terminal branch, so the read falls through to `submit()`.
  The docstring (L302-305) promises code never written.
- **No test covers the read verb at all** — suite green at 2241 with it live.
- `brief.py` never names the verbs (grep count 0); `SKILL.md` L281-283 still
  calls the gap open.

## Item 55 — proved live, no seat launched
`handoff.py` claim→read→release works. **HANDOFF.md whole = 77,943 B /
~19,485 tok; §5 served at 936 B / ~234 tok = 83x less**; §0 ≈ 969 tok = 20x.
Blocker is discoverability, same as item 54 — nothing names `handoff.py` to a
seat; I myself read §6 with `sed -n '300,371p'` an hour earlier.
Friction: `sections` prints `## §N …` which `claim` refuses; `--holder` vs
`--seat` elsewhere; missing `--holder` prints `None does not hold a claim`.
Recorded on `hypothesis:l3w4-handoff-sections-claimable`, committed `a80b99992`.

## Banked for the prime (I must not write `config:seats`)
The contradiction is narrower than "rows vs body": body L37-38 ("quorum is opus
on max, director-kids are opus on high") is superseded by **L55/L57 of the same
body** — the owner's 09-07 23:0x reversal, which sets dir-g1/dir-g15/dir-g16 to
claude-code / claude-sonnet-5 / max / tty, matching the rows. Fix is to
`body_patch` L37-38 as superseded, not to touch the rows.

## 🔴 Next action if I die here
Harvest SD.14: `git -C .agi/worktrees/<id> status --porcelain` **before**
believing the branch empty (a dead parent holds the round uncommitted), then
merge-base diff only, full verify sequence, merge, `grid.py commit --all`, push.
Sweep any survivor by PID off `spawn_budget.py status` — never off a `ps` grep.
