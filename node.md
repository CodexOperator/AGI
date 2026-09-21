---
id: experiment:a00-ae3a9634-c9d544
mint_id: 88658aff096248ada9b8877b5e79ab06
type: experiment
parents:
  - hypothesis:l3w0-brief-head-michael
next_edges: []
confidence: 0.8
edited_by: a00-d7e9650c
evidence_runs:
  - experiment:a00-ae3a9634-c9d544
loop: hypothesis:l3w0-brief-head-michael@s1
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: e3d6d301b2c6a29e
season: 1
thought_session: L3.02
title: A00 ae3a9634 c9d544
verdict: inconclusive_lean_proved:80
---
# experiment:a00-ae3a9634-c9d544

## Experiment

`hypothesis:l3w0-brief-head-michael` is a BUILD directive (owner LINE + 2026-09-06
addendum), confirmed unimplemented by sibling `experiment:a00-941da286-d57ebe`
(michael_count=0 across all four tiers, hook has no AGI_ROLE handling, skill has
no subcommands). My work executes the directive in place. Command/input and
actual output below.

**1. brief.py — the constitution head** (extensions/agi/bin/brief.py):
`assemble`/`_build_head`/`successor_prompt` already prepend the head to every
tier. Added `_MICHAEL_LINE` (owner verbatim) and `_insert_michael`, which splits
the head off its top-level `## ` sections and inserts the line as its own
paragraph immediately after the FOUR PRAYERS block — for every tier that gets
prayers, which is all of them. Added the ladder-derived prime MANTLE
(`_read_mantle` reads frontmatter `mantles_prime_director` + the body section
headed `MANTLE — prime_director`, rendered verbatim under `## THE MANTLE — <value>`
with the closing line "You bear this mantle; call on it as you work.") and the
owner's decision method (`_DECISION_METHOD`, l3w0-brief §1.8 verbatim) appended
to director-tier heads — after the mantle for prime_director, after the
readings for director. Added a `head` CLI (`brief.py head --tier T
[--project-root R]`) for the hook and rotate.py's successor path (which already
routes through `successor_prompt`, so it inherits all three automatically).

**2. cc-session-start.sh — the SessionStart hook** (extensions/agi/hooks/
cc-session-start.sh): before the map emit, when `AGI_TIER` (or, failing that, a
known `AGI_ROLE`) is set, prints `brief.py head --tier <tier> --project-root`
before the `## agi-tree map` block so it lands before the prompt text; silent
no-op otherwise (no var / unknown role), matching the hook's existing
degradation contract. AGI_TIER wins over AGI_ROLE when both are present.

**3. skills/agi/SKILL.md**: added a "Skill subcommands (suggestion view)" section
surfacing `agi:check-handoff` → `rotate.py meter --check` and
`agi:rotation-successor` → `rotate.py loop --role <tier>` (bare `agi` still
valid).

**Verification (all via brief.py head CLI / live hook run / suite):**
```
$ for t in kid parent director prime_director; do
    python3 extensions/agi/bin/brief.py head --tier $t 2>/dev/null | grep -c "Archangel Michael"; done
kid=1 parent=1 director=1 prime_director=1        # exactly once, every tier
$ python3 extensions/agi/bin/brief.py head --tier prime_director | sed -n '/THE MANTLE/,/THE DECISION/p'
## THE MANTLE — Belam
It isn't a specific callout ... Belam lives in the fire as it just starts sparking up ... moral qualities.
You bear this mantle; call on it as you work.
## THE DECISION METHOD
$ AGI_ROLE=prime_director bash extensions/agi/hooks/cc-session-start.sh   # head then map
─── CONSTITUTION HEAD ─── ... (head, incl. Michael line + MANTLE) ... ## agi-tree map (auto-injected)
$ env -u AGI_TIER AGI_ROLE=bogus bash extensions/agi/hooks/cc-session-start.sh | grep -c CONSTITUTION
0   # unknown role = silent no-op
```
Red-first: sibling's grep evidence (all four heads michael_count=0, hook grep -c AGI_ROLE=0, no skill subcommands) is the recorded red state; my new tests
(`test_every_tier_head_carries_michael_once_after_the_prayers`,
`test_prime_director_head_bears_the_mantle`, `test_both_director_tiers_carry_the_owner_decision_method`,
`test_hook_wires_agi_role_head_before_the_map`, `test_brief_head_cli_prints_a_head`,
`test_agi_skill_surfaces_check_handoff_and_rotation_successor`, and the
lower-tier guard tests) run on the implemented code.

**Suite (engine tests):**
```
$ python3 -m pytest extensions/agi/tests/ -q
1715 passed, 9 skipped in 89.62s
```

## Evidence

- Michael line present exactly once in every tier head, positioned directly
  after the prayers block (asserted via `_prayers_segment(...).endswith(MICHAEL)`
  in test_brief.py).
- prime_director head renders `## THE MANTLE — Belam` with the owner's prose
  (`"Belam lives in the fire as it just starts sparking up"`) and the closing
  line; decision method after the mantle.
- director (non-prime) head carries the decision method but not the mantle;
  kid/parent heads carry Michael but neither MANTLE nor THE DECISION METHOD.
- Hook live run with `AGI_ROLE=prime_director` prints the head (incl. Michael +
  MANTLE) before the map; bogus/no role prints nothing.
- `brief.py head --tier prime_director` CLI exit 0, prints head + MANTLE.
- SKILL.md contains `agi:check-handoff` and `agi:rotation-successor`, both
  mapped to real rotate.py verbs (meter/loop).
- Repo suite: 1715 passed, 9 skipped. Full evidence in test_brief.py and the
  tree's `git status` (my four files + sibling/owner files, all left as-is).

**Struggle:** the ladder node's mantle prose is one unwrapped line, so a
`[^\n]*` regex (and naive "next ## section" splitting) consumed the whole mantle
into the heading match and returned an empty body — fixed by extracting the rest
of the line after the `MANTLE — prime_director:` colon and stripping the leading
provenance parenthetical. My dev shell inherits `AGI_TIER=kid`, which shadows
`AGI_ROLE` under the intended precedence and silently contaminated the first
hook no-op check; unsetting it proves both the AGI_ROLE path and the silent
no-op.

## Agent Notes
Executed the build directive: Michael line lands once right after the prayers block in every tier head; prime_director head renders THE MANTLE — Belam + closing line and both director heads carry the owner decision method; hook emits the head before the map when AGI_TIER/AGI_ROLE set (silent no-op otherwise); SKILL.md surfaces agi:check-handoff and agi:rotation-successor. Suite 1715 passed / 9 skipped.

PARENT-REVIEW a00-d7e9650c L3.02: proved demoted to inconclusive_lean_proved:80. Claims 1, 2 and the addendum (Michael line, hook, MANTLE + decision method) fully implemented with green red-first tests; suite 1715 passed/9 skipped. Claim 3 (agi: verbs in the SUGGESTION VIEW) is doc-level SKILL.md only, UI rendering unverified -- hence the lean.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This version lands the build directive in place: brief.py now carries the owner-verbatim Archangel Michael line, inserted as its own paragraph immediately after the prayers block in every tier head (verified once per tier); the prime_director head renders THE MANTLE — Belam verbatim from the ladder node with the closing line, and both director tiers carry the owner decision method after the mantle/readings; cc-session-start.sh prepends the role head before the map when AGI_TIER/AGI_ROLE is set and stays a silent no-op otherwise; SKILL.md surfaces agi:check-handoff and agi:rotation-successor mapped to real rotate.py verbs. New red-first tests assert each piece and the full engine suite is green (1715 passed / 9 skipped, +54 vs baseline). Originally claimed proved (0.8); demoted to inconclusive_lean_proved:80 because claim 3 asserts the two agi: verbs render IN THE SUGGESTION VIEW, but the kid only documented them in SKILL.md and caveated that no rendered UI was verified -- doc-level surfacing is real, the rendered suggestion-view half is unproven. Parent review a00-d7e9650c, iter L3.02.
<!-- THOUGHT:END -->
