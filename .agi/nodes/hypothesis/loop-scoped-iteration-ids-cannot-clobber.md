---
id: hypothesis:loop-scoped-iteration-ids-cannot-clobber
mint_id: a513aaafd8dc4d0da1a3b3df57ce3ab4
type: hypothesis
parents:
  - goal:g7
next_edges: []
edited_by: season.py
scaffold_hash: c06190f4587c9db7
scale: engine
season: 1
testable_claim: "A fresh driver.sh run cannot overwrite an existing .agi/sessions manifest: iteration ids are loop-scoped (L<loop>.<nn>) end to end -- sessions dir, commit subjects, cli.py/dispatch.py/zoom.py parsing -- the 116+ legacy iter-NNN dirs stay readable, and a test that points the driver at a populated sessions dir goes red when the guard is removed"
thought_session: season
title: Loop scoped iteration ids cannot clobber
---
# hypothesis:loop-scoped-iteration-ids-cannot-clobber

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
"Today: driver.sh starts at iter-001 and will clobber prior session manifests on a fresh run (documented data-loss hazard in SKILL.md, Long runs). This session is loop L1 and ran L1.01..L1.08 by hand in commit subjects only; the sessions dir meanwhile went iter-1006..1038 because nothing allocates ids. Claim: the smallest change that (a) makes loop-scoped ids real end to end, (b) cannot clobber an existing manifest -- allocate the next free id, never a fixed start -- and (c) keeps every existing iter-NNN directory readable. Read driver.sh, bin/cli.py, bin/dispatch.py, bin/zoom.py and .agi/sessions for everything that formats or parses iter-NNN. Falsifier: populate a sessions dir with an iter manifest, run the allocator, assert the manifest is untouched; remove the guard and watch it go red."

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
"Director-minted for L1.10; the hazard is nothing-lost (goal:g7), so it parents there rather than to a new goal."
<!-- THOUGHT:END -->