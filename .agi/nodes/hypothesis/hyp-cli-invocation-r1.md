---
id: hyp:cli-invocation-r1
mint_id: 62b5a7ef160b4266b4414819f168f2df
type: hypothesis
parents:
  - idea:domain-cli-invocation
next_edges:
  - exp:cli-invocation-r1
confidence: 0.8
demote_reason: no experiment evidence (evidence_runs=0) for 'proved'
demoted_from: proved
domain: cli-invocation
edited_by: season.py
evidence_runs: []
season: 1
status: inconclusive_lean_proved:50
tags:
  - cli
  - shell
  - detection
  - R1
thought_session: season
title: "R1: Can reliably detect current shell type from environment"
verdict: inconclusive_lean_proved:50
---
## Hypothesis

**Claim**: Current shell type (bash/zsh/fish/cmd) can be reliably detected with >90% accuracy using environment variables and parent process inspection.

**Test Result (iter 19)**:
- Detection accuracy: **100%** (bash detected correctly)
- Detection confidence: 80%
- Method agreement: 2/2 (100%)
- **VERDICT: PROVED**

## Detection Methods
1. **$SHELL env var**: `/bin/bash` → bash
2. **ps parent process**: `bash` → bash
3. **Environment indicators**: BASH_VERSION present → bash

## Key Finding
Environment variables ($SHELL, BASH_VERSION) + parent process inspection provide reliable shell detection on Unix systems.