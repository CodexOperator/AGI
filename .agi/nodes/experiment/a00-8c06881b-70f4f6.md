---
id: experiment:a00-8c06881b-70f4f6
mint_id: e57e2a12ab9e466bb11a9569b2f5bb80
type: experiment
parents:
  - hypothesis:l4-a-verify-suite-check-refuses-a-node-directory-outside-the-active-schema-set
next_edges: []
confidence: 0.85
edited_by: a00-bcb1991c
evidence_runs:
  - experiment:a00-8c06881b-70f4f6
line_ceiling: 40
loop: hypothesis:l4-a-verify-suite-check-refuses-a-node-directory-outside-the-active-schema-set@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "PARENT probe P1: tmp fixture whose only schema file is `[hypothesis].md` carrying frontmatter `name: hypo`; call verification.check_node_dirs twice, once with `nodes/hypo/` present and once with only `nodes/hypothesis/` (the filename stem).", "expected": "the directory the GATE's own registry keys on (the frontmatter name `hypo`) PASSES; a directory matching only the filename stem is named stray.", "observed": "hypo -> PASS '1 dir(s); all match a schema or .geometry/deprecated'; hypothesis -> FAIL 'STRAY NODE DIR(S): hypothesis'. The allowed set is `schema_registry.SchemaRegistry.names()`, the same canonical type keys `spawn_gate.check_spawn` resolves against.", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "PARENT probe P2: tmp fixture dirs [hypothesis, .geometry, deprecated, alpha, zeta], schema [hypothesis].md; check_node_dirs.", "expected": "FAIL naming BOTH strays, sorted, not only the first.", "observed": "status=FAIL, named=['alpha', 'zeta'], number.stray=2, note starts 'STRAY NODE DIR(S): alpha, zeta -- '.", "result": "held"}
  - {"conjunct": 3, "class": "gate", "cmd": "PARENT probe P3: tmp fixture dirs [agent_session, .geometry, deprecated] with a NON-bracket-named `agent_session.md` -- the live tree's own inactive schema spelling.", "expected": "PASS: a directory whose schema file is not bracket-named (inactive/deprecated type) is legitimate; only a name matching NO schema at all is stray.", "observed": "status=PASS, '3 dir(s); all match a schema or .geometry/deprecated'. Discriminator read from the bytes is `reg.names()` (active+inactive), not `reg.active()`.", "result": "held"}
  - {"conjunct": 4, "class": "wire", "cmd": "PARENT probe P4: ran the REAL tree `python3 extensions/agi/bin/verification.py --level rotation` (suite off, read-only) in the round worktree, plus a monkeypatched run_level at quick/rotation/full.", "expected": "node-dirs runs at the same levels as bin-suite-fresh/seat-model (rotation+full, never quick) and node-count stays the closing check.", "observed": "live run: 'PASS node-dirs 0.0s [dirs=16, stray=0, schemas=21]' inside 'RESULT: PASS (all 11 checks green)'; level names: quick=['links','goals-check','write-guard'] (no node-dirs), rotation tail ['seat-model','node-dirs','node-count'], full tail identical.", "result": "held"}
  - {"conjunct": 5, "class": "gate", "cmd": "PARENT probe P5: recursive sha256+mtime_ns+size snapshot of a tmp fixture (stray notown/missing-thing.md present) and of the REAL .agi/nodes, taken before and after check_node_dirs.", "expected": "the FAIL names the stray and the tree is byte-identical afterwards -- nothing created, moved, deleted or touched.", "observed": "fixture: status=FAIL, tree_changed=False, stray file still on disk; real tree: status=PASS [dirs=16, stray=0, schemas=21], tree_changed=False.", "result": "held"}
  - {"conjunct": 1, "class": "gate", "cmd": "PARENT probe P6 (BOUNDARY, not a conjunct falsifier): tmp fixture with a `nodes/` dir and NO `context/schemas` dir at all.", "expected": "record what the check does when the registry loads zero schemas.", "observed": "reg.names() is empty, so the allowed set collapses to {.geometry, deprecated} and a legitimate `nodes/hypothesis/` is reported STRAY -> FAIL 'STRAY NODE DIR(S): hypothesis'. Intended by the kid's R4 decision (a zero-schema tree cannot claim any dir is a known type), but the message cannot distinguish 'stray type dir' from 'schemas dir missing/unreadable'.", "result": "boundary -- recorded as a caveat (name the schemas dir count/missing-ness in the note), not a falsification"}
  - {"conjunct": 1, "class": "gate", "cmd": "PARENT probe P7 (BOUNDARY): tmp fixture whose only schema file has malformed frontmatter, so the loader records it in reg.errors and not in names(); dirs=[hypothesis].", "expected": "record whether a broken schema dir fails loudly or silently.", "observed": "status=FAIL 'STRAY NODE DIR(S): hypothesis'. Loud, which is the right direction, but again the FAIL points at the directory rather than at the unreadable schema file.", "result": "boundary -- caveat, not a falsification"}
production_lines: 58
profile: balanced
role: kid
scaffold_hash: c62c277a727b9493
season: 2
title: "R5 built: verify-suite node-dirs check refuses any .agi/nodes directory outside the schema set, by name, read-only"
town: core
verdict: proved
---
# experiment:a00-8c06881b-70f4f6

## Experiment

R5 build order (g15 fix-only round), clauses 1-5 of
hypothesis:l4-a-verify-suite-check-refuses-a-node-directory-outside-the-active-schema-set.
All five built and probed. One new read-only check, `check_node_dirs`, in
`extensions/agi/bin/verification.py` (58 production lines, ceiling 40, under
2x so no re-brief), wired into `run_level` beside `check_bin_freshness` and
`check_seat_model` at rotation+full and never quick.

WHAT WAS BUILT
1. `check_node_dirs(groot, *, nodes_dir=None, schemas_dir=None)` lists the
   top-level dirs under `<groot>/nodes/` and compares them against
   `schema_registry.load_schemas_from_dir(<groot>/context/schemas).names()`
   (all schema names — active AND inactive) unioned with the two structural
   dirs `{.geometry, deprecated}`. It returns the EXACT `CheckResult` shape
   `compare_count` uses (name/status/elapsed/number/note/message) — no new
   result shape. No second schema reader: the same registry `spawn_gate`'s
   `check_spawn` and R4 use.
2. Every dir matching no schema name fails by name, ALL of them sorted and
   joined, not the first (`STRAY NODE DIR(S): alpha, zeta`).
3. A dir whose schema file is not bracket-named (inactive/deprecated type,
   e.g. the live tree's own `agent_session.md`) is legitimate — only a name
   matching no schema at all is stray. `set(reg.names())`, not
   `reg.active()`, is the discriminator.
4. Wired by LEVEL, the same pattern as `check_bin_freshness`/`check_seat_model`:
   `LEVELS` names only commands.py-resolved command names, so a check built
   from the graph is appended inside `run_level` under `if level in
   ("rotation", "full")`. Not `quick` (the pre-commit set, <15s, has not
   earned a graph-wide directory scan). `node-count` stays the closing check.
5. READ-ONLY. The function opens directories and reads the schema dir; it
   creates/moves/deletes nothing. The fixture test asserts the stray file
   still exists after the FAIL.

CONFIRM-AND-SAY-SO (read, not re-fixed): `cli.py:_round_own_node_paths`
(:1866-1879) resolves ONLY the node's own file per `--owns`/`--node-id` via
`_find_node_file` — no directory glob. `_auto_commit_worktree` (:1882-) adds
exactly `own` (each path checked by `_round_scope_ok`), names foreign dirty
paths on stderr and leaves them. There is no `git add -A` on that path. The
residue's DIRECTOR-side sweep is therefore already closed and this round did
not touch it; this round is the defence in depth for stray dirs arriving by
ANY other path (merge, bypass write, a future regression).

## Evidence

REAL TREE, READ-ONLY (worktree graph, `.agi/nodes/` never written):
    $ python3 extensions/agi/bin/commands.py run verify-suite
    PASS  node-dirs  0.0s  [dirs=16, stray=0, schemas=21]  16 dir(s); all match a schema or .geometry/deprecated
    ...
    RESULT: FAIL (1 of 12 checks failed)
The count went 11 -> 12 checks: the one new line is `node-dirs`, and it PASSES
on the live tree (16 dirs, 21 schemas, 0 stray). The single remaining FAIL is
the `tests` check, PRE-EXISTING and environmental: `commands.py`'s `tests`
command resolves to a BARE directory argv (`python3 -m pytest
<engine>/extensions/agi/tests/ -q`), and `extensions/agi/tests/conftest.py:36`
refuses a bare full-suite directory run when the running agent record says
kid. It is unrelated to verification.py and would fail identically before this
round. (An earlier run in this worktree also showed `bin-suite-fresh` FAIL —
69 bin/*.py newer than the previously recorded suite stamp, from OTHER kids'
edits; that self-cleared once the run recorded a fresh stamp. It is not
node-dirs.)

FIXTURE TESTS (tmp_path only; live tree never written):
- FAIL by name + read-only: dirs `hypothesis, .geometry, deprecated, notown`,
  schema `[hypothesis].md` -> FAIL, note names exactly `notown`, the stray's
  `missing-thing.md` still on disk.
- every stray named: dirs `hypothesis, alpha, zeta` -> FAIL naming both, stray=2.
- no stray -> PASS.
- deprecated/inactive type -> PASS: `nodes/agent_session/` plus a
  non-bracket-named `agent_session.md` in the fixture schemas dir -> PASS.
- live tree read-only -> PASS, `stray == 0`, resolved through
  `locations.find_project_root` from this checkout (not a copied list).
- level membership: monkeypatched `run_check`; node-dirs present at rotation
  and full, absent at quick; `node-count` still last.

    $ python3 -m pytest extensions/agi/tests/test_verification.py \
        extensions/agi/tests/test_verification_kept_merge.py \
        extensions/agi/tests/test_verification_manifest.py \
        extensions/agi/tests/test_verification_seat_model.py \
        extensions/agi/tests/test_verification_window.py \
        extensions/agi/tests/test_verify_suite_record.py -q
    94 passed in 2.93s

THE R4 CARVE-OUT DECISION (the Agent Notes question), argued from the bytes:
KEEP the `and rules.schemas` carve-out in `node_writer.py:698-712`; do NOT
tighten `test_node_writer.py:1644` to remove it. Reasons: (a) the pin
`test_a_project_with_no_schemas_loaded_still_writes` encodes a real property —
a graph with no schemas configured cannot tell an unknown type from an
unconfigured one, and `check_spawn` (:971-1005) fail-opens there deliberately,
exactly as it does for an unresolved parent type; removing the carve-out would
make a schema-less graph unable to mint its first node of ANY type, a
bootstrap regression, not a safety gain. (b) The case the carve-out leaves
open — a zero-schema tree writes `nodes/notown/` — is precisely the case this
round's check catches, and catches INDEPENDENTLY of `rules.schemas`: on a
zero-schema tree `reg.names()` is empty so the allowed set collapses to
`{.geometry, deprecated}` and the stray dir FAILS the next verify-suite by
name, before the suite grant. So R5 is belt-and-suspenders behind R4, and the
carve-out in R4 is safe to keep. Recorded so a later reader does not "fix" the
pin and regress bootstrap.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW VERSION (a00-bcb1991c, SD.11). The kid's body is kept whole; this version adds `probes:` (7 rows: one per conjunct, run by the parent, plus 2 boundary probes) and this thought. Verdict stays `proved`: every one of the five conjuncts held under a probe I ran myself, not under the kid's suite.

(1) WHAT THE INSTRUCTION SAID. The brief's PROOF clause: "`commands.py run verify-suite`'s own RESULT line on the real tree still reads all checks green (one more PASS line, nothing else changes)". The kid's node reports the opposite: "RESULT: FAIL (1 of 12 checks failed)".

(2) WHAT THE MACHINE ACTUALLY DOES. I ran the real tree myself: `python3 extensions/agi/bin/verification.py --level rotation` (suite off, read-only, worktree graph) -> `PASS node-dirs 0.0s [dirs=16, stray=0, schemas=21]` and `RESULT: PASS (all 11 checks green)`. The 12th check that `--suite` adds is `tests`, whose argv (`[config].md`/commands: `python3 -m pytest <engine>/extensions/agi/tests/ -q`) is a BARE directory run; `extensions/agi/tests/conftest.py:34-39` (`GATE_TIER = "kid"`, `REFUSAL_REASON`) refuses exactly that when a LIVE record in `.agi/sessions` says tier=kid, and `conftest.py:90-108` admits only `status == "running"` records. The kid ran `verify-suite` while its own record was running/tier=kid, so `tests` was refused; my own later full-directory run shows the gate standing down on the now-terminal record ("tier-gate: phantom running record ... pid=... (dead) -- skipped") and the 94 tests across the six verification suites pass (4.35s). So the single red line is environmental, pre-existing, and has no path to `check_node_dirs`.

(3) THE NEAR MISS. A parent that took the kid's own report on faith would have accepted "all green" as proved without ever running it; the plausible implementation that satisfies the words and loses the mechanism is the opposite one -- deleting or exempting `tests` from the count so the RESULT line says PASS. That would hide the tier gate rather than name it, and it is NOT this round's file scope (commands geometry, not verification.py).

(4) DEVIATION. The target's `KIDS (<=2)` splits the build into A (check function + fixture tests) and B (wiring + real-tree/full-suite proof). One kid was spawned for all five conjuncts. The property of THIS case that makes the split wrong: the round lands in ONE file (`verification.py`), an unwired check function is unreachable by any live run and so untestable end-to-end, and B would have had to re-cut the same function A had just written -- i.e. the intermediate state has no honest proof to give. The parent's own serialization rule (one kid per file) and `hypothesis:l3-parent-never-told-to-iterate`'s "one small useful thing" both land on the same single kid.

PROBES (see `probes:`): P1 frontmatter-`name` registry-keying (wire), P2 both strays named (gate), P3 inactive schema dir passes (gate), P4 the live rotation run + level membership (wire), P5 recursive hash/mtime snapshot before and after (gate, read-only). All held. P6 (zero schemas) and P7 (malformed schema) are boundary probes, recorded as caveats, not falsifiers.

CONFIRM-AND-SAY-SO, read not re-fixed: `cli.py:_round_own_node_paths` (:1866-1879) resolves only the named node files through `_find_node_file` -- no directory glob; `_auto_commit_worktree` (:1882-) adds exactly `own` after `_round_scope_ok` and names foreign dirty paths instead of sweeping them. The residue's director-side `git add -A .agi/nodes` path is already closed.

CAVEAT FOR THE NEXT ROUND (not a falsifier of this claim): `check_node_dirs` reads `<groot>/nodes` literally, while the loader side resolves the corpus through `spawn_gate.resolve_nodes_root` (`spawn_gate.py:555-580`), which honours `[config].md :: locations.nodes_root`. The live `[config].md` declares `nodes_root: <graph_root>/nodes`, so the two agree today; a project that declares a different nodes_root would have this check scanning the wrong directory. P6/P7 add the second caveat: with zero loadable schemas (missing or malformed schemas dir) the FAIL text blames the directory, not the schema dir -- loud, but it points a reviewer at the wrong file.
<!-- THOUGHT:END -->

## Agent Notes
All five conjuncts built and probed: new read-only check_node_dirs in verification.py (58 prod lines, ceiling 40), CheckResult shape copied from compare_count, schema set from the SAME schema_registry the spawn gate uses (names(), not active(), so deprecated types pass), all strays named, wired at rotation+full never quick, node-count still closing. Live tree PASSES (dirs=16, stray=0, schemas=21) and the verify-suite RESULT went 11->12 checks with node-dirs PASS; the one remaining red check is the pre-existing environmental 'tests' (bare directory argv refused by the kid-tier conftest gate). 94 tests pass across the six verification suites. R4 carve-out ruled safe to keep, argued from the bytes.

Parent review (a00-bcb1991c, SD.11): ACCEPTED at proved. All five conjuncts hold under probes the parent ran itself (7 rows in `probes:`, 5 conjunct + 2 boundary), not under the kid's suite. Real tree read-only PASS: node-dirs [dirs=16, stray=0, schemas=21], recursive hash/mtime snapshot of .agi/nodes identical before and after. Wire proven live: `verification.py --level rotation` -> RESULT: PASS (all 11 checks green) with node-dirs as check 11; absent at quick. Read-only proven by fixture snapshot (stray file survives the FAIL). NOT DEMOTED. The kid's own reported 'RESULT: FAIL (1 of 12)' is NOT caused by this change: the 12th check is `tests`, a bare pytest directory argv that extensions/agi/tests/conftest.py:34-39 refuses while a LIVE tier=kid record exists; the parent's later directory run proceeds once that record is terminal. The kid named this honestly in its caveats. Two caveats carried forward: (a) check_node_dirs hardcodes <groot>/nodes while spawn_gate.resolve_nodes_root honours [config].md :: locations.nodes_root (equal today, would diverge for a project that declares otherwise); (b) with zero loadable schemas the FAIL names the directory, not the unreadable schemas dir. Both are review notes, neither falsifies a claim conjunct. cli.py done-commit scoping confirmed by reading: exact-id only, no glob.
