---
id: verdict:a00-a667efeb-43f94e
mint_id: 4fced004ecda4f679b11c79c633f0866
type: verdict
parents:
  - experiment:a00-a10998e3-ca0b99
confidence: 0.85
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
evidence_runs: 1
scaffold_hash: f81f04e561adacb7
title: A00 a667efeb 43f94e
verdict: inconclusive_lean_proved:50
wired_at: 1788276225
wired_from: a00-a667efeb
---
# verdict:a00-a667efeb-43f94e

## Verdict

`proved` (confidence 0.85)

The hypothesis's core claim — the read-side fragmentation is a
**normalization and failure-semantics** problem, not a parsing problem, and a
single `parse_node(path, on_error=...)` pinning one body normalization and one
failure semantic would replace every read parser without changing any
frontmatter any caller observes (observable deltas = rule-determined bodies +
latent failure semantics only) — is **proved as scoped**: read path only,
measured against the live corpus, exactly the scope the hypothesis declared.
All three "what would prove it" criteria pass on 848/848 files; none of the
four "what would disprove it" triggers fired.

## Evidence

Source: `experiment:a00-a10998e3-ca0b99` (differential run, 2026-09-01, verbatim
output in that node). Judged criterion by criterion against
`hypothesis:a00-5b27ca07-438c0a`:

1. **Parser agreement — pass.** 848/848 frontmatter dicts identical across all
   read parsers (P1 `graph_core` / P2 `load_directory` / P3 `post_wire` /
   P4 `stitch` / P5 `snapshot-goals` inline split). Body deltas 100%
   accounted for by the two declared rules — leading blank line + trailing
   newline — and nothing else (`bodies not explained by the two rules: 0`).
2. **Stub reproduction — pass.** A stub `parse_node` built from P1's exact
   normalization reproduces every caller's frontmatter and each split-based
   body modulo the two rules, 848/848 (`stub parse_node mismatches vs P1: 0`).
3. **Downstream invisibility — pass.** `render_goals` on the normalized bodies
   is byte-identical to the split-based render and to `GOALS.md` on disk (97
   goals); `scaffold_hash` and `_is_untouched_scaffold` unchanged on 848/848.

**Disproof triggers: 4 declared, 0 fired.**

| Trigger (hypothesis) | Check | Result |
|---|---|---|
| fm disagreement on a well-formed node | 848/848 differential | 0 |
| body whitespace observable downstream | render round trip + both hash forms | byte-identical / unchanged |
| a failure semantic load-bearing | 0 malformed nodes in corpus; P3's whole-text-as-body quirk measured, no caller distinguishes it | none |
| duplicate id where first-wins ≠ last-wins | census + `load_directory` | 0 duplicate ids |

**Two corrections to the hypothesis, neither a disproof.**

- *Refinement:* the trailing rule is "drop **exactly one** trailing newline",
  not "all" — 5 of 848 files carry k=2 trailing newlines and would be changed
  by an rstrip-all normalization. The unified reader must pin the
  exactly-one rule to be byte-identical with P1 today. The delta stays inside
  the hypothesis's two-rule envelope, so criterion 1 still passes.
- *Inventory correction:* the hypothesis's `metrics._parse_frontmatter` row is
  stale — metrics now routes through `graph_core.loader.load_directory`, which
  wraps `load_node_file` in `except Exception: continue`. The read side is
  therefore two stacks (graph_core with **two** failure semantics one call
  apart: raise vs silent-skip; ad-hoc split ×3) rather than five flat
  parsers. This sharpens the thesis (the "accidents" live *inside* one stack
  too); the disproof triggers are defined on behavior, and behavior is
  unchanged by the correction.

**Failure semantics measured, not assumed.** On two synthetic malformed files
the five readers behave in five distinct ways (`FrontmatterError` raised /
silent per-file skip / `{}` + entire file as body / `None` + warning / silent
absence from dict). They differ in code and agree only because the corpus
contains 0 malformed nodes and 0 duplicate ids — the "latent" clause of the
claim, verified rather than assumed. Corpus re-censused 2026-09-01 at
judgement time: 849 ids, 0 duplicates, evidence node resolves.

**Scope honored.** The claim is corpus-relative by its own terms ("latent
because the corpus currently contains nothing that would tell them apart").
A future corpus with malformed nodes or duplicate ids would force a semantic
choice (which `on_error`, which dupe-winner) *before* unification — that is
the next design step in the chain, not a refutation of this claim.

## Confidence

0.85

- All three declared proof criteria met with measured evidence; all four
  declared disproof triggers affirmatively checked and zero. That is what
  `proved` is for — hence not the experiment's own 85% lean restated.
- Not higher, because: single run on a single corpus snapshot; the harness
  lives in `/tmp` (reproducibility rests on the fully-written-out method in
  the experiment node, not a checked-in script); and the hypothesis's
  supporting inventory needed one correction (stale metrics row), a signal
  that its details are less solid than its core.

## Caveats

- Corpus-relative proof: re-verification is cheap (the method is fully
  described) but the claim does not by itself carry the unification design —
  the `on_error` / dupe-winner choice is owed to the next node.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version. The experiment self-stamped `inconclusive_lean_proved:85`; this
judgement applies the hypothesis's *own* contract instead of inheriting the
experiment's self-rating. The hypothesis declared three proof criteria and
four disproof triggers up front; the experiment met 3/3 with verbatim output
and fired 0/4. A claim that pre-declares its own test and then passes it is a
proof at the declared scope, and the two corrections the experiment found
(one rule refined from "all" to "exactly one", one inventory row stale) both
land strictly inside the declared envelope or outside the declared triggers.
The residual uncertainty — one run, /tmp harness, corpus-relative scope — is
real, so it is carried in the confidence number (0.85), not by demoting the
state. If the next experiment (the unification design or a malformed-corpus
run) surfaces a load-bearing semantic, this node gets re-judged as a verdict
on a verdict, which the schema explicitly allows.
<!-- THOUGHT:END -->



## Agent Notes
proved 0.85: 3/3 declared proof criteria met on 848/848 files, 0/4 disproof triggers fired; two corrections (exactly-one trailing-newline rule, stale metrics row) both inside the declared envelope