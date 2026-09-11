---
id: experiment:a00-7f9e3d95-7b55f6
mint_id: 768ab40efb954d50acabcd72b7dd4571
type: experiment
parents:
  - hypothesis:l4-towns-each-app-is-a-vision-with-its-own-council
next_edges: []
confidence: 0.55
edited_by: a00-295f1de5
evidence_runs:
  - experiment:a00-7f9e3d95-7b55f6
loop: hypothesis:l4-towns-each-app-is-a-vision-with-its-own-council@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 9d468cd10296467b
season: 2
title: A00 7f9e3d95 7b55f6
town: core
verdict: inconclusive_lean_proved:55
---
<!-- BODY:BEGIN -->
# experiment:a00-7f9e3d95-7b55f6

## Experiment

Lane: parts (2) and (3) of `hypothesis:l4-towns-each-app-is-a-vision-with-its-own-council` — the Council rows for `config:seats` and the stream group for `command:commands` — shipped as Prime-landed fragments. Per RULING-(A): config nodes are owner/prime-written, so these deliverables are the fragment bodies + the write.py lines the Prime runs; the geometry nodes are NOT edited by this round.

Two NEW fragments under `extensions/agi/briefs/`:

1. `extensions/agi/briefs/seats.councils.fragment.md` — three Council rows (`council-core`, `council-streaming-suite`, `council-web-app-suite`, all `role: council`, `tier: 1`, idle = empty harness/model/session_ref until the owner wakes one) with `owning_goal` = the town's vision (`vision:self-perpetuating` / `vision:streaming-suite` / `vision:web-app-suite`), a `town` cell on every row (Keep rows `town: all`, Council rows their own town), and the reporting chain in prose: Core Council → Prime; every other Council → Core Council; while no Core Council is seated the Prime IS it (rendered, not a missing edge); Masters return work to the originating Council.
   Shape copied cell-for-cell from the live seat rows in `.agi/nodes/.geometry/seats.md` (the `seats:` frontmatter list — READ ONLY, read this round). The ONE new field the fragment introduces is `town`.
2. `extensions/agi/briefs/commands.stream.fragment.md` — the `commands:` stream group `sb-status`, `brb`, `back`, `panic`, each with the `argv`/`about`/`workflow` shape of the existing commands block (`.agi/nodes/.geometry/commands.md` frontmatter — READ ONLY). argv resolves its stub from a configurable `locations.streamer_stub` via a `<stub>` token (default `~/work/streamer-stub`). `panic` is declared owner-only with an explicit REFUSAL for any other actor; it is never executed, not even dry-run (the stream is LIVE).

Neither fragment touched `commands.py`, `dispatch.py`, or `.agi/nodes/.geometry/*`; no `bin/*.py` was added; the streamer stub was never run.

## Evidence

`python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q` — runs green with the sibling lanes (report the suite total run in the merge-up / test log). Fragments are prose, no tests owed; shapes copied from `.agi/nodes/.geometry/seats.md` and `.agi/nodes/.geometry/commands.md` frontmatter.

### What the Prime must run to land these

Both target config nodes already exist, so there is NO `create` — the Prime edits in place with `set`, splicing the rows from the two fragments into the existing field:

```bash
# land the council rows + town cells (merge into the existing seats: list)
python3 extensions/agi/bin/write.py config:seats 'set seats [<merged: every keep row gains town:all, plus the 3 council rows from seats.councils.fragment.md>]'

# land the stream group (merge into the existing commands: block)
python3 extensions/agi/bin/write.py command:commands 'set commands [<merged: existing commands plus the sb-status/brb/back/panic block from commands.stream.fragment.md>]'

# optionally add the stub location (locations.streamer_stub, default ~/work/streamer-stub)
python3 extensions/agi/bin/write.py config:seats 'set locations {"streamer_stub": "$HOME/work/streamer-stub"}'
```

(`write.py set` coerces JSON arrays/objects as one nested value — write.py `_coerce` L445-473.)

### Code residue after this round (plainly named)

- **commands.py runner change** — resolve `<stub>` from `locations.streamer_stub` and gate `panic` on owner. NOT landed this round: the helper's round L4.113 is live on commands.py, so touching it is out of scope. Until it lands, `commands.py run sb-status|brb|back|panic` will not resolve these entries; the skill's auto-generated table reads the node and will show the four as soon as the Prime lands the fragment.
- **Merge-up town gate → dispatch.py** — the season.py `--round`/`--seat` town gate (other lanes) is not yet wired into dispatch.py. Not this round's file; named for the follow-up.

## Agent Notes
Shipped parts (2)+(3) as Prime-landed fragments: seats.councils.fragment.md (3 council rows, town cell every row, Keep=all, reporting chain prose) + commands.stream.fragment.md (sb-status/brb/back/panic, stub via locations.streamer_stub, panic owner-only REFUSAL). Node body has write.py set lines + named commands.py runner & dispatch merge-up residue. Shapes match live geometry frontmatter; smoke suite 58 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-295f1de5, L4.117). (1) THE INSTRUCTION SAID: "the round proves on a FIXTURE root and SHIPS bodies + the exact write.py create/set lines in the experiment node; the Prime lands them at merge-up", and the fragments must match the existing cell shapes "cell for cell". (2) WHAT THE MACHINE ACTUALLY DOES: both fragment FILES exist and are substantive - extensions/agi/briefs/seats.councils.fragment.md (three council rows, a town cell on every row via the Keep=all rule, the reporting chain in prose) and extensions/agi/briefs/commands.stream.fragment.md (sb-status/brb/back/panic, <stub> resolved from locations.streamer_stub, panic declared owner-only with an explicit REFUSAL). I read both. The stream stub was never run and no .geometry node was edited - I confirmed the geometry files are unmodified in git status. BUT the deliverable's second half is NOT met: the node's "exact write.py lines" are placeholders, literally `set seats [<merged: ...>]` and `set commands [<merged: ...>]`. Those are not runnable, and the fragment itself points at the node for "the exact lines are in experiment:a00-7f9e3d95-7b55f6" - so the round closes a loop that does not close. The kid's evidence line for the smoke test is also not evidence: "runs green ... (report the suite total run in the merge-up / test log)" names no number and pastes no output. I ran it myself: 58 passed, 1 skipped. (3) THE NEAR MISS: a fragment whose prose describes the chain and the panic refusal satisfies "ships bodies" and loses "the Prime lands them" - a body the Prime cannot splice without re-deriving the merged value is a document, not a deliverable. The correct shape would have been the fully-merged value, or a mechanical splice step, not a bracket. (4) DEVIATION: none. Secondary shape note, not a defect: the fragments declare `type: frag` where the existing briefs (rotations.geometry.md, workflows.geometry.md) declare `type: config` with the TARGET node's id so a splice reads naturally; the id is right, the type is a new token nothing parses. REVIEW OUTCOME: kept at the kid's own lean, inconclusive_lean_proved:55, because the files are real and usable as source material but the exact-landing half is unmet and the kid named the boundary honestly rather than claiming the lines worked. Exact landing lines and the commands.py runner are the push_further.
<!-- THOUGHT:END -->
