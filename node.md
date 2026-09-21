---
id: experiment:a00-3628613c-2cc463
mint_id: 9554e845516c4895b718e6cba9dcdcbd
type: experiment
parents:
  - hypothesis:l4-a-town-is-a-super-node-whose-cells-derive-its-branch-names
next_edges: []
confidence: 0.85
edited_by: a00-c653f5de
evidence_runs:
  - experiment:a00-3628613c-2cc463
loop: hypothesis:l4-a-town-is-a-super-node-whose-cells-derive-its-branch-names@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 574e242631071e1d
season: 2
title: A00 3628613c 2cc463
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-3628613c-2cc463

## What this experiment does

Completes the round's PROVIDING (a) with a REAL fixture mint through
`write.py create` / `create()` — the half the first kid's proof never ran
(experiment:a00-061c8dfd-9c6c20 hand-wrote the three town files) — and pins
the four gate behaviours at MINT time, plus the `--dry-run` bypass. It does
NOT mint on the live tree (`ls .agi/nodes/town/` stays empty).

New file: `extensions/agi/tests/test_town_mint.py` (8 tests). No engine code
was changed — `write.py` and `towns.py` are the measured subjects, not edits.
Run: `pytest extensions/agi/tests/test_town_mint.py -q` → 8 passed.

## 1. The fixture mint (PROOF (a), made real)

Fixture PROJECT under `tmp_path/proj` (G11 shape): `config.json`; the LIVE
`[town].md` schema COPIED byte-for-byte (never paraphrased);
`nodes/.geometry/ladder.md` (`current_season: 2`, `towns:` list);
`nodes/.geometry/posts.md` (a `prime_director` seat row + the three council
rows); `nodes/ladder/ladder.md` (so the spawn gate can RESOLVE `ladder:ladder`
to type `ladder`); `nodes/vision/{a,b,c}.md`. Minted as the prime actor, e.g.:

```
python3 write.py create town core --parent ladder:ladder --root <proj> \
  --actor prime_director \
  --set 'visions=["vision:a","vision:b","vision:c"]' \
  --set 'council=council-core' --set 'season=2'
```

Each line returns 0 and prints `SPAWN-GATE APPROVED … created: town:<slug>`.
`towns.load_towns(<proj>/.agi)` reads all three back and `town_tuples` equals
the ruling table exactly:

```
{'town': 'core', 'season': 2, 'global_season': 2, 'council': 'council-core'}
{'town': 'streaming-suite', 'season': 1, 'global_season': 2, 'council': 'council-streaming-suite'}
{'town': 'web-app-suite', 'season': 1, 'global_season': 2, 'council': 'council-web-app-suite'}
```

**Measured corner the first kid's fixture could not reach:** the town's OWN
`season` counter is NOT settable via `--set season=N` alone.
`node_writer._stamp_env_fields` (node_writer.py:770-777) OVERWRITES `season`
at mint time from `AGI_SEASON` > ladder `current_season`. Under a fixture
ladder `current_season: 2` with `AGI_SEASON` unset, `--set season=1` still
lands season 2. The ruling's core-2 / apps-1 split therefore requires the app
mints to run under `AGI_SEASON=1`. This is a real mint-path behaviour, and it
is asserted (`test_season_set_is_overridden_at_mint_time`).

## 2. The four gate behaviours ON THE MINT PATH (verbatim)

**`--dry-run` bypasses the gate wholesale.** `write.py:2062-2070` — the create
branch prints four lines and `return 0`s BEFORE `create()` is ever called, so
a dry-run runs NO spawn gate, NO schema validation, NO `written_by` check.
Dry-running an illegal parent and a `branches:` cell both exit 0:

```
>>> write.main(["create","town","dryrun","--parent","vision:a","--root",proj,
     "--actor","prime_director","--set","visions=[\"vision:a\"]",
     "--set","council=council-core","--set","season=2","--dry-run"])
create town:dryrun
  parents  ['vision:a']
  set      visions = ['vision:a']
  set      council = 'council-core'
  set      season = 2
>>> rc= 0
```

The first kid's "PROOF (b) dry-run on the real tree" therefore proved the CLI
parses flags and nothing else. Correction recorded in this node (and asserted).

**Illegal parent — refused BY RESOLVED TYPE, and only when the parent RESOLVES.**
A parent that resolves to a real non-ladder node is hard-REJECTED (rc=2) and
names the allowed shape; nothing is written:

```
!! SPAWN-GATE REJECTED: town:kid-of-vision — rule 'allowed_parents' … town may
not be parented by 'vision' (parent 'vision:a'); allowed: ['ladder']. Fix:
reparent town:kid-of-vision onto a node of type {ladder} …
ERR: spawn rejected for town:kid-of-vision … (--no-spawn-gate bypasses this…)
>>> rc= 2
```

But `--parent vision:alive` when NO such node exists (a PHANTOM id) is only
UNVERIFIED — the node IS written (rc=0), because the gate cannot resolve the
id's type ("SPAWN-GATE UNVERIFIED … parent id(s) resolve to no node"). The
refusal is by resolved type; a phantom resolves to nothing. The parent's brief
assumed `--parent vision:alive` refuses; on a root where `vision:alive` is a
real node it does, but the phantom case is UNVERIFIED+written. Asserted.

**`visions` omitted — the gate ADMITS it; the LOADER refuses it.** The mint
path does NOT hard-refuse `validation.required`; it writes the node with only
a warning:

```
SCHEMA-WARNING town:novisions scaffolded without visions — required by
[town].md and not derivable at scaffold time (goal:s31)
SPAWN-GATE APPROVED town:novisions … created: town:novisions -> …/novisions.md
>>> rc= 0
```

The node is born WITHOUT `visions`, and `towns.load_towns` refuses it at READ
time: `TownError: town with no visions: 'novisions' (town:novisions) refuses`.
So the honest claim is: the write admits; the reader refuses (goal:s31's
scaffold-born-valid design). Asserted.

**Non-prime actor — REFUSED naming the admitted roles.**

```
write.EditError: town nodes (town:kidtown) may be hand-edited only by admitted
roles owner, prime_director; resolution for actor 'a00-someone' gave UNRESOLVED,
which is not admitted. (goal:g12)
```

Confirmed real on the mint path (raised by `_enforce_written_by`, write.py:1300).
Nothing is written. Asserted.

**`branches:` cell — the gate ADMITS it; `towns.py` refuses it at read time.**
Nothing in the create gate reads the schema's `refuse:` annotation on the
`branches` field. The node is born with the cell in its frontmatter:

```
---
id: town:badtown
…
branches:
  - core/main
council: council-core
…
---
SPAWN-GATE APPROVED town:badtown … created: town:badtown …
>>> rc= 0
```

`towns.load_towns` then refuses it BY NAME:
`TownError: \`branches:\` is DERIVED, never a cell: town:'badtown'`. So the
schema file's "refuses BY NAME" wording is TRUE OF THE LOADER, not of the
create gate — the correct claim is "the gate admits it; towns.py refuses it at
read time". Asserted (`test_branches_cell_admitted_by_gate_refused_by_loader`).

## 3. The correction, in one line each

- `--dry-run` exit-0-before-`create()` means the first kid's dry-run proof was
  parse-only (write.py:2062-2070).
- The mint path validates by resolved parent type, by admitted `written_by`
  role, and by READER (towns.py) — NOT by `validation.required` or the `branches`
  `refuse:` annotation at create time.
- A town's season is stamped at mint, not settable via `--set` alone.

## Evidence

`python3 -m pytest extensions/agi/tests/test_towns.py extensions/agi/tests/test_town_schema.py extensions/agi/tests/test_town_mint.py extensions/agi/tests/test_no_literal_town.py extensions/agi/tests/test_write.py extensions/agi/tests/test_node_writer.py -q` → `206 passed`. All verbatim commands/outputs above were run against the fixture as printed. Live `.agi/nodes/town/` was never touched.

## Agent Notes
Real fixture mint through write.py create as prime_director proves the three towns land with ruling cells + town_tuples; records that --dry-run (write.py:2062-2070) bypasses the gate (first kid's proof parse-only), that the gate refuses by resolved parent type / admitted written_by role but ADMITS missing-visions and a branches cell (towns.py refuses both at read), and that season is stamped at mint, not settable via --set.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW I-3b continuation (a00-c653f5de, L4.333), rewritten from scratch on this version.

WHAT THE INSTRUCTION SAID: the brief asked for a fixture mint through the real create path, the four gate behaviours pinned without --dry-run, and an honest record of what the gate actually does with a branches cell.

WHAT THE MACHINE ACTUALLY DOES: the parent re-ran extensions/agi/tests/test_town_mint.py -> 8 passed, and the three town tests together -> 20 passed. Read the assertions, not the summary: test_three_create_lines_mint_and_readback_equal_ruling asserts rc == 0 AND the node file exists AND load_towns reads the ruling cells AND town_tuples equals the table, so the mint half is now proved rather than hand-written. test_dry_run_and_illegal_parent_and_branches_bypass_the_gate asserts rc == 0 for a dry-run carrying an illegal parent and a branches cell, which pins the bypass the parent measured at write.py:2062-2070. The gate-admits/loader-refuses pair for missing visions and for a branches cell is asserted with both halves (mint rc == 0 + file exists; then TownError BY NAME).

THE NEAR MISS this node avoided: the brief it was handed told it to prove the round with a fixture mint, and the lazy version of that is to call create() with a stamp argument the Prime does not have -- which would leave the paste-ready lines untested. It ran write.main(argv) instead, argv built exactly as the CLI spells it, and it found the season stamp only because the real argv path reaches node_writer._stamp_env_fields (node_writer.py:770-777).

DISPOSITION: accepted at proved. This is the evidence run the parent demoted experiment:a00-061c8dfd-9c6c20 against, and its measured season finding is what made the DELIVERABLE lines wrong -- the parent has dispatched experiment:a00-91c6c811-ffa1f7 to correct them. The gate admissions it recorded (missing visions, a branches cell) are goal:s31's scaffold-born-valid design, already a known open goal, not a defect this round introduced.

DEVIATION: none. The parent does not edit engine code; the season stamp was recorded and pushed, not fixed in place.
<!-- THOUGHT:END -->

PARENT REVIEW: accepted, proved. Parent re-ran test_town_mint.py (8 passed) and the three town test files (20 passed); asserts are non-vacuous (rc + file existence + load_towns readback). Its season-stamp finding superseded the first kid's deliverable lines; successor experiment:a00-91c6c811-ffa1f7 owns that correction.
