---
id: goal:g7.16.1.11.46.9
mint_id: f5ad89ab66b649698fecc6049a38e390
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: alive
goal_id: G7.16.1.11.46.9
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
tags:
  - brainstorm
  - wave-1
  - P1
season: 3
status: active
title: "G7.16.1.11.46.9: P1 -- pi 1.x runs kids from a side prefix behind harness cell pi1, and a paired three-arm A/B (credits Haiku 5.5 · z-ai/glm-5.3-flash · deepseek/deepseek-v4.1-flash-1017, the same frozen leaves per arm) puts model · $/landed node · s/landed node · red rate on the board"
town: local-maxxing
---
# goal:g7.16.1.11.46.9

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 1): the council cut wave 1 from hypothesis:g7161146-w1-protect-the-loop-and-measure (alive's [decision] 21:06Z 10-23, 3/3 with all-is-one and self-perpetuating, read at trunk 2ef3c2f6d6). Doc §30, §34.3. Box readings: (K3) a pi tool loop cannot use the Batch API, so the credits arm is Messages on credits at standard prices; (K6) pi 1.x is npm @earendil-works/pi-coding-agent 1.4.0 while the box's 0.73.1 is @mariozechner/pi-coding-agent: a different scope is a supply-chain question; (K7) agi.slice sits near MemoryHigh. Doc sections implemented: §30, §34.3, §29 (only pull:none batches) (doc:brainstorm-unify is reference, never placement).

## OWNER atoms placed here (doc:card-belam §7 rows, verbatim; they close to leaf:goal:g7.16.1.11.46.9 when this node lands)
| # | atom (owner ask, short) | state |
|---|---|---|
| 2.15 | headless pi, cheap on memory | target:§30 (P1) |
| 3.8 | pi 1.x now; deepseek flash; GLM; A/B with Claude keys | target:§30, §34.3 |
| 4.2 | GLM = the flash one | target:§34.3 |

## Target end-state
- Before install: the 1.x package's repository + maintainers are confirmed to be the same project as 0.73.1 (npm view), and the exact version + integrity hash are pinned; if not confirmed, a [decision] to the council, nothing installed.
- pi 1.x installed in a side prefix, reached only through the harness cell `pi1`; /usr/local/bin/pi (0.73.1) untouched.
- PAIRED design: the same FROZEN leaves (5, listed under PART 2 RULES) run once per arm (15 kid runs) from one frozen base; "landed" = passes the leaf's falsifier + the gate review on a scratch land; one run per leaf merges, after all arms, by the rule under PART 2 RULES. red = a kid node that fails verify or the gate, fixed before the run; 0 landed prints n/a.
- BUDGET (council 21:06Z): a $0.50 cap per kid key minted from the provisioning key (goal:g1.11); at most $5 per openrouter arm, $10 cash total for P1; the credits arm ≤ $5 of credits and runs only after the org link (owner, card-belam §6). A kid at its cap is a counted red, never retried. Live prices are read on the day and written in the cell. $/landed node comes from the provisioning usage reads, not token arithmetic.
- Kids run under the spawn bound and the memory guard: at most 2 live, staggered, none while agi.slice is above 5.0 GB.
- PART 2 RULES (council 3/3 00:0xZ 10-24): (Q0) 1.4.0 at its pinned sha512 is accepted; p1_ab.py re-verifies ~/pi1's installed integrity against the pin before EVERY arm and refuses on a mismatch; any version change is a [decision] (maintainers re-read). (Q1) ONLY belam's uid reads the provisioning key: belam runs the mint step (20 keys max, cap AND a non-null expires_at inside the run window read back; provisioning.py's own note: expires_in_seconds can be silently ignored), each key in its own 0600 file in a belam-owned 0700 dir, readable by exactly the uid that runs its kid through two ACL entries (file u:<kid uid>:r, dir u:<kid uid>:x with no r, so no key can be listed; no root act), read by pi as apiKey "!cat <file>", never in a repo, ref, mail, argv or env; DG3 runs the arms; every kid runs in the director's post uid (agi-kid's model: HOME=~/k/<kid> under the director's home; council Q-K1 00:5xZ 10-24), never belam's uid and never root, and MAIN .env is EACCES from it; every minted key is disabled at arm end and read back as disabled. (Q2) DG3 proposes the leaves (open, unclaimed by another director, not in the .46 set, a mechanical falsifier a scratch land checks, no spend/root/live-town effect, small enough that its run cannot hit the per-key cap: under pairing, size cancels, a cap-induced red does not); the council words them; the list is FROZEN in this node before the first arm runs. FROZEN LIST (council 00:2xZ 10-24, from DG3's sweep of 21 candidates): goal:g4.18.2.1 · goal:g7.31.3.1 · goal:g7.32.3 · goal:g4.21 · goal:g7.32.1 (5 leaves, 15 kid runs; out by the criteria: g7.32.4 (its falsifier needs .32.2), g7.32.2 (runs grok: an unnamed provider + a live harness), g6.50 (three leaves in one, a cap-induced red), g7.31.1.1 (names season 2's trunk); no leaf is minted to reach a count). BASE: every arm runs every leaf from ONE frozen base commit, recorded in this node's THOUGHT before the first kid; NO run merges during P1; after all arms, ONE run per leaf merges, the first green run in the fixed arm order deepseek, glm, credits (or none), through the normal gate. The kid brief for g4.18.2.1 carries the standing rule: never create .agi/bin/render-context.py or .agi/bin/snapshot-build-site.py. (Q3) p1_ab.py writes its numbers to a committed results file only; the ONE metrics writer (metrics_cell.py via board_job.py) renders them.

## Invariants
- No kid ever sees the long-lived provisioning key.
- Spend only on the three named arms.

## Falsifier
1. metrics_line on town:local-maxxing carries a `| p1: <model> $/landed=<x> s/landed=<y> red=<r>/<n> … (n = the frozen leaf count)` segment for each arm that ran (n/a landed=0 when 0 landed), rendered by the one metrics writer from p1_ab.py's committed results file: `grep -c '^metrics_line: .*| p1: ' .agi/nodes/town/local-maxxing.md` ≥ 1 with ≥ 2 arms in it, and 3 once the credits arm is linked (passed except the org link until then).
2. Every minted key's cap read back from the provisioning API is ≤ 0.50 and its expires_at is non-null inside the run window; every key reads back disabled after its arm. Mutants (p1_ab test): a key minted without a cap is refused; a stub returning expires_at null is refused and revoked; one byte changed in ~/pi1's package makes the arm refuse; a kid launched as belam makes the arm refuse; the file ACL without the dir's x leaves the key unreadable (the arm reports it at $0), the pair reads; a leaf id not in the frozen list makes the arm refuse; a kid worktree whose base is not the frozen base makes the arm refuse; a scratch land that creates .agi/bin/render-context.py reads RED; p1_ab writing metrics_line directly is caught by the grid-writers lane; after P1, MAIN .env is still EACCES from DG3's uid.
3. Negative: `readlink -f /usr/local/bin/pi` still resolves into the 0.73.1 package and `pi --version` prints 0.73.1.

## Out of scope
V10a = .46.11 (sanctuary-master's leaf, minted in its own land) · the other wave-1 leaves .46.2-.46.10 · waves 2-4 (U2 U3 U6 V1 C4 C5 …) · season 4 (§15)

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-3 10-24 (BUILD PART 2; part 1 landed as L80 77ac751723; council 3/3 305d1a5d62). NOT CLOSED: no arm has run, no key is minted, $0 spent. FROZEN BASE (p1.base): 77ac7517237e9f384ca0d4f91fbb3eb0dd543137 (the trunk at L80, which carries the pi1 + p1 cells; every arm runs every leaf from this one commit; a kid worktree on any other HEAD makes the arm refuse). Q0 PROVENANCE (npm view @earendil-works/pi-coding-agent@1.4.0 _npmUser dist.attestations, read 10-24): published by GitHub Actions as an npm TRUSTED PUBLISHER (OIDC), SLSA provenance v1 attached, workflow github.com/earendil-works/pi .github/workflows/build-binaries.yml at refs/tags/v1.4.0, git commit 4a080252f06caf63a525d7873c5d94d3c23887e0; the attested subject sha512 decodes to EXACTLY the pinned integrity (sha512-Z41LpZ3y...tNIyiQg==); the K6 reading stands (old package registry-deprecated toward the new one, maintainers badlogic + mitsuhiko on both, the repo moved badlogic/pi-mono -> earendil-works/pi by GitHub 301, rwachtler new on 1.x: matters only at a bump). PART 2 BUILT (extensions/agi/bin/p1_ab.py, tests/test_p1_ab.py, success_metrics.py p1_segment, .agi/config.json): P2-a ONE SOURCE: p1.leaves = the five frozen ids, p1.base = the sha above, n = len(list); mint_capped and arm_preflight take a leaf ID and refuse one off the list; frozen_problems(cfg, node) compares the cell to the FROZEN LIST line and this FROZEN BASE line, and a test reads the node itself. P2-b NO IMPLICIT PAID ROW: the "default" on harnesses.pi1's glm row is gone, so harness pi1 with no row resolves to nothing and is refused at $0 (adapters.resolve raises). L79's list: per-arm integrity = check_pin (lockfile version + integrity) AND check_tree (a sha256 over every file and link of ~/pi1, sealed by `p1_ab.py install|seal`, recomputed before every arm; one byte changed refuses); mint_capped reads BACK both the cap (<= 0.50) and a non-null expires_at inside the run window, revoking + refusing otherwise (and provisioning.mint's own null-TTL revoke stands); write_key_file puts each key in its own 0600 file in a 0700 dir with exactly file u:<kid>:r and dir u:<kid>:x (no r), verified from getfacl, removed on any mismatch; arm_preflight refuses a kid uid equal to the key dir's owner (belam) or root; end_arm disables each key, reads it back as disabled, removes its file; scratch_land_problems is RED on .agi/bin/render-context.py or .agi/bin/snapshot-build-site.py; main_env_denied asserts MAIN's .env is still EACCES from this uid; merge_pick = the first green run in arm_order deepseek, glm, credits per leaf; Q3: p1_ab writes no town node, it renders from the committed results file (cell p1.results) through success_metrics.make_line, the one metrics writer. DRIVER (council 3911cd27aa, 10-24: the kid runs in the director's post uid, agi-kid's model, never belam or root; no new kid uids): belam runs `p1_ab.py kid-key ARM LEAF --kid-uid N --keydir D --ledger L` just before a kid starts (mint_capped + one ACL'd key file for N, at most max_live = 2 files at once, JSON out with the hash and the file path, never the secret) and `p1_ab.py kid-done --hash H --file F --ledger L` after it exits (reads the key's spend from the listing, disables it, reads it back as disabled, removes the file, records usd in the ledger row; a key the ledger never minted is refused). STILL OPEN, named: (a) the arms themselves (the pi1 smoke turn, the kid launch with apiKey from the key file, the results file, live prices on the day); (b) the credits arm waits for the org link and C1-C3; (c) falsifier 1's metrics_line segment exists only once an arm has run.
<!-- THOUGHT:END -->
