---
id: experiment:a00-fc6bf436-6fefe6
mint_id: 0ea729018f0e47739238876ae7cb049a
type: experiment
parents:
  - hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes
next_edges: []
confidence: 0.9
edited_by: a00-e5014ec9
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
PARENT RE-REVIEW (DH.473). What the instruction said, quoted: "A kid that passes its own tests and fails your probe is lean_disproved, with the probe NAMED." What the machine actually does, cited to bytes: mutating test_boxkit_templates.py:410 back to the masked-only override {**tokens, **over} turns row 7f (:430) red on the exact host-vs-stand-in bytes, and neutralising the synthetic collision string turns it red on the branch-forcing assert, so the claim "the two paths now produce the same bytes" is the thing the suite actually decides and not a restatement of the code. The manifest counts (24 rows, 24 cells, 24 files) are a measurement I repeated against the file, and the b04fa632 body now carries 24 in both places it asserts its own work. NEAR MISS: accepting the kid own red-first paste as the red-first -- a transcript of a run is not a run, and a mutation run is reproducible by the next parent in one command. IF I DEVIATED from a standing rule, the property of THIS case: the standing rule bans git to a kid so a shared worktree commit cannot sweep up a half-written node; my mutation probe needed the file inside the tests dir because the suite derives PROJECT from parents[3] of __file__, and I honoured the rule by writing the mutant to a sibling file and deleting it in the same command, so the tree I handed back carries no artifact of the probe. The kid is accepted; the shape-vs-arity residue is named in the review and left to 7b.
<!-- THOUGHT:END -->

## Agent Notes
Collision fallback now re-renders through one _with_the_whole_stand_in_set helper (all identity stand-ins, no partial override); new row 7f walks the branch with a synthetic literal collision, RED before the fix and GREEN after (full file 180 passed). b04fa632 body counts corrected 25->24. 0 production lines.

PARENT REVIEW (DH.473, a00-e5014ec9) -- ACCEPTED, verdict proved, on five probes I ran myself, never on the kid own suite. (1) GATE/MUTATION: a sibling copy of the suite inside the same tests dir (so PROJECT = parents[3] still resolves) with _anonymized_live_render reverted to the pre-fix masked-only override {**tokens, **over} -- row 7f goes RED, and it fails on exactly the mixed bytes (expected /box/agi/... vs got /data/work/agi/...): the fix is load-bearing, the row is a real falsifier. (2) GATE/VACUITY: with collides = "zzz-not-a-literal-9" the first assert fires RED ("the synthetic collision did not force the fallback: 5 occurrence(s), 5 site(s)"), so the branch-forcing assertion is live and 7f cannot pass without really entering the branch. (3) WIRE: read the bytes, not the summary -- _with_the_whole_stand_in_set at :363-372 is ONE mapping {**tokens, **{k: STANDINS[k] for k in IDENTITY}} and the fallback at :410-411 calls exactly that helper; no partial override survives anywhere in the file. (4) MEASUREMENT: manifest.json parses to 24 rows / 24 fixture_sha256 cells / 24 .fixture files; b04fa632 :36 now reads 24/24 and :138 reads "24 added", while :18 and :171 keep their 25/25 strings as the historical record of the discrepancy -- correct, a correction must not rewrite the probe that found it. (5) FENCE: I ran the whole file myself -- 180 passed, 0 skipped, 0 failed -- and no committed row reads a live unit. NEAR MISS the kid avoided, named so a later reader does not undo it: making the fallback re-render with the stand-in set for the masked keys PLUS hard-coding the remaining identities per piece, which satisfies "the fallback is fixed" in letter while leaving a second source of what a fixture is. ONE RESIDUE, carried and NOT closed here: the arity check is still not a shape check (a REPO_ROOT with a trailing slash substitutes back and stays green) -- 7b, out of this scope.
