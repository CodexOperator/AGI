---
id: hypothesis:trunk-tests-follow-the-owners-0927-ultracode-drop-and-facts-collapse
mint_id: 1ff23358041b4a3683337daee82903d9
type: hypothesis
parents:
  - goal:g7.33.19
next_edges: []
edited_by: director-engine
scaffold_hash: 2f794e43a47f9fcf
season: 2
testable_claim: "test_ladder_node roles-table and test_sensei_wake_audit whois-fact read the live truth (settings not ultracode; F3 points at skill agi-send, which carries the whois shape once) with their contracts kept; test-only (assigned: director-engine)"
title: Trunk tests follow the owner 09-27 ultracode drop and facts collapse
town: core
---
# hypothesis:trunk-tests-follow-the-owners-0927-ultracode-drop-and-facts-collapse

## Measured
TMM.298 (thought-master 13:31Z 09-27): two TRUNK reds that fail without the zero-USD fix too; reproduced on the post branch 32ff79e53 (2 failed in 0.14 s). Attributed by the director:
(1) test_ladder_node.py:70 `assert prime.get("settings") == "ultracode"` -- 20283d21b (belam-S2-L5-XI, owner 09-27: ultracode dropped from every row) set the tier-3 prime_director row's settings to "" (.agi/nodes/.geometry/ladder.md:37). The test pins a value the owner removed.
(2) test_sensei_wake_audit.py:832 `exactly one live fact must cite send.py whois <token>: []` -- cdcfe5c0b (belam-S2-L5-XIII) collapsed config:rotations facts to pointers; F3 now reads `F25+F3 -> skill agi-send (§1)` and the shape `send.py whois <session_name> --claim <post>` lives at skills/agi-send/SKILL.md:24. No live fact carries the shape any more.

## CLAIM
Both tests read the live truth again with their contract kept: (1) the tier-3 prime_director row still resolves harness/model/effort, and its settings is NOT "ultracode" (owner 09-27); (2) exactly ONE live fact points F3 at skill agi-send, and that skill file carries the `send.py whois <token>` shape exactly once in a command line -- the prose-shadow guard (a fact whose prose says whois never wins) is kept. No production line and no graph node changes.

## Dispatch line
config-max: none / template-max: none / code: none -- test-only (the graph is the source; the tests follow it).

## FALSIFIERS
- either test still fails on the post branch;
- a test is deleted, skipped or xfailed instead of retargeted;
- any file outside FILE SCOPE changes.

## TESTS
test_ladder_node.py test_sensei_wake_audit.py (whole files) + test_sensei.py test_bin_help_smoke.py once. timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE.

## FILE SCOPE
extensions/agi/tests/test_ladder_node.py · extensions/agi/tests/test_sensei_wake_audit.py · the kid's own node

## CEILING
HARD CAP: 1 kid · 0 production lines · <= 30 test lines net · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
