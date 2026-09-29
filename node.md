---
id: goal:g7.16.1.3
mint_id: 9ebfd326afc549f2ab52eea1876eeb84
type: goal
parents:
  - goal:g7.16.1
next_edges: []
confidence: 0.6
edited_by: alive
goal_id: G7.16.1.3
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: ade4f360fae97c26
season: 2
seeds: []
status: active
tags:
  - formation
  - council-loop
  - bundle-3
  - local-maxxing
  - core-simplify
title: "G7.16.1.3: COUNCIL BUNDLE 3 -- grok core simplify: H heal first (g4.18.3 adopt gate, g4.18.4 config:posts always loads, one park form, bundle-2 residues) -> S1 messaging is ONE route or a verdict -> S2 the unwired five explained, not ported"
town: core
---
# goal:g7.16.1.3

# goal:g7.16.1.3

## Why this exists
goal:g7.16.1 (the council loop), order of work step 2: grok's work on core/season2/main and core/main ("probably way overbuilt on core": simplify). The council loop resumed on the owner's word ("we can Keep working till 7pm next", 16:5xZ 09-29). The Prime's review doc:council-loop-review-s2 advised landing goal:g4.18.3 and goal:g4.18.4 before this bundle or keeping them out of its scope, and the council chose to land them first. What the council measured at 17:1xZ 09-29 on origin/core/season2/main at fca147fe1, against this trunk: 374 core-only commits · 67 engine files +6295/-239 · 41 new files. Messaging is a dm_* family of 7 modules (628 lines), all behind dm_engine (<- send.py, crons.py), added BESIDE the inbox route, never instead of it: core's send.py still carries 149 `inbox` refs (trunk 152). Five new modules, 918 lines, are imported only by their own test: kid_write_gate 156 · spawn_refusal 151 · parent_slots 195 (+ .geometry/parent-slots.md) · needs_rotate 158 · session_ingest 258. Four of them are core's goal:g7.31.3.3 .1-.5 seeds, marked COMPLETE on core while the wiring is still open. Bundle 2's lens reviews (all-is-one, self-perpetuating) left the residues in row H4.

## Target end-state
Rows in council order. A row closes when its line holds in the bytes.
- **H1 · one gate for every verb.** goal:g4.18.3: `write.py <id> adopt` applies the type's written_by (and its self_row / actor_rows grants) before any mint; an actor outside written_by is refused by name and nothing is minted.
- **H2 · the organ every post reads always loads.** goal:g4.18.4: a key-row write never inserts one row into a config:posts that lacks it (refuse by name, or write the whole row set), and every config:posts write is YAML-loaded before it is committed.
- **H3 · one park form.** The 5 body-table carriers of parked ROWS (goal:g7.33.19 · 11, hypothesis:pass10-0927-residue-batch · 11, pass11-0927 · 3, pass12-0928 · 8, passb1-0928 · 6 = 39 rows) carry the tag `parked:g7.16.2`, with no status change on a carrier that also holds keep rows. The formation check FAILs when a live node holds a `triage: parked: formation` row but no carrier tag, so a switch to g7.16.2 wakes the carrier and its body names the rows.
- **H4 · bundle-2 residues.** rotate._dump_record / rotate._resolve_record_path and verification's parked_carriers move to ONE small shared module that rotate, heal, sensei, write and verification import. No `_private` name is imported across modules, and write.py never imports the verifier. heal never swallows ImportError on a rotation-record write. skills/agi-master-gate/SKILL.md:66 points at anonymize.CLASSES + HOME_PATH_RE instead of hand-listing classes. goal:g7.32.5 returns to its pre-park status (park is tag-only). Plus every refuter-confirmed residue of the council mur wf_4e0708df-4ef over 794a0782e..9c54fb3c4 (the convener sends them to director-general-1 by name).
- **S1 · messaging is ONE route, or a verdict.** The first leaf MEASURES: send routes on the trunk before and after, and which goal:g7.32.6 targets the trunk lacks. S1 lands ONLY as a replacement: the dm_* family + send_transport fold into ONE module (or send.py itself) on this trunk, carrying the union of their tests, and the SAME row retires the inbox route (152 refs down to what a retirement pointer needs), so routes go 2 -> 1, with CC SendMessage as the interim. The dm file format stays byte-compatible: one test reads a real committed .agi/comms/**/dm/*.md file through the folded module. If the retirement does not fit, S1 becomes a verdict node like S2, and nothing is ported. adapters/magic_pane follows S1's outcome.
- **S2 · the unwired five are explained, not dropped.** None is ported. ONE verdict node on this trunk carries, per module: (a) the goal it serves (g7.31.3.3 .1-.5 for kid_write_gate, spawn_refusal, parent_slots, needs_rotate; session_ingest = a SECOND mint door that folds into `write.py create` with a derived id, never a new module); (b) the start point for when that goal is worked: core sha + its test file + its pass count; (c) the gap in one line ("built + tested, not wired into heal/rotate"). Our goal:g7.31.3.3 records module != wired, so no successor reads core's COMPLETE as done. ONE TRUTH ACROSS TOWNS: core marks g7.31.3.3 and .1-.5 complete while our trunk has g7.31.3.3 active and no .1-.5. The verdict node names this for the Prime's merge: the true status is ACTIVE until wired, so g7.31.3.3 stays active and its leaves land active, each with a BODY status line in Target end-state ("built at <core sha>, test <file> <n>/<n>, not wired into heal/rotate"), never in THOUGHT, because it is state, not delta. The convener sends the Prime one [merge-note] line; nothing is written on core.
- **Convention for every port:** a folded or ported module names its core module + sha in its build node (provenance lives on THIS trunk, never a write on core), and its tests are named by behaviour, never by goal id.

## Invariants
- No parent/kid dispatch (goal:g7.16.1). Every node is written through write.py. Nothing is deleted. Nothing is written on core/season2/main or core/main (another town's tree: read it, never write it).
- A fold never lands without the test that proves its behaviour.
- One director works the bundle at a time: DG1 -> DG2 -> DG3 -> sanctuary-master -> council. Tests run ONE file at a time while a PASS runs on this box.

## Falsifier
1. goal:g4.18.3 and goal:g4.18.4 read complete, with their own falsifiers run · the formation check FAILs on a fixture carrier with a parked row and no tag, and PASSes on the live graph · `git grep -nE 'from rotate import _|rotate\._(dump_record|resolve_record_path)' -- extensions/agi/bin` prints 0 · `git grep -n 'import verification' -- extensions/agi/bin/write.py` prints 0 · the S2 verdict node exists and names all 5 modules with sha + test + pass count · `python3 extensions/agi/bin/links.py links` = 0 broken · `snapshot-goals.py --render --check` exits 0.
2. Negative: `git ls-files extensions/agi/bin | grep -cE 'kid_write_gate|spawn_refusal|parent_slots|needs_rotate|session_ingest'` prints 0 · if S1 landed: `git ls-files extensions/agi/bin | grep -c '^extensions/agi/bin/dm_'` <= 1 and the trunk carries ONE send route · if S1 is a verdict: no dm_* file on the trunk.

## Out of scope
bundle 4 = core's edits to EXISTING files (write.py +125, dispatch.py +86, boxes.py +87, provisioning.py, rotate.py) together with profile_sync (it moves with its rotate/write callers) · then the season-2 close (outcomes -> bigger outcomes -> overviews, handed to the Prime) · goal:g7.31.3.3 itself (only its record is corrected) · goal:g5.22 through goal:g5.31

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by alive (convener) after the council converged over SendMessage, 17:1xZ 09-29. alive drafted H1-H4 + S1 fold + S2 verdict + S3 strays. all-is-one: S1 only as a REPLACEMENT that retires the inbox route (core added dm_* BESIDE the inbox, 149 refs, so porting as-is gives 2 routes), else a verdict; session_ingest = a second mint door, folding into write.py create; S3 dissolved (profile_sync moves with its bundle-4 callers, magic_pane follows S1, behaviour-named tests become a convention). self-perpetuating kept S3, and its port-by-use survives in bundle 4, so alive took the dissolve. self-perpetuating: a byte-compatible dm-format test; S2 says built-not-wired with sha + test + pass count as the start point, never 'dropped'; no pointer written on core (withdrawn after all-is-one cited HEAD rule E). all-is-one: one truth across towns (core's g7.31.3.3 complete vs ours active); self-perpetuating: that status line lives in the BODY, not THOUGHT, and all-is-one conceded. The council also chose to land g4.18.3/.4 first, on belam's advice in doc:council-loop-review-s2.
<!-- THOUGHT:END -->
