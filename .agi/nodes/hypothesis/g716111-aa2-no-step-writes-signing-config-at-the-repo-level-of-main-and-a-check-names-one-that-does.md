---
id: hypothesis:g716111-aa2-no-step-writes-signing-config-at-the-repo-level-of-main-and-a-check-names-one-that-does
mint_id: 005de3e906ee4efb8f245a27d8408ce0
type: hypothesis
parents:
  - goal:g7.16.1.11.12
next_edges: []
confidence: 0.6
edited_by: director-general-1
season: 2
testable_claim: "(a) after a stand-up, a move, a spawn and a hand restart on a scratch MAIN, `git config --local --get-regexp` for gpg.*, user.signingkey, commit.gpgsign and tag.gpgsign prints nothing: no engine step writes signing config at the repo level of MAIN; (b) a read-only check in the verify pass fails and NAMES the key and its value when MAIN's local config holds any of them, and passes when it holds none; (c) a post whose own global cell is right still verifies its own commit as `<post>@agi` after the check passes, and reads 'No principal matched' when a local key overrides it (the measured case), so the check is the cause-finder; (d) the agi-post skill states the rule in one section."
title: "AA2: no step writes signing config at the repo level of MAIN (it overrides every post's own cell in every worktree), and a read-only verify check names one that does (belam 04:2xZ finding)"
town: core
---
# hypothesis:g716111-aa2-no-step-writes-signing-config-at-the-repo-level-of-main-and-a-check-names-one-that-does

## Measured
- belam 04:21Z (decision, A9 run): director-thought-1's commit bb5ebe515 read `U ... No principal matched` after the new unit, because MAIN `.git/config` set `gpg.ssh.allowedSignersFile=<MAIN>/.git/allowed_signers` (1 line, director-general-5, written 10-01 09:39 as its first move). A repo-level key overrides the post's global cell in every worktree of MAIN. belam unset that one local key; `bb5ebe515` then read `G director-thought-1@agi`. Rollback: `git config --local gpg.ssh.allowedSignersFile <path>`.
- grep over extensions/ and skills/ and the .geometry engine pieces (trunk 73bc94ad5): no engine code writes it; the only mention is engine-post.md's gitconfig cell (`allowedSignersFile=~/.signers`, the post's GLOBAL file). So the writer was a hand step, and the guard is a check plus a rule, not a code fix.

## CLAIM
(a) after a stand-up, a move, a spawn and a hand restart on a scratch MAIN, `git config --local --get-regexp` for gpg.*, user.signingkey, commit.gpgsign and tag.gpgsign prints nothing: no engine step writes signing config at the repo level of MAIN; (b) a read-only check in the verify pass fails and NAMES the key and its value when MAIN's local config holds any of them, and passes when it holds none; (c) a post whose own global cell is right still verifies its own commit as `<post>@agi` after the check passes, and reads 'No principal matched' when a local key overrides it (the measured case), so the check is the cause-finder; (d) the agi-post skill states the rule in one section.

## Dispatch line
config-max: none / template-max: none / code: ONE check in the verify pass (`commands.py run verify`, skill agi-verify), read-only, 0 B in the engine and 0 B on the base; the skill section (landed with this round).

## FALSIFIERS
1. A scratch MAIN with `git config --local gpg.ssh.allowedSignersFile /x`: the check exits non-zero and its output contains the key name and the value `/x`; with `--unset`, it exits 0.
2. Each of gpg.format, gpg.ssh.program, user.signingkey, commit.gpgsign, tag.gpgsign set locally: each named, each non-zero.
3. A key that is NOT signing config (core.editor, user.name locally): not flagged.
4. The measured case end to end in a scratch: a post global cell that verifies its commit, then the local override makes `git verify-commit` print the no-principal line, the check names the key, and unsetting it restores `G <post>@agi`.
5. Stand-up, move, spawn and hand restart paths (the four callers of the stand-up verb, run against a scratch MAIN with the real code and stubs for tmux and systemd): after each, falsifier 1's query prints nothing.

## TESTS
Shell and python3 tests in the existing verify test dirs; scratch repos only; no live MAIN is touched. No armoured block anywhere. Every ROOT act is belam's own GO.

## FILE SCOPE
The verify pass (extensions/agi/bin/commands.py verify list or the module it calls), one new test file, skills/agi-post/SKILL.md section 5. Nothing in .geometry/engine*.md.

## CEILING
1 parent - kids <= 1 - 0 B on the engine and the base - <= 25 production lines - 1 new test file - 0 USD - regular review.
