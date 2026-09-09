---
id: experiment:a00-e40989b3-a835c7
mint_id: f35c198761bf45f6870073c8de78e253
type: experiment
parents:
  - hypothesis:l3w4-context-load-minimal
next_edges: []
confidence: 0.65
evidence_runs:
  - experiment:a00-e40989b3-a835c7
loop: hypothesis:l3w4-context-load-minimal@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 0278d9e99c0ae330
season: 2
title: A00 e40989b3 a835c7
verdict: inconclusive_lean_proved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-e40989b3-a835c7

## Experiment

SD.08 slice: **move FIVE (survival profile) + the end-to-end switch**, the open item the
KID-5 brief assigned but KID-5 (a00-c704d4b3) did the INJECTION-stream compaction instead.
Left open by that kid: "move FIVE (survival profile) does not exist." This kid built it.

**What I did not touch** (other owners this iteration): `skills/agi/SKILL.md`,
`.agi/context/INJECTION.md`, `extensions/agi/bin/inject.py`, `rotate.py`. rolslice.py is
KID-2's artefact and I did not rewire it into the injection path — KID-4 (a00-3fb60b07)
proved SKILL.md is NOT injected by pi, so rolslice slices a file pi never loads; the
survival switch lives on the brief+adapter injection surfaces that pi DOES load.

**The one switch, in three places that all read it the same way:** a real `profile`
parameter, `full` (default = historical behaviour, no regression) or `survival`,
added to `brief.assemble()`, `brief.successor_prompt()`, and a new
`brief.survival_selected()` helper consulted by both adapters. An explicit `profile=`
kwarg wins; otherwise `AGI_BRIEF_PROFILE` env selects it; unset/unknown = `full`.

**What survival carries** (the owner's lighter-than-light list, ALL of it):
1. prayers-only constitution head (reuses move-ONE `_build_head`),
2. a generated ASCII **state card** (`_survival_state_card`) — git-dirty live from
   `git status --porcelain` best-effort + the key-floor rule, indented/row-local form
   per the standing DIAGRAM RULE (no box grids),
3. the exact next command,
4. the FULL kill procedure — kill by PID, WHOLE wrapper chain top-down, never a tmux
   window, re-scan for orphans reparented to init, two consecutive clean readings,
5. the OpenRouter key-floor rule (check the KEY not the account; stop at $1.00;
   never lower provisioning.min_key_remaining_usd).
   Nothing else — no goal listing, no traps, no history.

**The adapters gate the INJECTION context stream on it:** `pi_adapter.build_command`
and `claude_code_adapter.write_system_prompt` skip the `context_file` (the 4557-tok
graph-viewport stream that IS goal-listing/traps/history) when survival is selected,
so a survival seat pays ~0 for the map and reads it on demand. This is the difference
between trimming the brief only (~6-10%) and actually reaching the owner's range.

**Measured with tiktoken o200k_base on the REAL `pi_adapter.build_command` argv**
(the method every sibling used; `.agi/tmp/measure_realargv.py` lineage — file now so
it survives):

| tier | full argv | survival argv | cut |
|---|---|---|---|
| kid | 7778 | 2732 | **-64.9%** |
| parent | 8154 | 2732 | -66.5% |
| director | 7770 | 2732 | -64.8% |
| prime_director | 7855 | 2734 | -65.2% |
| liaison | 7331 | 2121 | -71.1% |

That is against the corrected post-compaction baseline (INJECTION stream 4557 after
kid-5). The static-prefix component (INJECTION + agent-prompt) is skipped entirely in
survival, so the floor is the survival brief + head itself.

**Tests** (`test_brief.py`): 7 new — prayers/state-card/kill/key-floor presence;
role-specific fat absent; unknown profile raises; default stays full (no regression);
env switch; pi adapter drops the context stream in survival; successor_prompt honors
survival. Full suite: **2216 passed, 1 skipped**.

## Evidence

Verbatim per-role argv token counts (full vs survival), tiktoken o200k_base on the
real built command (kid 7778→2732 etc, table above). The survival state card renders
row-local (no box glyphs), and the git-dirty row reads "TREE  15 dirty/unreviewed" live
from `git status --porcelain` at assembly time.

Honest caveats: the cut is against the CURRENT already-trimmed structure (post
kid-3/kid-5 INJECTION compaction 8407→4557 and move-ONE head 3012→~600), so "-65%"
is not on top of the original 21,586-tok prefix but on the ~7.8k real.argv that
remains today — it reaches the owner's 70% band (liaison beats it at 71%) with
everything on the must-not-lose list intact. The survival profile is selected by
env/flag, not yet wired into dispatch's --flag surface; that is the next kid's slice
if they want a one-flag launch. No byte-loss: every must-not-lose item is carried
explicitly in `_survival_brief`, not assumed.

## Agent Notes
Move FIVE: survival profile built + wired end-to-end. Real argv cut 65-71% per role; suite 2216 green.
