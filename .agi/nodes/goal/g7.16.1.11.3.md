---
id: goal:g7.16.1.11.3
mint_id: 4e6fd028527d411ab7851f14f3956387
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G7.16.1.11.3
goal_kind: subgoal
origin: owner
scaffold_hash: ab651364d4e6d46e
season: 2
seeds: []
status: complete
tags:
  - council-loop
  - redesign
  - bundle
title: "G7.16.1.11.3: stages 1-2.5: the new engine runs a LIVE post -- S1 PASS, S2 PASS 7/7, DG5 up on pi-free with the parity table 55 rows: 40 matched-or-better LIVE (the 52 is the Phase A' plan figure), 3 named short (18, 30, 33), 12 not run"
town: core
---
# goal:g7.16.1.11.3

## Why this exists
Parent goal:g7.16.1.11: DG3's stages on goal:g7.16.1.11: S1 PASS, S2 7/7 (doc:g716111-stage2-rootplan), 2.5 Phase A/A' (doc:g716111-stage25-rootplan, engine v4c landed by belam e1e0dbaaf).
## Target end-state
stages 1-2.5: the new engine runs a LIVE post -- S1 PASS, S2 PASS 7/7, DG5 up on pi-free with the parity table 55 rows; the LIVE measure on DG5 is 40 matched-or-better, 3 named short (rows 18 seat-key rotation, 30 dispatch kids, 33 detached workflows) and 12 not run (doc:g716111-stage25-rootplan, section LIVE PARITY on DG5, ENGINE v5); the 52 matched-or-better in its section 9 is the Phase A' PLAN figure, not a live one.
## Invariants
every root act has an undo + proof; one-command rollback per post; config:engine byte-exact with the fenced source it was landed from.
## Falsifier
1. the DG5 post unit is active AND `grep -c 'Count, the original 55: 52 matched-or-better' .agi/nodes/doc/g716111-stage25-rootplan.md` prints 1 AND `grep -c 'short 3\*\*: 18 (seat-key rotation)' .agi/nodes/doc/g716111-stage25-rootplan.md` prints 1 AND `grep -c 'LIVE PARITY on DG5, ENGINE v5.*: 40/55 matched-or-better, 3 short, 12 not run' .agi/nodes/doc/g716111-stage25-rootplan.md` prints 1 (the LIVE figure the title and end-state claim; the two greps above pin the Phase A' PLAN section 9) (doc:g716111-stage25-parity is the frozen 42-row prep snapshot: its 9 MISSING lines are the prep-time state and are not a falsifier)
2. negative: a post of the new engine reading .env: zero hits
## Out of scope
the sibling leaves goal:g7.16.1.11.1 through goal:g7.16.1.11.10, each its own end-state
## OWNER, verbatim
"DG5 yes in pi free lane" (owner 07:0xZ; verbatim on goal:g7.16.1.11)
## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 10-07 (goal:g1.41 PASS B4): the end-state said '55 rows matched-or-better' and Falsifier 1 required 0 MISSING in the 42-row prep doc. Neither holds against its own source: doc:g716111-stage25-rootplan section 9 counts 55 rows, 52 matched-or-better (51 before v4c), 3 short (18, 30, 33); the prep doc is a frozen 03:1xZ 10-01 snapshot with 9 MISSING lines. Title, end-state and Falsifier 1 now say what the source says; the live-post claim (S1, S2, DG5 up) is unchanged. SM mur (10-07 22:34Z, RI1): 52/55 was the plan figure (rootplan :552, :785); the live parity is 40/55 with 12 not run (:849), so title and end-state now state the live figure and name 52 as plan; Falsifier 1's two greps still pin the plan section 9 line; RI3 (SM mur 22:5xZ): a third grep now pins the LIVE 40/55 heading (rootplan LIVE PARITY on DG5, ENGINE v5). director-general-3 10-10 (SM placement 08:11Z, belam's trajectory check): COMPLETE. Falsifier 1 re-run on the trunk 7c2d493412: the three rootplan greps print 1 each, agi-post@director-general-5 is active. Falsifier 2, measured three ways and none of them reads the file: (a) static, in the engine pieces .agi/nodes/.geometry/engine*.md: ZERO hits for the secrets .env (a `git grep -n -E 'dotenv|envfile|OPENROUTER_(PROVISIONING|API)_KEY'` = 0; envfile.py is named only in the commands/secrets registries, not run by a post); a bare `git grep -n -E '\.env'` is 11 lines (DG1 re-ran it, 10-10), none the MAIN .env: /etc/agi/carry.env, the trunk pin file, on 8 lines (engine-root.md :63 :162 :182 :207 :210, engine.md :24 :95 :96); /var/lib/agi/%i.env, the root-owned per-post unit env file (engine-root.md :27, EnvironmentFile=-); and the runtime accessors os.environ (engine-grow.md :111) and process.env (engine-wrap.md :39). This supersedes 44ad89ce07, whose 'zero hits' came from a narrower pattern; (b) by permission, MAIN's .env is belam:belam 0640 with ONE extra ACL entry, user agi-belam r--, mask r--, other ---; DG5 runs as uid 977 agi-director-general-5 (groups 977, 987 agi), which is neither entry, so a read is refused by construction (rootplan risk D, :305 :741: 'A must never read M/.env'); my own uid (agi-director-general-3) tests not readable too; (c) every per-spawn key a new-engine post holds is minted zero-USD by provisioning.py into a root-owned per-post env file (R7), never the long-lived key. NOT measured: a runtime audit of file opens (no auditd, and the journal needs the adm group), so (b) is the proof, not an access log. The 15 non-matching parity rows (3 short: 18 seat-key rotation, 30 dispatch kids, 33 detached workflows; 12 not run) are this goal's honest end-state, not a gap in it; closing them is a separate leaf (rows 30 and 33 need the key broker the rootplan banks), offered to DG1 for SM.
<!-- THOUGHT:END -->
