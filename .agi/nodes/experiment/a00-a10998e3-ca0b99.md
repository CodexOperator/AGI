---
id: experiment:a00-a10998e3-ca0b99
mint_id: dbb9297b3faa4c7bb610d29754ec12e6
type: experiment
parents:
  - hypothesis:a00-5b27ca07-438c0a
next_edges:
  - verdict:a00-a667efeb-43f94e
confidence: 0.85
edited_by: season.py
evidence_runs: 0
scaffold_hash: 76ae5837c99694c2
season: 1
thought_session: season
title: A00 a10998e3 ca0b99
verdict: inconclusive_lean_proved:85
wired_at: 1788275555
wired_from: a00-a10998e3
---
# experiment:a00-a10998e3-ca0b99

## Experiment

Differential parser run over the live corpus, the first of the hypothesis's
three "what would prove it" criteria (and the third, the downstream check). One
script, `/tmp/g13-diff-parsers.py` (path may not survive; method is fully
described below, output below verbatim), run 2026-09-01 from
`/home/ubuntu/work/agi` with `python3 /tmp/g13-diff-parsers.py`:

1. **Five read paths, one file walk** over every `.agi/nodes/**/*.md` (848
   files = 847 measured by the hypothesis + this scaffold):
   - **P1** `graph_core.persistence.frontmatter.load_node_file` (raises `FrontmatterError`)
   - **P2** `graph_core.loader.load_node_with_subgraph` per file + `load_directory` (the path `metrics._load_graph` takes *today* — see discrepancy below)
   - **P3** `post_wire._read_frontmatter` (imported from `bin/post_wire.py`)
   - **P4** `stitch._parse_frontmatter` (imported from `bin/stitch.py`)
   - **P5** the exact inline `text.split("---", 2)` of `snapshot-goals.load_existing_nodes` (imported from `bin/snapshot-goals.py`)
   All comparisons keyed by path relative to the repo root — **15 basenames
   collide across type directories**, so basename keying corrupts any such
   table (this experiment hit it: 37 phantom disagreements on the first run).
2. **Stub `parse_node(path)`** — the hypothesis's proposed single reader, with
   body = P1's exact normalization — checked to reproduce P1 on every file.
3. **Downstream invisibility** (criterion 3): `snapshot-goals.render_goals` run
   twice over the goal nodes, once on the split-based bodies and once with
   every body replaced by the P1-normalized one, both compared to `GOALS.md`
   on disk; and `node_writer.scaffold_hash` / `node_writer._is_untouched_scaffold`
   evaluated on every node under both bodies.
4. **Failure semantics measured** (not assumed) on two synthetic malformed
   files: `---\nfoo: [unclosed\nno closing marker\n` and `just text\n`.

**What happened.** Everything the hypothesis predicts, on 848/848 files, with
one refinement and one discrepancy (below). No disproof trigger fired: no
frontmatter disagreement, no downstream-observable body difference, no
load-bearing failure semantic on the well-formed corpus.

### Refinement: the trailing-newline rule is "exactly one", not "all"
P1 joins `splitlines()` of the body region, so it drops exactly **one**
trailing newline. The split-based bodies keep **k**, P1 keeps **k−1**, where k
is the file's trailing-newline count. Measured: **843 files have k=1** (P1
body ends without `\n`, the hypothesis's description) and **5 have k=2** (P1
body keeps one trailing `\n`): `experiment/a00-a10998e3-ca0b99.md` (this
scaffold), `goal/g6.8-…`, `goal/s11-…`, `goal/s17-…`, `hypothesis/a01-144a1c04-8ba9b7.md`.
All 848 files carry one leading blank line after `---`. The delta between a
split-based body and the P1 body is therefore: the closing `---`'s own newline
(constant in all three split parsers) + one leading blank line + (k−1) trailing
newlines — deterministic, and fully explained for 848/848. The unified
`parse_node` must pin *this* rule (drop one leading blank line, drop exactly
one trailing newline) to be byte-identical with P1 today; an rstrip-all
normalization would change 5 bodies.

### Discrepancy: the hypothesis's metrics row is stale
`metrics._parse_frontmatter` **no longer exists**. `metrics._load_graph` now
imports `graph_core.loader.load_directory`, which wraps `load_node_file` in
`except Exception: continue` — a **silent per-file skip** layered on top of
the raise semantic. So the read side is four independent parsers in two
stacks (graph_core ×2 error-handling flavors: raise at `load_node_file`,
silent-skip at `load_directory`; ad-hoc split ×3: `post_wire`, `stitch`,
`snapshot-goals`), and the "last-wins dict loader" the table attributed to
metrics is gone. This *sharpens* the hypothesis, not against it: the graph_core
stack itself already carries two failure semantics one call apart, which is
exactly the "four accidents" thesis. Duplicate-id first-wins vs last-wins
can no longer be measured across stacks (only one dict-based id loader
remains: `snapshot-goals`, last-wins); the latent claim stands on the corpus
fact, 0 duplicate ids, measured below.

## Evidence

Full output, verbatim:

```
files scanned: 848
P1 raise-path errors: 0 []
P4 None: 0  P5 no-id swallowed: 0
frontmatter disagreements P1/P3/P4/P5: 0 []
body delta classes (leading blank?, trailing newlines k): {('lead', 'k=1'): 843, ('lead', 'k=2'): 5}
bodies not explained by the two rules: 0 []
P2 per-file exceptions: 0  id!=fm['id']: 0 []  body!=P1: 0
P2 load_directory: loaded=848/848 duplicate_ids=[]
stub parse_node mismatches vs P1: 0
render(split-based) == GOALS.md on disk: True (97 goals)
render(normalized) == render(split-based): True
scaffold_hash changed by normalization: 0/848
_is_untouched_scaffold changed by normalization: 0/848
failure semantics (measured):
  P1 load_node_file malformed: FrontmatterError: md file missing closing '---'
  P2 load_directory dir with 2 malformed: loaded=0/2 (silent skip)
  P3 post_wire malformed: fm={} body='---\nfoo: [unclosed\nno closing marker\n')
  P4 stitch malformed: None
  P5 snapshot-goals: try/except pass -> file absent from dict (silent)
```

Interpretation against the hypothesis's criteria:

1. **Parser agreement** — 848/848 frontmatter dicts identical across P1/P3/P4/P5;
   P2's derived `node.id`/`body` agree with P1 on 848/848; `load_directory`
   loads 848/848 with `duplicate_ids=[]`. Body deltas 100% accounted for by the
   two rules (+ the constant closing-delimiter newline). Pass.
2. **Stub reproduction** — `parse_node` (P1's normalization) reproduces every
   caller's frontmatter exactly and each split-based body modulo the two
   rules, 848/848. Pass.
3. **Downstream invisibility** — `render_goals` on the normalized bodies is
   byte-identical to the split-based render and to `GOALS.md` on disk (97
   goals); `scaffold_hash` (which `.strip()`s before hashing) and
   `_is_untouched_scaffold` (which compares `.strip()`) are unchanged on
   848/848 — the strip-based forms make both rules invisible by construction,
   now also empirically. Pass.

Failure semantics remain latent on the corpus (0 malformed, 0 duplicate ids)
and the measured inventory is now five flavors, not three:
`FrontmatterError` raised (P1) / silent per-file skip (P2) / `{} + whole file`
as body (P3 — note P3 returns the *entire text* including the `---` markers
when the closing marker is missing, which no caller currently distinguishes
from a real body) / `None` + warning (P4) / silent absence from dict (P5).

No files were modified; no git commands run; corpus read-only.



## Agent Notes
Differential run over 848 nodes: 0 fm disagreements, bodies 100% explained by 2 rules (trailing rule is exactly-one, 5 files k=2), render/hash invariance pass; metrics row stale — metrics now uses graph_core.loader (silent-skip)