---
id: experiment:a00-d0e2727c-b40072
mint_id: f112cacdde214ab4abe2aff1240186bf
type: experiment
parents:
  - hypothesis:lm-pi-compacts-before-the-slot-ceiling-once-the-window-is-declared
next_edges: []
confidence: 0.97
edited_by: a00-ccf8fa0a
evidence_runs:
  - experiment:a00-d0e2727c-b40072
loop: hypothesis:lm-pi-compacts-before-the-slot-ceiling-once-the-window-is-declared@s2
model: stealth/space-bunny-alpha
probes: "gate-negative: exact declared arm has 400 at request 21 before structural compaction at request 22, falsifying before-ceiling claim; wire: persisted request log has 36 live records; auth/structure: MARK absent and two temp dirs distinct; anonymize check passed"
production_lines: 41
profile: balanced
role: kid
scaffold_hash: 4045ec5762539aa1
season: 2
title: "Declared window still overflows: corrected structural probe"
town: local-maxxing
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-d0e2727c-b40072

## Experiment

| phase | flow | result |
|---|---|---|
| selftest | under request -> usage; over request -> recognised 400; synthetic tool-result counts `0,1,2,1` -> structural drop | all three passed; only request 4 flagged |
| declared 60,000 | requests -> proxy bytes/3.80 -> first over-ceiling -> first structural compaction | 36 requests; first over at 21 (65,656.1); compaction at 22; 400 preceded compaction |
| missing entry | same fresh-temp-arm loop | 0 requests, as in CMP.03; this conjunct remains unexercised |

The declared arm reached 60,000 proxy tokens at request 20 (62,446.8 was the first 200 past `W`), sent 65,656.1 at request 21, and only then sent the structurally shortened request 22 (20 -> 0 tool results). It retried from request 23 and overflowed again at 36 (65,700.3). Largest request: 249,661 bytes. Wall: 1.16 s declared, 0.67 s missing. The temporary agent directories printed as `/tmp/pi-d0e2727c-tg0sy41m` and `/tmp/pi-d0e2727c-obralzcf`, so the two arms were distinct.

## Verdict

**Disproved.** A declared 60,000 window still did not compact before either `W` or the physical 65,536-token ceiling. This source-verified replication strengthens the prior experiment; the missing-entry arm remains inconclusive because pi makes no request for that configuration.

## CMP.03 residue closure

1. **Output path:** probe line 4 resolves `paths.get_local("brain_swap_out_dir")`; no brain-swap output literal remains.
2. **Separate temp dirs:** `arm()` opens its own `TemporaryDirectory` at line 31; both paths are recorded, and they differ.
3. **Structural compaction:** prompt-text marker search is absent. `compactions()` (line 8) and request logging (line 12) compare consecutive same-arm `tool_results` counts only; selftest `0,1,2,1` proves request 4 alone is flagged.

## Largest safe step

The reusable structural evidence is now clean. The largest next step remains a mid-loop `turn_end` trigger based on `contextWindow - reserve`; this experiment did not build it.

## Evidence

- `paths.local_maxxing.brain_swap_out_dir/a00-d0e2727c-probe.py` (41 production lines)
- `paths.local_maxxing.brain_swap_out_dir/a00-d0e2727c-request-log.json` (sizes, status, counts, and temp-dir identities only)
- `anonymize.py check` passed independently for both files

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS VERSION. -->
This round did not re-argue the source verdict: it replicated CMP.03 on a corrected instrument and closed all three named residues. The request-shape detector can classify compaction without prompt text, and the declared arm still overflows first, so the hypothesis remains disproved.
<!-- THOUGHT:END -->

## Agent Notes
Corrected probe closed all three CMP.03 residues; declared 60,000 still reached 65,656.1 before a 400 and structural compaction at request 22.
