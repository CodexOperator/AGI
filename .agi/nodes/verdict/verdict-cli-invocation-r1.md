---
id: verdict:cli-invocation-r1
mint_id: 38ccedb9f9684f47af3e56be1a415b51
type: verdict
parents:
  - hyp:cli-invocation-r1
next_edges:
  - mvp:cli-invocation-r1
  - exp:cli-invocation-r1-extend1
confidence: 0.8
domain: cli-invocation
edited_by: season.py
evidence_runs:
  - exp:cli-invocation-r1
season: 1
status: proved
tags:
  - cli
  - shell
  - detection
  - R1
thought_session: season
title: "R1: Shell type detection accuracy"
verdict: proved
---
**Verdict:** PROVED

**Detection Metrics:**
- Accuracy: 100%
- Confidence: 80%
- Method agreement: 2/2 (100%)
- Detected shell: bash
- Ground truth: bash
- Threshold: 90%

**Detection Methods:**
- Method 1 ($SHELL): /bin/bash
- Method 2 (ps parent): bash
- Method 3 (/proc/status): python3
- Method 4 (env indicators): ['bash']

**Analysis:**
Shell detection via environment variables and process inspection provides
80% confidence. Method agreement rate: 100%.