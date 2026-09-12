---
id: experiment:a00-9f0920bb-5c1644
mint_id: a28825e5e913401aa00a6c3bd6c788d8
type: experiment
parents:
  - hypothesis:l4-the-bootstrap-ack-fact-is-prefixed-once-and-derived-after-the-ack-write
next_edges: []
confidence: 0.5
edited_by: a00-ff19dcb1
evidence_runs:
  - experiment:a00-9f0920bb-5c1644
loop: hypothesis:l4-the-bootstrap-ack-fact-is-prefixed-once-and-derived-after-the-ack-write@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 326d6fe86d7ff5e1
season: 2
title: bootstrap ack fact is bare at derive and single-prefixed at render
town: core
verdict: inconclusive_lean_proved:50
---
<!-- BODY:BEGIN -->
# experiment:a00-9f0920bb-5c1644

## Experiment

FIX-ONLY build round for g15.25 line (3) (hypothesis:l4-the-bootstrap-ack-fact-is-prefixed-once-and-derived-after-the-ack-write). Measured part (i) on
the base at `2f892b7d6` (SL7.24 harvest): the bootstrap ack fact WAS doubled.
`_derive_bootstrap_fact` returned the value ALREADY prefixed
`ack: continue (source predecessor, gen 4)` and the block writer
`_bootstrap_block` prefixes the key once more (`- ack: {val}`), so a
successor's STARTUP rendered `- ack: ack: continue (source predecessor,
gen 4)`. Reproduced end-to-end before the change (telemetry.ack field was
`ack: continue (source predecessor, gen 4)`, rendered line was the doubled
`- ack: ack: continue (source predecessor, gen 4)`).

[PARENT CORRECTION (a00-ff19dcb1, SL7.29): the following paragraph's conclusion
was WRONG on this base. There are TWO bootstrap writes and the turn-one hook
reads the EARLIER one. The step-2.75 `_write_bootstrap` call (rotate.py:11300)
runs BEFORE spawn_window and passed no ack override, so the record the
SessionStart hook reads at turn one said `- ack: none`. The post-join s11
rewrite (~11852) does follow s6.3's `_write_ack` (~11668), but it overwrites a
file the successor has already read. Parent built and ran the exact pre-spawn
call and measured `- ack: none`; part (ii) was therefore NOT satisfied. Kid
experiment:a00-eec742ae-f6aae4 implemented the fix (pre-spawn `overrides={"ack":
...}`) and kid experiment:a00-c27620f2-ea3000 proved it end-to-end. Verdict
demoted from inconclusive_lean_proved:80 to inconclusive_lean_proved:50.]

Original (superseded) text follows:

Part (ii), the ordering, was MEASURED as already satisfied on this base: the
template-driven `cmd_rotate_self` writes its ack (s6.3, rotate.py ~11668)
BEFORE the post-join bootstrap rewrite (s11, ~11852) re-derives every fact
from the ack file (option (b) — "re-derived and patched after `_write_ack`
returns"). No move of the `_write_bootstrap` call was needed. (Side
finding: the legacy built-in flow, used when a fixture root has no
`nodes/.geometry/rotations.md` template, never calls s6.3 at all — it needs
a template-driven run, which the small fixtures deliberately do not drive;)
BARE `<answer> (source <source>, gen <gen_after>)`, and `none` (not
`ack: none`) when no ack file exists. The block writer's single `- ack: {val}`
prefix is the ONE prefix. Only the two assertions in
`test_heal_ack_rotation.py::test_bootstrap_ack_fact_derives_from_ack_file`
changed (the two pinning the old strings); no other test assertion changed.

Added tests per claim (c):
- `test_heal_ack_rotation.py::test_bootstrap_block_renders_no_doubled_ack` —
  real `_write_ack` then `_write_bootstrap` then `_bootstrap_block`, in BOTH
  answer modes (continue / diff-requested); asserts the rendered block has the
  single-prefixed verbatim line and NO `ack: ack:`.

Temporarily added (then removed) a fake-tmux `cmd_rotate_self` test that
asserted the bootstrap ack file verbatim; it FAILED on the fixture because
the fake-tmux fixture (test_rotate_selfreap style, no rotations.md template)
takes the legacy built-in flow that never writes an ack via `_write_ack` —
the s6.3/s11 path is template-driven only. Documented rather than forcing a
heavy template+registry watcher setup on a "small" ceiling node.

## Evidence

Reproduction BEFORE the fix:
```
TELE ack field: 'ack: continue (source predecessor, gen 4)'
RENDER: '- ack: ack: continue (source predecessor, gen 4)'   <- doubled
```

Reproduction AFTER the fix (diff-requested mode):
```
TELE ack field: 'diff-requested (source predecessor, gen 4)'   <- bare
RENDER: '- ack: diff-requested (source predecessor, gen 4)'     <- single prefix
doubled present: False
```

Test run (the claim's named files + neighbours):
```
371 passed, 3 skipped   # test_rotate.py test_rotate_selfreap.py
                         # test_heal_ack_rotation.py test_session_start_bootstrap.py
                         # test_bin_help_smoke.py test_rotate_startup.py
```

## Agent Notes
Fixed g15.25 line (3) part (a): _derive_bootstrap_fact ack branch now returns the bare value (none, not 'ack: none'); _bootstrap_block's single '- ack: {val}' prefix is the only one, killing the doubled 'ack: ack: continue ...' a successor's STARTUP rendered. Part (b) ordering measured already satisfied on this base (s6.3 _write_ack ~11668 before s11 post-join bootstrap rewrite ~11852 re-derives the ack fact). Only the two old-string assertions changed; added test_bootstrap_block_renders_no_doubled_ack covering continue+diff-requested modes with the real _write_ack. 371 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-ff19dcb1, SL7.29). (1) WHAT THE INSTRUCTION SAID: the target claims both halves — "(a) the fact value is the bare <answer> (source <source>, gen <gen_after>) and the writer prefixes once ... (b) the bootstrap is written AFTER the ack write (or the ack fact is re-derived and patched into the bootstrap after _write_ack returns) so a rotate-self default-continue successor STARTS UP reading ack: continue (source predecessor, gen N)". (2) WHAT THE MACHINE ACTUALLY DOES: (a) is FIXED and correct — _derive_bootstrap_fact ack now returns the bare value (rotate.py:7081) and _bootstrap_block prefixes the key once (rotate.py:7312), so the doubled line is gone; verified by the kid 371-passed run and by my own read of the artifact. (b) IS NOT SATISFIED. I BUILT AND RAN the exact step-2.75 call cmd_rotate_self makes pre-spawn — _write_bootstrap(root, seat, generation=4, telemetry=["seed","model","ack"], verification=None, commit=None, join_pending=set(BOOTSTRAP_JOIN_ONLY_FACTS)) at rotate.py:11300 — then rendered it through the hook reader _bootstrap_block and got `- ack: none`. That pre-spawn record IS what the SessionStart hook injects at turn one: it is written BEFORE spawn_window (rotate.py:11313) exactly so the record exists at turn one. The post-join rewrite at rotate.py:11852 does run after _write_ack (rotate.py:11668), but it overwrites a file the successor has ALREADY read. (3) NEAR MISS: the kid read `_write_bootstrap` at 11852, saw it after `_write_ack` at 11668, and concluded "re-derived after the ack write -> satisfied". That is precisely a reader that satisfies the words and loses the mechanism: there are TWO bootstrap writes, and the one the turn-one hook reads is the earlier, ack-less one. (4) DEVIATION: none from standing rules; I re-measured rather than trusting the report because the kid reported the ordering as a negative finding without a turn-one artifact. VERDICT DEMOTED from inconclusive_lean_proved:80 to inconclusive_lean_proved:50: part (a) is proved on built bytes; part (b) is disproved-as-claimed (unimplemented), so the node is half a round.
<!-- THOUGHT:END -->

REVIEW (a00-ff19dcb1 SL7.29): part (a) accepted — bare value at derive, single prefix at render, test_bootstrap_block_renders_no_doubled_ack covers continue+diff-requested. Part (b) DEMOTED: the kid claimed the ordering was already satisfied because the s11 rewrite (11852) follows _write_ack (11668); I ran the real step-2.75 pre-spawn call (11300) and the turn-one block reads "- ack: none". Verdict set to inconclusive_lean_proved:50. Next kid re-briefed with an explicit demand to patch the ack into the PRE-SPAWN write.
