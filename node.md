---
id: mvp:complete-md-the-post-loop-completion-report
mint_id: d999aebe622e4d4f9ecbce439460ad7a
type: mvp
parents:
  - hypothesis:a-loop-that-does-not-report-its-own-completion-repeats-its-gaps
next_edges: []
confidence: 0.8
edited_by: sanctuary-director
scaffold_hash: a544d6be1303f546
season: 1
status: open
tags:
  - mvp
thought_session: sanctuary-director-genVI
title: Complete md the post loop completion report
---
# mvp:complete-md-the-post-loop-completion-report

## MVP

What does this script/module do? Show the code or describe the implementation.

## Inputs

What does it take?

## Outputs

What does it produce?

## Agent Notes
**The minimum `COMPLETE.md` must satisfy.**

- **Location and shape:** repo root, `COMPLETE.md`, a `build` node with
  `payload_ref: COMPLETE.md`, versioned by the grid like `HANDOFF.md`.
- **Append-only across loops.** One section per completed loop, newest first,
  each headed with the loop id and the date range. Unlike `HANDOFF.md` it is
  never replaced — that is the entire point of having a second file.
- **Six required sections**, in `goal:g1.13`'s order: what ran; the scoreboard;
  per-active-goal progress; goals actually closed plus unsubstantiated
  completions; completion-failure categories for everything that did not close;
  what was minted in response.
- **Every per-goal claim is grounded** in a commit, a node diff or a parent
  report — never recollection. A claim that cannot be grounded is written as
  ungrounded.
- **A banked decision is a completion failure** and is categorised as one.
- **Machine-readable enough to train on:** the failure categories are a fixed
  closed set, so a classifier can later be scored against a director's labels
  (`goal:g14`).

**Falsifier:** a second loop's `COMPLETE.md` is produced with the same sections
and the carried-hazard list shrinks rather than repeats. If the second report is
a copy of the first with a new date, the format is decoration.

**Not in scope here:** generating the report mechanically. This mvp specifies the
artifact; `goal:g14` owns replacing the director with a small model that emits it.

CORRECTION 2026-09-05, owner: strike the append-only requirement above. COMPLETE.md is replaced whole by default and appended only on owner request, exactly like HANDOFF.md. Everything else in this mvp stands -- the six sections, the closed failure-category set, grounded claims, and a banked decision counting as a completion failure.

FORMAT UPDATE 2026-09-05: SEVEN required sections, not six. Section 6 is findings that are not failures, optional and omitted when empty; what was minted becomes section 7. The falsifier is unchanged.

## SD.18 BRIEF — DRAFT the L3 section of COMPLETE.md (director, gen VI, 2026-09-09)

Standing exit duty of every loop (`goal:g1.13`), not new work. **L3 is NOT closed** — whether to close it is banked to the owner — so the section lands **marked DRAFT at its top**.

### Measured by the director. Do not re-derive; verify by using.

**SCOPE, corrected against the order.** The dispatch order said `iter-L3.01..L3.44`. Measured: **47 contiguous dirs, `iter-L3.01`..`iter-L3.47`**, and **39** commits matching `^iter-L3\.`. Plus the SD rounds.

🔴 **ITERATION DIRS ARE NOT A ROUND LEDGER. Ground rounds in COMMITS.** Measured: `iter-SD.12` and `iter-SD.13` **do not exist as dirs** although both rounds demonstrably ran (SD.12 built `dispatch.py --prompt-file`; SD.13 minted 65 build nodes at commit `7fa1cca4a`), while `iter-SD.09`, `iter-SD.10`, `iter-SD.11` and `iter-SD.18` are **empty dirs that never ran**. Counting rounds by directory would overcount the dead and undercount the real.

**THE LOOP BOUNDARY.**
- L2's last round commit: **`fed533924`** (`iter-L2.13`, tests 1661).
- L3's first round commit: **`000cc83f3`** (`iter-L3.01`).
- The L3 span is therefore `000cc83f3^..HEAD`.

🔴 **START-STATE TRAP: COMPLETE.md's own L2 section is NOT L3's start state.** That section reports `tests 1629` at L2's close — but L2 then ran two more rounds, `iter-L2.12` (tests 1650) and `iter-L2.13` (tests **1661**). Take the start state from the **L2.13 commit**, and say in the report that you did and why.

🔴 **COUNTING-METHOD TRAP, measured today.** A naive `git ls-tree -r <rev> --name-only .agi/nodes` path count gives HEAD **1591 active / 189 deprecated**. The engine's own smoke gives **1586 / 194**. They disagree by exactly 5 because **deprecation is a frontmatter `status:`, not only a directory**. **Derive the start number and the end number with the SAME method, or the delta you print is fiction.** State which method you used.

**END STATE, measured by the director today (authoritative):**
- smoke: `node_count` **1780**, active **1586**, deprecated **194**
- `pytest extensions/agi/tests/ -q` -> **2256 passed, 1 skipped**
- `links.py links` -> **1760 resolved, 0 broken**
- `outcome_coverage` **0.152**

### Shape — seven sections, these exact headings, in this order

Copy the L2 section's structure verbatim (it is directly below the insertion point):
`1. What ran` · `2. Scoreboard` · `3. Per active goal` · `4. Goals closed` · `5. Completion-failure categories` · `6. Findings that are not failures` · `7. Minted or changed in response`

**The failure-category set is CLOSED. Use only these seven, and print `none` for an empty one rather than dropping it:** `saturation`, `ceiling-found-by-dying`, `late-minting`, `hazard-carry-over`, `banked-to-owner`, `verification-blindness`, `attribution-void`.

**Grounding rule, quoted from COMPLETE.md's own header — obey it literally:** every per-goal claim is grounded in a commit, a node diff or a parent report; **a claim that cannot be grounded says so**; **a decision banked to the owner IS a completion failure** — the harness's, for not giving the director enough to decide with. Never write a claim from recollection.

**PLACEMENT: newest first, APPENDED, never replaced.** Insert the whole L3 section immediately after the `---` that closes the header block and immediately **before** `## Loop L2 — 2026-09-06`. Nothing already in the file may change.

### Landing mechanism — this is also a live adoption proof

Land through **`python3 extensions/agi/bin/write.py build:COMPLETE.md "patch -"`** with the unified diff on stdin. It is fail-closed: a diff that does not apply changes nothing on disk.

🔴 **THE RECIPE, paid for in SD.15 — read it before you build the hunk.** The applier's view of the file is offset by one from a naive split, and `read` shares that exact view. So: run `write.py build:COMPLETE.md "read payload N:M"` first and **build the hunk from those exact bytes, never from your own line count.** A hunk built from a naive count is refused.

### Kids — ceiling 3, one job each

1. **Gather and ground.** Walk `000cc83f3^..HEAD`. Produce the scoreboard (same method both ends) and, per active goal, the commit / node / parent-report that grounds each claim. Mark anything ungroundable as ungroundable.
2. **Write the section**, seven headings, DRAFT marked at the top.
3. **Verify every pointer resolves** before landing.

### Acceptance — report actual output, not a summary

1. Every commit hash cited resolves: `git cat-file -e <sha>` for each.
2. Every node id cited resolves: `python3 extensions/agi/bin/links.py links` -> `broken_links` 0.
3. 🔴 **Proof it was appended, not replaced:** `git diff COMPLETE.md` shows **insertions only** — the L2, L1.13 and L1 sections byte-unchanged. A deletion anywhere below the new section fails this item.
4. The word DRAFT appears at the top of the new section.
5. `pytest extensions/agi/tests/ -q` -> 2256 passed, 1 skipped.
6. `python3 extensions/agi/bin/write_guard.py check` -> silent.
7. `python3 extensions/agi/bin/grid.py commit --all`.

**HARD CEILING: 3 kids.** DONE means the section is in COMPLETE.md, landed via `write.py patch -`, with acceptance 1-7 shown. If a claim cannot be grounded, the report says so in the report itself — that is a correct outcome, not a failure. A truthful partial beats a green report (trap 0ah).
