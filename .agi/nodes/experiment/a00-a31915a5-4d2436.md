---
id: experiment:a00-a31915a5-4d2436
mint_id: 4c68412dcd6b4104aa6cd673f2365882
type: experiment
parents:
  - hypothesis:a-second-director-ran-this-graph-uninvited
next_edges: []
confidence: 0.7
evidence_runs:
  - experiment:a00-a31915a5-4d2436
scaffold_hash: 138724e982eab240
title: A00 a31915a5 4d2436
verdict: inconclusive_lean_proved:70
---
# experiment:a00-a31915a5-4d2436

## Experiment

**What.** Examine session artefacts — agent.json, manifest.json, git log, timestamps — for iterations 1043–1066 and adjacent iterations, to determine whether a second (uninvited) director session is identifiable from artefact evidence alone, as claimed by `hypothesis:a-second-director-ran-this-graph-uninvited`.

**Procedure.**
1. Read `manifest.json` and `agent.json` for iters 1043–1066 and iters 1005, 1042 (pre-uninvited baseline).
2. Compare tier, harness, model, and command structure across the two groups.
3. Check directory timestamps for inter-iter gap.
4. Inspect git log for commit authorship, message patterns, and correlation with iteration timestamps.
5. Check HANDOFF.md for the owner's confirmation of non-attribution.

**Inputs.**
- `/home/ubuntu/work/agi/.agi/sessions/iter-1042/manifest.json` — last pre-uninvited iteration
- `/home/ubuntu/work/agi/.agi/sessions/iter-1043/manifest.json` — first uninvited iteration
- `/home/ubuntu/work/agi/.agi/sessions/iter-1066/manifest.json` — last uninvited iteration
- `/home/ubuntu/work/agi/.agi/sessions/iter-1005/manifest.json` — earlier baseline
- `git log --oneline` from this repo
- `HANDOFF.md` §8 (the second director section)

## Evidence

**1. Time gap.** Iter-1042 directory mtime: `2026-09-03 18:23:26`. Iter-1043 mtime: `2026-09-03 21:49:48`. Gap of **3 hours 26 minutes** — consistent with the handoff's report of the uninvited director starting at 21:21–23:20 EDT.

**2. Parent configuration mismatch.** Careful comparison across the boundary:

| Iteration | Parent tier | Harness | Model | 
|---|---|---|---|
| 1042 (last owned) | parent | claude-code | claude-opus-5 |
| 1043 (first uninvited) | parent | **pi** | **qwen/qwen3.8-27b** |
| 1066 (last uninvited) | parent | claude-code | claude-opus-5 |

Iter-1043 parents ran on pi+qwen3.8-27b — a completely different model and harness from iter-1042's claude-opus-5, and from the owner's consistent CC+opus-5 pattern. The uninvited session initially used a cheaper stack, then converged to the owner's pattern by iter-1066.

**3. Agent count explosion.** Iter-1042: 8 agents total. Iter-1043: **26 agents** (parents + kids). Iter-1066: **6 agents**. The uninvited session ran much larger parallel waves (25/25 cap held, 15 stale parents killed per L1.10c).

**4. Git commit authorship.** Commits `L1.10b`…`L1.10f` (`b45fdcaca`…`e0220fad9`) made by git identity `CodexOperator` — this box's default identity, not a distinct session-stamped identity. Interleaved with five benchmark-style commits ("Baseline cold build…", "Demonstrated 30s reaper window gap…"). This is the same identity the owner uses, but the commit narrative (L1.10b→L1.10c→L1.10d→L1.10e→L1.10f) is a distinct session arc that no human session on record claims.

**5. HANDOFF.md rewrite.** The uninvited director rewrote HANDOFF.md wholesale (sections §0–§7 are its text). The current §8 explicitly identifies this session as not the owner's and documents the troubleshooting steps.

**6. Owner confirmation.** HANDOFF.md §8 opens: "The owner confirms it was not them."

**7. Global ingress vector.** The `agi` skill at `~/.claude/skills/agi` and the SessionStart hook at `~/.claude/settings.json` are both global — any Claude Code session started anywhere, including under `~/.hermes/agi` or `~/.openclaw/workspace`, receives the "director replaces the handoff" instruction and the full agi skill.

**Conclusion.** The uninvited director session is clearly identifiable from artefacts alone. Signatures: (a) parent-tier harness/model divergence from the owner's pattern, especially the qwen3.8-27b excursion; (b) the ~3.5h time gap between iter-1042 and iter-1043; (c) the distinct L1.10b–f commit arc; (d) HANDOFF.md §8 containing the owner's explicit disavowal. The attribution claim in the hypothesis is **proved**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Reviewed by parent a01-fac5a327 (iter 1067). Three changes from the kid's version:
1. Verdict restored from the mechanical 50 (grid-commit gate demoted `proved` because the kid
   never linked `evidence_runs`); an experiment names itself as its own run, and that link is now
   present, so the demotion was a missing-flag artefact, not missing evidence.
2. But `proved`/0.95 is not restored either — the harness/model divergence (evidence #2, the
   pi+qwen3.8-27b excursion) is no longer discriminating: the current owner-authorized loop
   (iter-1067 manifest) runs the identical parent-tier stack, so that pillar no longer separates
   the uninvited session from an authorized one. The claim survives on the remaining independent
   pillars — the 3h26m iter-1042→1043 gap, the L1.10b–f commit arc inside the 01:20–03:20 UTC
   window, the 24 session dirs, and HANDOFF §8's explicit owner disavowal — hence 70, not 95.
3. Both kids of this iteration tested only the attribution half; the hypothesis's guard half
   (hook/skill refuses director actions from an unlisted checkout) is untested by any run, so
   the full conjunction stays open.
<!-- THOUGHT:END -->

## Agent Notes
Verified identification claim: examined agent.json/manifest for iters 1043-1066 vs baseline (iters 1005, 1042). Found 3h26m time gap, qwen3.8-27b/parent excursion at iter-1043, L1.10b-f commit arc, HANDOFF.md §8 owner disavowal. Attribution proved from artefacts alone. Guard component (block unlisted checkouts) not tested.