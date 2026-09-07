---
id: exp:level3-scan-r1
mint_id: 4ed92dffa50c468fb3f4e01e43733acf
type: experiment
parents:
  - hyp:level3-node-anatomy
confidence: 0.8
edited_by: season.py
evidence_runs: 1
season: 1
tags:
  - zoom
  - level3
  - g2.1
thought_session: season
title: Level-3 scan, first generated pass
---
**Built:** `extensions/agi/bin/level3.py` (engine repo) — one `type: level3`
node per code file under `extensions/agi/src/**/*.py` and
`extensions/agi/bin/*.py`, written to `nodes/level3/`. Plus 20 new tests in
`extensions/agi/tests/test_level3.py`. No `level3.goalmap.json` was created
— see deviations below for why.

Frontmatter carries zero new keys: `id` (minted as `level3:<slug-of-path>`),
`type: level3`, `title`, `payload_ref` (repo-relative file path, source lives
on disk exactly once), `tags: [level3, g2.1]`, `confidence`, and `parents`
when a census match exists. `origin: level3-scan` is stamped via
`write_frontmatter`, imported by file path from `snapshot-goals.py` (not
re-implemented), called with `preserve=existing_fm` per H0i. Pruning is
scoped to `origin: level3-scan` only; a missing/non-git engine root returns
before touching the filesystem (verified by test).

The contract block lives in the body between harness-owned HTML-comment
markers (`BUILD-CONTRACT:BEGIN`/`:END`), as a fenced `yaml` block:
`payload_ref`, `parse_ok` (+ `parse_error` when false), `inputs`, `outputs`,
and (when present) `uncovered` — each entry `{name, how, why, perf,
security}`. `how` is derived purely with the standard library `ast` module:
module-level `import`/`from...import` statements, top-level `def`/`class`
(public vs. private, with signature), detected `open()` / `Path.read_text` /
`.write_text` / `.read_bytes` / `.write_bytes` / `json`/`yaml`/`pickle`
`load`/`dump` call sites, `sys.argv`/`argparse`/`os.environ`/`os.getenv`
(literal-key only)/`sys.stdin`/`input()`, and `print()` call sites. `why`,
`perf`, `security` are always the literal string `TODO(model)` — never
authored by this script. Parent linkage reads `unit_path`/`unit_kind` off
existing `idea:engine-*` census nodes (written by `decompose-engine.py`):
exact match for `bin_script`, longest directory-prefix match for
`src_package`. No match → parentless, printed as `NO_PARENT`, never guessed.

**Run — real, against `/home/ubuntu/work/agi-tree`:**

```
files scanned: 72
level-3 nodes wrote: 72
  with census parent: 69
  flagged NO_PARENT (parentless): 3
contract entries: 1045 derivable, 0 uncovered, 0 file(s) failed to parse
stale level3-scan nodes pruned: 0
```

1045 derivable entries = 644 inputs + 401 outputs, across all 72 files, 0
`parse_ok: false`. The `uncovered` bucket (built for the non-literal-`open()`-
mode case) exists and is unit-tested, but **never fired on real data** — no
file in this codebase currently calls `open()` with a computed mode string.
The three `NO_PARENT` files: `extensions/agi/bin/dashboard.py`,
`extensions/agi/bin/decompose-engine.py`, `extensions/agi/src/__init__.py`.

**Idempotence**, checked twice (before and after a mid-run fix, both real
runs against `agi-tree`, not the test fixtures): copied `nodes/level3/` to a
scratch dir, re-ran, `diff -rq` against the copy — **zero differences, all 72
files byte-identical**, both times. `git status --short -- nodes/level3`
collapses to a single `?? nodes/level3/` line (an entirely-untracked
directory prints as one line without `-uall`, which this repo's tooling
avoids for memory reasons) — consistent with the earlier engine-census-r1
finding that plain `git diff`/`git status --short` is not, by itself, proof
of byte-identity for untracked paths; `diff -rq` is the load-bearing check.

**Test suite:** 20 new tests in `test_level3.py`, all passing — discovery
scope (nested `src/` depth vs. direct-children-only `bin/`), mechanical
derivation of imports/defs/read-write-argv-env-stdout, the non-literal-mode
`uncovered` path, syntax-error handling, empty-file handling, both parent-
matching shapes, the missing/non-git engine-root no-op (including "prunes
nothing"), dry-run, idempotence, the H0i preserve round-trip, prune-scoping
(spares `build-site`/unstamped), and the no-project-local-lookup surface.
Full engine suite: `python3 -m pytest extensions/agi/tests -q` → **420
passed, 0 failed** — clean, no red anywhere (the sibling agent's concurrent
work on `loader.py`/`snapshot-goals.py` did not break anything observed here;
re-ran after my own last edit specifically to check).

**Against the anatomy node's own claims:**

| Anatomy claim | Measured | Match |
|---|---|---|
| Zero new frontmatter keys | Confirmed — `set(fm) <= {id,type,title,payload_ref,tags,confidence,parents,origin}` | yes |
| Source lives on disk once, never inlined | Confirmed — body never contains file content, only `payload_ref` + derived `how` fragments | yes |
| Contract in body, not frontmatter | Confirmed — fenced `yaml` block between HTML-comment markers | yes |
| `how` mechanical, `why`/`perf`/`security` placeholders | Confirmed — 1045/1045 `how` fields derived, 0 fabricated `why`/`perf`/`security` | yes |
| One canonical node per file | Confirmed — 72 files, 72 nodes, no splitting needed this pass | yes |
| Harness-attached fields hit 1.000 recall by construction | Confirmed by construction + test (`payload_ref` always set from the scanned path, `origin` always `level3-scan`, contract shape always present even when empty) | yes |
| Model-authored prose stays ≥0.792 recall | **Untested this run** — no model pass was executed against the `TODO(model)` slots; this is the falsifier's actual hard test and it remains open, same as the rename-case gap the sibling's `engine-census-r1` experiment flagged for itself | open |

**What the anatomy node got right:** the field-set argument (zero new
frontmatter keys) held exactly, with no friction — `payload_ref`/`origin`
were sufficient and no third field was ever needed. The "IO map as data, not
frontmatter" call was correct in a way I didn't expect until building it:
`write_frontmatter`'s own flattening (`str(v).replace("\n"," ")`, single-line
quoting) would have mangled a multi-entry structured IO map instantly had it
gone into frontmatter — the body/fenced-YAML placement isn't just
architecturally cleaner, it's the *only* placement that survives the
existing writer unmodified. "One canonical node per file" also held clean:
nothing in the real 72-file scan hit the "several distinct public surfaces"
ambiguity the anatomy flagged as an open judgment call.

**What turned out wrong or impractical, reported plainly:**

- **The anatomy's GitNexus-vs-`ast` split didn't survive contact with
  implementation.** §2 of the anatomy proposed using GitNexus `context`/
  `impact` output for `how` where GitNexus has coverage (implicitly `src/`),
  falling back to `ast`-derived `uncovered` only for `bin/*.py`. This KID's
  own brief overrode that with a simpler instruction — `ast` uniformly for
  everything, no GitNexus dependency at all — and it worked better than the
  split would have: one code path, one honesty story, no coverage seam to
  explain per-file. GitNexus was not invoked by this generator at all. This
  is a real correction to the anatomy node, not a cosmetic one — anyone
  reading §2 and expecting a GitNexus call in this script's `how` derivation
  will be wrong.
- **The anatomy never specified an id-prefix / `type` value for level-3
  nodes**, only that "id (minted)" is harness-attached. I chose `type:
  level3`, id `level3:<slug>` (matching `identity.py`'s
  `type_prefix:slug` scheme, same one `decompose-engine.py` uses for `idea:`)
  because it's the one value consistent with the goal's own name (`g2.1`,
  "Level 3") and doesn't collide with the goal→idea→hypothesis→...→outcome
  chain vocabulary. This is a judgment call the design left open — flagging
  it rather than treating it as settled.
- **Unbounded `how` text was a real bug, not a hypothetical one.** Feeding a
  call site straight through `ast.unparse` is mechanical and correct, but
  for `bin/heal.py`'s `healer_ctx.write_text(f"""...""")` (a multi-paragraph
  markdown template, escaped-newlines-and-all) it produced an 865-character
  single `how` value — technically valid YAML (proved by parsing it
  correctly once I bounded extraction to the harness markers instead of
  naively splitting on ` ``` `, which the embedded template's own markdown
  fences defeated) but a bad contract entry: unreadable, and a trap for any
  future non-YAML-aware consumer that tries to find the block by string-
  matching fences instead of parsing YAML. Fixed by capping derived text to
  240 chars (80 for `open()`/attribute call *names*) with an explicit
  `...[truncated, N chars total]` suffix — honesty preserved, blob removed.
  Re-verified idempotence and the full suite after the fix; both still hold.
  The anatomy node's "how is mechanical, derive it" is correct as written,
  but "mechanical" turned out to need an explicit size bound to stay
  *useful*, which the design didn't anticipate.
- **Two of the three `NO_PARENT` files are a census-staleness problem, not a
  level3.py problem** — `dashboard.py` and `decompose-engine.py` are real
  `bin/*.py` files with no `idea:engine-*` counterpart because the checked-in
  census predates them (`decompose-engine.py`'s own idea-node census has
  never been re-run against a tree that includes itself or `dashboard.py`).
  Correct behavior for this script (flag, don't guess), but it's evidence
  that `decompose-engine.py` needs a re-run before level-3 parent coverage
  can be complete — noted here rather than silently worked around (e.g. by
  re-running `decompose-engine.py` myself, which was out of my file-ownership
  scope for this task).
- **No `level3.goalmap.json` was needed.** Unlike `decompose-engine.py`,
  parent resolution here reads a field (`unit_path`) that already exists on
  disk in real census nodes — there was no missing mapping to declare
  ahead of time. Creating an unused file just to mirror the sibling's shape
  would have been ceremony, so I skipped it; noted since the brief left it
  optional ("if you need one") and I'm reporting the "didn't need one"
  branch explicitly rather than leaving it ambiguous.
- **Scope landed at 72 files, not the "roughly 50–60" estimate** (58 under
  `src/`, 14 under `bin/`) — a minor miss in the brief's own sizing, not a
  defect; recorded so the next zoom-level pass isn't surprised by the count.