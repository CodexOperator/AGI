---
confidence: 0.9
evidence_runs: 1
id: "exp:prose-surface-probe"
parents:
  - exp:noncode-surface-census
subgraph: false
tags:
  - g6.6
  - level3
  - stitch
title: "Probe: stitch.py cannot express or detect a prose contract for SKILL.md"
type: experiment
---

**What was run:**

```
# 1. baseline verify, no probe node present
cd /home/ubuntu/work/agi-tree
python3 /home/ubuntu/work/agi/extensions/agi/bin/stitch.py \
  --project /home/ubuntu/work/agi-tree --verify

# 2. what the real generator would emit if pointed at SKILL.md — called
#    level3.py's own analyze_file/build_node directly (imported by file
#    path, not reimplemented) rather than guessing at the shape
cd /home/ubuntu/work/agi/extensions/agi/bin
python3 -c "
import importlib.util
from pathlib import Path
spec = importlib.util.spec_from_file_location('level3', 'level3.py')
level3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(level3)
rel = 'skills/agi/SKILL.md'
abs_path = Path('/home/ubuntu/work/agi') / rel
print(level3.build_node(rel, abs_path, parent_id=None))
"

# 3. hand-minted probe node (origin: iter-9007-probe, NOT level3-scan — see
#    note below) written verbatim from that output to:
#    nodes/level3/skills-agi-SKILL.md.md

# 4. verify again with the probe node present
python3 /home/ubuntu/work/agi/extensions/agi/bin/stitch.py \
  --project /home/ubuntu/work/agi-tree --verify

# 5. falsifier: edit one word of the LIVE SKILL.md, well past its
#    frontmatter, verify, restore, verify the restore
cd /home/ubuntu/work/agi
cp skills/agi/SKILL.md /tmp/SKILL.md.backup
sed -i '101s/spending tokens on those is waste;/spending tokens on those is wasteful;/' skills/agi/SKILL.md
python3 extensions/agi/bin/stitch.py --project /home/ubuntu/work/agi-tree --verify
cp /tmp/SKILL.md.backup skills/agi/SKILL.md
git status --short   # must be empty
```

**What happened:**

Baseline (before the probe node existed):

```
stitch --verify: project=/home/ubuntu/work/agi-tree
  engine root: /home/ubuntu/work/agi (ok)
  level-3 nodes: 74
  in-scope engine files: 74

  [1] missing_payload: 0
  [2] orphan_files: 0
  [3] duplicate_payload_ref: 0
  [4] stale_contracts: 0 (+ 0 unreadable)

  runtime: 0.820s
```

Calling `level3.analyze_file`/`build_node` directly on `skills/agi/SKILL.md`
shows why: `ast.parse` fails immediately —
`SyntaxError: invalid character '—' (U+2014) (SKILL.md, line 4)`, the em
dash in the YAML frontmatter's `description:` field. `parse_ok: false`,
`inputs: []`, `outputs: []` — nothing past line 4 is ever reached. This is
the exact, real output `level3.py` would write if its scope predicate
included `.md` files; I used it verbatim for the probe node rather than
inventing a shape.

**Probe node** (`nodes/level3/skills-agi-SKILL.md.md`, `id:
level3:skills-agi-SKILL.md`) is stamped `origin: iter-9007-probe`, not
`origin: level3-scan`. Reason, stated plainly: `level3.py:599-612` prunes
every `origin: level3-scan` node it did not write on its own run, and
`skills/agi/SKILL.md` is outside `discover_files`'s scope (`extensions/agi/
src/**/*.py` + `extensions/agi/bin/*.py` only) — a real scan would never
write or keep this node, so stamping the real origin would make the next
live `level3.py` run silently delete the probe on its very first pass.

With the probe node present:

```
stitch --verify: project=/home/ubuntu/work/agi-tree
  engine root: /home/ubuntu/work/agi (ok)
  level-3 nodes: 75
  in-scope engine files: 74

  [1] missing_payload: 0
  [2] orphan_files: 0
  [3] duplicate_payload_ref: 0
  [4] stale_contracts: 0 (+ 0 unreadable)

  runtime: 0.816s
```

`nodes` ticks 74 -> 75; every other number is identical, and nothing in the
report names `SKILL.md` or `level3:skills-agi-SKILL.md` at all. `--verify`
is silent about the file's presence in the graph — not flagged wrong, not
flagged right, just invisible unless you already knew to grep the node
count.

**Falsifier** (G6.6's own test: edit one word of `SKILL.md`, does `--verify`
report drift?). Line 101, inside a bolded directive clause: `spending
tokens on those is waste;` -> `spending tokens on those is wasteful;`, live
file, then `--verify` again:

```
stitch --verify: project=/home/ubuntu/work/agi-tree
  engine root: /home/ubuntu/work/agi (ok)
  level-3 nodes: 75
  in-scope engine files: 74

  [1] missing_payload: 0
  [2] orphan_files: 0
  [3] duplicate_payload_ref: 0
  [4] stale_contracts: 0 (+ 0 unreadable)

  runtime: 0.816s
```

Zero drift. **G6.6's falsifier fires: the surface is not covered.** Cause is
mechanical and load-bearing for the design question below: `ast.parse`
throws at line 4 (the em dash) *unconditionally*, every single run,
regardless of anything edited afterward. `stale_contracts` diffs
`parse_ok`/`parse_error`/entry-lists between stored and fresh — and both
sides are always `parse_ok: false` with the identical line-4 message, so the
diff is always empty. An edit would only register if it touched line 4
itself (or removed the em dash, which would just relocate the failure to
whatever the next non-Python token is — still not a meaningful contract).
The one-word edit at line 101 was never going to be visible to this
machinery no matter what it said. Restored the file immediately after; `git
-C /home/ubuntu/work/agi status --short` came back empty.

**What a prose contract could be:**

- *Content hash.* Reacts to every edit uniformly — would have caught the
  line-101 edit, trivially. But it is pure binary noise: a typo fix and a
  rule reversal look identical (both "changed"), so it can never be the
  thing that flags a *meaningful* edit versus a *cosmetic* one, and it
  carries zero information about *what* changed — a human still has to
  diff by hand to find out. `stitch.py`'s own docstring already rejects
  this shape for code, on almost the same grounds; nothing about prose
  makes the objection weaker.
- *Extracted structure* (headings, fenced code blocks, tables — the prose
  analogue of ast's top-level defs). Deterministic and mechanical like
  code's `how`. But it is blind to the exact class of edit that mattered
  here: the line-101 edit sits inside a paragraph, touches no heading and
  no fence, so a structure-only contract would have produced the *same*
  silent zero-drift result the real run did — no better than what exists
  today.
- *Extracted claims* — the rules/imperative directives a doc asserts
  (numbered list items, bolded directive clauses like `**No git, no push,
  no sync, no cli.py**`), each with a line number, mechanically pulled the
  same way code's `how` is pulled. This is the only option of the three
  that reacts to *this specific* edit, because the edit sat inside a
  directive clause (`spending tokens on those is waste` -> `...is
  wasteful`) — if that clause is captured as a claim string, the claim
  changes and a stored-vs-fresh diff (exactly `diff_contract`'s existing
  shape) fires. It is not immune to the structure-only failure mode: an
  edit inside descriptive prose that isn't part of any extracted claim
  would still be invisible, same as today. That is a narrower blind spot
  than "any edit outside a heading/fence," not zero.
- *No contract, payload identity only.* Concedes the point outright — track
  that the node exists and its file exists, nothing about content. Cheapest
  to build, but it is not a smaller version of the falsifier passing; it is
  the falsifier failing by design, permanently, stated as policy instead of
  discovered as a bug.

Pick: **extracted claims**, with the same "harness derives `how`
mechanically, a model fills `why`" split code contracts already use — but
say plainly what it does *not* buy, per the next section.

**Would it have caught the agent-prompt/SKILL contradiction:** **No.** That
finding (`exp:noncode-surface-census`, "Judgement call" section) is not a
single-file-goes-stale problem — it is two files that never agreed with
each other in the first place, each internally self-consistent, each
carrying a claim (`agent-prompt.md` rule 5/6: "commit your work" / "signal
via `cli.py done`" vs `SKILL.md`: "do not commit... no cli.py") that
contradicts the other's claim on the same procedure. `stitch.py` has
exactly one cross-node check today — `duplicate_payload_ref` — and it
compares nodes only on an *exact string match* of `payload_ref`, never on
content. `stale_contracts` (the category any prose-contract idea plugs
into) is architecturally 1-node-vs-its-own-file: it diffs a node against a
fresh derivation of *the same file*, never against a second node. Extracted
claims would give you two claim-lists, one per node — but nothing in
`stitch.py`'s current four categories compares claim-lists *across* nodes,
and even if a fifth category did, "commit your work" contradicting "do not
commit" is a semantic negation, not a string diff — the same kind of
judgment call the previous iteration's node explicitly labeled a
"Judgement call," i.e. `TODO(model)` territory, not `how` territory. So the
honest answer is two-part: a claims-shaped contract is the right *first*
mechanical layer (it is the only one of the four options that reacts to
directive-level edits at all), but it is necessary and not sufficient —
catching this specific, real, already-found bug needs a new check *class*
stitch.py does not have (cross-node claim comparison) plus a model
judgment step stitch.py's mechanical/model split does not currently reserve
space for anywhere in its four drift categories.
