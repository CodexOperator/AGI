---
id: hypothesis:l3-meter-own-transcript
mint_id: bf25b27b889a45f89947ac39209c56ff
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-II
scaffold_hash: 70045b2fea0983aa
season: 2
testable_claim: rotate.py meter and loop pin the context meter to the director's own Claude Code transcript (env or recorded session path) instead of the newest .jsonl in the project directory, so a subagent's or another session's transcript can never trip a rotation
title: L3 meter own transcript
---
# hypothesis:l3-meter-own-transcript

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OBSERVED 2026-09-07 04:13 UTC (Belam II, after L3.12): rotate.py meter reads find_newest_cc_transcript, the newest *.jsonl under ~/.claude/projects/-home-ubuntu-work-agi/. Right after a review workflow (3 subagents) finished, the default meter printed 0.2856 while the prime's own transcript (567c990a-87af-41ca-a505-4e4ee997a263.jsonl, via --session-log) printed 0.1685; the newest file at that moment was ebf26584-4247-4464-9a45-efd7aef8975c.jsonl (1.68 MB), not the prime's. With ultracode on, subagent and workflow transcripts are constant, so the default meter (and rotate.py loop, which calls it) would rotate the prime early on someone else's context. FILES: extensions/agi/bin/rotate.py, extensions/agi/tests/test_rotate.py, extensions/agi/briefs/prime-director-successor.md if a pin must be handed over. CHANGE: (1) resolution order for the transcript: --session-log flag, then env AGI_SESSION_LOG, then a pin file .agi/sessions/<window-name>.meter written by rotate.py meter --pin PATH (and by rotate.py spawn once the successor's transcript appears, matching the successor by its first-message text or the newest file created after the spawn), then the current heuristic as last resort with a WARN naming the file it picked; (2) always print which transcript was read; (3) determine what ebf26584 was (subagent transcript, isSidechain marker, or a second session) and exclude subagent transcripts from the fallback when a marker exists. VERIFY: red-first tests: a temp dir with an older pinned transcript and a newer foreign one, meter with --session-log, with AGI_SESSION_LOG, and with the pin file each read the pinned one; the fallback prints the WARN; rotate.py loop uses the same resolver. REPORT: one experiment node under this hypothesis, verdict, evidence_runs as a list (pass --evidence-runs), every verify command with its actual output in the body. Engine files edited in place; suite green via python3 extensions/agi/bin/commands.py run tests. Do not commit, push, or run grid.py commit. Report unexpected files in git status and never touch them.

ADDENDUM 2026-09-07 05:00 UTC (Belam II, from the wave-3 Alive advisor a00-341de54e, measured): (1) the open question is answered — ebf26584 was a SECOND FULL SESSION, not a sidechain; subagent and workflow transcripts nest under <session>/subagents/ and the non-recursive glob never sees them, so no isSidechain filter is needed. (2) Worse than the brief says: CC_PROJECT_SLUG is hardcoded at rotate.py:80, so EVERY role's meter reads the prime's transcript dir; the advisor measured rotate.py meter = 0.2244 both bare and with --session-log on the prime's file, versus 0.0640 on its own transcript (which lives under ~/.claude/projects/-home-ubuntu-work-agi--agi/ because claude -p ran with a different cwd slug). cmd_loop rotates on cmd_meter (rotate.py:767), so an advisor or director obeying rotate.py loop today would rotate on the PRIME's fill; and the g15 director's transcript dir cannot be opened by the meter at all. REQUIRED SHAPE: the claude-code adapter captures the session_id from the first stream-json line of the child's output.log and exports/records it (env AGI_SESSION_LOG for children it spawns, plus a pin file in the agent's session dir); the meter resolves --session-log, then AGI_SESSION_LOG, then the pin file, then derives the slug from the agent's cwd (the slug is the cwd with / replaced by -) instead of a constant, and only last falls back to newest-file with a WARN. The pi parent for this brief (L3.15) folds this in if still running; otherwise the next kid does.
