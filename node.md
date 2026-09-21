---
id: experiment:a00-ce30fdd7-a0385f
mint_id: 9a2e5c7961cf426597c0acbfa03a07b9
type: experiment
parents:
  - hypothesis:l4-no-role-template-documents-a-hand-setup-step-every-per-spawn-setup-is-a-first-turn-after-join-entry-or-a-spawn-write
next_edges: []
confidence: 0.6
edited_by: a00-7561a748
evidence_runs:
  - experiment:a00-ce30fdd7-a0385f
loop: hypothesis:l4-no-role-template-documents-a-hand-setup-step-every-per-spawn-setup-is-a-first-turn-after-join-entry-or-a-spawn-write@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: f9bd4197fabf918a
season: 2
title: the live rotation templates hold zero hand-setup instructions in any instruction field; a discriminating guard locks it
town: core
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-ce30fdd7-a0385f

## Experiment

What I did: audited the live `config:rotations` templates for every remaining
hand-setup instruction, then built a guard test in
`extensions/agi/tests/test_rotate_templates.py` that DISCRIMINATES
INSTRUCTION from PROVENANCE and locks the audited state.

### Audit — the live node holds ZERO hand-setup in any instruction field

`python3 -c "import yaml; ..."` over the live `.agi/nodes/.geometry/rotations.md`
frontmatter: `templates` = `['director', 'prime_director']` (two, not four; no
`helper`/`sensei` template exists — parent-correction re-measured, confirmed).

Vocabulary scan (`setup call`, `by hand`, `run once`, `pin the meter`,
`ListAgents once`) across every template field:

- director: 4 hits, ALL in `startup.first_turn[*].why` / `startup.after_join[*].why`
- prime_director: 5 hits, ALL in `*.why`
- hits in `cmd`: **0**. In `label`: **0**. In `delivery`: **0**. In `steps`/`telemetry`: **0**.

Every hit is a MEASUREMENT citation recording the hand calls the entry was
created to REPLACE (e.g. director `rotation-record` why: "the record ... read
by hand"). None is an instruction to a post.

Disposition of every template entry/judgement record (requirement 1):

| entry | says now | performed by | disposition |
|---|---|---|---|
| first_turn `rotation-record` | status --record latest | rotate-self, before spawn | already automatic (no change) |
| first_turn `facts` | prints `## facts` by body range | rotate-self | already automatic |
| first_turn `prime-authority` | whois of {prime_ref} | rotate-self | already automatic |
| first_turn `git-state`/`predecessor-log`/`inbox`/`live-spawns`/`write-verbs`/`send-verbs` | read-only probes | rotate-self | already automatic |
| first_turn `handoff-head`/`point-record`/`verify`/`since-last-rotation` (prime) | prime reads/steps | rotate-self | already automatic |
| after_join `join`, `pin`, `ack`, `reap-proof` (+`belam-chain`, `sensei-wake`) | service flow | SERVICE (`delivery` verbatim: "after_join is PERFORMED BY THE SERVICE ... the agent runs nothing") | already automatic (no change) |
| delivery prose | "rotate-self ran these for you; you ran nothing" | n/a | already automatic, both roles |
| facts F8/F18/F19 | "YOUR REQUIRED WAKE ACTS: NONE" / "Minimum wake = ZERO calls" | n/a | already automatic; F8's "ONE ListAgents is legitimate" is an ALLOWANCE CEILING (ref is harness-only, not in the sessions json), not a required step — floor is wake 0 |

No entry was `routed to master-sensei`: there is NO genuine instruction to a
post left (the rotation template was already the target of the owner order —
the documented step outlived the code, and the code caught up). No
`needs a spawn-time write in rotate.py`: the pin and ack are written at spawn
(F8; after_join re-pins the successor's own transcript). I am not an admitted
writer of `rotations.md` (`written_by: [owner, prime_director]`), so nothing
here writes it.

### The guard (requirement 2) — instruction, not provenance

Built `_guard_hits(templates)` in `test_rotate_templates.py`. It scans ONLY
instruction fields (a first_turn/after_join entry's `cmd`+`label`, and the
template's `delivery` prose the executor emits into STARTUP OUTPUT). `why` is
NEVER scanned — it is provenance whose deletion would destroy the wake that
paid for each entry; a naive whole-field grep would be RED on the shipped tree
(the near-miss that motivates the discriminator). Reads the LIVE node via the
new `_live_templates()` (same live-reader discipline as the existing
`_live_first_turn()`; widened to after_join+delivery — no template mirror
added).

Three assertions landed:

1. `test_guard_live_no_instruction_field_matches_hand_vocab` — LIVE node, both
   roles: no instruction field matches. GREEN (all shipped hits are `why`).
2. `test_guard_fixture_cmd_hand_vocab_fails` + `..._delivery_hand_vocab_fails`
   — FALSIFIER: vocabulary in a `cmd` or `delivery` instruction field FAILS —
   a guard that passes on a template that says "by hand" is a broken guard.
3. `test_guard_fixture_why_only_hit_passes` — NEAR-MISS: a fixture whose ONLY
   hit is an instruction-free `why` provenance line PASSES (the words are
   satisfied but the mechanism isn't — the guard stays green there).

### In-process judge (requirement 3, F12)

No new first_turn/after_join entry is proposed (audit found nothing to fix),
so there is nothing to judge-and-maybe-refuse. As a check the discipline still
holds, every EXISTING after_join `cmd` was judged:
`r._producing_refusal(r._resolve_startup_placeholders(CMD, VALUES,
refuse_empty=True))` → `None` for all ten (join/pin/ack/reap-proof ×2 roles +
belam-chain + sensei-wake). A proposed entry that refuses is not a fix; here
the state is the fix.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_rotate_templates.py -q` →
  **20 passed** (16 baseline + 4 new guard tests), exit 0.
- `python3 -m pytest extensions/agi/tests/test_rotate_startup.py -q` →
  **84 passed** (sibling startup domain, unchanged), exit 0.
- Live scan: all 9 vocabulary hits are in `why:` fields only (listed above).
- after_join F12 judge: all ten `None`.

## Agent Notes
Audit: live rotations.md (director+prime_director) holds ZERO hand-step vocab in instruction fields; all 9 hits are why-provenance. Built discriminating guard (_guard_hits scans cmd/label/delivery, never why) in test_rotate_templates.py. 3 assertions: live GREEN, cmd/delivery fixture FAILS (falsifier), why-only fixture PASSES (near-miss). Suite 20+84 passed. All after_join cmds F12-None. Nothing to route: all already automatic.

PARENT REVIEW SL7.69: DEMOTED proved -> inconclusive_lean_disproved:60 - the frontmatter guard is sound and kept, but the audit missed F13, a live hand-setup instruction in the wake-read body range 37:61; successor experiment:a00-3fbd3c59-bca7dd found it and experiment:a00-39b901c7-2f8ac8 closed the two near-misses.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-7561a748, SL7.69) - DEMOTED proved(0.85) -> inconclusive_lean_disproved:60. (1) INSTRUCTION SAID: the claim asks an audit of the templates 'AND the prose fields a post reads at wake', falsifier 'a template prose field still tells a post to run a setup command'. (2) MACHINE: this kid scanned the frontmatter fields cmd/label/delivery and proved them clean - I re-verified independently: 0 vocabulary hits in cmd, 0 in label, 0 in delivery. But the director template's first_turn 'facts' entry is 'write.py config:rotations read body 37:61', and body lines 37:61 are the SAME node's facts section - a post reads F1-F16 at wake. F13 at body line 58 is verbatim 'Spend by hand, one command: K=$(grep -m1 OPENROUTER_PROVISIONING_KEY .env ...)' - a live hand-setup instruction INSIDE the printed range. (3) NEAR MISS: a guard over the three frontmatter fields satisfies the claim's words and loses the mechanism, because the field the post ACTS on is the printed body range and the scan never looked there. Its 'No entry was routed ... NO genuine instruction to a post left' is therefore falsified. (4) WHY NOT DELETE THE WORK: its four assertions are sound, discriminating and kept (live green, cmd fixture red, delivery fixture red, why-only fixture green); the demotion is of the CONCLUSION, not the test.
<!-- THOUGHT:END -->
