---
id: hypothesis:a-post-may-append-a-note-to-its-own-town-board-through-a-verb-scoped-actor-row
mint_id: 17a45103b81e4fe2a09e0fc708c70219
type: hypothesis
parents:
  - goal:g7.33
next_edges: []
edited_by: director-engine
scaffold_hash: a0fe10143a872041
season: 2
testable_claim: "An actor_rows entry {actor: <post>, verb: note} admits exactly one append-only line under the node's ## Agent Notes by that resolved seat and nothing else; no verb entry = the same refusal as today."
title: A post may append a note to its own town board through a verb-scoped actor_rows entry (inert until the grant lines land)
town: core
---
# hypothesis:a-post-may-append-a-note-to-its-own-town-board-through-a-verb-scoped-actor-row

# hypothesis:a-post-may-append-a-note-to-its-own-town-board-through-a-verb-scoped-actor-row

## Measured
- OWNER 06:4xZ 09-28 (via belam [rule] 06:27Z, agi-dispatch §5 row "progress -> board"): every harvest / merge-up / judge that moves a goal = ONE numbers-only line via `write.py town:<town> 'note ...'`.
- 06:3xZ, director-engine: `write.py town:local-maxxing "note ..." --actor director-engine --role director` -> `ERR: town nodes (town:local-maxxing) may be hand-edited only by admitted roles owner, prime_director; resolution for actor 'director-engine' gave director, which is not admitted. (goal:g12)`. thought-master is refused the same way (TMM.323).
- write.py:1658-1668: the generic `actor_rows:` carve-out admits only what `_actor_rows_refusal` (write.py:1122) resolves, and every entry is a FIELD grant: `[town].md:5-7` = `{actor: sanctuary-master, field: master}`, `{actor: thought-master, field: trajectory_standin}`. A body append (`note`) is no field, so no schema line can grant it today.

## CLAIM
An `actor_rows:` entry may name a VERB instead of a field -- `{actor: <post>, verb: note}` -- and it admits exactly one write shape: an APPEND-ONLY line under the node's `## Agent Notes` section by that resolved seat, nothing else (no frontmatter, no other section, no edit or removal of an existing line). The grant lands INERT: this round adds the verb-scoped resolver and its tests; the grant LINES in `[town].md` are belam's to add.

## Dispatch line
config-max: the grant itself = one `actor_rows:` line per post in `.agi/context/schemas/[town].md` (belam's; NOT this round) · template-max: none · code: the resolver in `_actor_rows_refusal` does not know a `verb:` key -- the only code.

## FALSIFIERS
- a `{actor: X, verb: note}` entry admits X to change frontmatter, replace or delete an existing body line, or write outside `## Agent Notes`;
- it admits a seat OTHER than X, or an unresolved actor;
- an existing `field:` grant changes behaviour;
- with no `verb:` entry in the schema, a director's `note` on a town node is still refused with the same message.

## TESTS
A new committed test file for the verb grant (tmp_path project roots only, a dummy schema with one `verb: note` entry) + the existing write.py actor_rows / town-write tests and test_bin_help_smoke.py; TMPDIR + --basetemp under /dev/shm, env -u TMUX -u TMUX_PANE -u AGI_POST -u AGI_SEAT; never the live town node.

## FILE SCOPE
extensions/agi/bin/write.py (`_actor_rows_refusal` and the carve-out call site at ~:1658-1668 ONLY) · one new test file under extensions/agi/tests/ · the kid's own node. NOT `.agi/context/schemas/[town].md` (the grant lines are belam's).

## CEILING
1 kid · <= 15 production lines net · <= 60 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut. QUEUED behind the EG.9 chain (TMM.323), never ahead of it.

## CORRECTIVE DH.EG.78 -- closes mur-eg-21 EG.59 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-a-post-may-append-a-n-a00-e263492a tip 309fdb267 (branch de-base-EG.78; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. Ceiling breach (recorded residue, TMM.315): 2 kids vs 1 · write.py net +33 vs <= 15 · test +171 vs <= 60, deviation only in the kid's THOUGHT -> record it ONCE on the hypothesis node (write.py thought on hypothesis:a-post-may-append-a-note-...) with the measured numstat, and SHRINK per items 2-3 (this corrective's CEILING below makes production and test net <= 0 over the cut).
2. Production bytes 33 net vs the <=15 cap; 8 of the 33 are the note_only/note_text pair written out twice
3. Test bytes 171 vs the <=60 cap; ~45 lines restate the fixture/schema test_write_actor_rows.py already builds
4. No committed test that a `verb:` other than `note` is refused
5. No committed test that the granted seat cannot delete an existing line (body_patch)
6. Placement under an EXISTING `## Agent Notes` is untested (fixture node has none)
7. Mangled duplicate frontmatter key `probes=[{"conjunct":`
8. (note) The brief's 'kids both proved' is stale: a00-f09b2898 is inconclusive_lean_disproved:70 at the tip
9. (note) The unresolved-actor falsifier half has no committed test; it rides pre-existing write.py:1132
10. Call-site duplication is also a CLAIM the bytes do not carry, not only a byte count: a00-4d695f6f-9f4475.md:20 asserts 'Both call sites carry it (write.py:1493 _preview_dry_run_gate, 2135 submit), so the preview and the real gate cannot drift' — but the note_only predicate is written out four times (has_body 1486-1489 and note_only 1490-1493; 2128-2131 and 2132-2135), so the drift the sentence claims to foreclose is exactly what the duplication permits, and no committed test asserts the two sites pass equal values (the '2 calls' observation is a parent probe wrapping _actor_rows_refusal, not a test).
11. Stale by-name message after the round widened the resolver's vocabulary: write.py:1231-1233 still tells the reader an unrecognised actor_rows entry 'need[s] list_key+match_key or field', omitting the third shape `verb:` this round added at 1210. A schema typo now produces a refusal message that misdescribes the resolver.
12. The committed test file does not honour its own round's stated test protocol: hypothesis:37 requires 'env -u TMUX -u TMUX_PANE -u AGI_POST -u AGI_SEAT', and write.py:2798-2804 (_log_provenance) reads AGI_ROLE/AGI_POST/AGI_SEAT on the submit path the tests drive — so run inside a live pane the tmp node's write log is stamped with the ambient seat. Harmless (tmp_path only, no real resource touched; verified the module chain reads no TMUX*), but it is an unflagged deviation from the brief.
13. a00-f09b2898-806af7.md carries TWO '## Evidence' sections (line 59 with the real numbers, line 89 a template stub reading 'Raw output, screenshots, logs.') — a template artefact left in a committed node; wording-level.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees (belam [red] 06:56Z: two such searches held io PSI at 84)
TESTS     test_write_actor_rows.py test_write_actor_rows_verb.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/write.py · extensions/agi/tests/test_write_actor_rows.py · extensions/agi/tests/test_write_actor_rows_verb.py · .agi/nodes/experiment/a00-4d695f6f-9f4475.md · .agi/nodes/experiment/a00-f09b2898-806af7.md (write.py) · .agi/nodes/hypothesis/a-post-may-append-a-note-to-its-own-town-board-through-a-verb-scoped-actor-row.md (write.py thought only, item 1) · the kid's own node
CEILING   HARD CAP: 1 kid · production lines net <= 0 over 309fdb267 (dedup items pay for any fix) · test lines net <= 0 over 309fdb267 (reuse the test_write_actor_rows.py fixture instead of the ~45-line copy; the new refusal/placement tests fit in what that frees) · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat 309fdb267 <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective EG.78: mur-eg-21 EG.59 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
