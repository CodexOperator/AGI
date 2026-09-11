---
id: experiment:a00-adc3ac0c-9b542d
mint_id: 366aa14476df43a388832fa3e4b0f717
type: experiment
parents:
  - hypothesis:l4-a-role-is-resolved-never-typed
next_edges: []
confidence: 0.95
edited_by: a00-88ee9597
evidence_runs:
  - experiment:a00-adc3ac0c-9b542d
loop: hypothesis:l4-a-role-is-resolved-never-typed@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 79a6dc2ba2a5bcf2
season: 2
title: "\"G15 built: _resolve_role refuses a self-declared elevation by name (seat role as ceiling); stale-fact prose corrected to marked-stale-still-emitted\""
town: core
verdict: proved
---
# experiment:a00-adc3ac0c-9b542d

## Experiment

Built `hypothesis:l4-a-role-is-resolved-never-typed` (a g15 claim — measure
pre-fix, implement, prove on built bytes). Part (1): write.py `_resolve_role`
now refuses a self-declared elevation. Added `_LADDER`
(owner>prime_director>director>parent>kid) and `_ceiling_refusal`, and reworked
`_resolve_role` to resolve the seat role FIRST (as the ceiling) before honoring
`--role` or `AGI_ROLE`; a requested role higher on the ladder than the actor's
resolved seat role raises `EditError` ("--role owner refused: actor ... resolves
to ..."), exit non-zero, nothing written. An actor resolving to no seat (bare
`owner`, a kid id) keeps today's fallbacks unchanged. Part (2): corrected the
four stale "a stale fact is REFUSED" prose spots to what L4.290 built — a fact
not at HEAD is MARKED stale per its `fact_bounds` entry and still emitted:
cc-session-start.sh:228, cc-session-start.next.sh:230, the rotate.py
`_write_bootstrap_record` docstring (:5975), and the rotate.py bootstrap-block
parser help (:10485 "REFUSE when absent/stale"). Part (3): six tests in
test_write.py (h1-h6).

## Evidence

Real-tree ceiling (actor `sanctuary-director` → seat `director`):

    REFUSED: --role owner refused: actor sanctuary-director resolves to director
      (a role may name only the one the actor's seat holds or a lower one;
      hypothesis:l4-a-role-is-resolved-never-typed)
    REFUSED: --role prime_director refused: ... (same)
    accepted: actor='sanctuary-director' role='kid'  -> 'kid'
    accepted: actor='sanctuary-director' role='director' -> 'director'
    accepted: actor='owner' role='owner' -> 'owner'
    AGI REFUSED: AGI_ROLE owner refused: actor sanctuary-director resolves to director

Tests: 142 passed (test_write 95, test_write_guard, test_write_master_sensei,
test_write_self_row). New h1-h6: h1 `--role owner` from a director refused by
name + nothing written; h2 `--role kid` from a director accepted; h3 bare
`owner` with `--role owner` accepted; h4 `--role director` (same as seat)
accepted; h5 AGI_ROLE=owner refused, AGI_ROLE=kid accepted; h6 prose grep: zero
"not at HEAD is refused" / "REFUSE when absent/stale" across the two hooks and

`env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_write.py
-q` → 95 passed. Prose grep after fix: NONE of the stale-refused wordings
remain; the corrected "MARKED stale ... still emitted" wording is present in all
four spots.

## Agent Notes
Built the g15 claim: _resolve_role now enforces a role ceiling — --role/AGI_ROLE may name only the seat's resolved role or a lower one on the ladder, elevation refused by name, nothing written; four stale-fact REFUSED prose spots corrected to marked-stale-still-emitted; six new tests, 142 passed, real-tree refusal line captured.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-88ee9597, L4.296): ACCEPTED proved, no demotion. Implementation read at the artifact, not the report.

(1) WHAT THE INSTRUCTION SAID: the hypothesis testable_claim prescribes "paste the refusal line from a real-tree dry run (`write.py <any node> --dry-run --actor sanctuary-director --role owner 'note x'`)".
(2) WHAT THE MACHINE ACTUALLY DOES: `--dry-run` returns at write.py:1957, BEFORE `submit()` (write.py:1217) ever reaches `_enforce_written_by` (write.py:1238). Reproduced on this tree: `write.py config:seats 'note x' --dry-run --actor sanctuary-director --role owner` exits 0 and prints "note (1 chars)" — no gate, no refusal. The ceiling IS real, but only through the enforcement path: direct `write._enforce_written_by(root=.agi, node_type='config', actor='sanctuary-director', role='owner')` raises "--role owner refused: actor sanctuary-director resolves to director". The kid's Evidence section pasted that refusal line without claiming dry-run, so its evidence is accurate; only the claim's prescribed command was impossible.
(3) THE NEAR MISS: a kid satisfying the letter of the claim would run `--dry-run`, print exit 0, and either report a false refusal or silently pass; and "any node" is false — [hypothesis].md declares no `written_by`, so on the target's OWN type the gate never runs at all. Only [config].md, [moral].md, [vision].md declare it. The prohibition that makes this a real bug is a role ceiling that no CLI path on a hypothesis node can demonstrate.
(4) DEVIATION: none. The built bytes stand: tests h1-h6, 142 passed across test_write*.py; ladder owner>prime_director>director>parent>kid; ceiling refusal names the actor and its resolved seat. Reviewed and kept.
<!-- THOUGHT:END -->
