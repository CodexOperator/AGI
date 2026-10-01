---
id: hypothesis:heal-ack-line-comes-from-config-rotations-by-role
mint_id: 9f097430380345e0b2a7dc69682f6d02
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: director-general-3
scaffold_hash: db2d84353e605c80
season: 2
testable_claim: heal builds a recovered seat's ack instruction from a config:rotations cell keyed by row role and recovered/resumed, so every built line is accepted by rotate.py ack for that row, and heal.py carries no ack text literal
title: "heal's recovered-seat ack line comes from config:rotations keyed by role: no --gen for non-prime seats"
town: core
---
# hypothesis:heal-ack-line-comes-from-config-rotations-by-role

## Measured
- heal.py `ack_gate` (both arms, RECOVERED and RESUMED) hard-codes `rotate.py ack --seat {seat} --gen {gen} --ref <ref> continue` into EVERY recovered seat's prompt; the agi-rotate skill §3 gives `--gen` to the recovery path, while non-Prime posts write no generation (master template §3: "Non-Prime posts write no gen N").
- The ack line is text a template owns, not code: it belongs in config:rotations keyed by role.
- Ordered by belam 19:0xZ 10-01 (direct message, relayed on doc:card-sanctuary-master §1).

## CLAIM
heal builds the recovered seat's ack instruction from a config:rotations cell keyed by the row's role (prime vs every other role) and by recovered/resumed, so every built line is one rotate.py ack ACCEPTS for that row (a RESUMED non-prime seat is never told `--gen`; a FRESH one keeps `--gen`, its row carries generation per goal:g15.25 -- DH.1 correction, mur-heal-ack-by-role-2/-3); heal.py carries no ack text literal.

## Dispatch line
config-max: the ack line per role moves to a config:rotations cell / template-max: the recovered/resumed wording lives in that cell, not in heal.py / code: the lookup by row role, with a by-name refusal when the cell is absent.

## FALSIFIERS
- A built line that rotate.cmd_ack refuses for its own row (fresh non-prime, resumed non-prime, prime recovered, prime resumed) -- DH.1 correction; the old falsifier (any --gen for a non-prime row) rested on the superseded premise.
- heal.py still contains the literal `rotate.py ack --seat`.
- The cell absent -> a silent empty prompt instead of a refusal by name.

## TESTS
A committed test building the prompt for a prime row and a director row from a fixture config:rotations (fakes only); the live config:rotations gains the cell in the same round (check the LIVE config holds it, not only the test fixture).

## FILE SCOPE
extensions/agi/bin/heal.py (`ack_gate` only) · .agi/nodes/.geometry/rotations.md (the one cell) · its test · this node.

## CEILING
1 pi-free parent · <= 12 production lines · 0 USD.

## RESULT (kid aaacd632f, director record)
NUMSTAT 14e06f47b..aaacd632f: rotations.md 7/0 · heal.py 12/10 · test_heal_ack_by_role.py 135/0 · 6 neighbour tests +14..16 each (fixture seed only, director-checked). 7 files 136 passed (director, 20:0xZ 10-01). mur-heal-ack-by-role-2 (pi-free, extra signal): review accept_with_residue, verify DEMOTE. The gating claude-code mur follows the corrective.

## CORRECTIVE DH.1 -- closes mur-heal-ack-by-role-2 heal-ack-code (demote)
BASE      CUT FROM heal-ack-by-role tip aaacd632f (worktree /mnt/agi-ram/worktrees/heal-ack-by-role). No merge. Never rebase.
1. a FRESH non-prime recovery is handed an ack line that exits 2 -- rotations.md recovery_ack.default.recovered -- heal.py writes the successor row with session_id '' (_successor_row_write(session_id=resume or "")) and cmd_ack then demands --gen (rotate.py ~3089-3093); the row DOES carry generation for every role (rotate.py ~9957). TRUE WHEN the default recovered arm hands a command cmd_ack ACCEPTS for a fresh non-prime row (e.g. back to `--seat {seat} --gen {gen}`, or heal stops writing an empty session_id -- pick the smaller, name why in the commit). Both prime arms stay byte-identical. The node's Measured premise ('non-Prime posts write no generation') is superseded by goal:g15.25 (rotate.py ~9951): say so in the commit.
2. the test that pins the broken line -- test_heal_ack_by_role.py ~99-105 -- TRUE WHEN the built line is fed back into rotate.cmd_ack on a FIXTURE root (tmp_path, fakes; never the live root, a live pane or the tmux server) and ACCEPTED for: a fresh non-prime row (recovered arm), a resumed non-prime row (resumed arm), a prime row (both arms).
3. the refusal tuple -- heal.py ~3665 -- TRUE WHEN a malformed config:rotations (FrontmatterError), a stray brace (ValueError) or a positional field (IndexError) refuses the recovery BY NAME and never raises into the watch loop (precedent: rotate.py ~5040-5046 _load_templates, bare except Exception), AND the refusal reaches stderr + _watch_log like the sibling refusal at heal.py ~3553-3558; one test with a malformed node.
4. the second copy of the recovery ack -- skills/agi-rotate/SKILL.md:40 -- TRUE WHEN the line points to config:rotations recovery_ack and carries no command copy.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
FILE SCOPE extensions/agi/bin/heal.py (the ack_gate block only) · .agi/nodes/.geometry/rotations.md (recovery_ack only) · extensions/agi/tests/test_heal_ack_by_role.py · skills/agi-rotate/SKILL.md (line 40) · this node (director)
CEILING   HARD CAP: 1 Sonnet 5.5 kid · <= 14 production lines · <= 90 test lines · 0 USD -- over it = the round is cut

## CORRECTIVE DH.2 -- closes mur-heal-ack-by-role-3 heal-ack-code (accept_with_residue; gating, claude-code) -- TEXT ONLY
BASE      CUT FROM heal-ack-by-role tip ef1ddf9e6 (worktree /mnt/agi-ram/worktrees/heal-ack-by-role). No merge. Never rebase.
1. a test name + the module docstring overstate -- test_heal_ack_by_role.py (test_non_prime_seat_recovered_line_has_no_gen + docstring) -- TRUE WHEN both say what they pin: the FIXTURE cell's non-prime arm, while the LIVE default.recovered carries --gen (DH.1); no logic change.
DEMOTED   CLAIM / FALSIFIER 1 wording = node prose, corrected by the director (4b2947e58) · 6 fixture seeds copied = the suite idiom (mur-heal-ack-by-role-2 verify: conftest has no rotations seeder; 20 test modules write their own rotations node) · SimpleNamespace bypasses argparse = verify confirmed --post is a real alias (rotate.py ~22747).
FILE SCOPE extensions/agi/tests/test_heal_ack_by_role.py (names + docstring only)
CEILING   HARD CAP: 1 Sonnet 5.5 kid · 0 production lines · <= 12 test lines changed · 0 USD
