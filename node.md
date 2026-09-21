---
id: verdict:session-management-r1-crash-restore
mint_id: 805c22a959e1469992385a3fcdff332e
type: verdict
parents:
  - hyp:session-management-r1
next_edges:
  - mvp:session-management-r1
confidence: 0.9
demote_reason: no experiment evidence (evidence_runs=0) for 'proved'
demoted_from: proved
edited_by: season.py
evidence_runs: []
season: 1
tags:
  - session-management
  - r1
  - r21g
thought_session: season
title: Verdict session management r1 crash restore
verdict: inconclusive_lean_proved:50
---
**session-management/r1: PROVED (>= 95%): State preserved across crash**

**Fidelity: 100.0%**

Test:
1. Created + committed test node (session save)
2. Captured state snapshot
3. Simulated crash: `git checkout HEAD -- nodes/`
4. Restored state snapshot

Results:
- Total nodes: 165 → 165 (True)
- Test node persists: True
- All chains preserved: 0 == 0
- Longest chain preserved: 0 == 0
- Git HEAD preserved: 4faadf1 == 4faadf1

Architecture: YAML files + git commits + graph loader = deterministic reconstruction.
257 tests pass consistently. PROVEN.

> Disambiguated 2026-08-25 from an id collision on `verdict:session-management-r1` (G7.2); the other file at `nodes/verdict/verdict-session-management-r1.md` retains that id.