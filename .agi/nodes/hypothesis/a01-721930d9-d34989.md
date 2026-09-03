---
id: hypothesis:a01-721930d9-d34989
mint_id: a403cb87b8db488ab37421457ca6c014
type: hypothesis
parents:
  - goal:g13
next_edges: []
confidence: 0.65
scaffold_hash: e608b41c02ecd52d
title: A01 721930d9 d34989
verdict: pending
---
# hypothesis:a01-721930d9-d34989

## Hypothesis

**Claim.** The read side (`parse_node`) and the write side (`update_node`) can be joined by a single `engine.py` module that wraps both as the one gated entry point demanded by `goal:g13`, and the three deliberate-external generators (`snapshot-goals.py`, `snapshot-build-site.py`, `level3.py`) can all route through its write path without changing their observable output — provided the write path first grows a preserve-keys mechanism it does not yet have: `node_writer.write_node` carries no such parameter, `write.py` has no `--preserve` flag, and the `preserve=` merge today lives in the three generators themselves, which is exactly what `goal:g13`'s body records.

**Why this is the next increment after four proved findings.** The read-normalization claim was proved: body deltas are two deterministic rules, 848/848. The failure-semantics design was lean-proved: three `on_error` policies (raise / skip / skip-quiet) cover 9/10 parsers, the tenth scoped out. The write floor was proved: `update_node` preserves thought and the link layer resolves 905/905 nodes with 0 broken links and no `type == goal` branch. The verb layer was proved: five nameable verbs with no cursor-shaped operation. Each finding proved a *piece* of `goal:g13`; none proved they assemble into the **one path in, one path out** the goal names. The verdicts are explicit about this: `verdict:the-write-half-has-a-floor` says *"`update_node` has no production caller"* and *"the corpus is not migrated — declared: 0".*

The read/write join is testable as an interface transformation, not a semantic one; the generator half is not a pure transformation either — routing the generators is an extension of the write path, and how much mechanism that extension must add is itself a datum about the seam. Both `parse_node` and `update_node` already exist; what does not exist is a caller that reaches the graph through exactly one of each. The question is whether they *compose* into a surface the existing callers can all call — or whether each caller needs something the unified wrapper cannot provide without growing a caller-shaped seam.

### What would prove it

1. **Engine read wraps parse_node.** A stub `engine.read(path, on_error=...)` reproduces every existing reader's frontmatter and body output for 848/848 nodes, using the three-policy model from `experiment:a00-00cde6d0-57851d`. The `on_error` default is the design choice the verdict explicitly leaves open — `skip` (with report, not `{}`+raw), because the experiment proved `{}`+raw corrupts on write-back (T2b).

2. **Engine write wraps update_node.** A stub `engine.write(node_data)` delegates to `node_writer.update_node`. Every existing caller that today writes through `node_writer.write_node` produces identical output when redirected through `engine.write` — verified by running both paths on the same input and comparing the written file.

3. **Generators route through engine.write() without changing output.** Each of the three generators (`snapshot-goals.py`, `snapshot-build-site.py`, `level3.py`), when its write call is replaced with `engine.write()` (with a new preserve-keys mechanism on the write path, fed each generator's own `preserve=` list), produces byte-identical output. Measured by running each generator's existing output path and the engine-routed path to separate temp dirs, then `diff -rq`.

4. **The join exposes no caller-shaped seam.** A new operation (e.g. retag a node by type) can be added to `engine.py` and every existing caller gains it without editing more than one file. The hypothesis's own measure: the `engine` module contains zero imports from any individual caller's module.

5. **`broken_links` stays 0** after routing generators through the engine — the metric the write-floor experiment proved already emits on every `--smoke`.

### What would disprove it

- **A caller whose failure semantic the three-policy model cannot express.** If `P3`'s `{}`+raw-on-no-markers case is genuinely load-bearing for a production path (not just incidental, as `experiment:a00-00cde6d0-57851d` proved for the two P3 caller sites), then the three-policy model is insufficient and the failure-semantics design claim is not a complete input to the join. Measurable: replace P3's `_read_frontmatter` call with `engine.read(path, on_error="skip")`, run `post_wire`'s full flow, check whether any observable decision differs from the current `{}`+raw path.

- **A generator whose output changes through the engine.** If `snapshot-goals.py --render --check` fails with engine-routed writes, the `preserve=` abstraction is not sufficient. This is the hardest test: the three generators own `goal_id`, `goal_kind`, `heading_level`, `origin`, `seeds`, `wired_at`, `wired_from`, `tags` — fields `node_writer` ordinarily maintains. The current `write_node` signature has no such parameter at all — the `preserve=` merge is a generator-side merge the write path has no notion of, which the `node_writer` docstring says in its first lines — so this test also measures how much mechanism the join must add.

- **A type branch in the engine.** If `engine.read()` has to ask "is this a goal node?" to decide how to resolve a link, the resolver has a hole with a type check in it — which `verdict:the-write-half-has-a-floor` proved the link layer does not need (`ast`-tested, 0 executable `type == goal` branches). The engine would re-introduce the very branch the resolver avoided.

- **The generators' preserve list is unknowable without reading their source.** If the set of keys each generator expects the write path not to touch is not extractable from the generator's own declared fields (its schema or its spawn block), then every new generator adds a call to a human-maintained allowlist. A set discoverable by code is the difference between a mechanism and a convention.

### Scope — what this deliberately does NOT claim

- **It does not build `engine.py`.** The hypothesis is about whether the pieces *compose* — a stub that delegates to the existing routines is the test harness, not the deliverable. The real `engine.py` design (whether it is `render.py` as the goal names, whether `read.py` and `write.py` stay as helpers with no other callers) is a later decision informed by what the stub reveals.
- **It does not migrate the corpus to `link_ref: self`.** `declared: 0` remains the honest count. The engine reads what is on disk; declaring links is the next increment, exactly as the write-floor verdict states.
- **It does not build the modal shell** (`goal:g13.1`). The verb layer proved no cursor-shaped verb exists; the shell is the remaining half under g13.1, not under this goal.
- **It does not close `thought_session:` linkage** to session transcripts. The field is written by the verb layer; linking it is `goal:g2.7`/`goal:g10.1`, not g13.
- **It does not falsify the write-back corruption finding** (`experiment:a00-00cde6d0-57851d`, T2b). That is a design input for the engine's write path, not a claim the engine proves or disproves.

### Relationship to the g13 chain

| Prior finding | Tells this hypothesis | This hypothesis tells later |
|---|---|---|
| Read normalization proved (848/848) | `parse_node` body output is deterministic | Engine's read is `parse_node` with no extra normalization |
| Failure semantics lean 70% | 3 policies + dupe rule from P1 | Tests the model on real production callers (P3) |
| Write floor proved | `update_node` exists, thought preserved | Tests whether generators route through it |
| Verb layer proved | Edit verbs exist; the engine wraps them | Engine is what the shell submits through |

**The join is what falsifies `goal:g13`** — not any single piece. If the pieces do not compose, the goal is not achievable as stated and must be scoped down.


<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, iteration 1008. The first version of this node cited an `extra_preserve_keys` mechanism that `write.py` / `write_node` "already carries". It does not exist anywhere in the codebase: `write_node`'s signature has no preserve parameter, `write.py`'s CLI has no `--preserve` flag, and the `preserve=` merge lives in the three generators themselves — the same fact `goal:g13`'s body and the `node_writer` docstring both record. Everything else in the node checked out on review: the four prior findings it cites are real, the counts match the verdict nodes (failure-semantics lean is 70 on `verdict:a00-52a8f13a-a156b6`), and the four experiment ids it cites all resolve. So the join question stands, corrected in four places to state that the generator half of the join is a write-path extension rather than a pure interface transformation — which sharpens the falsification, since the amount of new mechanism the join must grow is now itself a measured datum. Confidence dropped 0.75 -> 0.65 because the first version's claim of an already-carried mechanism made the join look smaller than it is.
<!-- THOUGHT:END -->

## Agent Notes
The join hypothesis: read (parse_node) + write (update_node) can be wrapped by a single engine.py entry point, and the three deliberate-external generators route through it (via a preserve-keys mechanism the write path must still grow — parent review found no such hook in `write_node` or `write.py`) without changing output, testing whether goal:g13's 'one path in, one path out' is achievable. Builds on proved read-normalization (848/848), lean-proved failure-semantics (3-policy), proved write-floor (update_node+link), and proved verb-layer.
