---
id: hypothesis:pb3-hw-name-scrubbed-and-four-lost-corrections-restored
mint_id: 50f36824f1df451aad27a087572b0cba
type: hypothesis
parents:
  - goal:g1.31.3.2
next_edges: []
edited_by: director-general-3
scaffold_hash: da11c4685214d0f1
season: 2
testable_claim: "Through write.py only: the #4 node names the card GPU2070S (URGENT, first); a00-797ee7be carries no pi-encoded repo path; the a00-600cf080 pair and a00-2fa1fab0 carry, in their BODIES, the corrections the 2bb73cae62 scrub dropped (grid v3 1c8ff9c77, v3 2c52576a9, v4 f17651ebc); a00-6b761b8c carries <user> in all 5 places with its authored THOUGHT kept -- the falsifier exits 1 at HEAD acda46f75b and 0 after."
title: "Six nodes fixed via write.py: <hw> -> GPU2070S, encoded repo path and box user scrubbed, 4 lost THOUGHT corrections restored"
town: core
---
# hypothesis:pb3-hw-name-scrubbed-and-four-lost-corrections-restored

## Measured
goal:g1.31.3.2, 5 upheld residues + 1 coordinator addendum, all open at HEAD acda46f75b (re-checked):
```
#   node (.agi/nodes/)                                        open at HEAD                                       lost text survives in
4   hypothesis/lm-bonsai2-27b-abc-coding-test-on-the-8gb-box  <hw> in the "ACCEPTED with residue (merge          — (a pure leak; TMM.56 THOUGHT records only
    URGENT, stream live                                       95a58827ca)" paragraph; testable_claim = GPU2070S     the testable_claim swap)
33  experiment/a00-797ee7be-e9c742                            11 lines, pi-encoded repo path (probes             — (never scrubbed: the scrub matched the absolute
                                                              frontmatter ×2, store-dir table, store_prefix,       form only; its THOUGHT says "carries no box path")
                                                              "Derivation probe" block, Agent Notes ×2);
                                                              ROOT in that block is already <repo>/…
35  experiment/a00-600cf080-0cd865-exp                        `## M3` + `## What remains` read as current;        grid v3 1c8ff9c77 (= v2 a4a1a4059) THOUGHT
                                                              grep -ci stale = 0                                   "PASS 8 items 2+3+4 … STALE … DANGEROUS"
36  hypothesis/a00-600cf080-0cd865                            DANGEROUS paragraph points at "PARENT REVIEW        grid v3 2c52576a9 THOUGHT "PASS 8 ROUND
                                                              (a00-613b8582)" (no such block: it is PARENT         a00-28bbc0b9 … ITEM 2: M3 …"
                                                              PROBES) and "the THOUGHT below" (= scrub note, no M3)
44  experiment/a00-2fa1fab0-b7d2a0                            PARENT REVIEW DH.368: "the kid declared that it     grid v4 f17651ebc THOUGHT "PASS 8 row 47 …
                                                              wrote the cell, and it did"; 0 × 800a925981           director committed the cell … 800a925981"
+   experiment/a00-6b761b8c-b6ae8b (addendum)                 the box user (cell `box.user`) on 5 lines: a        — (a leak; the THOUGHT is an authored parent
                                                              pytest basetemp `/tmp/pytest-of-<user>` ×4 (one      review, NOT a scrub note: it must survive)
                                                              in the THOUGHT, 2 in Agent Notes) + an `ls -l`
                                                              owner/group pair in (A)
```
- Root cause #33–#44: the DG4 L2b repo-path scrub (2bb73cae62) replaced each whole THOUGHT with one generic note ("Content otherwise unchanged"); 80 node files carry it; the correction lived ONLY in the THOUGHT, so it left the working tree.
- 800a925981 = director-engine, `.agi/config.json` only: cells `reaper.late_reap_wait_max_s` + `reaper.term_grace_s` (live 15).
- write.py `sub`/`sub!` resolve over frontmatter + body, inside a THOUGHT too (dry-run on the addendum node: admitted), and print the diff — so every run on a leak is piped through a masker.

## CLAIM
The 6 nodes are corrected through write.py only; each correction lives in the BODY (state); a THOUGHT names this version's delta and the grid version it restores from, and no authored THOUGHT is replaced by a generic note:
(4) the paragraph names the card by its class label GPU2070S; the THOUGHT records both substitutions (testable_claim + this paragraph).
(33) every pi-encoded repo path uses the placeholder form ROOT already uses (`--<repo>-.agi-worktrees-…`), so the derivation still checks; the THOUGHT's "carries no box path" becomes true.
(35) `## M3` and `## What remains` each open with a STALE line pointing at hypothesis:a00-600cf080-0cd865's DANGEROUS paragraph (text from grid v3 1c8ff9c77, repo path → `<repo>`).
(36) the pointer names PARENT PROBES (a00-613b8582) and a body block restored from grid v3 2c52576a9 (ITEM 1/2/3/7, incl. the M3 reasoning); the THOUGHT names M3.
(44) PARENT REVIEW DH.368 says director-engine committed `reaper.term_grace_s` in 800a925981 (a round cannot commit `.agi/config.json`); `config.json 2/1` and "the LIVE config declares the cell" say "since 800a925981"; the THOUGHT carries the v4 f17651ebc correction, not "Content otherwise unchanged".
(+) a00-6b761b8c-b6ae8b carries `<user>` in all 5 places; its authored THOUGHT is kept (sub! only, never the `thought` verb); the scrub is recorded by one `note` line.
```
grid vN (git show <sha>:node.md, READ ONLY) ─► THOUGHT text ─► repo path → <repo> ─► /tmp/pb3b/<n>.txt ─► write.py replace body / sub / thought
leak (#4, +)  ─► value read live (sed shape / box.user cell), never typed ─► write.py … 2>&1 | sed mask ─► grep -c placeholder
```

## Dispatch line
config-max: none (#44 cites the existing cell `reaper.term_grace_s`; the addendum reads `box.user` to find the value, writes nothing to it). template-max: none. code: none — a node-answer round; write.py verbs `sub`/`sub!`, `replace body L:L <file>` (standalone), `thought`, `note`. #4 FIRST, the addendum second.

## FALSIFIERS
From the repo root. `"--data""-work"` is shell-split so this node never matches itself; the goal nodes are excluded because goal:g1.31.3.2's own negative (and goal:g1.31.3's) quote the string — as written there it self-matches (3 + 1 hits) and can never pass.
```bash
bash -c 'H=.agi/nodes/hypothesis; E=.agi/nodes/experiment; A=$H/a00-600cf080-0cd865.md; P=$E/a00-2fa1fab0-b7d2a0.md
BU=$(python3 -c "import json;print(json.load(open(\".agi/config.json\"))[\"box\"][\"user\"])")
! grep -qP "(?<!GPU)2070" $H/lm-bonsai2-27b-abc-coding-test-on-the-8gb-box.md &&
[ -z "$(git grep -n -e "--data""-work" -- .agi/nodes ":!.agi/nodes/goal/g1.31.3*")" ] &&
[ $(grep -ci stale $E/a00-600cf080-0cd865-exp.md) -ge 2 ] &&
! grep -q "REVIEW (a00-613b8582)" $A &&
{ ! grep -q "THOUGHT below" $A || sed -n "/THOUGHT:BEGIN/,/THOUGHT:END/p" $A | grep -q M3; } &&
! grep -q "the kid declared that it wrote the cell, and it did" $P && grep -q 800a925981 $P &&
! sed -n "/THOUGHT:BEGIN/,/THOUGHT:END/p" $P | grep -q "Content otherwise unchanged" &&
! grep -qwF "$BU" $E/a00-6b761b8c-b6ae8b.md &&
grep -q "THOUGHT:BEGIN" $E/a00-6b761b8c-b6ae8b.md && ! sed -n "/THOUGHT:BEGIN/,/THOUGHT:END/p" $E/a00-6b761b8c-b6ae8b.md | grep -q "Content otherwise unchanged"'
```
exits 1 at acda46f75b (every conjunct but the last, which guards the kept THOUGHT; each run alone, measured). The leaf's own #4 conjunct (`grep -n 2070 … | grep -qv GPU2070S`) is pipe-fragile — under a grep wrapper it PASSED at HEAD with the leak present — so this one is a single `grep -P` with a look-behind. Also false if: `links.py links` broken ≠ 0 · `links.py schema` gains a violator among the 6 · active + deprecated node count drops · any edit lands outside write.py · any THOUGHT, note, commit message, dm or probe output carries `<hw>`, the box user, or a repo/home path · a measurement line is deleted rather than marked.

## TESTS
No code. Per node: `write.py <id> 'read body 1:200'` before and after (the two leak nodes piped through the same mask); the falsifier above; then
```
python3 extensions/agi/bin/links.py links          # broken 0
python3 extensions/agi/bin/links.py schema         # no new violator
python3 extensions/agi/bin/commands.py run verify  # quick set incl. anonymize
python3 -m pytest extensions/agi/tests/test_anonymize_guard.py -q --basetemp /tmp/pb3b
```

## FILE SCOPE
(write.py only; each edit self-commits by exact path)
.agi/nodes/hypothesis/lm-bonsai2-27b-abc-coding-test-on-the-8gb-box.md · .agi/nodes/experiment/a00-797ee7be-e9c742.md · .agi/nodes/experiment/a00-600cf080-0cd865-exp.md · .agi/nodes/hypothesis/a00-600cf080-0cd865.md · .agi/nodes/experiment/a00-2fa1fab0-b7d2a0.md · .agi/nodes/experiment/a00-6b761b8c-b6ae8b.md

## CEILING
kids ≤ 1 (or the parent itself, pi-free) · 0 production lines · ≤ 4 write.py calls per node · 0 USD.
- #4, never typing the name: `L=<body line from read body>; write.py <id> "read body $L:$L" | sed -E 's/ 2070 [A-Z]+:/ GPU2070S:/' > /tmp/pb3b/4.txt`; check by `grep -c GPU2070S`, never by printing the line; `replace body $L:$L /tmp/pb3b/4.txt`; then `thought`.
- addendum, never typing the user: `BU=` from the `box.user` cell (as in the falsifier); `write.py experiment:a00-6b761b8c-b6ae8b "sub! pytest-of-$BU => pytest-of-<user> && sub 1 $BU $BU => 1 <user> <user>" 2>&1 | sed "s/$BU/<user>/g"`; then `note` one line naming the scrub + goal:g1.31.3.2; NO `thought` (the authored parent review stays whole).
- #33: one `sub! --data''-work-agi => --<repo>` (shell-split, so the brief never carries the path), then `thought`.
- Grid versions are read with `git show <sha>:node.md` / `grid.py log|diff`, NEVER `grid.py checkout`. The pre-scrub bytes stay in git + grid history: rewriting them is irreversible → BANKED for the owner, never done here. Out of scope: the 3 other node files with the <hw> token, the 76 other scrub-note THOUGHTs, the 8 other files with a `/tmp/pytest-of-<seg>` path.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Corrective dg6-03 (goal:g1.31.3.2 b, director-general-3, 2026-09-30): the merge-up review verify_dg6-03 found the falsifier conjunct that greps the old reaper-cell sha passing on a citation that does not resolve after the 2026-09-30 history rewrite (an object-type lookup refuses it). The reaper-cell commit is now cited as 800a925981 (director-engine, 02:54:42Z 09-26) and the DG4 L2b scrub as 2bb73cae62. The shas named in this node and in the falsifier are corrected to the new ids, and the corrected node a00-2fa1fab0-b7d2a0 carries 800a925981, so the conjunct is satisfied by a real commit. Nothing else in the node changed.
<!-- THOUGHT:END -->

## Agent Notes
DIRECTOR TRIAGE (director-general-3, 2026-09-30, mur dg6-03c accept_with_residue; review defects 1-2 REFUTED by verify: a bare login outside a path is out of class per Prime ruling n144): 3 goal:g1.31.3.2 falsifier runs from the repo root, no box path; 4 + M1 every pre-rewrite commit citation in the 4 round nodes re-pointed through the local map (9 occurrences; 0 map-known tokens left; never printed); 5 dated note on hypothesis:a00-600cf080-0cd865; M2 both --data""-work negatives exclude goal nodes (0 hits elsewhere; falsifier 1 verbatim exits 0); M3 the ruling lives once, here (the goal THOUGHT copy replaced); M4 DEMOTED: a regression guard reading HEAD is by design (it guards the live tree forward), the round's tip is certified by the mur re-run of its four regexes (all 0).
