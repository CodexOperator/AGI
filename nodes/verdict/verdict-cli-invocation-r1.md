---
id: "verdict:cli-invocation-r1"
title: "R1: Shell type detection accuracy"
type: verdict
parent_hypothesis: hyp:cli-invocation-r1
domain: cli-invocation
status: proved
confidence: 0.80
evidence_runs:
  - exp:cli-invocation-r1
tags:
  - cli
  - shell
  - detection
  - R1
next_edges:
  - mvp:cli-invocation-r1
  - exp:cli-invocation-r1-extend1
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
