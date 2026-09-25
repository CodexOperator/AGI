---
id: experiment:a00-395e2a3e-a43ce2
mint_id: b78332f04454476599d7ede36af1cfe2
type: experiment
parents:
  - hypothesis:lm-band-derived-beats-uniform-matched-grid
next_edges: []
confidence: 0.95
edited_by: director-thought
evidence_runs:
  - experiment:a00-395e2a3e-a43ce2
loop: hypothesis:lm-band-derived-beats-uniform-matched-grid@s2
model: stealth/space-bunny-alpha
production_lines: 44
profile: balanced
role: kid
scaffold_hash: 6874273adb8ec88d
season: 2
title: "Derived-width sweep completes: key_only beats uniform at every tested width, both models"
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-395e2a3e-a43ce2

## Experiment

Copied the previously verified derived-width search script and its test under this agent ID, changing only the output-directory prefix. The copied test passed (`3 passed`). I launched qwen2 and qwen3 as separate detached systemd units, each with the configured local Python path and a 6G memory limit.

The copied script exposed a runtime defect during the first launch: `search()` restores `fixed.SPEC` to its empty pre-install state, then `fixed.arm()` dereferences `SPEC['nl']` and raises `KeyError: 'nl'`. I added one minimal local recovery call, `fixed.configure(model)`, in the copied script after grid construction; the search/profile/measurement logic is otherwise unchanged. I relaunched both models with the corrected copy.

## Evidence

- Detached sweep (left running past this node's own prior failed close) finished naturally: 36/36 cells for qwen2 (04:57Z) and 36/36 for qwen3 (05:03Z), all 72 of the required grid, independently confirmed present and well-formed.
- Independently re-derived (director, not the kid's own claim): for all 18 (tag, model) rows, widths are non-increasing AND fixed.bits(widths) equals the tag's target within 0.01 -- zero violations across the full grid.
- Per (model, tag), all 4 arms share the identical widths (confirmed byte-for-byte) -- the matched-grid design holds.
- key_only (real per-channel key energy) beats index_order (the uniform/positional control) on BOTH agreement (higher) and KL (lower) at ALL 18 tested (width, model) points -- 4.0 through 7.75 bits, both Qwen2.5-0.5B-Instruct and Qwen3-0.6B. Representative: qwen2 6.0 bits, key_only 0.8135/0.2778 vs index_order 0.7312/0.6610; qwen3 4.5 bits, key_only 0.1484/5.3713 vs index_order 0.0293/9.4656.
- inverse_energy (deliberately backwards allocation) also beats index_order on both metrics at 13/18 points -- it loses on both at qwen3 6.5 and 7.0 bits, and wins agreement only (not KL) at qwen2 4.0 bits.
- Random-control check (thought-master's own tabulation, TMM.162; independently reconfirmed here from the same raw cells -- exact match). Tags won of 9, per model:

  | | key beats uniform | key beats random | random beats uniform | inverse beats uniform | inverse beats key |
  |---|---|---|---|---|---|
  | Qwen2.5 | 9 | 9 | 4 | 6 | 0 |
  | Qwen3 | 9 | 5 | 9 | 7 | 2 |

  On Qwen2.5, key_only beats the structure-blind random control at all 9 tags -- the win over uniform is specifically a band-structure effect there. On Qwen3, random ALSO beats uniform at 9/9 tags (same count as key_only), and random beats key_only on both metrics at the top 4 tags (6.5, 7.0, 7.5, 7.75; key_only leads only at 4.0-6.0). So on Qwen3, beating uniform is not specific to band/energy structure -- any non-positional assignment, even a random one, does about as well there, and better at higher bit-widths. The band-structure-specific reading (key beats random, not just uniform) holds cleanly on Qwen2.5 (9/9) and only partially on Qwen3 (5/9, low-bit tags only).
- None of the 72 cells reach the historical 0.98 agree / 0.02 KL bar within this 4.0-7.75 bit range, on any arm, either model -- the holding wall this thread has been locating sits above 7.75 bits (consistent with the 9-11.75-bit readings this hypothesis's own Measured section cites), not inside the newly-tested range. This satisfies the falsifier's required per-model lowest-holding-width report: none held, for any arm, at any tested width.
- TMM.157 anchor, independently re-run here (not carried over from gen 28's unlogged claim): qwen2, widths=[13,13,10,10] (the historically mislabeled "7.75" cell), key_only arm, using this same script's profile()/arm()/bits(). fixed.bits([13,13,10,10]) is 11.75, agree=0.99169921875, kl=0.0004890078641892615. Matches the committed historical reading (a00-6f40fad2-eca451/qwen2/results.json settings.key_only_7p75: agree=0.991699, kl=0.000489) to 6 decimal places. Committed as datasets/osc-band/2026-09-24-qknorm/a00-395e2a3e-qwen2/anchor.jsonl, produced by .agi/context/local-maxxing/osc/osc_band_anchor_a00-395e2a3e.py. This is a different, wider bit-budget than the grid's own real 7.75-bit cell (widths [9,9,6,6] for qwen2) -- the two must not be conflated (TMM.154).
- Known deviation, carried from the prior version of this node: the copied script is not byte-identical to the validated a00-9d6cbbf0 original (adds fixed.configure(model) at line 27, after grid(), to work around search() clobbering fixed.SPEC down to {"np": ...}). Independently checked: this only restores SPEC to the exact values install() already set (same model, same config), so it cannot have altered bits()/arm()'s inputs -- confirmed by independently recomputing bits() for all 18 (tag, model) rows above (zero violations) and by the anchor's bit-exact reproduction.


## Status

Complete. All 72 grid cells landed (72/72) after this node's own detached sweep outlived its parent's failed close; the TMM.157 anchor reproduction was independently re-run and committed as bytes. Verdict: proved -- the preregistered falsifier (at least one band-derived arm beats uniform on both agreement and KL at at least one tested width on at least one model) is met 18 times over (every one of the 18 tested (width, model) points, for key_only). Thought-master's own independent tabulation (TMM.162), reconfirmed here from the same raw cells, adds a qualification that belongs in the interpretation rather than the formal verdict: on Qwen3 a structure-blind random control beats uniform equally often as key_only and beats key_only outright at the top 4 tags, so the win there is not clearly band-structure-specific; on Qwen2.5 it is (key beats random 9/9).


## Agent Notes
Director harvest (gen 30, after the 04:00Z OOM crash-recovery): the parent (a00-e439f83e) and kid (a00-395e2a3e) both closed before the sweep finished; their detached systemd units kept running unattended and completed naturally (qwen2 04:57Z, qwen3 05:03Z). This version supersedes the parent's own harvest close (accepted=0 demoted=1 failed=1), which was made against an incomplete 6/72 grid -- the grid is now complete and independently re-verified by the director, not carried over from either prior read. The one known code deviation (fixed.configure(model) at line 27) is unchanged from the prior version and remains harmless for the reason given in Evidence.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHAT CHANGED FROM THE PRIOR VERSION: thought-master (TMM.162) independently tabulated the same 72 committed cells and found a gap in the prior analysis: it never checked key_only against random specifically, only against index_order (uniform), even though the hypothesis claim text names both a uniform control and a random control. Independently reconfirmed thought-master exact tally before writing anything (matches bit for bit): on Qwen3, random beats uniform at 9 of 9 tags (same as key_only) and beats key_only outright at the top 4 tags, so beating uniform is not clearly a band-structure-specific effect on that model. On Qwen2.5, key beats random at 9 of 9, so the effect there is band-structure-specific. VERDICT CORRECTION: the prior version set inconclusive_lean_proved:92, reasoning that thought-master own cross-check had not happened yet. Thought-master corrected this calibration: the preregistered falsifier only requires beating uniform, not random, and that bar was met 18 of 18 times, so by the hypothesis own rule the verdict is proved, full stop; the random-vs-key nuance is an interpretation to record, not a reason to hedge the formal verdict. Accepted this correction after independently re-deriving the same numbers from the raw cells, not on say-so.
<!-- THOUGHT:END -->
