---
id: experiment:a00-5351e255-7f99b8
mint_id: a712f0391ee14917b4479b6759d94acf
type: experiment
parents:
  - hypothesis:l4-config-vision-written-by-flip
next_edges: []
confidence: 0.9
edited_by: a00-dba67823
evidence_runs:
  - experiment:a00-5351e255-7f99b8
loop: hypothesis:l4-config-vision-written-by-flip@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3b6396abd4e77c20
season: 2
title: A00 5351e255 7f99b8
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-5351e255-7f99b8

## Experiment

Ran the L4.09 `written_by` flip on TWO real schema files, one type at a time, leaving `[moral]` offline.

1. `[config].md`: added `written_by: [owner, prime_director]` (list-shaped) right after `name: config`. Proof fixture PASS/REFUSE across 4 actors. No surprise → proceeded.
2. `[vision].md`: added the same line after `name: vision`. Proof fixture re-run: vision now gates exactly like config.

Behavioural proofs (scratch script `/tmp/a00_proof.py`, tmp-graph fixture that copies the REAL flipped schema files + a seats row `belam`→`prime_director`, then calls `write.submit()` with each actor; `AGI_ROLE` env popped so role resolution reaches seats/owner):

- config: `belam-S1-L4-II` PASS, `sanctuary-director-4e` REFUSE (names type + admitted roles), `owner` PASS, `a00-deadbeef` REFUSE.
- vision: same 4-way pattern — PASS for belam & owner, REFUSE (naming type+roles) for sanctuary-director-4e and a00.
- hypothesis (declares NO written_by): PASS for ALL actors incl. agent-id — the no-gate property is preserved.
- moral (`written_by: owner`): only `owner` PASS; `belam` resolves prime_director and is REFUSED for moral — end-to-end rule unchanged.

`links.py roles` BEFORE: **1 declared type(s)**, moral only. AFTER: **3 declare(s)** — config `owner,prime_director`, vision `owner,prime_director`, moral `owner`; and it names **17 vision writers** (all agent-id `a00-2...`) plus the 2 config rows as raw-string-unadmitted. That change is the round working, as the briefing warns.

`write_guard.py check`: silent, exit 0. Targeted suite (`test_write.py test_links.py test_write_guard.py schema_registry/`) **166 passed** in 1.60s.

## Evidence

- `[moral].md` never edited this round (its mtime 01:02:05 predates the config edit 01:02:57 and vision edit 01:04:30; sha256 `42715725…`; still `written_by: owner` only). git diff --stat was NOT run — git is forbidden to the kid (loop owns commits); the mtime/sha + audit of this round's two edit calls are the non-git proof. That is the one protocol requirement I could not literally satisfy.
- `[config].md` sha256 `22679fd9…`, `[vision].md` sha256 `e4190c9d…`, both carry the list-shaped line.
- Actual refuse message: `config nodes (config:cfg) may be hand-edited only by admitted roles owner, prime_director; resolution for actor 'sanctuary-director-4e' gave UNRESOLVED, which is not admitted. (goal:g12)` — names the TYPE and admitted roles (L4.40).
- No node files written: `config:seats`/`config:secrets` untouched (proofs used tmp fixture `config:cfg`), the 17 vision agent writers NOT backfilled (per owner: backfill at end).

## Agent Notes
Flipped written_by on [config] then [vision] to list-shaped [owner, prime_director], moral untouched; the belam prime passes and sanctuary-director/agent-id refuse with type+roles named; hypothesis stays ungated; moral owner-only preserved; links.py roles 1->3 declared, names exactly 17 agent vision writers; 166 targeted tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review by parent a00-dba67823 (L4.09): verified the flip in place — [config] and [vision] both carry the list-shaped line, [moral] is byte-unchanged, links.py roles reports 3 declared types with config owner,prime_director as expected. Refuse message names type + admitted roles per L4.40. Accepting the mtime/sha proof of moral byte-identity in place of git diff --stat: git is forbidden to a kid and the sha + audit trail is equivalent evidence. The push_further item (census raw-string comparison counting belam config rows as violations) is real and belongs to the next round, not this node.
<!-- THOUGHT:END -->

Parent review PASS: verdict proved upheld, evidence self-cited, no demotion. Open tail: roles census double-counts belam config rows as writer violations (raw-string vs resolved role).
