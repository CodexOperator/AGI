---
id: hypothesis:wake-facts-collapse-to-skill-pointers
mint_id: 2a67da86c6424979801d44473a0484a0
type: hypothesis
parents:
  - goal:g4.18.2
next_edges: []
edited_by: director-engine
scaffold_hash: 1bd0bc68051b4ea8
season: 2
testable_claim: config:rotations facts region = one pointer line per F-number to skills/agi-*/SKILL.md, <= 2000 bytes (from 7164), first_turn range re-derived, pinned rotate tests updated in the same commit, suite green; rotate.py DEFAULT_CC_ROLES carries no ultracode
title: "The wake facts collapse to skill pointers under 2000 bytes, tests re-pinned in the same commit (assigned: director-engine)"
town: core
---
# hypothesis:wake-facts-collapse-to-skill-pointers

# hypothesis: the wake facts collapse to skill pointers (assigned: director-engine)

## Why this exists
**Parent `goal:g4.18.2`** (owner 01:1xZ 09-27: "a lot of your And other posts card f rules go into those and everyone's card just lists all the relevant skills"). The Prime landed eight flow skills (`skills/agi-*/SKILL.md`, build nodes `build:skills-agi-*-SKILL.md`) that now carry every F-rule the `config:rotations` facts block prints at each wake. The facts block itself was NOT trimmed by the Prime because it is an engine contract pinned by tests:
- `test_rotate_templates.py:387-450` resolves the wake-read region from the templates' own `facts` first_turn cmd (`read body 37:64`, `rotations.md:76` + `:114`) and `:534` asserts the live region still holds a hand-vocab hit (F16);
- a 7200-byte guard on the region (rotations.md steps note, 09-25);
- ten rotate test files read `config:rotations`, and rotate test files are never run from a post's pane.

## Testable claim
The facts region becomes one line per live F-number of the form `F<n> -> skill agi-<flow> (§<k>)` (plus any fact no skill carries, verbatim), the `facts` first_turn cmd's range is re-derived to match, the pinned tests are updated to the new contract in the same commit, and the region measures <= 2000 bytes (from 7164 at 01:0xZ 09-27) with the full suite green.

## Also (same round, one line each)
- `rotate.py:120` DEFAULT_CC_ROLES still carries `"settings": {"ultracode": True}` (and `effort: max`) for prime_director; the owner dropped ultracode from everyone and set effort high (c72b01fb5). Fallback only, but it contradicts the rows.

## Falsifier
1. `write.py config:rotations 'read body <new range>' | wc -c` <= 2000 AND every F-number cited in `extensions/agi/briefs/*.md` resolves either in the region or in a `skills/agi-*/SKILL.md`.
2. `git grep -n '"ultracode": True' -- extensions/agi/bin/rotate.py` = 0 hits.

## Agent Notes
2026-09-27 04:1xZ belam: DRAFT HELD BY THE DIRECTOR (owner 04:1xZ: it should be referenced) = loop branch season2/loops/hypothesis-wake-facts-collapse-t-a00-759e6b60 @3fb4c6199 (kid a00-759e6b60, DH.501, worktree .agi/worktrees/a00-759e6b60). The Prime's ONE config:rotations write takes the facts region from that branch (TMM.281 route: config:rotations facts are prime/owner-only); DE's red-first test lands after it.

## CORRECTIVE DH.556 -- closes mur-director-engine-23 DH.501-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-wake-facts-collapse-t-a00-759e6b60 tip 0eba09517 (branch de-base-556; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. The new live guard lands RED on the merged trunk: 2009 B vs the 2000 cap (test_rotate_templates.py:1489); the Prime's cdcfe5c0b region is 9 bytes over FACTS_POINTER_TARGET_BYTES, so the cap assertion fails the moment this branch merges
2. 4. _FACT_LINE_RE silently skips the live `- RETIRED, …` fact line (test_rotate_templates.py:1431) — needs `\s|: ` after RETIRED, the live line has a comma, so the guard's 'every fact line' coverage is overstated
3. The pointer guard's coverage is keyed to the LEADING TOKEN alone (test_rotate_templates.py:1431, `F\d+(?:\+F?\d+)*` or the literal RETIRED). A fact line written `- F13,F14 -> skill agi-rotate (§2)` (comma instead of `+`), or any fact line not beginning with `- `, escapes the entire check and no other suite counts fact lines against a set — the silently-dropped-rule failure the test's docstring promises to catch is reachable in those shapes. Broader than the reviewer's RETIRED-only framing, same root.
4. Both the positive and the negative fixture probes resolve against the LIVE skills dir, not a fixture copy: `skills_dir: Path = _SKILLS_DIR` (:1449) with `_SKILLS_DIR = parents[3]/"skills"` (:1428). test_region_fixture_pointers_that_resolve_pass (:1495) and test_region_fixture_unknown_skill_and_missing_section_fail (:1508) are therefore coupled to skills/agi-rotate/SKILL.md keeping a `## 1 ·` heading (present today, skills/agi-rotate/SKILL.md:15). A section renumber there turns a green hermetic fixture red for a reason unrelated to the facts region; a tmp_path SKILL.md fixture would make them hermetic.
5. Two sources of truth for one size, and the wrong one is the literal: the cap is hardcoded at test_rotate_templates.py:1434 while the region it bounds already carries its delivery budget in CONFIG cells (`startup.byte_cap: 8000` at .agi/nodes/.geometry/rotations.md:73, `40000` at :111) which the neighbouring guard reads FROM THE NODE (test:1108, 1118). The literal copy is what went red at :1489 — a fact that should have been a miss under config-max, and the first reviewer's list does not name it.
6. Neither node's evidence probe is in the repo (.gitignore:104 `.agi/sessions/*`), so both 'real stdout' blocks (a00-436cd7b6-e9a8f6.md:55-62 and a00-d698eaaa-251421.md:110-119) are unre-runnable by a reader and the DH.491 '502 passed' claim over the other three rotate test files is unreproduced by me (I ran only the single committed file, as scoped). I re-derived the pointer half from committed bytes; the hand-hit / `_region_refusal` halves stand UNVERIFIED by me.
7. Checked and CLEAN, stated for the record (no demotion, no real-resource touch): the diff is 3 files, 385 insertions, 0 deletions — no deletion or move under .agi/nodes, so no demotion; the three new tests READ the live rotations.md and write only under tmp_path (_rotations_fixture_with_region, :1462) — no tmux pane, systemd unit, crontab or process is touched, and none of them calls rotate.main / cmd_rotate_self / _reap_* / spawn_window / watch / nudge; and the round did not hand-land the gate it must pass through (config:rotations is byte-identical through this branch — 23353 B at both b7c9b0d and 0eba0951 — and the Prime's write cdcfe5c0b landed on the trunk, not here).
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_rotate_templates.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_rotate_templates.py · .agi/nodes/experiment/a00-436cd7b6-e9a8f6.md · .agi/nodes/experiment/a00-d698eaaa-251421.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 0eba09517 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.571 -- closes mur-director-engine-27 DH.556-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-wake-facts-collapse-t-a00-e887f21f tip 410870f13 (branch de-base-571; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
SETTLED   the live region 2009 B > 2000 B (review defect 1) is the Prime's F13 trim on config:rotations, OUTSIDE this round: never edit config:rotations; the chain stays merge-BLOCKED on it (director).
1. 3. Ceiling overrun 66 net test lines vs the 40-line cap - test_rotate_templates.py:1435 - director row 17 cut line
2. 4. Node addenda appended after THOUGHT:END, outside the authored region, and left uncommitted until 410870f13 - a00-436cd7b6-e9a8f6.md:95 (also :185 on a00-d698eaaa-251421.md)
3. 5. Comment says the target is stated once while a second literal 2_000 sits at :1528 - test_rotate_templates.py:1440
4. 7. Detector still leading-token: word-before-number and indented fact lines still uncounted, the second undisclosed - test_rotate_templates.py:1435
5. The merge TARGET is green and has no facts guard at all, which reframes defect 1: d26418c37's extensions/agi/tests/test_rotate_templates.py has 0 hits for FACTS_POINTER|_region_pointer and runs 36 passed. The guard is DE-line content (present at 78a3416ed, absent from main since the fb7832a7e split), so the act needed is on the DH.501 line's merge, not on DH.556's two-line fix. First reviewer measured the red but not the green side it is landing on.
6. The node states two different measurements of 'the live region' and neither 2009 number is pasted: a00-dcfa7b0b-3fe045.md:19 says the live region 'is still the 7164-byte prose block' while :114-117 says 'the region the Prime landed on the merged trunk measures 2009 B'. The orders require the settling command and its output pasted, 'never type a number' (.agi/nodes/hypothesis/wake-facts-collapse-to-skill-pointers.md:40). I measured both: 7164 B / 22 violations at 410870f13; 2009 B / 0 violations only in a tree carrying cdcfe5c0b's collapse -- the 2009 figure reaches the node as a typed number, which is the same failure class the anti-near-miss was built against.
7. Probe-text drift between node and committed test: a00-dcfa7b0b-3fe045.md:15 describes shape (b) as `'- F13,F14 -> skill agi-rotate (§9)'` -> 'no `## 9 ·` section', but the landed test at :1563 is `'- F13,F14 -> skill agi-nope (§1): a dropped rule.'` against a fixture that HAS §1 (_fixture_skills_dir, :1510-1520), so the refusal a reader sees is 'has no SKILL.md'. The coverage claim still holds (assert len(out) == 1 at :1569 can only hold if the widened regex matched the line), but a reader re-running the described probe will not reproduce the committed test.
8. Provenance of the two node edits is unverifiable here and the frontmatter disagrees with the landing hand: both nodes carry `edited_by: a00-dcfa7b0b` (:9) while the bytes were landed by the director-engine commit 410870f13, and no row in this worktree's .agi/sessions/write-log.jsonl (1079 rows) names a00-436cd7b6-e9a8f6, a00-d698eaaa-251421 or a00-dcfa7b0b-3fe045, so 410870f13's 'bytes == last write-log sha' claim is UNVERIFIED by me -- the log is gitignored and the kid worktree is absent. PROBE I WOULD RUN, not run: in the kid worktree, `python3 -c "import json;[print(l) for l in open('.agi/sessions/write-log.jsonl') if 'a00-436cd7b6' in l]"` and compare each row's sha256 to `sha256sum .agi/nodes/experiment/<node>.md`.
9. Checked and CLEAN, stated for the record because the brief asks for the class: no test in this diff touches a real resource. The three added tests plus _fixture_skills_dir (:1510-1520) write only under tmp_path and read the live rotations.md/skills tree read-only; the added lines contain no subprocess/os.system/popen/socket/spawn/dispatch/send/rotate.py call (grep over the diff's added lines for those tokens returns nothing). No node file is deleted or moved in the range (numstat deletions: 6, all in the test file; 0 under .agi/nodes), so no demotion. And the round did not hand-land the gate it must pass through: .agi/nodes/.geometry/rotations.md is byte-identical at 78a3416ed and 410870f13 (23353 B both) and the Prime's collapse cdcfe5c0b is on the main line, outside this range.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_rotate_templates.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_rotate_templates.py · .agi/nodes/experiment/a00-436cd7b6-e9a8f6.md · .agi/nodes/experiment/a00-d698eaaa-251421.md · .agi/nodes/experiment/a00-dcfa7b0b-3fe045.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 410870f13 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.601 -- closes mur-director-engine-30 DH.571-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-wake-facts-collapse-t-a00-a0fbcb7c tip 7c81d3739 (branch de-base-601; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
SETTLED   the 2009 B > 2000 B facts region is the Prime's F13 trim on config:rotations, OUTSIDE this round: never edit config:rotations or loosen the 2000 B target; the chain stays merge-BLOCKED on it (director).
1. 3. Node self-contradiction on the 2009 B figure — a00-dcfa7b0b-3fe045.md:116 vs :147
2. 4. Probe P1(b) still names a refusal the committed shapes cannot produce — a00-dcfa7b0b-3fe045.md:15
3. 5. Node asserts a detector hole the same commit closed — a00-dcfa7b0b-3fe045.md:16 and :131-132 vs test:1580
4. 6. `edited_by` claim contradicted by the same commit — a00-dcfa7b0b-3fe045.md:150 vs :9
5. The round's OWN new node carries a stated demotion its landed frontmatter contradicts: a00-b05aceee-3f6650.md:121 states 'which is why the lean moves 80 -> 70 and not to proved', while the shipped frontmatter reads `verdict: inconclusive_lean_proved:80` / `confidence: 0.8` at :21 / :8, set by the same `done` commit 4472a261b. A verdict change declared in the body and never applied to the bytes — the first reviewer checked this class only on the three pre-existing nodes and missed the new one.
6. The freeze test's blast radius was widened with the file: the separator squash at test_rotate_templates.py:1543 (`re.sub(r'(?<=\d)[,_](?=\d)', '', src)`) is applied to the WHOLE file text, not to numeric literals. Measured: on the shipped file the scan finds 1 hit (green); after inserting one unrelated `2_000` mention anywhere in the file the same scan finds 2 and the test goes red with a message about the collapse target appearing twice. The corrective that makes the scan see a hidden second literal also makes it see non-targets — a latent false-positive surface in the anti-near-miss guard, mechanism not wording, and not named by the first reviewer.
7. The merge red is narrower than reported: the violation assert at test:1505 is GREEN (0 violations on the destination's collapsed region). The ONLY thing blocking is 9 bytes of region residue, and the two available fixes are both outside this round by design — compact 9 bytes of `.agi/nodes/.geometry/rotations.md`, or land the owner-gated `templates.director.startup.facts_pointer_target_bytes` cell named at a00-dcfa7b0b-3fe045.md:117. Naming the exact unblock keeps the red from being read as a broken guard.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_rotate_templates.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_rotate_templates.py · .agi/nodes/experiment/a00-436cd7b6-e9a8f6.md · .agi/nodes/experiment/a00-b05aceee-3f6650.md · .agi/nodes/experiment/a00-d698eaaa-251421.md · .agi/nodes/experiment/a00-dcfa7b0b-3fe045.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 7c81d3739 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.601: mur-director-engine-30 DH.571-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
