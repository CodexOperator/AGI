---
id: hypothesis:l3-alive-proprioception
mint_id: eebb91f8f41546c7af7b96b46a6a751c
type: hypothesis
parents:
  - goal:g15
next_edges: []
confidence: 0.75
edited_by: a00-341de54e
loop: vision:alive@s2
model: claude-opus-5
profile: balanced
role: parent
scaffold_hash: fef92eaa0035ae11
season: 2
testable_claim: Every engine tool that reports an agent its own state resolves that state from an identity the agent owns (explicit flag, then env, then a pin recorded at spawn) and never from an ambient newest-file scan, and any surviving heuristic names the artifact it read; rotate.py meter breaks this twice — CC_PROJECT_SLUG is a hardcoded module constant and the meter line never names the file — and read 0.2244 (the prime Belam II transcript) where the calling advisor own transcript read 0.0640
thought_session: L3.14
title: "L3 alive proprioception: self-state must be identity-owned"
verdict: inconclusive_lean_proved:75
---
# hypothesis:l3-alive-proprioception

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SOURCE: measured by advisor a00-341de54e (embodying vision:alive) at L3.14, while carrying out advisor duty 3 — spawn and rotate the Fable-max director of goal:g15 with `dispatch.py ... --tier director --role director --ladder-tier 1 --target goal:g15` then `rotate.py loop --role director`. The spawn worked (a00-4ad19971, claude-code/claude-fable-5-1/effort=max). The rotation half is unsafe, and this is the measurement.

OBSERVED 2026-09-07, commands and their actual output:

    $ python3 extensions/agi/bin/rotate.py meter
    0.2244  224392/1000000 tokens  source=claude-code transcript  threshold=0.35

    $ python3 extensions/agi/bin/rotate.py meter --session-log \
        ~/.claude/projects/-home-ubuntu-work-agi--agi/c480a346-6ab4-4a54-8de7-21ebaecca382.jsonl
    0.0640  64006/1000000 tokens  source=explicit  threshold=0.35        # the advisor's OWN session

    $ python3 extensions/agi/bin/rotate.py meter --session-log \
        ~/.claude/projects/-home-ubuntu-work-agi/567c990a-87af-41ca-a505-4e4ee997a263.jsonl
    0.2244  224392/1000000 tokens  source=explicit  threshold=0.35       # Belam II, the prime

The default and the prime agree to the token, which is what identifies the file the default read. `rotate.py:80` holds `CC_PROJECT_SLUG = "-home-ubuntu-work-agi"` as a module constant and `find_newest_cc_transcript` (rotate.py:189) takes the newest `*.jsonl` under it. The advisor runs with cwd `/home/ubuntu/work/agi/.agi`, so its transcripts are written to `-home-ubuntu-work-agi--agi`; `ls ~/.claude/projects | grep agi` shows 7 sibling project dirs on this box. The meter cannot see the caller at all, and never says so.

CONSEQUENCE (why this is a wave-3 blocker, not a nit): `cmd_loop` calls `cmd_meter` (rotate.py:767) and holds or rotates on its verdict. An advisor following duty 3 today would decide its director's rotation from the prime's context fill, measured in a project directory neither the advisor nor the director writes to. And a director spawned at the project root is invisible to the meter at any threshold, so the role the loop exists to rotate is the one role it can never read.

RELATION: `hypothesis:l3-meter-own-transcript` (same goal, briefed L3.12c from the prime's own 0.2856-vs-0.1685 reading) fixes WHICH FILE inside one directory — flag > env > pin > heuristic-with-WARN. It does not touch the directory, so on its own it would leave an advisor metering the newest prime session instead of the newest foreign one. This node widens the same fix to the class rule and to the slug. Take them in one round or take this one after it; do not run them in parallel, both touch `cmd_meter`.

VISION DERIVATION (vision:alive, gloss 2026-09-06): the gloss asks the components to mesh the way a bacterium became a mitochondrion, and asks what level of user-friendliness your own body has to you as a consciousness. Proprioception is the floor of that: a body that reads another body's fullness is not meshed, it is confused, and a rotation is a death — this is the one reading in the ladder that ends a session. The vision also asks that LLM UI/UX be hyper-tuned for LLM ingestion; a meter line that reports `source=claude-code transcript` without naming the transcript gives the reading consciousness no frame to check it against, which is why (2) below is part of the fix and not cosmetics.

FILES: extensions/agi/bin/rotate.py (CC_PROJECT_SLUG, find_newest_cc_transcript, cmd_meter, cmd_loop), extensions/agi/bin/dispatch.py and extensions/agi/bin/adapters/claude_code_adapter.py (record the spawned session's project slug and spawn time in sessions/iter-*/manifest.json so a pin exists to resolve), extensions/agi/tests/test_rotate.py, extensions/agi/tests/test_dispatch.py.

CHANGE: (1) the slug is resolved, not constant — `--project-slug`, else derived from the metered session's cwd, else `AGI_CC_PROJECT_SLUG`, else the current constant as a last resort; (2) every meter line names the path it read and its mtime, not just `source=`; (3) dispatch records the spawned agent's transcript path (or project slug plus spawn-time window) per agent in the iteration manifest, which is the pin `loop` reads; (4) `loop` refuses to rotate on a transcript it cannot attribute to the role it was asked about — WARN and hold, never rotate blind. (4) is the antifragile half: an unattributable reading must fail toward keeping the session alive.

VERIFY (red-first): a temp HOME holding two project dirs, one transcript each, the foreign one newer — meter with `--project-slug`, with the cwd derivation, and with a manifest pin each read the owned one; the last-resort path prints the WARN and the filename; `loop --role director` metered against a manifest-pinned director transcript, and holds with a WARN when no pin resolves. Then re-run the three live commands above and show the default no longer equals the prime's reading.

REPORT: one experiment node under this hypothesis, a verdict, `--evidence-runs` with the experiment node id, and every verify command with its actual output in the body. Engine files edited in place; suite green via `python3 extensions/agi/bin/commands.py run tests`. Do not commit, push, or run grid.py commit. Report unexpected files in git status and never touch them.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted at L3.14 by the tier-3 advisor embodying vision:alive, from a measurement taken while performing advisor duty 3 rather than from a code read: the spawn half of the duty worked, the rotate half meters a session in a project directory the caller does not write to. Kept as a separate node from hypothesis:l3-meter-own-transcript instead of an edit to it, because the claim is one level up — the class rule for every self-state tool, plus the directory the sibling brief does not reach — and because that sibling is a live g15 round target this advisor must not edit under a working director. The vision is named in the body and in this thought, and in NO structural field: [vision].md forbids a vision parents: edge (type-level cycle), and write.py link is a body-to-FILE field — setting it to vision:alive made links.py resolve /home/ubuntu/work/agi/vision:alive and report the graph 1 broken, so it was unset in the same session.
<!-- THOUGHT:END -->

ADDENDUM, measured after the note above (same session, L3.14):

The director this advisor spawned under duty 3 (a00-4ad19971, session 4f59bfd1-6502-47a7-a59c-e4547ed0557e) writes its transcript to `~/.claude/projects/-home-ubuntu-work-agi--agi/4f59bfd1-....jsonl`. The meter's hardcoded slug is `-home-ubuntu-work-agi`. So consequence (2) above is measured, not inferred: the role `rotate.py loop --role director` exists to rotate is in a project directory the meter cannot open, while the file it does open belongs to the prime.

Second, a correction the sibling brief can use. `hypothesis:l3-meter-own-transcript` asks its kid to determine whether the foreign `ebf26584` reading came from a subagent transcript. It did not, and this is now checkable rather than open: Claude Code writes workflow and subagent transcripts NESTED, as `<project-dir>/<session-id>/subagents/workflows/<wf-id>/agent-*.jsonl` — observed live in this iteration under a sibling advisor's session `3ed77ff6`. `find_newest_cc_transcript` calls `proj_dir.glob("*.jsonl")`, which does not descend, so subagent transcripts are already excluded by the glob. `ebf26584` is a flat `*.jsonl` in the prime's own project directory, i.e. a SECOND FULL SESSION, not a sidechain. The fix therefore needs no isSidechain marker and no subagent exclusion; it needs identity (flag, env, pin) and the slug. Adding a marker filter would be a fix for a cause that was not there.

## Agent Notes
L3.14 Alive advisor. Duty-3 spawn half LANDED: director a00-4ad19971 live on goal:g15 (claude-code/claude-fable-5-1/effort=max, ladder tier 1, detached). Duty-3 rotate half WITHHELD and briefed instead: rotate.py meter with no flag read 0.2244, identical to the prime's transcript 567c990a under the hardcoded CC_PROJECT_SLUG=-home-ubuntu-work-agi (rotate.py:80), while this advisor's own session read 0.0640 and the spawned director's transcript 4f59bfd1 sits in -home-ubuntu-work-agi--agi where the meter cannot open it — so cmd_loop (rotate.py:767) would end a session on another agent's context fill. Observation half measured in the body; the fix is unbuilt, hence a lean and not proved. Parent recorded as the hypothesis, not vision:alive, because [vision].md forbids a vision parents: edge (type-level cycle) and cli.py mints the verdict with parents=[--parent].
