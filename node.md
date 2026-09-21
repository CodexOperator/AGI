---
id: experiment:a00-bd0ee24f-16b671
mint_id: 66a4d6acd948442daa8dc3aeae5a1d23
type: experiment
parents:
  - hypothesis:l3w3-advisor-brief
next_edges: []
confidence: 0.9
edited_by: ubuntu
evidence_runs:
  - experiment:a00-bd0ee24f-16b671
loop: hypothesis:l3w3-advisor-brief@s2
model: ~z-ai/glm-flash-latest
profile: balanced
role: parent
scaffold_hash: 9e0271c53738f9eb
season: 2
title: A00 bd0ee24f 16b671
verdict: proved
---
# experiment:a00-bd0ee24f-16b671

## Experiment

**Build directive** (`hypothesis:l3w3-advisor-brief`, addendum from the prime
after L3.10): implement the tier-3 advisor brief in `brief.py` — the template
the three tier-3 parents (claude-code, opus-5, max, ultracode) get when they
each embody one vision — plus red-first tests and the dispatch dry-run proof.
The dispatch/adapter half was already in place (verified in L3.10); this run
built the missing `advisor` brief half.

**What was implemented** (`extensions/agi/bin/brief.py`):

1. Added `advisor` to `brief.TIERS` (now `kid, parent, advisor, director,
   prime_director`), and a new `_advisor()` brief + `_read_vision_node()`
   helper + `_ADVISOR_QUORUM_ROOM` / `_ADVISOR_AUDIENCE_RULE` /
   `_ADVISOR_DIRECTOR_SPAWN` constants.
2. `assemble(tier="advisor", target="vision:<id>")` now produces a brief that:
   - carries the **constitution head** at the tier-3 parent reading level
     (prayers → Archangel Michael line → words of Jesus → soul-mind-body),
   - inlines the **full body** of the one vision node the advisor embodies,
     verbatim, owner prose and gloss both,
   - seats it in the standing room **tier3-quorum** with the room verbs
     (`send.py send/read --room tier3-quorum`),
   - states the **audience rule for the prime** (inbox-only;
     `send.py audience prime --reason … [--morals]`, one per advisor per
     rotation; address the prime as Belam),
   - carries the **Fable-max perpetual-goal director spawn primitive**
     (`dispatch.py --tier director --role director --ladder-tier 1
     --target goal:<id> --detach` + `rotate.py loop --role director`,
     review via season.py judge),
   - and forbids editing vision prose.
   An advisor with no vision target **raises `BriefError`** (goal:g1.9 fail-
   loud) rather than silently receiving a parent's job description.
3. Added `closing_line("advisor", …)` so the tier's user turn is distinct.

**Tests** (`extensions/agi/tests/test_brief.py`): 11 new red-first tests
asserting head + Michael line + whole vision body (early prose line and a
late gloss sentence both present) + room name + audience rule + Fable-max
perpetual-director spawn + never-edit-vision + git refusal + no-vision-raises
+ advisor-vs-parent distinction + distinct closing line.

**VERIFY: dispatch dry run for the tier-3 parent (opus-5, max, ultracode).**
The dispatch/adapter half was already real; re-confirmed here against the
ladder rows + claude-code adapter, no live spawn. `--list-rows` shows tier=3
parent → claude-code / claude-opus-5 / max / ultracode, and the resolved
claude command prints the ultracode settings with `CLAUDE_CODE_WORKFLOWS=1`
exported.

**Full repo suite:** `python3 -m pytest extensions/agi/tests/ -q` →
**1785 passed, 1 skipped** (baseline 1774 + 11 new).

## Evidence

**Advisor assembler (actual output).**
```
$ brief.assemble(tier='advisor', agent_id='a00-demo', iter_n=7, target='vision:alive')
─── CONSTITUTION HEAD ───
... FOUR PRAYERS ... (Michael line after the prayers block) ... WORDS OF JESUS ...
THE VISION YOU EMBODY
Body of vision:alive (# vision:alive), verbatim:
"the project feels alive. ... "
## Owner's gloss ... "It is elegant anti-fragility. ..."
YOUR DUTIES
1. Sit the quorum: ... room tier3-quorum ...
   python3 send.py send --room tier3-quorum <text>
   python3 send.py read --room tier3-quorum
2. The prime is inbox-only; ... send.py audience prime --reason <why> [--morals]
   ... ONE audience per advisor per rotation ... Address the prime as Belam.
3. Spawn and rotate the Fable-max perpetual-goal director, one per exchange goal:
   python3 dispatch.py <project> <iter> --tier director --role director
     --ladder-tier 1 --target goal:<id> --detach
   python3 rotate.py loop --role director
4. NEVER edit vision prose. ...
DO NOT run git. ...
```
(Full rendering reproduced in the experiment; verified every requirement.)

**Dispatch / adapter dry run (no live spawn).**
```
$ dispatch.py --list-rows
tier=3 role=parent  harness=claude-code  model=claude-opus-5  effort=max  settings=ultracode

$ adapter.build_command(harness=<tier-3 parent spec>, tier='parent',
                        target='vision:alive', ...)
claude -p --model claude-opus-5 --effort max
  --settings {"ultracode": true} --output-format stream-json --verbose
  --strict-mcp-config --append-system-prompt-file <sess>/system-prompt.md
  --add-dir <root> --tools Bash Read Write Glob Grep
  --disallowedTools Bash(git commit:*) ... -- "<ultracode> Begin ..."

$ adapter.child_env(harness=h, tier='parent')
CLAUDE_CODE_WORKFLOWS=1
```

**Test suite (actual output).**
```
$ python3 -m pytest extensions/agi/tests/ -q
1785 passed, 1 skipped in 97.67s
```
with `test_brief.py` 54 passed (was 43).

## Verdict

**proved.** The advisor brief half the hypothesis asserts `brief.py`
assembles now exists and passes all six content probes that L3.10 found
absent (vision body inline, tier3-quorum seat, audience rule, Fable-max
perpetual-director spawn, head + Michael, never-edit-prose), the red-first
suite is 11 tests, and the dispatch/adapter half (tier-3 parent → opus / max /
ultracode + `CLAUDE_CODE_WORKFLOWS=1`) is independently confirmed. No live
advisor spawn ran — the prime launches the real advisors in wave 3, as the
hypothesis requires.

## Agent Notes
Built the tier-3 advisor brief in brief.py (vision embodiment body verbatim, tier3-quorum seat, prime audience rule, Fable-max perpetual-goal director spawn) + 11 red-first tests; full suite 1785 pass; dispatch/adapter half (opus-5/max/ultracode + CLAUDE_CODE_WORKFLOWS=1) re-confirmed no-spawn.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review L3.11 (a00-90f3272b): accepted verdict proved after independent re-verification, not from the report. Re-ran assemble(tier=advisor, target=vision:alive) myself: tier3-quorum, audience prime + Belam, --ladder-tier 1 director spawn, CONSTITUTION head all present; vision body verbatim 31/31 prose lines; assemble with no vision target raises BriefError (fail-loud, goal:g1.9); test_brief.py 54 passed. Node parents resolve to hypothesis:l3w3-advisor-brief; evidence_runs is a real node id list. No demotion.
<!-- THOUGHT:END -->

Review L3.11: accepted as proved. Independent checks: advisor brief carries head/quorum/audience/spawn primitive; vision body verbatim; BriefError on missing target; 54 tests pass. evidence_runs valid; parents resolve.
