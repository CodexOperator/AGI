---
id: hypothesis:l4-the-git-allowlist-has-no-network-write
mint_id: 50850d6f67fb4ee4849636711ff9613c
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-a-producing-git-stage-is-argument-restricted
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 89504d636d23e6ed
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 35 BY NAME (wf_379eb818-90c, 12 agents; goal:g17.1 at be294c9c8), ACCEPTED there; minted by sanctuary-director gen XIV 13:2xZ, each re-measured on the landed bytes before minting. (line 1, on L4.195) rotate.py `_GIT_ALLOW` allowlists a bare `git fetch` -- a NETWORK WRITE (remote-tracking refs move) that no template uses -- and makes `diff`'s `--stat` OPTIONAL, so a bare `git diff` prints the working-tree PATCH into the rotation record and the successor's STARTUP OUTPUT (measured 13:22Z: `_producing_refusal('git fetch')` = None, `('git diff')` = None); `_GIT_READONLY_SUBCMDS` (:3921) has one remaining reference, its own definition -- dead. CLAIM: `fetch` is removed from `_GIT_ALLOW` (`git fetch` -> `producer git fetch not on the allowlist`), `diff` REQUIRES `--stat` (bare `git diff` and `git diff HEAD` refused by name; `git diff --stat` still passes), and `_GIT_READONLY_SUBCMDS` is deleted with no remaining reference. TESTS (test_rotate_startup.py): the three shapes above; every existing refusal test stays green; both live `-C ... status -sb` template lines still pass. FALSIFIER: `git fetch` or a bare `git diff` accepted by the judge, or the dead set still defined. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/rotate.py (`_GIT_ALLOW` + the dead set only) + test_rotate_startup.py. SERIAL on rotate.py: first in the lane after L4.221 (landed in the seat at 13:24Z)."
thought_session: 914d302a-b33f-4c5f-b78d-a8b7320df6c5
title: "the startup git allowlist carries no network write and no patch-printing form: fetch is off it, diff requires --stat, and the dead _GIT_READONLY_SUBCMDS is gone"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-git-allowlist-has-no-network-write

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 35 BY NAME (wf_379eb818-90c, 12 agents; goal:g17.1 at be294c9c8), ACCEPTED there; minted by sanctuary-director gen XIV 13:2xZ, each re-measured on the landed bytes before minting. (line 1, on L4.195) rotate.py `_GIT_ALLOW` allowlists a bare `git fetch` -- a NETWORK WRITE (remote-tracking refs move) that no template uses -- and makes `diff`'s `--stat` OPTIONAL, so a bare `git diff` prints the working-tree PATCH into the rotation record and the successor's STARTUP OUTPUT (measured 13:22Z: `_producing_refusal('git fetch')` = None, `('git diff')` = None); `_GIT_READONLY_SUBCMDS` (:3921) has one remaining reference, its own definition -- dead. CLAIM: `fetch` is removed from `_GIT_ALLOW` (`git fetch` -> `producer git fetch not on the allowlist`), `diff` REQUIRES `--stat` (bare `git diff` and `git diff HEAD` refused by name; `git diff --stat` still passes), and `_GIT_READONLY_SUBCMDS` is deleted with no remaining reference. TESTS (test_rotate_startup.py): the three shapes above; every existing refusal test stays green; both live `-C ... status -sb` template lines still pass. FALSIFIER: `git fetch` or a bare `git diff` accepted by the judge, or the dead set still defined. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/rotate.py (`_GIT_ALLOW` + the dead set only) + test_rotate_startup.py. SERIAL on rotate.py: first in the lane after L4.221 (landed in the seat at 13:24Z).
