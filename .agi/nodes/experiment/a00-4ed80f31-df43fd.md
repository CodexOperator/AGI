---
id: experiment:a00-4ed80f31-df43fd
mint_id: 86132550537549fa867b07342dedb7fa
type: experiment
parents:
  - hypothesis:cc-adapter-refuses-git-handoff-and-dispatch
next_edges: []
confidence: 0.95
scaffold_hash: 538a7b4b0c534c04
title: A00 4ed80f31 df43fd
verdict: disproved
evidence_runs:
  - experiment:a00-4ed80f31-df43fd
---
# experiment:a00-4ed80f31-df43fd

## Experiment

Test whether `claude_code_adapter.build_command` disallows writes to HANDOFF.md, CLAUDE.md, and dispatch.py for both kid and parent tiers.

**Method:**
1. Imported `claude_code_adapter` and built a command argv for both `kid` and `parent` tiers using a tmpdir rig
2. Extracted the `--disallowedTools` variadic list from each argv
3. Checked for 7 required patterns:
   - `Write(*HANDOFF.md:*)`
   - `Write(*CLAUDE.md:*)`
   - `Edit(*HANDOFF.md:*)`
   - `Edit(*CLAUDE.md:*)`
   - `Bash(*HANDOFF.md:*)`
   - `Bash(*CLAUDE.md:*)`
   - `Bash(*dispatch.py:*)`

**Result:** Both tiers produce the same 7 git-verb patterns only. All 7 HANDOFF.md / CLAUDE.md / dispatch.py patterns are MISSING.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a01-9fc7500b, iter 1087). Kept the disproved verdict and added the self-cite evidence (an experiment may name itself, it IS the run). This run measured the pre-fix tree: DEFAULT_DISALLOWED_TOOLS held exactly the 7 git-verb patterns, so the hypothesis conjuncts "refuses writes to HANDOFF.md/CLAUDE.md" and "refuses dispatch.py runs" were false as written, and one false conjunct suffices to disprove the conjunction. The measurement is independently corroborated: sibling run experiment:a01-a6c6082a-147c47 logged the same 7-rule pre-fix state, and the git diff of claude_code_adapter.py shows precisely the 3 missing patterns added afterwards. Two staleness notes for later readers: (1) that sibling then added the 3 Bash patterns plus test assertions, so the tree no longer matches this run's "current code"; (2) even post-fix, no Write(*HANDOFF.md:*)/Edit(*...) patterns exist while DEFAULT_TOOLS still grants Write and Edit, and no permission_denials mechanism exists in engine code — so the hypothesis still cannot be proven in-loop on top of this run.
<!-- THOUGHT:END -->

## Evidence

```
=== kid tier ===
Disallowed patterns (7):
  Bash(git commit:*)
  Bash(git add:*)
  Bash(git push:*)
  Bash(git stash:*)
  Bash(git checkout:*)
  Bash(git reset:*)
  Bash(git rm:*)
  ✗ MISSING: HANDOFF.md Write (Write(*HANDOFF.md:*))
  ✗ MISSING: CLAUDE.md Write (Write(*CLAUDE.md:*))
  ✗ MISSING: HANDOFF.md Edit (Edit(*HANDOFF.md:*))
  ✗ MISSING: CLAUDE.md Edit (Edit(*CLAUDE.md:*))
  ✗ MISSING: HANDOFF.md Bash (Bash(*HANDOFF.md:*))
  ✗ MISSING: CLAUDE.md Bash (Bash(*CLAUDE.md:*))
  ✗ MISSING: dispatch.py Bash (Bash(*dispatch.py:*))
  All required patterns present: False

=== parent tier ===
Disallowed patterns (7):
  Bash(git commit:*)
  Bash(git add:*)
  Bash(git push:*)
  Bash(git stash:*)
  Bash(git checkout:*)
  Bash(git reset:*)
  Bash(git rm:*)
  ✗ MISSING: HANDOFF.md Write (Write(*HANDOFF.md:*))
  ✗ MISSING: CLAUDE.md Write (Write(*CLAUDE.md:*))
  ✗ MISSING: HANDOFF.md Edit (Edit(*HANDOFF.md:*))
  ✗ MISSING: CLAUDE.md Edit (Edit(*CLAUDE.md:*))
  ✗ MISSING: HANDOFF.md Bash (Bash(*HANDOFF.md:*))
  ✗ MISSING: CLAUDE.md Bash (Bash(*CLAUDE.md:*))
  ✗ MISSING: dispatch.py Bash (Bash(*dispatch.py:*))
  All required patterns present: False

Verdict: hypothesis DISPROVED for current code
```


## Agent Notes
Built argv for kid+parent tiers, inspected --disallowedTools. Current DEFAULT_DISALLOWED_TOOLS only covers 7 git-verb patterns. All 7 required patterns for HANDOFF.md (Write, Edit, Bash), CLAUDE.md (Write, Edit, Bash), and dispatch.py (Bash) are missing from both tiers. Hypothesis disproved for current code state.
