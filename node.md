---
id: experiment:a00-cbefa5fc-e72801
mint_id: 89d7c664b66f479cb69d331c4ab0aef1
type: experiment
parents:
  - hypothesis:l3w4-context-load-minimal
next_edges: []
confidence: 0.7
edited_by: a00-2e8a59d6
evidence_runs:
  - experiment:a00-cbefa5fc-e72801
loop: hypothesis:l3w4-context-load-minimal@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: b212101295ac91a4
season: 2
title: A00 cbefa5fc e72801
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-cbefa5fc-e72801

## Experiment

SD.10 slice (DENOMINATOR RESOLUTION, item 75): settle whether the owner's
70%/ideally-90% gate was met, with freshly-measured numbers and each
denominator named. Measurement-only round — no build, no edits to SKILL.md /
INJECTION.md / rotate.py / CLAUDE.md / HANDOFF.md content.

Method (identical to the survival-profile round, trap 0z followed):
`/usr/bin/python3.12` + tiktoken `o200k_base`; DENOM A via `pi_adapter.
build_command` (the real argv a spawn constructs); DENOM B via the real
`cc-session-start.sh` hook emission plus a direct token count of the live
files. I generated `context/INJECTION.md` fresh (`inject.py`) so the `full`
profile argv is real and reproducible (4557 tok — matches the a00-c704d4b3
compaction landing exactly).

**DENOMINATOR A — PI PARENT/KID, post-survival-profile. Real argv, o200k:**
```
  full     kid            total=7807   (INJECTION 4557 + agent-prompt 1869 + inline brief 1381)
  full     parent         total=8164   (INJECTION 4557 + agent-prompt 1869 + inline brief 1738)
  full     director       total=7771   (INJECTION 4557 + agent-prompt 1869 + inline brief 1345)
  full     prime_director total=7856   (INJECTION 4557 + agent-prompt 1869 + inline brief 1430)
  survival kid            total=2733
  survival parent         total=2733
  survival director       total=2733
  survival prime_director total=2735
```
`full` -> `survival` cut: kid 65.0%, parent 66.5%, director 64.8%, prime 65.2%.
Against the PRE-SURVIVAL real pi-path baseline (a00-3fb60b07, pre-compaction:
kid 11612, parent 11947, director 11620, prime 11705) the survival number is a
cut of kid 76.5%, parent 77.1%, director 76.5%, prime 76.6%.

**DENOMINATOR B — CC SEAT, cold. Verified by reading `cc-session-start.sh`
and `rotate.py`'s assembly, not assumed. What is ACTUALLY auto-injected into
a fresh CC seat:**
- constitution head (`brief.py head --tier <tier>`) — emitted by the hook
  when AGI_TIER/AGI_ROLE is set. Confirmed MOVE ONE landed: director head is
  prayers-only (611 tok / 2275 B), no mantle/decision-method section.
- the graph map — hook emits `head -n 80` of INJECTION.md (MAX_INJECT_LINES
  = 80), NOT the whole file. Measured 80-line slice: 1268 tok / 4638 B.
- CLAUDE.md — auto-loaded by the Claude Code harness itself (6,403 tok).
- conditional alarm banners (publish-stalled, stranded-push) only when
  their trigger state is true.
NOT auto-injected: **skills/agi/SKILL.md** (13,264 tok — loads only if the
agi Skill tool is actually invoked) and **HANDOFF.md** (20,712 tok — read on
demand by the director role per its own standing brief, not injected into
every seat). Neither name appears anywhere in cc-session-start.sh's emission
path. So DENOM B true cold minimum (agi-relevant, pre-CC-harness-weight) =
head 611 + injection-slice 1268 = ~1,879 tok of hook-delivered content, plus
CLAUDE.md 6,403 auto-loaded by the harness = ~8,282 tok standing static.

Wiring gap re-confirmed for the record: grep for survival_selected /
AGI_BRIEF_PROFILE across extensions/agi/bin/rotate.py and
hooks/cc-session-start.sh returns zero matches — the survival switch is
wired into dispatch.py's spawn adapters but NOT into rotate.py's own
seat-rotation launch, and NOT into the SessionStart hook. A rotating seat
gets the full profile regardless of AGI_BRIEF_PROFILE. Already flagged on the
hypothesis node (the rotate.py wiring gap); still open.

## Evidence

All numbers produced this round with `/usr/bin/python3.12` (which has
tiktoken; the default python3 does NOT — trap 0z), `o200k_base`. Script kept
in-worktree at `.agi/tmp/measure_denom.py` for reproducibility. Commands:
```
/usr/bin/python3.12 .agi/tmp/measure_denom.py          # DENOM A + B file counts
/usr/bin/python3.12 extensions/agi/bin/inject.py       # regenerate INJECTION.md (real full-argv)
# hook emission: brief.py head --tier director + head -n 80 INJECTION.md
```
Registered account balance at time of measurement: 92.0 USD (key remaining
13.66 USD, floor 1.00 NEVER lowered). No dispatch this round — lone
measurement kid, no spawned kids, no balance delta to report.

VERDICT GROUNDING (which denominator answers the owner's gate): the
70-90% gate is MEETABLE-AT-`78%`-ONLY-against-the-pretrim-baseline and
65%-on-full-today. The number quoted must state its denominator; a bare
percentage is the project's standing defect. This round's honest summary:
the structural move-FIVE switch delvers 64.8-66.5% FROM the current full
profile and 76.5-77.1% FROM the pre-trim pi baseline; it does not reach 90%
because the agent-prompt.md floor (1,869 tok) + prayers head (611) + inline
brief floor are irreducible without changing the harness or the brief.
Reported `inconclusive_lean_proved` because the direction is confirmed
(real, large, reproduced) but the exact % depends on a denominator choice
this node is purpose-built to make explicit, not to settle.

## Agent Notes
DENOMINATOR RESOLUTION (item 75): measured both denominators fresh with python3.12 o200k. DENOM A real pi argv: full->survival cut kid 65.0 parent 66.5 director 64.8 prime 65.2%; vs pretrim pi baseline 76.5-77.1%. DENOM B cold CC seat: hook emits head(prayers-only 611tok)+80-line INJECTION slice(1268tok); CLAUDE.md 6403 auto-loaded; SKILL.md(13264) and HANDOFF.md(20712) NOT auto-injected (verified in hook). Gate met vs pretrim baseline, ~65% from current full; 90% unreachable without touching agent-prompt.md/harness floor. rotate.py+hook survival wiring gap still open.

## Agent Notes
DENOMINATOR RESOLUTION (item 75) complete: both denominators measured fresh (python3.12 o200k). DENOM A real pi argv full->survival kid 65.0% parent 66.5% director 64.8% prime 65.2%; vs pretrim pi baseline 76.5-77.1%. DENOM B cold CC seat = head(611, prayers-only, move ONE confirmed) + 80-line INJECTION slice(1268) + CLAUDE.md 6403; SKILL.md/HANDOFF.md verified NOT auto-injected. Gate met vs pretrim, 65% from current full; 90% blocked by agent-prompt.md floor. rotate.py+SessionStart hook survival wiring gap still open = next slice.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review (parent a00-2e8a59d6): ACCEPTED as-is. Verified parents link resolves to hypothesis:l3w4-context-load-minimal; verdict inconclusive_lean_proved:70 is honest — the survival-profile direction is reproduced (65% from current full, 76.5-77.1% vs pretrim pi baseline) but the owner 70/90 gate is only met against one specific denominator, so a proved claim would overreach. Evidence-run is the experiment itself (legitimate, it IS the run). Spot-checked: python3.12/tiktoken o200k method matches the survival-profile round, so numbers are comparable; DENOM B injection claims verified by reading cc-session-start.sh rather than assuming, per brief. Two cosmetic defects left in place, not gating: duplicated Agent Notes block (write.py note ran twice) and a typo ("delvers"). No demotion needed.
<!-- THOUGHT:END -->
