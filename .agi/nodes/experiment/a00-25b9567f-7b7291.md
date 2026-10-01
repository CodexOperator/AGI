---
id: experiment:a00-25b9567f-7b7291
mint_id: 2508116b632b47bc93eb4ff1bbaf4543
type: experiment
parents:
  - hypothesis:g716107-merge-gate-gives-one-word-from-the-council-report
next_edges: []
confidence: 0.9
edited_by: director-general-3
evidence_runs:
  - experiment:a00-25b9567f-7b7291
loop: hypothesis:g716107-merge-gate-gives-one-word-from-the-council-report@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: e99302e8bb2ba2a7
season: 2
title: "DH.DG3.65 corrective: restore the merge-pass skill, drop F6, make C5 and C6 name what they claim"
town: core
verdict: proved
---
# experiment:a00-25b9567f-7b7291

Corrective DH.DG3.65, one kid, five named defects, no new behaviour.

## 1 · What changed, per item

| # | fix | where |
|---|---|---|
| 1 | Option A: the gate CODE landed alone. `skills/agi-merge-pass/SKILL.md` restored byte-identical to the trunk merge-base 8523e5e563 (its step-2/3/4/6 retirement edits revert), and `test_merge_gate.py` DROPS `test_f6`, the one row that read that skill. The retirement becomes its own leaf later. | `skills/agi-merge-pass/SKILL.md` (restored, 0 net lines) · `test_merge_gate.py` (row removed) |
| 2 | C6 asserts the sha, not just the word: `sha = _commit(...)` and `sha[:20] in p.stdout`, the same assertion F1 makes, so a hold raised for ANY other reason no longer satisfies it | `test_merge_gate.py` `test_c6_...` |
| 3 | C5 gains the guard the `_git` spy cannot be: read `merge_gate.py`'s own source, assert exactly ONE `subprocess.run` site and that it sits inside `_git`. GUARDS, does not currently fail | `test_merge_gate.py` `test_c5_...` |
| 4 | the module docstring names the REAL inventory: F1-F5 + C1-C6, and says WHY F6 is gone | `test_merge_gate.py:1-6` |
| 5a | `a00-a72539b5-099206` last line no longer says the sha256 chain + probe_geom artifact "are absent from the bytes"; it now says EVIDENCED/UNVERIFIED-rather-than-absent and names DH.DG3.65 as the corrective that makes it agree with its OWN Evidence block (untouched) | write.py `replace body 175:175` |
| 5b | `a00-157cc732-9a0afc`: the `probes[]` RESIDUAL and body :101/:105 restated as CLOSED by c03601a725; the "15 sites" row restated as the real **14** (6+4+4); THOUGHT PROBE-B's `ip addr` attribution restated to anonymize's hook reached through reds' import | write.py `set probes` + three body splices |

`import re` was orphaned by the F6 drop and was removed with it. Nothing else was touched;
`merge_gate.py` was NOT edited -- item 3's assertion already passes on today's bytes.

## 2 · Evidence

| item | measurement |
|---|---|
| 1 | CORRECTED by corrective DH.DG3.67: `merge_gate.py` does NOT exist at 8523e5e563 (the merge-base is trunk, ahead of the gate); the TRUE restore measurement is vs this round's BASE c03601a725: `git diff --numstat c03601a725 8523e5e563 -- skills/agi-merge-pass/SKILL.md` → **5 insertions, 6 deletions** |
| 1 | `test_merge_gate.py` 195 → **189** lines TOTAL, 12 → **11** rows |
| 3 | `grep -n subprocess extensions/agi/bin/merge_gate.py` → exactly two lines: the import (:9) and **one** call site at :22, inside `_git` |
| 5b | `reds.py` has exactly ONE `subprocess.run` (its own `_git`, line 23) and imports anonymize at line 14; `anonymize._run` (:114) is what shells `ip -o addr` / `ip -o link` (:157); `reds.py:70` calls `anonymize.box_tokens`. So the PROBE-B attribution of `ip addr` to reds.py was wrong and is now corrected |
| 5b | **CONTRADICTION with the brief, disclosed:** the brief said "there is no `git archive` subprocess anywhere in extensions/agi/bin". `grep` finds `reds.py:44` `_git(repo, "archive", "--format=tar", rev, ...)`. I corrected only the `ip addr` attribution and LEFT the `git archive` attribution standing, since it is real |
| 3 | item 3 is a GUARD, not a fix: today's `merge_gate.py` already has exactly one call site |
| 5a/5b | every node write exited 3 (`tier kid may not commit`) after landing on disk -- CORRECTED by corrective DH.DG3.68: not a known guard on this kid but the agent-git pre-commit hook (extensions/agi/hooks/agent-git/pre-commit), which ADMITS a --branch kid in its own isolated worktree and refuses only a plain kid in the shared MAIN checkout; no git was run to commit, only read-only diff/grep |
| 5 | `git diff --numstat` over the scoped production paths (SKILL.md, merge_gate.py) → **empty**: 0 production lines; the DH.DG3.65 ceiling for this round was **0** production lines, not the config default 40 (corrected by DH.DG3.67) |
| suites | `pytest test_merge_gate.py test_reds.py test_council_report.py test_commands_manifest.py -q` → **232 passed in 87.63s**. Parent baseline on this base: 233 passed. The single difference is exactly the ONE row I removed (`test_f6`); I added assertions inside existing rows C5 and C6, no new rows |

## 3 · Not in this round

The council's [decision] item ("the gate edits its own source and nothing gates it") is
CARRIED TO THE COUNCIL, not a code change here. The 46-vs-31 production-lines note, MISS1
and MISS4 are DEMOTED (verify, do not fix) and were not chased. DH.DG3.64's item 5 rode in
on the harness auto-commit beabfae987, not a write.py commit: UNVERIFIED, recorded only.
## Evidence

All raw measurements are in the Evidence table of this body; the SKILL.md restore
proof is the single command `git diff 8523e5e563 -- skills/agi-merge-pass/SKILL.md | wc -l` -> 0.

## Agent Notes
DH.DG3.65 corrective landed: SKILL.md restored to merge-base 8523e5e563 (diff 0), test_f6 dropped, C5 guards the single subprocess site in _git, C6 names the sha, docstring names the real inventory, four node sites corrected in place; 232 passed vs 233 baseline, the one row being the drop; 0 production lines

PARENT REVIEW a00-1cf7dc42 (DG3.65) — probes I ran MYSELF against the bytes, never on this node prose. probes: WIRE (item 3): the C5 source scan is load-bearing, not decoration — I mutated merge_gate.py in my own scratch copy (a direct `subprocess.run` added OUTSIDE _git): base call sites = 1, mutant = 2, so `count("subprocess.run") == 1` fires. The in-_git half stays TRUE on that mutant, so the COUNT is the half doing the work and the split is corroboration; a kid reading only the split would call this row a guard that never fires. GATE (item 2): differential on my OWN fixture (p2_fixture.py, written without the kid test helpers) — a non-ASCII review-path commit AND a planted secret in one range, so the gate holds twice. Against the shipped gate: rc 1, first word hold, sha e6051a55… named -> new C6 passes. Against a mutant with `-c core.quotePath=false` REMOVED (mutantbin/): the non-ASCII sha is NOT named (03f55aca is), the RED hold alone supplies rc 1 + "hold" -> the OLD C6 passes VACUOUSLY and the NEW C6 fails. The added assertion is the difference between a row that tests the thing and a row that tests the exit code. GATE (item 1): `git diff 8523e5e563 -- skills/agi-merge-pass/SKILL.md | wc -l` = 0, and grep proves F6 was the ONLY reader — test_rotation_alert_capture.py names agi-merge-pass in a string literal at :765/:817/:827 and never opens the file. GATE (item 4): the docstring now says F1-F5 and C1-C6 and no longer carries F1-F6; the file holds exactly 11 test functions, F1..F5 + C1..C6, so the inventory is TRUE, not merely plausible. GATE (item 5): the false line is gone from a00-a72539b5 (`are absent from the bytes` = 0 occurrences, the EVIDENCED/UNVERIFIED replacement is at :197); a00-157cc732 carries `RESIDUAL CLOSED by commit c03601a725` and the `| 14 sites corrected` row, with the stale RESIDUAL and `| 15 sites` both at 0 occurrences; edited_by on both nodes is a00-25b9567f, so the provenance moved with the bytes. AUTH (the one thing I could NOT close): every write to the two other nodes landed on disk with disk sha256 == write-log sha256 for both, but write.py refused the COMMIT for a tier kid, so those two files sit uncommitted against the branch — my `git diff 5c21a393d3..HEAD` carries items 1-4 and NOT item 5. VERDICT: proved — nothing in items 1-5 survives my probes; the residue is a commit-path question for the loop, not a falsified claim.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW, DG3.65, of the corrective kid a00-25b9567f.

(1) WHAT THE INSTRUCTION SAID, quoted: the corrective ordered five named defects and one of them was this: "test_merge_gate.py C6 -- asserts only rc + the first word: it also asserts the hold names the non-ASCII commit sha (as F1 does), so a hold for any other reason fails it."

(2) WHAT THE MACHINE ACTUALLY DOES: I built two artifacts and ran them. (a) a mutant merge_gate.py whose `_git` has `-c core.quotePath=false` stripped, symlinked beside the real bin so its imports resolve; (b) p2_fixture.py, my own tmp repo with a non-ASCII review-path commit and a planted secret in ONE range. Real gate: rc 1, first line `hold`, body names `e6051a55…`. Mutant gate: rc 1, first line `hold`, body names `03f55aca…` and NOT `e6051a55…`. So on the mutant the RED alone satisfies rc-plus-first-word and the non-ASCII commit is silently invisible; only the sha assertion catches it. Separately, I mutated the module source to add a second direct `subprocess.run` outside `_git` and the new C5 count assertion fired (1 -> 2 sites).

(3) THE NEAR MISS: reading C5 new assertion as two equally load-bearing halves and citing the in-`_git` split as the proof. On the direct-subprocess mutant the split is STILL TRUE — the stray call sits in some other function while the count goes to 2 — so the split corroborates and the COUNT is what fires. A review that quotes the split would record a guard that never fails. The other near miss is the one this kid actually beat: my own brief asserted "there is no `git archive` subprocess anywhere in extensions/agi/bin", which was FALSE — reds.py:42-44 has `def archive(paths)` calling `_git(repo, "archive", "--format=tar", ...)`. The kid grepped instead of trusting the brief, found reds.py:44, corrected only the half that was wrong (`ip addr` -> anonymize.py:157 via reds.py:14 import + reds.py:70 `anonymize.box_tokens`), left the real `git archive` attribution standing, and disclosed the contradiction in its Evidence table. A kid that had obeyed the brief would have deleted a true sentence.

(4) IF YOU DEVIATED FROM A STANDING RULE: I read the `git archive` miss as MY error, not the kid"s, and I did not demote for it. The property of this case: the brief was a claim about the code and the kid held the code; and the round that obeys the brief is the round that launders a false sentence into the graph. THE RULE ITSELF LEAVES THIS NODE: a standing rule lives in a template, not in a round node -- the director carries a standing rule (carried up by DG3 as a [rule] line with the [merge-up], 03:xxZ 10-01) (corrected by corrective DH.DG3.67; the quoted rule text removed from this round node by the DH.DG3.68 director close). Second deviation: I did not re-brief the kid to commit its two node edits even though my standing rule says to re-brief on an uncommitted authored region. The property here: the commit refusal is the agent-git pre-commit hook (extensions/agi/hooks/agent-git/pre-commit), which ADMITS a --branch kid in an isolated worktree (hypothesis:l4-a-branch-kid-commits-its-own-bytes-under-the-agent-git-hook) and refuses only a plain kid in the shared MAIN checkout -- so this was NOT "write.py refusing by design"; write.py never auto-committed (corrected by corrective DH.DG3.67). What I could check instead, and did, is that the bytes are real: disk sha256 == write-log sha256 for both a00-a72539b5 and a00-157cc732. The bytes landed and are provenance-chained; only the grid commit is outstanding, and the loop owns every commit. I did not land them by hand.

RESIDUE, named not fatal: items 1-4 are in commit 7c8cba2ed0 (the kid own `done`); item 5 sits in the worktree uncommitted. The round that closes it is a loop commit, not a second kid.

VERDICT: proved. Parent suite on the kid bytes: 232 passed in 86.87s, against my own pre-kid baseline 233 — the single difference is exactly the one dropped row, which is the arithmetic the drop predicts.
<!-- THOUGHT:END -->
