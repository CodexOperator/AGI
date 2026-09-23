---
id: experiment:a00-39a8276d-9dfd67
mint_id: 494c17ef86e34e9aab0b73d19ef9c01a
type: experiment
parents:
  - hypothesis:l5-tracked-files-name-origin-by-its-current-url
next_edges: []
confidence: 0.65
edited_by: a00-b2669331
evidence_runs:
  - experiment:a00-39a8276d-9dfd67
line_ceiling: 40
loop: hypothesis:l5-tracked-files-name-origin-by-its-current-url@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "git grep -c 'CodexOperator/agi[^-]' -- README.md", "expected": "README.md carries a live-repo literal (claim 1 names it)", "observed": "0 -- README.md's only match is CodexOperator/agi-tree at :49, a different repo never renamed; the live literals were QUICKSTART.md:62,66 and context/refs/legacy-prestate.md:23, which the claim's scope did not name", "result": "refuted -- claim (1) membership is wrong"}
  - {"conjunct": 2, "class": "wire", "cmd": "git remote -v; git show 1347bf7c8 --numstat; git grep -c 'CodexOperator/AGI' -- QUICKSTART.md TODO.md package.json context/refs/legacy-prestate.md", "expected": "changed bytes name the live repo and each rewrite lands", "observed": "origin https://github.com/CodexOperator/AGI.git; 2/2 QUICKSTART.md, 3/3 TODO.md, 1/1 legacy-prestate.md, 1/1 package.json; each now carries AGI 2/3/1/1", "result": "held for the 4 files the parent rescoped; claim (2)'s README.md and '2 nodes' were NOT rewritten -- by the parent's own corrected order, no node hand-edited"}
  - {"conjunct": 3, "class": "gate", "cmd": "git grep -n 'CodexOperator/agi' -- .", "expected": "only the rotation record", "observed": "12 residual lines: doc/l5-owner-decisions.md:111, experiment/a00-75e7c869:50,101, hypothesis/l4-a-worktree:36, rotations/...sensei-director...json:80, README.md:49 + TODO.md:839 (agi-tree substring), plus the kid's own node quoting them", "result": "refuted -- claim (3) is false as written; the kid recorded it false rather than falsifying records"}
  - {"conjunct": 4, "class": "wire", "cmd": "git show --name-only --format= 1347bf7c8 | grep -c 'extensions/agi/bin/'; git grep -n 'CodexOperator/agi' -- extensions src skills", "expected": "0 bin/ files changed so test_bin_help_smoke.py is untouched; no code consumes the old literal", "observed": "0 bin/ files in the diff; no matches under extensions/, src/, skills/ (agi-tree excluded)", "result": "held -- the smoke-test precondition is real and nothing consumes the literal"}
production_lines: 7
profile: balanced
role: kid
scaffold_hash: e1f5521e0bc0d9ad
season: 2
title: Repointed the live-repo origin literal CodexOperator/agi -> CodexOperator/AGI in 4 files (7 lines); 7 named residuals stay, none an address
town: core
verdict: inconclusive_lean_proved:65
---
# experiment:a00-39a8276d-9dfd67

## Experiment

Build order, not a measurement exercise (goal:g15). The target claim (1) named
the wrong file set; the parent's correction supplied a measured list. I ran the
grep myself and rewrote the LIVE-repo address literal `CodexOperator/agi` ->
`CodexOperator/AGI` in the four files that name the repository address. Target
CEILING was 6 changed lines; the measured live-address set is 7, so the ceiling
is crossed by one line and reported rather than padded down.

### 1. Pre-change measurement (my checkout, cwd at branch HEAD)

Command: `git grep -n 'CodexOperator/agi' -- .`

Live-address literals (the rename target), all measured:

| file:line | content (trimmed) |
|---|---|
| QUICKSTART.md:62 | `` `CodexOperator/agi` is **private**, default branch `master` `` |
| QUICKSTART.md:66 | `git clone git@github.com:CodexOperator/agi.git ~/work/agi` |
| TODO.md:601 | `agi/  ← GITIGNORED drop-in clone of CodexOperator/agi` |
| TODO.md:606 | `# agi research-loop engine (drop-in clone of CodexOperator/agi — never commit here)` |
| TODO.md:859 | `Update ... README with prominent pointer to CodexOperator/agi.` |
| package.json:8 | `"url": "git+https://github.com/CodexOperator/agi.git"` |
| context/refs/legacy-prestate.md:23 | `... README updated to point at CodexOperator/agi` |

Target claim (1) named README.md, TODO.md, package.json, "2 nodes", and the
rotation record. Measured: **README.md carries NO live-repo literal** — its only
match is `CodexOperator/agi-tree` (line 49), a *different repository that was
never renamed*. The target's membership was wrong and is recorded as false, not
deleted.

`origin` is `https://github.com/CodexOperator/AGI.git` (measured: `git remote -v`).

### 2. Edits made (7 lines, 4 files)

`QUICKSTART.md:62,66`; `TODO.md:601,606,859`; `package.json:8`;
`context/refs/legacy-prestate.md:23` — the address literal rewritten in place.
`package.json` verified parseable (`json.load` -> `git+https://github.com/CodexOperator/AGI.git`).
These are build-node payloads (`.agi/nodes/build/QUICKSTART.md.md`,
`build:package.json`, `build:context-refs-legacy-prestate.md`); under goal:g11
the payload IS the source file, so the edit is made directly in the source tree —
no node hand-edit, no `grid.py checkout`, no `write.py` for payloads.

### 3. Post-change grep — the residuals, line by line, and why each stays

`git grep -n 'CodexOperator/agi' -- .` after the change returns exactly:

1. `.agi/nodes/doc/l5-owner-decisions.md:111` — owner-decision history: the
   2026-09-18 delete/recreate log entry. It names the literal as a *past event*.
   Rewriting a record of what happened would make the record untrue. STAYS.
2. `.agi/nodes/experiment/a00-75e7c869-24b9f0.md:50` — prose inside a historical
   experiment record ("same repo, same origin (`CodexOperator/agi.git`)"). It is
   the node's account of the state observed at that run, not a live address
   document. STAYS.
3. `.agi/nodes/experiment/a00-75e7c869-24b9f0.md:101` — **pasted command output**
   (`origin https://github.com/CodexOperator/agi.git (fetch)`). This is a
   MEASUREMENT. Rewriting it makes the record claim an output never observed.
   STAYS (parent's explicit order).
4. `.agi/nodes/hypothesis/l4-a-worktree-looks-like-a-project-to-the-crontab.md:36`
   — **pasted error text** (`fatal: unable to access '.../CodexOperator/agi.git/':
   ... 403`). Same reasoning: a measurement, not an address. STAYS.
5. `.agi/sessions/rotations/sensei-director.20260916T072304Z.json:80` — a rotation
   record. History; not a live address. STAYS (parent's explicit order).
6. `README.md:49` and `TODO.md:839` — `CodexOperator/agi-tree`, a **different
   repository, never renamed**. A naive substring grep matches them. Rewriting
   another repo's name to make a grep come clean manufactures a false artifact.
   STAYS.

**Target claim (3) — "after the change grep finds only the rotation record" — is
FALSE as written**, for reasons 6 (substring collision with `agi-tree`) and 1-4
(history/measurement records). Recorded false; not satisfied by falsifying files.

Net: zero *live-address* literals of the old URL remain in tracked files. Seven
residuals remain, each named above with a reason; none is an address.

## Evidence

- Pre-change grep: table in §1 above (full output captured from this checkout).
- Post-change grep: the seven residual lines in §3, verbatim above.
- Live-address check post-change:
  `git grep -cn 'CodexOperator/AGI' -- QUICKSTART.md TODO.md package.json context/refs/legacy-prestate.md`
  -> `QUICKSTART.md:2`, `TODO.md:3`, `context/refs/legacy-prestate.md:1`, `package.json:1`.
- Production lines: `git diff --numstat` -> `2 2 QUICKSTART.md`, `3 3 TODO.md`,
  `1 1 context/refs/legacy-prestate.md`, `1 1 package.json` = **7 changed lines**
  (7 added, 7 removed). Target CEILING 6 -> crossed by 1 (reason: the measured
  live-address set is 7 lines, not 6). Production-line ceiling 40 -> well under.
- JSON validity: `python3 -c "import json;print(json.load(open('package.json'))['repository'])"`
  -> `{'type': 'git', 'url': 'git+https://github.com/CodexOperator/AGI.git'}`.
- TESTS: `python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q`
  -> `71 passed, 4 skipped in 12.47s` (nothing under `bin/` changed).
  Tier gate printed one phantom-record skip line, not a failure.

## Agent Notes
Repointed live-repo literal CodexOperator/agi -> CodexOperator/AGI in QUICKSTART.md:62,66, TODO.md:601,606,859, package.json:8, context/refs/legacy-prestate.md:23 (7 lines, target CEILING 6 crossed by 1 and reported); tests 71 passed/4 skipped. Claim (1) membership and claim (3) 'only the rotation record' measured FALSE and recorded as false: 7 residuals stay with a reason each (rotation record, owner-decision history, experiment pasted output at :101, experiment prose at :50, pasted fatal:403, and CodexOperator/agi-tree substring collisions at README.md:49/TODO.md:839). Old literal remains nowhere as a live address.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW by parent a00-b2669331, iter 149. (1) WHAT THE INSTRUCTION SAID: the target claim (1) says "The old literal origin URL appears in 6 tracked files (README.md, TODO.md, package.json, 2 nodes, 1 rotation record)" and claim (3) says "grep -rn for the old literal over tracked files after the change finds only the rotation record". (2) WHAT THE MACHINE ACTUALLY DOES: git grep -c "CodexOperator/agi[^-]" -- README.md returns 0 -- README.md's only match is CodexOperator/agi-tree at :49, a DIFFERENT repo that was never renamed; the live-repo literals were instead in QUICKSTART.md:62,66 and context/refs/legacy-prestate.md:23, neither named by the claim. Post-change git grep -n "CodexOperator/agi" returns 12 residual lines, not one. Measured this checkout, branch HEAD 1347bf7c8. (3) THE NEAR MISS: a kid obeying claim (2) literally rewrites README.md:49 and TODO.md:839 (agi-tree, a repo that still exists under that name) and rewrites the pasted remote output at experiment/a00-75e7c869:101 and the pasted 403 at hypothesis/l4-a-worktree:36 -- and the grep then comes back clean while the record claims the machine observed something it never observed. Satisfies the words; destroys the artifact. (4) DEVIATION: I rescoped the kid to the MEASURED live-address set (QUICKSTART, TODO, package.json, legacy-prestate) and ordered pasted output and history left alone, because a g15 build order's product is a TRUE ADDRESS, not a clean grep. The kid obeyed, measured claim (1) and claim (3) false, and recorded them false rather than falsifying the residuals -- which is the behaviour I wanted. CEILING: target said 6 changed lines; the measured live-address set is 7 (QUICKSTART 2, TODO 3, legacy-prestate 1, package.json 1). The kid crossed by 1 and reported it; the overrun is MINE, not the kid's, since my correction widened the file set. RESIDUAL RISK (not this kid's scope): QUICKSTART.md:62 still says the repo "is private", but l5-owner-decisions:111 records the repo was recreated PUBLIC -- the rewrite carried a pre-existing falsehood forward. VERDICT: keep inconclusive_lean_proved:65. The implement landed and the wire is clean (4 probes above); claim (1) and claim (3) are false as written and were measured false, so the target claim as a whole is not proved.
<!-- THOUGHT:END -->

PARENT REVIEW (a00-b2669331): ACCEPTED, kept at inconclusive_lean_proved:65. Diff read, not the result file: 4 source files, 7 lines, all address literals (QUICKSTART.md:62,66; TODO.md:601,606,859; package.json:8; context/refs/legacy-prestate.md:23); zero files under extensions/agi/bin/; README.md and the 2 nodes deliberately untouched per the parent corrected order; no node hand-edited. Four parent-run probes recorded (see probes:). Probe conjunct 1 (gate) REFUTED the claim's file set -- README.md carries no live-repo literal, only the agi-tree substring. Probe conjunct 3 (gate) REFUTED "only the rotation record" -- 12 residual lines survive. Probe conjunct 2 (wire) HELD -- origin is CodexOperator/AGI.git and every changed byte names the live repo. Probe conjunct 4 (wire) HELD -- 0 bin/ files in the diff and no code/test consumes the old literal. No demotion: the kid REPORTED conjuncts 1 and 3 false instead of claiming them true, and did not falsify the residuals to make a grep come back clean. Ceiling note: production_lines 7 vs target CEILING 6 -- overrun owned by the parent rescope, not charged to the kid.
