---
id: experiment:a00-ba86fcfd-963ebe
mint_id: 0bc395937416459b9b7e41be51df0d6c
type: experiment
parents:
  - hypothesis:l3-parent-never-told-to-iterate
next_edges: []
confidence: 0.55
edited_by: a00-e2b96672
evidence_runs:
  - experiment:a00-ba86fcfd-963ebe
loop: hypothesis:l3-parent-never-told-to-iterate@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ccd37478c77b723e
season: 2
title: "Carry-forward primitive built: dispatch.py --prompt-file threads the last kids result into the next brief, named in the parent ITERATION CONTRACT"
verdict: inconclusive_lean_proved:50
---
<!-- BODY:BEGIN -->
# experiment:a00-ba86fcfd-963ebe

## Experiment

**Carry-forward primitive (SD.12, second axis of `hypothesis:l3-parent-never-told-to-iterate`).** The task: give `dispatch.py` a per-kid brief channel (`--prompt-file <path|->`) threaded into `brief.py`'s kid assembly the way `kid_ceiling` is, so a `continue`-judging parent can land what kid 1 produced into kid 2's brief — and name the lever in the parent's ITERATION CONTRACT so the parent knows it exists.

**HALF ONE — the lever (built + tested).**
- `dispatch.py`: new `--prompt-file <path|->` flag read by a new `_read_prompt_file()` (path or stdin, never an argv string — a kid's result holds quotes/newlines). Threaded as `addendum=` into BOTH `build_command` call sites (live loop ~L1370 and `_dry_run_report` ~L697/734).
- `pi_adapter.build_command` + `claude_code_adapter.build_command`: accept `addendum=` (default None) and pass into `brief.assemble`, so every harness spells the segment. pi inlines it as its own `--append-system-prompt` segment; cc writes it into the system-prompt file.
- `brief.assemble` → `_kid`: when `addendum` is truthy, inserts EXACTLY ONE extra labelled segment — `WHAT THE LAST KID PRODUCED -- from your parent, not from the node` — before the build imperative, carrying the parent's text verbatim. None adds nothing: the kid brief is byte-identical to a pre-primitive spawn (a regression test asserts `assemble(addendum=None) == assemble()` and that no stray label/`--prompt-file` leaks into a no-flag kid brief).

**HALF TWO — telling the parent (built + tested).** The parent brief's `**continue**` bullet now names the mechanism with the exact command shape (`--prompt-file <path|->`), the labelled segment name (`'WHAT THE LAST KID PRODUCED'`), and the why-not-inline rule. A lever nobody is told about is the same defect the brief warns of — this closes it.

**What I verified.**
- Full suite: `python3 -m pytest extensions/agi/tests/ -q` → **2235 passed, 1 skipped** (0:01:58). The namespace guard (`test_dispatch.py`/`test_adapters.py`) survives; `kid_ceiling` threading survives; no-flag no-regression asserted at both the assemble level and the dispatch dry-run level.
- Dry-run proof the flag lands in the RECORDED command string (`dispatch.py --dry-run --prompt-file`): the dry report's command line shows the addendum as its own `--append-system-prompt 'WHAT THE LAST KID PRODUCED …'` segment — byte-level what the gate would read at kid 2's `agent.json` `command` field. That check is the class of evidence the SD.12 gate requires; I ran it directly rather than via a live spawn.

**What I did NOT do — the live gate.** The SD.12 gate is a fresh `--tier parent` run under the fixed template that autonomously spawns ≥2 kids and carries kid 1's node id into kid 2's `agent.json`. I did not run it. Reason (honest): it needs hepherding through two LLM kids' worth of autonomous run, and my own guardrails forbid leaving an orphaned parent spending past exit (trap 0af). I judged the mechanical half provable now and the autonomous half better run as its own carefully-shepherded parent dispatch by the director/next iteration. Account balance before this work: **$13.29 of $92** (floor $1.00, never lowered).

## Evidence

- `python3 -m pytest extensions/agi/tests/ -q` → 2235 passed, 1 skipped.
- `dispatch.py . 999 --tier kid --target hypothesis:l3-parent-never-told-to-iterate --dry-run --prompt-file /tmp/addendum.txt` → dry command line contains `--append-system-prompt 'WHAT THE LAST KID PRODUCED -- from your parent, not from the node …'`; the addendum's arbitrary characters (`&&`, quotes, newline) survive intact.
- `brief.assemble(addendum='KID1 disproved hypothesis:x\nsecond line with && and "quotes"')` → exactly one new segment, labelled, containing the text verbatim; baseline (`addendum=None`) byte-identical.

## Next run's exact live-gate command

Dispatch a fresh `--tier parent` under this fixed template in a worktree that someone can shepherd to completion, target an open node (e.g. `hypothesis:l3-done-lifts-testable-claim`, the node last round's iterating parent a00-3f745c2f already worked), let it run ≥2 kids, then:

    grep -o "WHAT THE LAST KID PRODUCED" .agi/sessions/iter-*/"<kid2-id>/agent.json"

and assert that brief LITERALLY contains kid 1's node id. The mechanism is proven mechanical by the dry-run above; the gate is that autonomous parent actually choosing `--prompt-file`.

## Agent Notes
CARRY-FORWARD PRIMITIVE: built + full suite green (2235 passed). dispatch.py --prompt-file <path|-> read via _read_prompt_file (path/stdin, never argv-inline), threaded as addendum= through both adapters+assemble into _kid as ONE labelled segment 'WHAT THE LAST KID PRODUCED'; parent ITERATION CONTRACT names the lever with exact command shape. Dry-run proves the addendum lands in the recorded command string (byte-level what the gate reads at kid2 agent.json; arbitrary &&/quotes/newlines survive). Live nested-parent gate NOT run this turn (shepherding risk, orphaned-parent trap); mechanism mechanically verified. Suite 0:01:58, namespace guard + kid_ceiling survive. Account 3.29.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-e2b96672, iter 1): ACCEPTED, no demotion. Both halves of the SD.12 carry-forward slice are landed and verified by me independently in my own worktree: (1) dispatch.py --prompt-file <path|-> exists, routes through _read_prompt_file (path/stdin, never argv-inline — the doubled-ampersand trap the brief documents), and the addendum lands as its OWN labelled --append-system-prompt segment "WHAT THE LAST KID PRODUCED -- from your parent, not from the node" in the recorded command string — I reproduced the dry-run myself and read the segment; (2) the parent ITERATION CONTRACT names the lever with the exact command shape, closing the lever-nobody-is-told-about half. No-flag regression asserted at assemble and dry-run level by the kid; I re-ran test_dispatch/test_adapters/test_brief (197 passed). Verdict inconclusive_lean_proved:50 is honest — the mechanical half is proven, the autonomous live gate (a fresh tier-parent spawning 2+ kids with kid 1 node id literally in kid 2 agent.json) was not run and needs a shepherded dispatch this kid correctly refused to fake. Next run at THIS node: run that live gate, then grep kid 2 agent.json for kid 1 node id.
<!-- THOUGHT:END -->
