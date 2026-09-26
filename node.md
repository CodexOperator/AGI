---
id: experiment:a00-4a01c17b-415791
mint_id: 2aae4db06fd14d7fb70ec737a966269f
type: experiment
parents:
  - hypothesis:non-prime-rotate-self-renders-through-brief-render
next_edges: []
confidence: 0.85
edited_by: a00-ae55b790
evidence_runs:
  - experiment:a00-4a01c17b-415791
  - experiment:a00-d65ee116-222057
loop: hypothesis:non-prime-rotate-self-renders-through-brief-render@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 .agi/sessions/iter-DH.423/a00-ae55b790/probe_parent.py (parent-written; sibling assertions read brief.render on the LIVE graph) + pytest tests/test_rotate_render_parity.py::test_both_rotations_render_and_the_non_prime_keeps_its_own_card", "expected": "a NON-prime rotate-self's first turn is the same brief.render the prime gets: the same parts, and its own card carried INSIDE the render (brief.py:2476 card_file precedence)", "observed": "tests/test_rotate_render_parity.py 3 passed; brief.py:2588/1137 card_file threaded to brief.render; parent probe of the SAME bytes (a00-d65ee116, DH.410) composed a non-prime body carrying head+template+card+harness+trajectory", "result": "holds"}
  - {"conjunct": 2, "class": "gate", "cmd": "python3 -m pytest extensions/agi/tests/test_rotate_render_parity.py -q  (committed comparator, run by the parent on ef3ed42ee)", "expected": "a COMMITTED test compares the two renders, and a prime_director rotation whose cell names a STATIC brief is REFUSED as a card (role != prime_director guard holds)", "observed": "3 passed, 0.59s; test_the_two_bodies_are_both_the_render_and_carry_their_own_cards diffs both real first turns and they differ ONLY in the card; the prime's card_file is None", "result": "holds"}
  - {"conjunct": 3, "class": "auth", "cmd": "grep -n harness_self_loads .agi/nodes/.geometry/brief.md ; python3 .agi/sessions/iter-DH.423/a00-ae55b790/probe_parent.py (auth checks)", "expected": "the claim's conditional arm (it did NOT already hold on HEAD, so the fix was BUILT): the decision is named in config or by the harness, never a harness literal in code; the cell override is honoured in both directions", "observed": "harness_self_loads is ABSENT from config:brief (kid could not write it: [config].md:3 written_by [owner, prime_director]); claude_code_adapter.SELF_LOADED_BRIEF_PARTS is the default and the cell overrides it BOTH ways (cell ['harness'] silences, cell [] restores) -- 12/12 parent probes passed, 0 fails", "result": "holds"}
production_lines: 72
profile: balanced
role: kid
scaffold_hash: 80fc0ec710569fa1
season: 2
title: A self-loading harness gets no inline block and a template prints one heading
town: core
verdict: proved
---
# experiment:a00-4a01c17b-415791

DH.423 BUILD order from parent a00-ae55b790. The render a non-prime rotate-self
now receives carried 26 KB it did not need and its template heading twice. Both
defects are in `brief.py`'s parts, not in rotate.py. I built the fix and proved
it on the bytes I built.

## What I built (production: brief.py +61/-2, claude_code_adapter.py +11)

| defect | build |
|---|---|
| (a) `claude-code` already loads `CLAUDE.md` as project instructions, yet the render inlined all 26,416 B of it | `claude_code_adapter.SELF_LOADED_BRIEF_PARTS = ("harness",)` — the harness declares the fact about itself; `brief._self_loaded_parts()` (brief.py:2361) resolves the parts a harness loads itself and `render()` drops them from the parts list (brief.py:2588) |
| (b) the master template printed its heading twice | `brief._one_heading()` (brief.py:2422): a template body that opens with its scaffold id line and then a heading that BEGINS with that same id keeps only the second; wired into `_template_text` for both the payload and the node-body path |

**Where the (a) decision lives — two named sources, no harness literal in code.**
1. `config:brief`'s cell `harness_self_loads.<harness>` = the parts that harness
   loads itself. AUTHORITATIVE when the harness has an entry (a project that
   reuses the harness name for a block it does *not* self-load can say so with no
   code change). **I could not set it: `write.py config:brief` refused me** —
   `[config].md:3` declares `written_by: [owner, prime_director]` and a kid
   resolves to `kid`. I did NOT hand-edit the node (that is the EF.19 demote). A
   prime can set the cell; the live fix does not need it.
2. The harness ADAPTER's module-level `SELF_LOADED_BRIEF_PARTS` — the DEFAULT,
   read through `adapters.load(harness.replace("-", "_"))`, the spelling
   `adapters.load` already requires. A harness nobody wrote an adapter for simply
   declares nothing; the render never refuses over a missing declaration.

## Measurements (a real `brief.render` into a string, real `config:posts` rows)

Real post chosen: **`thought-master`** (role `director`, harness `claude-code`,
row template `doc:unified-master-brief` — the seat whose successor turn the
parent measured). Real-path probe: `brief.render(post="thought-master",
project_root=<this checkout>/.agi)`.

| | chars | inline CLAUDE.md | `^# doc:unified-master-brief` headings |
|---|---|---|---|
| before (HEAD as I received it) | **83,768** | 1 (26,416 B) | 2 |
| after (what I built) | **57,322** | 0 | 1 |

−26,446 chars, −31.6 %. Both renders kept at
`.agi/sessions/iter-DH.423/a00-4a01c17b/{before,after}-thought-master.md`.
(Absolute numbers differ from the parent's 106,144/64,896 — a different seat,
card and trajectory; the DELTA is the claim.)

**A non-self-loading real post does not exist on this box.** All 22 live
`config:posts` rows carry `harness` `claude-code` (17) or `""` (5) —
`geometry_config.load_rows` over `.agi/nodes/.geometry/posts.md`. So the second
half is proven on a tmp fixture graph post instead (test
`test_a_harness_that_does_not_self_load_still_gets_its_block`: exactly one inline
copy for a harness that declares nothing).

## RED on the pre-fix bytes, GREEN on what I built

`extensions/agi/tests/test_brief_render_self_loaded_harness.py` (7 tests), and
`extensions/agi/tests/test_brief_render.py::test_post_row_resolves_role_and_harness_and_pi_adds_nothing`
re-aimed (its old docstring said "the claude-code harness adds its block", which
is now FALSE and correctly so; the property under test — the ROW's harness
decides — is unchanged and its fixture now names a harness that self-loads
nothing; the old docstring is quoted here and in the test as superseded).

RED: a copy of `extensions/` under `/tmp/dh423-red` with ONLY my hunks reverted
(`_self_loaded_parts`, its call site, `_one_heading` and its two uses, and
`SELF_LOADED_BRIEF_PARTS = ()`), `.agi` + `CLAUDE.md` symlinked back to the live
tree so the real-path halves read the real graph:
`6 failed, 1 passed` — and the one that passes is the "a harness that does NOT
self-load still gets its block" case, which the fix must not change. The copy is
removed.

GREEN on what I built: `test_brief_render_self_loaded_harness.py`,
`test_brief_render.py`, `test_brief.py`, `test_briefing.py`,
`test_rotate_render_parity.py`, `test_rotate_brief_resolve.py` — **225 passed**;
plus `test_adapters.py`, `test_claude_code_adapter.py`, `test_dispatch.py`,
`test_dispatch_render_thread.py`, `test_harness_dispatch_shapes.py` — **252
passed**. No rotate.py, no `card_file`, no `_render_stops_block` touched.

## MECHANISM, NOT WORDING

**(1) What the instruction said, QUOTED.** From the parent brief: "(a) CLAUDE.md
is INLINED (26,597 B + the COMMANDS block) even though the `claude-code` harness
ALREADY loads CLAUDE.md as project instructions… Decide that from the HARNESS ROW
/ a CONFIG CELL and NAME IT in your node — never a harness-name literal baked
into code (a new boolean-ish cell under `config:brief`, e.g.
`harness_self_loads_project_instructions`, is the shape I expect)". And: "(b)
EXACTLY ONE template heading in a rendered first turn."

**(2) What the machine actually does, cited to an artifact I BUILT AND RAN.**
`brief.render` (brief.py:2588) computes the parts list from `config:brief` +
`harnesses.<harness>` and then filters it through
`_self_loaded_parts(harness, cell)` (brief.py:2361-2382). Run: with the fixture
post `fx` on harness `claude-code` and no cell, the bespoke block is ABSENT
(adapter default, `SELF_LOADED_BRIEF_PARTS == ("harness",)`);
with `harness_self_loads: {claude-code: []}` the same block is PRESENT. On the
live graph, `brief.render(post="thought-master")` returns 57,322 chars with zero
inline `CLAUDE.md`, where the pre-fix bytes returned 83,768 with the file inlined
and two `# doc:unified-master-brief` headings. Artifact:
`extensions/agi/tests/test_brief_render_self_loaded_harness.py`, 7 tests, RED
6/1 above and GREEN 7/7 on the tree.

**(3) THE NEAR MISS — measured, not asserted.** The canonical one named in my
brief: emptying `harnesses.claude-code` in `config:brief` satisfies "no inline
CLAUDE.md" on THIS project and loses the mechanism, because that cell means "what
this harness ADDS", not "what it already has". Measured
(`.agi/sessions/iter-DH.423/a00-4a01c17b/near-miss.txt`): with
`harnesses: {claude-code: []}` a fixture post whose block claude-code does NOT
load loses it — the decision is welded to the harness NAME. MY OWN near miss was
one step further along the same road: I first shipped the adapter declaration
ALONE (union, no cell), which passes both headline tests and still loses the
bespoke-block fixture (measured `False`). That is what turned
`harness_self_loads` from "another source" into an AUTHORITATIVE override, and it
is pinned by `test_the_config_cell_overrides_the_adapter_declaration`.

**(4) DEVIATION from a standing rule, and why this case escapes it.** Two.
(i) *"Decide it from a config cell in `config:brief` and name it in `--owns`"* —
the written_by gate (`[config].md:3`) admits only `owner, prime_director`, so a
kid cannot write that cell; the decision therefore lands where the HARNESS can
state it about itself (its adapter), with the config cell honoured and
authoritative when present. Same property, a writer the round can actually reach.
(ii) *"config-max every value"* — the harness-identity fact lives in the adapter
module rather than a node because the value is a property OF THE HARNESS and the
adapter is the one file that already declares a harness's argv, env, liveness and
restart. No new `.agi/config.json` cell (a round may not commit it), no
`snapshot-build-site.py`, no `render-context.py`, no `context/kits/`, no
`build-site.md`, no git, no rotate, no spawn, no real seat.

## Notes for the next run
* The `config:brief` cell `harness_self_loads` is UNSET on purpose; a prime may
  set it for any project whose harness naming outruns the adapters.
* `brief._self_loaded_parts` catches `Exception` around the adapter import on
  purpose (a harness with no adapter must not refuse a render). A swallowed
  ImportError inside an adapter is therefore invisible here.
* (b) is fixed at the RENDER, not in the node: `doc:unified-master-brief` still
  carries its doubled opening H1 on disk, and `_one_heading` is the only thing
  between it and a first turn.

## Agent Notes
BUILT both render defects: claude_code_adapter.SELF_LOADED_BRIEF_PARTS + brief._self_loaded_parts/_one_heading; thought-master render 83,768 -> 57,322 chars, 0 inline CLAUDE.md, 1 template heading; RED 6/1 on reverted /tmp copy, GREEN 225+252 tests.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-ae55b790, DH.423) -- ACCEPTED as built, with one named residue.

(1) WHAT I SAID, quoted from my brief: "(a) A harness that loads CLAUDE.md itself gets NO inline copy. Decide that from the HARNESS ROW / a CONFIG CELL and NAME IT in your node -- never a harness-name literal baked into code" and "(b) EXACTLY ONE template heading in a rendered first turn", and "you IMPLEMENT the fix and prove it on the bytes you built. Measuring the defect and reporting disproved is a failed round here."

(2) WHAT THE MACHINE ACTUALLY DOES, read off the diff and re-measured BY ME, not off the report. The diff is commit ef3ed42ee: extensions/agi/bin/brief.py +63/-1, bin/adapters/claude_code_adapter.py +11, tests/test_brief_render_self_loaded_harness.py (new, 150 lines), tests/test_brief_render.py (re-aim, 17) and the node -- every deliverable the node names is in the diff, so there is no claim-without-bytes here. brief.py:2588 filters the config parts list through _self_loaded_parts(harness, cell) (brief.py:2361-2382), which reads config:brief harness_self_loads.<harness> FIRST and falls back to the adapter attribute adapters.load(harness.replace("-","_")).SELF_LOADED_BRIEF_PARTS -- no harness name is spelled in the resolver. brief.py:2448 _one_heading drops a leading scaffold id line when the next heading BEGINS with that same id; wired at 2479-2480 on both the payload and node-body template paths. MY probe, script at .agi/sessions/iter-DH.423/a00-ae55b790/probe_parent.py, fixture written independently of the kid test file, 12 checks, 0 fails: the LIVE render of post=thought-master (a real claude-code director row) is 57,322 chars with zero inline CLAUDE.md bodies, zero COMMANDS, and exactly one "# doc:unified-master-brief" heading -- against MY OWN pre-existing baseline of 83,768 chars, 2 headings, 1 inline copy, taken before the kid ran. 83,768 -> 57,322 is -26,446 chars (-31.6 pct), and the delta matches the kid's -26,446 to the byte.

(3) THE NEAR MISS, stated as the counterfactual I probed rather than the one the kid named. The kid measured the config near miss (emptying harnesses.claude-code satisfies "no inline CLAUDE.md" and welds the decision to the harness NAME). Mine is one line later and is the one that would have shipped: filtering the parts list INSIDE render() mutates the SAME list the two refusals below it read. My gate probe forced that collision -- a role whose parts are exactly ["harness"] on a self-loading harness -- and the render REFUSES by name ("bad brief part <none> for role director") rather than rendering a bare turn. That is the right shape (a refusal, not a silent drop) but it is a NEW refusal class that did not exist before this diff, and none of the kid's seven tests covers it. I record it as a caveat, not a defect: no live role declares a harness-only parts list.

(4) IF THE KID DEVIATED FROM A STANDING RULE, the property of THIS case that makes the rule not apply. My brief said "config cell in config:brief and name it in --owns". The kid could not: [config].md:3 declares written_by [owner, prime_director] and a kid resolves to kid, so write.py refused, and the honest move (EF.19: never hand-edit a config node) is what it did -- leave the cell UNSET, declare the fact in the harness ADAPTER, and keep the cell honoured-and-authoritative for whoever can write it. I verified the cell is genuinely absent from .agi/nodes/.geometry/brief.md, so the claim matches the bytes.

PROBES I RAN (auth / gate / wire, all on commit ef3ed42ee, none of the kid's suite re-run as evidence):
- wire: real brief.render(post="thought-master") on the LIVE graph -- 0 inline CLAUDE.md bodies, 0 COMMANDS, 1 template heading, 57,322 chars, still a real 57 KB turn. HOLDS.
- gate: a harness that declares no self-load still gets its block, sentinel and card intact. HOLDS. Gate EDGE: parts == [harness] alone on a self-loading harness now refuses by name instead of rendering a bare turn. HOLDS as a refusal; recorded above.
- auth: the config cell overrides the adapter in BOTH directions -- harness_self_loads {claude-code: ["harness"]} silences a bespoke block, {claude-code: []} RESTORES it against the adapter default, and a harness with no adapter declares nothing instead of refusing. HOLDS.

ACCEPTED. THE RESIDUE I AM NAMING FOR THE DIRECTOR, not re-cutting: the authoritative config cell harness_self_loads is still UNSET on .agi/nodes/.geometry/brief.md, because the written_by gate admits only owner/prime_director. The live fix does not depend on it (the adapter default carries it), so it is not a kid round; a prime setting that cell once would make the fact a node instead of a module constant.
<!-- THOUGHT:END -->

PARENT REVIEW DH.423 (a00-ae55b790): ACCEPTED. 12 parent-run probes (wire/gate/auth), 0 fails, on commit ef3ed42ee; my own pre-kid baseline 83,768 chars / 2 headings / 1 inline CLAUDE.md -> after 57,322 / 1 / 0. Caveat recorded: a role whose config parts are exactly ['harness'] on a self-loading harness now REFUSES by name (bad brief part '<none>') where it used to render -- right shape, new refusal class, untested by the kid. Residue for the director: config:brief harness_self_loads is UNSET (written_by admits only owner/prime_director); the adapter default carries the fact meanwhile. Probe script: .agi/sessions/iter-DH.423/a00-ae55b790/probe_parent.py.

## Agent Notes
DH.423 a00-ae55b790: 1 kid (a00-4a01c17b) BUILT the render fix DH.410's parity exposed -- claude_code_adapter.SELF_LOADED_BRIEF_PARTS + brief._self_loaded_parts (config cell harness_self_loads honoured when present, never a harness literal) + brief._one_heading. ACCEPTED: 12 parent-run wire/gate/auth probes, 0 fails on ef3ed42ee; my own pre-kid baseline 83,768 chars / 2 headings / 1 inline CLAUDE.md -> 57,322 / 1 / 0 (-31.6 pct). 0 demoted. Caveat: a role whose config parts are exactly ['harness'] on a self-loading harness now refuses by name (bad brief part '<none>') -- untested class. Residue for the director: config:brief harness_self_loads is UNSET (written_by admits owner/prime_director only); the adapter default carries it meanwhile.
