---
id: verdict:spawn-gate-lands-on-writer-path
mint_id: 9a84308c787f492d9bc9359672f52dee
type: verdict
parents:
  - exp:node-type-corpus-survey
  - exp:spawn-gate-falsifier
next_edges:
  - mvp:spawn-gate
confidence: 0.85
contradicts: []
edited_by: season.py
evidence_runs:
  - exp:node-type-corpus-survey
  - exp:spawn-gate-falsifier
season: 1
supports:
  - hyp:spawn-check-on-writer-path
tags:
  - s17
  - schema
  - gate
thought_session: season
title: "Proved: the spawn rule is derivable, expressible and enforceable on the writer path — for 2 of ~6 writers"
verdict: proved
---
# verdict:spawn-gate-lands-on-writer-path

**`proved`, on the core claim, at the level it actually holds.**

## The claim that is proved

A spawn rule read from `context/schemas/[<type>].md` and applied inside
`cli.py` rejects an illegal spawn with a message naming **the rule, the schema
file, the node and the fix**; announces an explicit approval naming the schema
on a legal spawn; and leaves every historical violation in place.

All three registered falsifier points fired, with verbatim output in
`exp:spawn-gate-falsifier`:

| registered check | outcome |
|---|---|
| `verdict` with no parent | REJECTED, `min_parents` from `[verdict].md`, exit 2, no file |
| `task` with three parents | REJECTED, `max_parents` from `[task].md`, exit 2, no file |
| legal spawn | APPROVED, schema file + every rule that passed, on stdout and stderr |

Plus two unregistered runs: wrong parent type rejects by name, and the
fail-open path fired on a genuine typo of mine and declined to guess.

The three sub-claims of the hypothesis each resolve:

1. **Derivable** — the survey reproduces §S17's table exactly, and 721/778
   nodes (92.7%) already conform to the rules derived from it. Zero unresolved
   parent references corpus-wide, so parent types are always knowable.
2. **Expressible** — `goal`'s three shapes needed a discriminator, and one
   schema with `discriminator: goal_kind` expresses it. Forced, not chosen:
   `SchemaRegistry.resolve()` keys on `type:`, every goal is `type: goal`, so a
   `[g-goal].md` would never be reached and would be dead data that looked
   authoritative.
3. **Enforceable at the right moment** — the check runs before any write, so a
   rejection leaves nothing behind. Verified by `ls`.

## What is explicitly NOT proved — read this before citing the above

**Coverage is 2 of roughly 6 node-writing paths.** Gated: `cli.py scaffold`,
`cli.py done`'s fallback verdict node, and `post_wire.py`'s verdict creation.
**Not gated:**

- `dispatch.py` — carries a *duplicated, un-gated copy* of the whole scaffold
  routine, including its own `NODE_TYPES` (still hyphenated) and its own
  prompts dict. It is the pi-runtime path, so CC-native dispatch does not hit
  it, but a pi run writes nodes past this gate entirely. Not owned by this
  change; the duplication is the real defect and deleting it in favour of
  `cli.py scaffold` is the fix.
- `snapshot-goals.py`, `snapshot-build-site.py`, `level3.py` — generators.
  Arguably they should be gated *last*, since a generator that trips the gate
  is a generator bug and failing the loop over it is worse than reporting it.
  Undecided, deliberately.

### Update 2026-08-26 — the dispatch.py half is closed

The duplication was deleted, not gated: `bin/node_writer.py` is now the only
routine that creates a node file, and all four spawn writers reach it the same
way (`import node_writer` → `write_node`). Wiring the gate into dispatch.py's
copy would have left two gated routines to drift apart, which is the defect
S17 names rather than the fix for it.

What that closed, beyond the gate:

- **The hyphen generator is gone.** One type table, underscore-only, hyphens
  accepted as input aliases and never written. The 2 + 2 historical nodes were
  renamed the same day; `[bigger_outcome].md` and `[app_purpose].md` record it.
- **Every big-zoom scaffold was an illegal spawn.** `_pick_targets` returns
  `("big", None, …)`, so slot 0 had no parent, and `[hypothesis].md` says
  `min_parents: 1`. The un-gated copy wrote it anyway, with a literal empty
  string as its one parent. Big zoom now scaffolds an `idea` — one of the three
  parentless-legal shapes, and what the skill already calls slot 0.
- **`post_wire.py`'s fallback verdict had no `mint_id`** (so `grid.py commit
  --all` skipped it, goal:s14) **and named its file after the parent's slug**
  while its `id:` used the agent id, so path and id disagreed and two agents
  wiring one parent overwrote each other. Both fall out of deriving the path
  from the id in one place.
- **dispatch.py's re-scaffold branch was dead.** It compared an existing body
  against the type's *prompt*, but the body it writes is the `# <node-id>`
  heading followed by the prompt, so the comparison never matched.

Coverage is now **4 of 4 spawn writers**. The three generators are still
un-gated, still deliberately: they re-derive a whole node population from an
input file rather than spawning, own their own frontmatter keys, and already
share one `write_frontmatter` between them — so they are not a duplication
problem, and H0i is what a generator run going wrong looks like.

Tests: `payloads/extensions/agi/tests/test_node_writer.py`.

### The four, surveyed against the corpus — all four have zero residue

Each was fixed in code; the question left was what each had already written.
Measured over all 781 nodes, 2026-08-26:

| defect | corpus residue | how it was counted |
|---|---|---|
| big-zoom parentless `hypothesis` | **0** | nodes with a null or empty-string entry in `parents` |
| fallback verdict with no `mint_id` | **0** | nodes with no `mint_id` (the goal:s14 backfill had covered them) |
| unparseable stamp frontmatter | **0** | nodes whose frontmatter fails `yaml.safe_load`; also **0** nodes carry a spawn-gate stamp at all, the gate being one day old |
| dead re-scaffold branch | **n/a** | code-only; it preserved when it should have preserved, just never for the stated reason |

So three of the four were latent — real, reachable, and not yet reached.
Recorded rather than repaired, because there was nothing to repair.

### The fourth was not latent, and it was much larger than its symptom

The fallback verdict naming its file after the *parent's* slug looked like a
one-line path bug. It was the visible edge of the **read** side of this same
defect: `cli.py._find_node_file` and `post_wire.py._node_file_path` were two
copies of "id → file" that did not agree.

| | ids it could not resolve, of 781 |
|---|---|
| `post_wire.py._node_file_path` | **417** (53%) |
| `cli.py._find_node_file` | **147** |
| resolvable by `cli.py`, not by `post_wire.py` | **270**, incl. 56 verdicts |

Both copies assumed the id prefix names the directory. `post_wire`'s stopped
at two exact paths; `cli`'s added a frontmatter scan of those same two
directories, which is why it did better but still missed every id on an
abbreviated prefix — the 147 are all `exp:` and `hyp:` ids under
`nodes/experiment/` and `nodes/hypothesis/`.

**This one was live.** `post_wire`'s "file not found" branch does not report —
it treats the miss as "no verdict node exists yet" and **creates one**. So an
unresolved id minted a duplicate verdict instead of updating the node it meant
to update, on the writer whose entire job is updating verdicts.

`node_writer.find_node_file` is now the one lookup, beside the one write:
direct path, then a scan of the two candidate directories, then a
whole-corpus frontmatter index — built once per root and dropped by
`write_node`, so the only routine that adds a node is the only one that has to
remember. Both readers are thin aliases over it. After: **0 unresolved on both,
0 resolving to the wrong file, and the two agree on every id in the corpus.**

**The rule table is a description, not a justification.** It is transcribed
from 778 nodes. If the corpus embodies a bad habit, the table now blesses it.
The one place corpus and rule disagree is `min_parents`, and 53 nodes lose
that argument — see below.

**No claim about node quality.** The gate checks `type` and `parents`. It says
nothing about whether a node is worth having, and it does not run the
`validation:` block (`required`/`types`/`regex`) at write time — that engine
exists (`schema_registry/validation.py`) and is still unwired. Wiring it would
fail a large share of the corpus immediately; that is a separate decision.

**`[config].md` is one-field-read.** `spawn_gate.resolve_nodes_root` consults
`locations.nodes_root`, which clears G10.2's bar for a geometry declaration.
The other five locations — `engine_root` above all, still defined twice in
Python and once in shell — are **documented, not collapsed**. Collapsing them
means editing `level3.py` and `grid.py`. Residual, named, not claimed.

## The 53 — a report, not a purge

| type | violations | rule |
|---|---|---|
| hypothesis | 24 | `min_parents: 1` |
| verdict | 21 | `min_parents: 1` |
| experiment | 4 | `min_parents: 1` |
| level3 | 4 | `min_parents: 1` |

Every violation is the same rule. **Zero** nodes exceed `max_parents`; **zero**
name a disallowed parent type. So two of the three rules are pure description
and only `min_parents` is a claim the corpus contradicts.

None of the 53 was touched. `node_count` went 769 → 778 across this work and
never fell. G7's first invariant holds, and G7.1's policy — a bad reference is
fixed or dropped, never the node, and never inferred — is written into the
gate's own reject text and into its fail-open path.

Four further nodes are `unverified` rather than approved or rejected: three
carry **no `type:` field at all**, and `doc:goals-preamble` is a type minted
this session with no schema. The typeless three are a genuine hole — nothing
keyed on `type:` can ever apply to them.

## Why `proved` rather than a lean

`evidence_runs` names two experiment nodes that both exist. Every registered
falsifier point produced observed terminal output, not a description of
expected output. The claim is narrow enough to be checked in one command and
was checked. Confidence 0.85 rather than higher because the coverage gap
above is real: on a pi run, `dispatch.py` still writes nodes this gate never
sees.