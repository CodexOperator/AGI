---
id: hypothesis:a00-6b4ad6b2-a60b78
mint_id: 0424071f93d341469470382026663232
type: hypothesis
parents:
  - goal:g13
next_edges:
  - experiment:a00-00cde6d0-57851d
confidence: 0.75
evidence_runs: 0
scaffold_hash: 02ebd71abf062329
title: A00 6b4ad6b2 a60b78
verdict: pending
wired_at: 1788276861
wired_from: a00-6b4ad6b2
---
# hypothesis:a00-6b4ad6b2-a60b78

## Hypothesis

**Claim.** The read-side failure semantics measured by
`experiment:a00-a10998e3-ca0b99` collapse into **three policies** —
`raise` (default), `skip` (report and continue), `skip_quiet`
(silent drop) — and P1's `FrontmatterError` raise is the only semantic
that is *intentional*: it is the only one that names its own error type
and the only one whose caller can distinguish "file is malformed" from
"file not there." Every non-raising reader (P2 silent-skip, P3
`{}`+raw, P4 `None`+warning, P5 silent-absent) reaches its non-raising
value *incidentally to its processing need*, not as a chosen error
strategy, and each is reproducible by calling `parse_node(path,
on_error="raise")` inside a caller-local `try/except` that picks its
policy. No caller's control flow distinguishes "fm is `{}` because the
file was malformed" from "fm is `{}` because the file has no
frontmatter," so the unified reader does not need a fourth
`on_error="empty_fm"` mode.

**Inventory correction to the experiment.** The experiment scoped to
five parsers. A wider sweep of `extensions/agi/bin/*.py` finds **ten**
frontmatter parsers: the five measured, plus five more —
`crons._parse_frontmatter` (raises `CronsError`, single-node),
`envfile._parse_frontmatter` (raises `SecretsError`, single-node),
`verify_unified._read_frontmatter` (returns `None`, bulk verify),
`spawn_gate._read_frontmatter` (returns `None`, single-node scan),
`benchmark._parse_frontmatter` (returns `{}`+raw, single-node,
line-based, no YAML). The single-node readers (crons, envfile,
spawn_gate) already raise or return `None` — they are a second class,
"one file, no fallback," where the policy is determined by the caller
rather than the parser. They are not in scope for the unified
`parse_node` (which replaces the *bulk corpus readers*); they are
documented here because the hypothesis's claim is about the *pattern*,
and the pattern holds: every parser in the tree picks its failure
semantic from the caller's need, not from a shared policy.

**P3 nuance the experiment did not test.**
`post_wire._read_frontmatter` has no `try/except` around
`yaml.safe_load`. The experiment's malformed file (`---\nfoo:
[unclosed\nno closing marker\n`) hit the `len(parts) < 3` branch
(no closing `---`) and returned `{}` + raw. A file *with* a closing
`---` but malformed YAML between the markers would raise
`yaml.YAMLError` uncaught. P3's failure semantic is therefore
three-way, not one: no markers → `{}`+raw; one marker → `{}`+raw;
two markers + bad YAML → **raises**. The unified reader must model
all three, or the "no observable delta" claim has a gap.

**Dupe-winner.** P1's `load_directory` uses first-wins in a
**sorted walk** (`sorted(glob)`) and emits a visible `WARN` +
collects `graph.duplicate_ids`. P5 (`snapshot-goals`) uses last-wins
(dict assign, walk order = `Path.glob` = OS enumeration order). P4
(`stitch`) reads a single type directory and does not key by id. P2
inherits P1's first-wins (it wraps P1). No caller today observes a
dupe (corpus: 0 duplicates, measured). The unified reader should pin
P1's rule — sorted-walk first-wins with warning — because it is the
only rule whose winner is a function of the file path alone,
independent of OS enumeration order.

**What would prove it.**

1. **Policy collapse.** For each of P2–P5 (and the five additional
   parsers found by the sweep), the call site's non-raising behavior
   on malformed input is reproducible by wrapping
   `parse_node(path, on_error="raise")` in a caller-local `try/except
   FrontmatterError` with the matching fallback. The only code that
   moves is the parser call itself; the fallback logic stays at the
   caller.
2. **No empty-fm ambiguity.** No caller branches on "fm is `{}`" in a
   way that distinguishes "file was malformed" from "file has no
   frontmatter markers." Specifically: `post_wire._read_frontmatter`
   returns `{}` for both a file with no `---` and a file with one
   `---`; its caller at line 294 uses `fm` only to read
   `confidence`, `verdict`, `evidence_runs` — all of which are
   absent in both cases, so the branch is the same.
3. **P3's latent raise is a disproof check, not a design
   requirement.** A file with `---` markers but invalid YAML inside
   them, fed through P3, raises `yaml.YAMLError`. This is
   *currently untested and unhandled* by post_wire. It is not a
   disproof of the hypothesis (no such file exists in the corpus); it
   is a design input: the unified reader's `on_error` must cover it.
4. **Dupe rule is path-deterministic.**
   `sorted(Path.glob("nodes/**/*.md"))` produces the same order on
   Linux ext4 and APFS; `Path.glob` order does not. A dupe id where
   two files are in different sorted vs. OS order would select
   different winners under the two rules. Measurable: inject a
   synthetic dupe pair whose paths sort opposite to their
   `os.scandir` order, run both rules, confirm they diverge.

**What would disprove it.**

- A caller whose control flow branches on the non-raising value of a
  malformed file *specifically* — e.g., "if `fm == {}` and the file
  exists, create a new scaffold" where the `fm == {}` is the
  malformed-file path, not the no-frontmatter path, and those two
  paths lead to different branches. (P3's caller at line 294
  appears not to be this; check `cli.py scaffold` and `dispatch.py`
  which also call `_read_frontmatter`.)
- A caller that processes a directory and uses the *set of surviving*
  ids (after the non-raising drop) to drive a subsequent decision —
  e.g., "wire edges to every id that survived parsing" — where
  surviving-malformed (under `on_error="raise"` with `except:
  continue`) changes the id set versus the current silent drop.
- A parser in the sweep of ten whose failure behavior is
  *unreproducible* from the three policies — i.e., its fallback is
  not `raise`, not `skip` (report), not `skip_quiet`, but something
  else (e.g., "return a sentinel value the caller treats as a
  distinct state from both 'parsed' and 'missing'").

**Scope.** Failure semantics only: the `on_error` policy and the
dupe-winner rule for a unified `parse_node`. The body normalization
(leading blank line, exactly-one trailing newline) was proved
invariant in the previous chain and is assumed pinned here. The
write path, the `dispatch._node_type_for` / `spawn_gate`
two-definitions debt, and the `thought_session:` stamping are
separate hypotheses per the goal node's scope note.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version. Picked the failure-semantics design question because
the verdict's caveat named it explicitly ("the `on_error` /
dupe-winner choice is owed to the next node") and the goal's scope
note fenced it as "the next design step in the chain." Framed it as
a testable claim about policy collapse rather than a design
recommendation, because a design brief without a prior test is the
exact shortcut s22 exists to close. The wider sweep (5 → 10 parsers)
was done in the course of checking the P3 nuance; it strengthens
the claim (the pattern is universal, not corpus-specific) but does
not change its scope (the unified `parse_node` replaces bulk corpus
readers, not single-node config readers).
<!-- THOUGHT:END -->


## Agent Notes
Failure-semantics design: 5 observed semantics collapse to 3 on_error policies; P3 has untested latent yaml.YAMLError raise; wider sweep finds 10 parsers total