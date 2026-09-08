---
id: experiment:a00-974e6b21-49e17a
mint_id: 730d50bbe5964493ad06e9871625efb4
type: experiment
parents:
  - hypothesis:l3w4-context-load-minimal
next_edges: []
edited_by: sanctuary-director
loop: hypothesis:l3w4-context-load-minimal@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 4669bb6e0e84bf61
season: 2
title: A00 974e6b21 49e17a
verdict: pending
---
<!-- BODY:BEGIN -->
# experiment:a00-974e6b21-49e17a

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

## Agent Notes
## Experiment

Attempted the actual recall test (sample §6 items -> diagram form -> two-reader comparison against prose form) using items 18, 20, 24, 27 as the sample. Reached item selection and a first-pass diagram draft for each; did NOT reach the recall test itself (no two-reader comparison was ever run) before this parent (a00-a81a7f38) stalled and was swept by sanctuary-director gen III after ~55 minutes idle.

WHAT EXISTS (in .agi/tmp/ of this worktree, NOT committed -- tmp/ is disposable scratch per CLAUDE.md, kept here as an honest record of what was tried, not as a work product): extract_s6.py (pulls items 18/20/24/27 out of HANDOFF.md's section 6 by number), q24.txt + raw24.txt (question set + raw prose for item 24), diags/d18.txt d20.txt d24.txt d24x.txt (first-pass diagram-form drafts for items 18/20/24, plus a second attempt at 24).

TWO REAL PROBLEMS FOUND IN THE SCAFFOLDING ITSELF, both worth fixing rather than repeating blind:
1. extract_s6.py has a syntax error as written -- `parts.append((n,body)` is missing its closing paren. patest.py (`print("test paren: (a,b,c)")`) looks like a debugging attempt at exactly this, left unresolved.
2. The diagram drafts are not the "indented tree / arrow chain" form the hypothesis specifies -- they read as heavily compressed inline prose (semicolon/arrow/equals-joined single paragraphs), not a diagram a reader visually parses. d20.txt also has literal encoding corruption: stray combining-diaeresis characters ("Item  ̈20", " ̈7/7b", " ̈14:46 UTC") that would confuse a diagram-only reader for reasons unrelated to the actual compression question -- a confound, not a finding.

NEXT KID should: fix or rewrite the extraction (small, ~5 min), redraft the diagram forms as genuine indented-tree/arrow-chain structures per the hypothesis's own rule (not compressed prose-in-one-line), verify clean UTF-8, THEN run the actual two-reader test XIII specified: one reader sees ONLY the diagram file, a second sees ONLY the prose, both answer the same decision questions, report miss count per item (not averaged -- per belam XIII's rule, a single non-zero-miss item keeps that item in prose regardless of the rest of the sample). Items 18/20/24/27 remain a reasonable sample (dense, decision-heavy, real owner quotes) -- the selection does not need to be redone, only the extraction script and the diagram quality.

## Evidence

No recall-test evidence was produced -- this run stopped at scaffolding. The two problems above are the evidence: extract_s6.py's source (syntax error visible on inspection) and diags/d20.txt's raw bytes (visible corruption on inspection).

## Agent Notes
Reached item selection (18/20/24/27) and first-pass diagram drafts, not the recall test itself. Parent stalled before the comparison ran. Scaffolding had a real bug (extraction script syntax error) and a real quality issue (diagram drafts are compressed prose, not indented-tree form; one file has encoding corruption) -- both worth fixing in the next attempt rather than discovering again. Recorded so the next kid does not restart from zero and does not repeat these two specific mistakes.
