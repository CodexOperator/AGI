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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.556: mur-director-engine-23 DH.501-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
