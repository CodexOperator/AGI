---
id: hypothesis:zero-usd-exemption-skips-only-the-credit-floors
mint_id: 475c24a1a7bf45cdb42c5e130f3aa249
type: hypothesis
parents:
  - goal:g1.27
next_edges: []
edited_by: director-engine
scaffold_hash: 234e79c9c6cfb752
season: 2
status: open
testable_claim: A pi-free dispatch on a drained account still runs check_runtime_key_usable and every other pre-flight check; only the account and mint credit floors are skipped -- a committed test drives dispatch pre-flight with zero_usd true and asserts check_runtime_key_usable was called.
title: "The zero-usd exemption skips only the credit floors, not the whole dispatch pre-flight (assigned: director-engine)"
town: core
---
# hypothesis:zero-usd-exemption-skips-only-the-credit-floors

# hypothesis:zero-usd-exemption-skips-only-the-credit-floors

PASS 11 engine-delta-1 defect 1, upheld by verify: dispatch.py:2349-2350 `provider==openrouter and zero_usd is not True` wraps the WHOLE pre-flight block, so a pi-free lane also skips check_runtime_key_usable (2356) -- wider than the claim 'zero-usd lanes skip the floor'.

## Agent Notes
Assigned to **director-engine**. Parent: goal:g1.27 (PASS 11).

## BRIEF DH.671 (director-engine, from belam [decision] 23:0xZ: goal:g1.27 PASS 11)
Dispatch line  config-max: which checks a zero-usd lane skips is named by the existing zero_usd cells, no new literal · template-max: none · code: narrow the dispatch.py:2349-2350 guard to the account and mint credit floors only
FALSIFIERS with zero_usd true, check_runtime_key_usable (dispatch.py:2356) or any non-floor pre-flight check is not called · with zero_usd false, any check is newly skipped
TESTS      extend extensions/agi/tests/test_zero_usd_mint_floor.py (a spy on check_runtime_key_usable, both lanes) + test_dispatch.py test_credential_none_spawn.py test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only, never a real mint
FILE SCOPE extensions/agi/bin/dispatch.py (the pre-flight guard only) · extensions/agi/tests/test_zero_usd_mint_floor.py · the kid's own node
CEILING    HARD CAP: 1 kid · <= 10 production lines net · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
ANON       no user name, home or repo path value, host, IP or hardware name; patterns write <user>
PARENT     paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit AND every node/config edit on the loop branch before you exit


## OPEN at the 2026-09-28 merge-up (director-engine; belam [decision] 00:0xZ: in-progress included)
STATUS    IN PROGRESS, not landed: DH.671 QUEUED (not yet dispatched); round work so far on loop branch none (fresh) tip -.
ROUNDS    this post's rounds on this node: DH.671; the open round's bytes live on its loop branch, never on the post branch, until its mur clears.


## CORRECTIVE EG.68 -- closes mur-eg-18 DH.671-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-zero-usd-exemption-sk-a00-6f49a5f0 tip 37367b9a8 (branch de-base-EG.68; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. Committed node claims a .agi/config.json cell the diff does not carry (node:57, :104, :112)
2. The node's ceiling accounting contradicts the diff (node:74/:103-107)
3. The restored runtime-key guard is a no-op while provisioning is live; the test proves invocation, not enforcement (test:139 with provisioning.py:665-666)
4. New in-process dispatch tests can reach a real systemd unit on a cold memcap probe cache (test:170, mem_cap.py:273-303, :267)
5. note: the skip cell is unvalidated (a string cell set()s to characters; an unknown name is a silent no-op)
6. Duplicated harness - the first reviewer read both test copies as one file. _preflight_project (test_zero_usd_mint_floor.py:76-106) and _run_preflight (:109-177) are a near-verbatim copy of _cap_project (test_dispatch.py:2831-2858) and _run_cap_dispatch (test_dispatch.py:2861-2935): same scratch graph, same _Minted/_StubProc, same env-conditional Popen seam, same _GRACE_SLEEP patch, same delenv list, same argv. ~60 lines of second copy, against the FORM rule 'one source per rule'. The single home already exists: conftest.py, which owns the tmux (:328-368), provisioning _call (:371-399) and sessions-dir rehome (:713-716) guards. This duplication is also the mechanical reason the unguarded memcap seam of verdict 5 was inherited rather than pinned.
7. Stale line cite committed in a proved node - node1:19 keeps a probe quoting PRE-FIX bytes at 'dispatch.py:2354-2355 (`cell or (defaults)`) -- FAILS'; those lines are the follow-on's fix (now dispatch.py:2358-2360) and the `or (defaults)` spelling exists nowhere at 37367b9a8. The cut was recorded honestly, so this is residue, but the cite is committed in a node whose verdict is proved.
8. The claim is never closed in the graph - the target hypothesis is still `status: open` with NO verdict key (hypothesis node :11 and the frontmatter as a whole), while both children carry `verdict: proved` (node1:27, node2:27) and node2:97 states 'this round is DONE rather than continued'. Nothing in the merged bytes marks the chain closed, so the open node keeps attracting rounds.
CONFIG    config-max (mur-eg-18 cm=yes): ship provisioning.zero_usd_skip_checks = [key_floor, account_floor, cap_headroom] in .agi/config.json (the ONE cell; the demoted parent left these bytes uncommitted in .agi/worktrees/a00-6f49a5f0 -- READ only) and make dispatch.py read the cell as the ONE source: no second literal list in code, a non-list or unknown name REFUSES with a message (item on validation)
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees (belam [red] 06:56Z: two such searches held io PSI at 84)
TESTS     test_dispatch.py test_zero_usd_mint_floor.py + test_bin_help_smoke.py once (timeout 900, TMPDIR + --basetemp under /dev/shm, env -u TMUX -u TMUX_PANE -u AGI_POST -u AGI_SEAT (TMM.322)); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/dispatch.py · extensions/agi/tests/test_dispatch.py (its _cap_project/_run_cap_dispatch helpers: REUSE, never copy) · extensions/agi/tests/test_zero_usd_mint_floor.py · .agi/config.json (the ONE cell provisioning.zero_usd_skip_checks) · .agi/nodes/experiment/a00-9aa7572d-b16df9.md · .agi/nodes/experiment/a00-c46a37b3-77dd51.md · .agi/nodes/hypothesis/zero-usd-exemption-skips-only-the-credit-floors.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 37367b9a8 · <= 40 test lines net over 37367b9a8 · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat 37367b9a8 <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective EG.68: mur-eg-18 DH.671-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
