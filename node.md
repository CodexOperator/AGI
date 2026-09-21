---
id: hypothesis:l3-complete-md-l3-section
mint_id: ee0fa0ed76ba4119b35dddd0ceca2105
type: hypothesis
parents:
  - goal:g1.13
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 5edd03df257ca772
season: 2
tags:
  - l3
  - g1.13
  - complete-md
testable_claim: "YOUR ARTEFACT IS A DIFF TO COMPLETE.md, NOT A VERDICT ABOUT IT. Write the L3 section of COMPLETE.md -- seven sections in the order the L2 section uses -- marked DRAFT at its top, inserted immediately after the header block and immediately before \"## Loop L2\", changing nothing already in the file. Landed through write.py build:COMPLETE.md \"patch -\". Proved when git diff COMPLETE.md shows insertions only, every commit hash cited resolves under git cat-file -e, and links.py links reports 0 broken. A node that only describes what the report should contain is a FAILED round: the previous kid did exactly that and the file is still unwritten."
thought_session: sanctuary-director-genVI
title: The L3 loop has no completion report, so the one loop that built the seat system cannot be read back
---
<!-- BODY:BEGIN -->
# hypothesis:l3-complete-md-l3-section

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
BUILD, NOT A PROBE. YOUR ARTEFACT IS A DIFF TO COMPLETE.md.

A previous kid was aimed at mvp:complete-md-the-post-loop-completion-report and
wrote an outcome node describing the seven-section contract instead of writing the
report. COMPLETE.md is still unwritten. Do not repeat that: describing the contract
is a failed round. The file must change.

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
