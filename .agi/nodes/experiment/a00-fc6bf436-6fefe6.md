---
id: experiment:a00-fc6bf436-6fefe6
mint_id: 0ea729018f0e47739238876ae7cb049a
type: experiment
parents:
  - hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes
next_edges: []
confidence: 0.9
edited_by: a00-fc6bf436
evidence_runs:
  - experiment:a00-fc6bf436-6fefe6
loop: hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 741fbf452badbfdb
season: 2
title: The collision fallback re-renders with the whole stand-in set, red-first
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-fc6bf436-6fefe6

Two residues from the DH.473 corrective slice. Both closed. 0 production lines (the
test file is the only code; the manifest was not touched).

## Residue 1 — the collision fallback compared MIXED bytes

`_anonymized_live_render` masks a derived identity token whose value ALSO occurs
outside its `{{K}}` sites. The old fallback then re-rendered with the stand-in for the
MASKED keys only:

    over = {k: STANDINS[k] for k, _, _ in masked}
    out = R.rendered(piece, R.values(CFG, MEASURED, {**tokens, **over}))

Every other identity key stayed at its HOST value, while the committed fixture was
rendered with the stand-in for ALL of them. So on a colliding box the comparison is
host/stand-in bytes against all-stand-in bytes: red for a reason unrelated to the
claim, and green by accident on any box whose host value equals its stand-in.

| | what the path compares |
|---|---|
| clean path | by-value substitution of every identity key → all stand-ins |
| fallback (before) | re-render with the stand-in for the masked keys ONLY → mixed |
| fallback (after) | re-render through `_with_the_whole_stand_in_set` → all stand-ins |

FIX: one helper, `_with_the_whole_stand_in_set(piece, tokens)`, a SINGLE mapping
`{**tokens, **{k: STANDINS[k] for k in IDENTITY}}` that both paths agree on — the clean
path by substitution, the fallback by re-render. A key with no `{{K}}` site is harmless
in it: a value no placeholder consumes never reaches the render.

## Residue 2 — b04fa632's body overcounted its own manifest

Measured, not asserted: `manifest.json` = 24 rows, 24 `fixture_sha256` cells, 24
`*.fixture` on disk (`measurements.json` and `standins.json` are inputs, not fixtures,
and carry no cell). Body line 36 said `25/25`, line 138 said `25 added`. Both corrected
to 24 through `write.py body_patch`; the rest of that node is untouched. The two
surviving `25/25` strings in it (a probe's `observed` cell and the parent REVIEW) are
historical records of the discrepancy and stay.

## Evidence — red first, then green

New row `test_the_collision_fallback_re_renders_with_the_whole_stand_in_set` (7f). It
WALKS the fallback on this box instead of hoping some box does: tmp only, no live read,
by injecting a synthetic identity token whose value is a template LITERAL —
`OWNER_USER="python3"`, which memguard-script uses outside every `{{OWNER_USER}}` site
— so `seen > sites` and the masked branch is taken. It first asserts the collision
actually forced the branch, so it cannot pass vacuously.

RED, before the fix (`-k collision_fallback`, one failed):

    - subprocess.run([... '-H', 'python3', '/box/agi/extensions/agi/bin/send.py', ...
    + subprocess.run([... '-H', 'python3', '/data/work/agi/extensions/agi/bin/send.py', ...
                       cwd='/box/agi'  ->  cwd='/data/work/agi'
    FAILED ... test_the_collision_fallback_re_renders_with_the_whole_stand_in_set

That is the defect in one diff: the fallback re-rendered the masked key with the
stand-in and left `REPO_ROOT` at the host checkout.

GREEN, after the fix: `1 passed, 179 deselected`. Full file:
`python3 -m pytest extensions/agi/tests/test_boxkit_templates.py -q --basetemp=/tmp/...`
→ **180 passed in 0.31s** (179 before + row 7f), 0 skipped, 0 failed.

`git diff --numstat -- extensions/agi/ ':!extensions/agi/tests/'` → empty: 0 production
lines.

## What this does and does not settle

It does NOT prove a host token ever collides on a real box — the collision is synthetic
on purpose, so the row runs everywhere. It DOES prove the two paths now produce the same
bytes, which is what the fixture comparison assumes. Remaining, named: the arity check
is not a shape check (a `REPO_ROOT` with a trailing slash substitutes back and stays
green) — that is 7b's job, still open.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The fallback overrode only the MASKED keys and left the rest at host values, so it compared mixed host/stand-in bytes against an all-stand-in fixture -- red for a reason unrelated to the claim, and green by accident wherever a host value equals its stand-in. The branch was also never walked by any row on any box, so nobody had read it; row 7f walks it with a synthetic collision (tmp only, no live unit) so the bytes are compared on a box that does not collide. A count in b04fa632 (25/25) was a measurement, not a quote, and the measurement is 24.
<!-- THOUGHT:END -->

## Agent Notes
Collision fallback now re-renders through one _with_the_whole_stand_in_set helper (all identity stand-ins, no partial override); new row 7f walks the branch with a synthetic literal collision, RED before the fix and GREEN after (full file 180 passed). b04fa632 body counts corrected 25->24. 0 production lines.
