---
id: doc:card-director-general-3
mint_id: 960e181d30924fb3ba1a63ca4a6698f4
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-3
scaffold_hash: 67b067422d7509fe
season: 2
title: Card director general 3
town: core
---
# doc:card-director-general-3

# doc:card-director-general-3 — director-general-3's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (11:5xZ 09-29)
| | |
|---|---|
| post | director-general-3 |
| stage | stage 3 of 3 — MVPs + build nodes + tests; a build node may take the [goal, idea] parent set to shortcut chain growth |
| protocol | doc:council-loop (read it first) · goal:g7.16.1 (the owner's words) |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 high · seated 10:3xZ 09-29 by belam |
| skills | agi-node-write · agi-verify · agi-send · agi-rotate · agi-post |
| now | bundle 1 stage 3 DONE (A B C D landed); handed to sanctuary-master for review; waiting on residues |

## §1 Plan
```
done   B C D (5a828b3ce · 0055d30a2 · 396e3fa1d) · A (e27b43be2) · verify 12/13 (bin-suite-fresh = suite owed)
next   sanctuary-master's residues -> fix each in place, re-verify, hand back
owed   the Prime mints config:formations (command on mvp:dg3-a-one-formation-cell); until then check_formation SKIPs
```

## §2 Landed
- 5a828b3ce B one column-0 THOUGHT definition · C home token + 13-node scrub · D one ensure_mint_id; 3 mvps + build:bin-anonymize
- 0055d30a2 census idea parents kept on 3 build nodes ([goal, idea])
- 396e3fa1d goal:g4.18.1 Falsifier run: F1 3 not met (.2 .4 .5 gap-only) · F2 1 met
- e27b43be2 A: check_formation + 6-row test · 6 templates Posts + Stand up · g7.16 umbrella · g7.16.2 minted · mvp:dg3-a-one-formation-cell

## 🔴 Where it stops
11:5xZ 09-29 re-mur wf_aa3f01d4-2aa: all 18 first-pass residues closed; new rows 19-24 FIXED (19-20 DG1 50911a0d7, 21 DG2 e008169dc, 22-24 DG3 09123feeb + b886bdcdb); mur-3 wf_16ffb9a5-596 closed 19-24 (B E D accept, C A accept_with_residue); rows 25 27 28 29 FIXED at 1ecf92bd3; mur-4: row A clean accept; residue 31 (row C: new empty/binary file path) FIXED at 80c1c245d; BUNDLE 1 CLEAN (mur-5 wf_f35e4407-74c accepted row C at 80c1c245d; handed to alive 13:0xZ). BUNDLE 2 R1 (urgent, blocks PASS B3 17:47Z) built: code b9a4ca508 (anonymize.HOME_PATH_RE + home_relative, rotate._dump_record + _resolve_record_path) + record scrub d25e78e81 (320 records); falsifier 1 anonymize over d6cfe7749..HEAD ok; under mur wf_8da5e93a-72f (b2-R1-code, b2-R1-scrub; residues come straight back to me); R2-F follow from director-general-2 as one handoff (SendMessage wakes this session):
```
python3 extensions/agi/bin/send.py --from director-general-3 read director-general-3
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| `grep -r` / `find` over .agi/ or the repo root io-stalls the box | `git grep PATTERN -- <paths>` |
| `send.py read <self>` without `--from` | resolves self as 'unknown' and exits 2: always pass `--from director-general-3` |
| build parent shapes | [mvp] · [build, goal] · [goal, mvp] · [goal, idea] — a lone goal is refused; `--dry-run` skips the spawn gate |
| new build node | `--payload <path>` AND `--set payload_ref=<path>`, else level3.py mints a duplicate |
| config:* nodes | owner/prime only (goal:g12): a director's create is refused by name -> the command goes on an mvp, owed by the Prime |
| replace body on a heading line | refused (splice guard): replace the blank line ABOVE the heading instead |
| a new goal node renders only with origin goals-doc + heading_level | set both, then --render |
| no dispatch | this mode runs no dispatch.py and no Claude Agent/Workflow subagents |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken · `snapshot-goals.py --render --check`

## §6 BANKED
(none)

## Findings for the next bundle (rows, not fixed here)
- test_skills_first_turn_entry red: agi-post missing from config:rotations skills entry (b0b54f6fa)
- test_sensei_wake_audit item2 red: no live fact cites send.py whois (facts collapsed 09-27)
- write.py stamps town: core on nodes minted by local-maxxing posts (row says local-maxxing)
- anonymize check scans REMOVED diff lines too: a scrub commit would be refused once the hook is installed
- repo checkout path in 87 live nodes (verdict:dg2-c-home-path)
