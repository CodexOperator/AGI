---
id: hypothesis:l4-trimguard-subcommand
mint_id: 90c2928b0f4243039f8d5918b99baac6
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-helper
scaffold_hash: 39af27a67e5092f7
season: 2
testable_claim: trimguard.py (untracked, main-checkout .agi/sessions/) parses HANDOFF.md §6 for double-quoted owner spans and greps .agi/nodes/ to confirm each resolves, aborting on any miss; folded into an existing tracked bin/*.py as a subcommand (never a new bin/*.py, which test_bin_help_smoke would enrol), the subcommand must be invocable from a fresh checkout with no dependency on the untracked file and produce byte-identical ABORT/OK verdicts against the same HANDOFF.md fixture the original script would. Disproved if the fold changes the verdict on any fixture or lands as a new bin/*.py instead of a subcommand on an existing one.
thought_session: sanctuary-helper-cd
title: trimguard.py's owner-quote-loss guard is untracked; fold it into a tracked bin tool as a subcommand
---
<!-- BODY:BEGIN -->
# hypothesis:l4-trimguard-subcommand

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## L4.120 brief -- fold trimguard.py into a tracked subcommand

Assigned by sanctuary-director (rotation/verification noted in THOUGHT).

ROOT-CAUSED before writing this: .agi/sessions/trimguard.py exists in the
MAIN checkout (confirmed by direct read), absent from this seat's OWN
.agi/sessions/ only because each worktree's session dir is separate -- an
established pattern here, not a discrepancy. It parses HANDOFF.md's '## §6
Owner decisions' section, extracts every double-quoted span >=25 chars
(plus open-ended truncated quotes), greps .agi/nodes/ for each, and aborts
(exit 1) if any owner quote would be lost on a trim -- otherwise prints OK.
Real, working, load-bearing for the HANDOFF.md replacement policy CLAUDE.md
mandates (director replaces the live section wholesale each rotation) and
the standing rule that owner verbatim lives in nodes, never only in the
handoff.

NOT YET DECIDED, left to you: which existing tracked bin/*.py hosts this as
a subcommand. cli.py is a strong candidate on shape alone -- it already
uses argparse subparsers with cmd_* functions (done, pending, scaffold,
claim, detect-stale, reclaim, status, session-complete) and is not in the
point's exclusion set. Root-cause whether it or another tracked tool fits
better before committing; state your choice and why in your experiment
node.

CONSTRAINTS: do not create a new bin/*.py (test_bin_help_smoke would enrol
it -- that is the whole reason this is a fold, not a new file). Preserve
the exact ABORT/OK semantics and messages against the same HANDOFF.md
fixture -- this is a safety check, not a rewrite; behaviour must be
provably identical. Do not touch workflow.py, rotate.py,
extensions/agi/briefs/*, conftest.py, verification.py, season.py,
hooks/cc-session-start.sh, anything under .agi/nodes/.geometry/, or
config:seats (point's exclusion set -- this round's own exclusion is
everything except the host tool you pick and its test). Kid ceiling 2. No
full-suite run.

REPORT: one experiment node, verdict on whether the fold is
byte-behaviour-identical, which host tool and why, and whether the
original untracked script should then be deleted (it should, once the
subcommand supersedes it -- say so explicitly rather than leaving two
copies of the same check live).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Point rotated again this generation (sanctuary-director-11 [3d6888] ->
seat-sanctuary-director-16 [4a9edc], third rotation this session). Verified
independently, same as the prior two: tmux+ListAgents join (@245, busy,
matches) and config:seats read fresh at origin/season/s2 HEAD (sanctuary-
director row session_ref 4a9edc, matches). Proceeded on that basis. This
node's brief was root-caused against my own current tree before writing,
not transcribed from the assignment message.
<!-- THOUGHT:END -->
