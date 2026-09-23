---
id: experiment:cold-seat-briefs-name-all-five-routes
mint_id: 69ab123e01b0476d81c22df827b86573
type: experiment
parents:
  - hypothesis:a00-49362182-1cf2fb
next_edges: []
edited_by: a00-a3044689
evidence_runs: experiment:cold-seat-briefs-name-all-five-routes
line_ceiling: 40
loop: goal:g7.31.3.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 5a6ab9f155457afd
season: 2
title: Five pane routes named across three cold-seat director surfaces
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:cold-seat-briefs-name-all-five-routes

## Falsifier answer

**Falsifier (`goal:g7.31.3.1`):** a cold-seat brief / custom-instruction surface
lists the five pane-facing routes by the `goal:g7.31.3` table names
(write / read / send / dispatch|workflow / rotate|spawn) or records a
deliberate rename.

**Answer: PROVED.** Three canonical seat surfaces carry all five names; two of
them spell all five exactly as the table does.

## Command transcript

```
$ grep -n 'routes' extensions/agi/briefs/director-belam-duties.md \
    .agi/nodes/doc/unified-director-brief.md .agi/nodes/doc/director-grok-internals.md \
    extensions/agi/briefs/prime-director-successor.md extensions/agi/briefs/master-sensei-duties.md \
    extensions/agi/briefs/sensei-director-duties.md extensions/agi/lib/agent-prompt.md extensions/agi/bin/brief.py
extensions/agi/briefs/director-belam-duties.md:14:routes: write·read·send·dispatch/workflow·rotate/spawn
.agi/nodes/doc/unified-director-brief.md:36:routes write·read·send·dispatch/workflow·rotate/spawn
.agi/nodes/doc/director-grok-internals.md:152:routes: write.py · read · send · dispatch/workflow · rotate/spawn
.agi/nodes/doc/director-grok-internals.md:153:  (engine routes wording — prefer named CLIs / write.py route over raw tools)
extensions/agi/bin/brief.py:64:#: every call path routes through it, so the two cannot drift.   # unrelated prose
extensions/agi/briefs/master-sensei-duties.md:48:  touches a source file — routes to that director-kid instead.   # unrelated prose

$ grep -rn 'read\.py' extensions/agi/briefs/ .agi/nodes/doc/director-grok-internals.md extensions/agi/lib/agent-prompt.md
(no output)

$ grep -rn -iE 'sixth route|special .* route|grok route' extensions/agi/briefs/ .agi/nodes/doc/
(no output)
```

## Surface x five names

| surface | write | read | send | dispatch/workflow | rotate/spawn | handed to a cold seat? |
|---|---|---|---|---|---|---|
| `extensions/agi/briefs/director-belam-duties.md:14` | yes | yes | yes | yes | yes | YES — role file; every director card's first line points here (`.agi/sessions/quorum/director-belam.md:1`) |
| `.agi/nodes/doc/unified-director-brief.md:36` | yes | yes | yes | yes | yes | YES — "the ROLE every director runs", read whole once per generation |
| `.agi/nodes/doc/director-grok-internals.md:152` | `write.py` | yes | yes | yes | yes | YES — inside `### SECTION:PROFILE` (starts L55, ends L190), copied into the bot agent description by `SECTION:ROUTINE_SYNC` |
| `extensions/agi/lib/agent-prompt.md` (pi cold-seat prompt) | no | no | no | no | no | surface IS a cold-seat prompt; carries no route list |
| `extensions/agi/bin/brief.py` | no | no | no | no | no | assembled briefs carry no route list |
| `.agi/nodes/doc/standing-llm-ops.md` | — | — | — | — | — | RETIRED to a stub 2026-09-22; §4 is gone |

## Adversarial findings

1. **Sixth route / missing name:** none. Only three surfaces emit a
   `routes…` line, each with all five names; no surface names a route outside
   the table (third grep empty). The other `routes` hits are unrelated prose
   (`brief.py:64`, `master-sensei-duties.md:48`).
2. **Name drift:** `doc:director-grok-internals:152` spells the first route
   `write.py` (the engine seam) rather than `write` (the route). It still
   resolves to the named seam — its own L153 annotation says "prefer named
   CLIs / write.py route over raw tools". No surface claims a `read.py` file
   (second grep empty); `read` stays bare, matching the table's "not a
   separate read.py". `dispatch/workflow` and `rotate/spawn` are kept as
   slash-pairs — one route each, never split into four.
3. **Section boundary:** the grok-internals listing sits in
   `### SECTION:PROFILE` (L55, closed by the `---` at L191), and
   `doc:grok-harness-internals-sync` `SECTION:ROUTINE_SYNC` maps
   "SECTION:PROFILE -> profile description". So the listing reaches a seat;
   it is not dead prose.
4. **Should-carry-and-does-not:** two.
   - `extensions/agi/lib/agent-prompt.md` (the pi cold-seat prompt) carries
     no five-route list.
   - `doc:standing-llm-ops` — cited by `goal:g7.31.3` as the §4 source — was
     **folded to a stub on 2026-09-22** (`standing-llm-ops.md:19`,
     "Runtime spine RETIRED … directors -> `doc:director-grok-internals`"), so
     the parent's citation now resolves to a pointer, not a source.
   **No fix made**, per the order: at least one canonical cold-seat surface
   already carries all five, so the falsifier stands without an edit. The pi
   prompt is a different harness where raw tools are the contract, and the
   `standing-llm-ops` stub still resolves inbound links.

## Verdict

**proved.** `extensions/agi/briefs/director-belam-duties.md:14`,
`doc:unified-director-brief.md:36` and `doc:director-grok-internals.md:152`
(a `SECTION:PROFILE` line pasted into the bot's custom instructions) each name
all five routes; no sixth route exists anywhere in the surface set.
Production lines: 0 (node-only round).

## Agent Notes
Parent probes (a00-a3044689, DH.142): gate sixth-route grep of dispatch.py/rotate.py empty; gate all three routes lines parse complete (write/read/send/dispatch+workflow/rotate+spawn); wire director-belam card L1 points at the duties brief and grok-internals:152 sits inside SECTION:PROFILE. ACCEPT proved.
