---
id: build:src-graph-core-identity
mint_id: 3d0741824921496fb21882d0711fbb44
type: build
parents:
  - idea:engine-graph-core
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/src/graph_core/identity.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/src/graph_core/identity.py"
---
`extensions/agi/src/graph_core/identity.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-graph-core`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/src/graph_core/identity.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 23'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: hashlib
  how: '`import hashlib` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: re
  how: '`import re` at line 27'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tempfile
  how: '`import tempfile` at line 28'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: uuid
  how: '`import uuid` at line 29'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: warnings
  how: '`import warnings` at line 30'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 31'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: typing.Any
  how: '`from typing import Any` at line 32'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: typing.Iterable
  how: '`from typing import Iterable` at line 32'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: typing.Mapping
  how: '`from typing import Mapping` at line 32'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: typing.Optional
  how: '`from typing import Optional` at line 32'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: derive_slug
  how: 'defines public function `derive_slug` at line 43, signature: (source_text:
    str, min_tokens: int=DEFAULT_MIN_TOKENS, max_tokens: int=DEFAULT_MAX_TOKENS)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _build_id
  how: 'defines private function `_build_id` at line 64, signature: (type_prefix:
    str, slug: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: IdRegistry
  how: defines public class `IdRegistry` at line 68
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: mint_id
  how: 'defines public function `mint_id` at line 113, signature: (type_prefix: str,
    source_text: str, registry: Optional[IdRegistry]=None, min_tokens: int=DEFAULT_MIN_TOKENS,
    max_tokens: int=DEFAULT_MAX_TOKENS)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _digest_int
  how: 'defines private function `_digest_int` at line 152, signature: (seed: str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _to_base_alphabet
  how: 'defines private function `_to_base_alphabet` at line 166, signature: (value:
    int, width: int, alphabet: str=ALPHABET)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: mint_address
  how: 'defines public function `mint_address` at line 177, signature: (seed: str,
    taken: set[str], *, width: int=DEFAULT_ADDRESS_WIDTH)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: supernode
  how: 'defines public function `supernode` at line 224, signature: (node_id: str,
    level: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: is_valid_address
  how: 'defines public function `is_valid_address` at line 235, signature: (value:
    str, *, width: int=DEFAULT_ADDRESS_WIDTH)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: plan_reid
  how: 'defines public function `plan_reid` at line 240, signature: (nodes: Iterable[Mapping[str,
    Any]], *, width: int=DEFAULT_ADDRESS_WIDTH, group_width: int=DEFAULT_GROUP_WIDTH,
    out_path: Optional[str | Path]=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: mint_permanent_id
  how: defines public function `mint_permanent_id` at line 388
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: is_valid_mint_id
  how: 'defines public function `is_valid_mint_id` at line 426, signature: (value:
    str)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: out_path
  how: '`out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
    encoding="utf-8")` at line 358'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(result, indent=2, sort_keys=True)` at line 358'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
*The reasoning below was authored as `build:src-graph-core-identity@v2` and migrated here when the `@v2` convention was retired (G2.10): a version is a grid commit, not a second node file.*

## What changed

Added a second, independent scheme to `identity.py` alongside the existing
`<type>:<kebab-slug>` one (`derive_slug`, `mint_id`, `IdRegistry` — untouched,
still what `loader.py`/`db_loader.py` import and use; verified by running the
full suite before and after). New surface: `ALPHABET`, `mint_address`,
`supernode`, `is_valid_address`, `plan_reid`. Nothing in the corpus was
migrated — every node under `nodes/` still carries its old
`<type>:<kebab-slug>` id today. This node is a build-node version bump on the
code, not a statement that the address scheme is live.

## The address model, in my own words

An id is where a node *is*, not how it got there. Every real node is a fixed
7-character string over a 36-symbol alphabet (`0-9a-z`, lowercase only —
uppercase was rejected on purpose: git refs are case-sensitive but some
filesystems this project deploys to are not, and 26 extra slots per character
isn't worth a scheme that silently breaks on one of the two). A "zoomed-out"
view is never a different set of nodes — it's the *same* nodes, and the
renderer's only job is to truncate: `id[:6]` names the supernode a node
belongs to, `id[:5]` the group above that. No lookup table, no join, no
stored supernode row — truncation computes the containment relation directly
from the string. That's what makes it O(1) and unambiguous: hand anyone a
6-char string and "which nodes are in there" is answered by a prefix scan,
never a traversal.

The load-bearing distinction from the scheme it sits beside: the old id is
derived from *lineage* (a type prefix plus slug text, extended by a
collision counter) — two nodes sharing a slug are related by accident of
title, not by any structural claim. The new id makes no lineage claim at
all. Two nodes sharing a 6-char prefix are, today, unrelated except by
coincidence of hash — which is exactly the placeholder property below.

## The minting rule, and why it's stable under insertion

```python
def mint_address(seed: str, taken: set[str], *, width: int = 7) -> str:
    base = _to_base_alphabet(_digest_int(seed), width)   # blake2b(seed), truncated
    if base not in taken:
        return base
    # deterministic probe: rehash f"{seed}#1", f"{seed}#2", ... until free
```

`_digest_int` uses `hashlib.blake2b(seed.encode(), digest_size=8)`, not
Python's built-in `hash()` — `hash()` is salted per-process specifically to
resist collision attacks, which is precisely the property that makes it
wrong here: the whole point is that the same seed produces the same address
in every process, forever, including a process started tomorrow.

Stability under insertion follows directly from the address being a pure
function of `seed` alone in the non-colliding case — it never reads corpus
size, sort position, or any other node's assigned address, so there is
nothing for a newly-minted node to perturb. I verified this rather than
just asserting it: `test_mint_address_stable_under_insertion` mints 200
addresses, then mints a 201st against the grown `taken` set, and re-derives
each of the first 200 against `taken` with only its own address removed —
all 200 come back identical. Collisions are handled by rehashing with a
counter suffix, and a collision only ever moves the *new* seed to its next
candidate; an already-assigned address is never evicted or reassigned.

One place I want to flag rather than paper over: `mint_address`'s purity
guarantee is per-`(seed, taken)`-pair, not per-batch. Two seeds that
*simultaneously* collide on the same base slot will get different outcomes
depending on which one is processed first against a shared `taken` — that's
inherent to a single-seed function signature, and no amount of hashing
avoids it. `plan_reid` closes that gap the only way available to a batch
caller: it imposes its own canonical order (`sorted(ids)`) before calling
`mint_address` repeatedly, so its *output* — the full corpus mapping — is a
pure function of the input *set*, independent of what order the caller
iterated nodes in. Tested directly: `test_plan_reid_collision_resolution_is_order_independent`
forces 20 real base-hash collision groups (200 fixed seeds at width=2,
checked directly against the private hash helpers before writing the test,
not hoped-for) and confirms the mapping is byte-identical whether the 200
seeds are fed forwards or reversed.

Also worth recording as a real design hazard, not just an implementation
note: at a narrow width (e.g. width=1, 36 total slots) minting more distinct
seeds than there are slots makes `mint_address` loop forever once every slot
is taken — there's no exhaustion check. I hit this directly: my first draft
of the collision test used width=1 with 60 seeds and hung pytest solid. The
production default (width=7, ~78 billion slots) is nowhere near this
regime, but the function itself doesn't defend against it, and I did not add
a guard — flagging it here rather than silently leaving a latent footgun
undocumented.

> **Owner decision, 2026-08-25 — read before treating the section below as an
> open defect.** Two things were settled after this node was first written, and
> both land in its favour:
>
> 1. **The grid-keying question is decided.** A separate **mint id** — permanent,
>    opaque, assigned once, never re-derived — keys `refs/grid/node/*`. The
>    7-character address stays deliberately mutable *because* no durable history
>    hangs off it. So the re-ID-on-retag cost this node flags is gone: retagging
>    changes an address and renames nothing. See G2.5's "two identifiers, two
>    jobs" table.
> 2. **The one-member-per-prefix result is accepted, not patched.** A two-stage
>    scheme (group key → shared 6-char prefix, member → last character) was
>    drafted and then withdrawn: the only grouping available today would be a
>    placeholder keyed on `type`, and `type` values are themselves being retired
>    as legacy zoom-level wording (S11). Building a taxonomy on a name that is
>    being deleted is throwaway work. The prefix hierarchy stays present in the
>    *format* and unexercised in the *data* until G2.6's tags supply real group
>    keys, at which point the ≤36-members-per-prefix budget starts binding.
>
> The finding below therefore stands as an accurate description of current
> behaviour and a correct call-out — it is simply no longer a thing to fix here.

## The placeholder grouping, and what replaces it

Until goal:g2.6's tag taxonomy exists, the 6-char supernode prefix is just
`supernode(new_id, 6)` — the leading 6 characters of the same hash-derived
address, not anything a human chose. `GOALS.md`'s G2.5 section is explicit
that grouping is arbitrary-but-stable until tags land, and this is the
literal implementation of that: stable (same id → same group, forever, same
reasoning as address stability), and balanced in the abstract (uniform hash
output), but **not yet meaningful** — nothing about a shared prefix says two
nodes are related. `plan_reid`'s docstring states this plainly and points at
G2.5's own recorded open tension: once G2.6 tags determine the prefix
instead, a re-tag changes a node's group, which changes its id, which is a
grid-ref rename — that migration cost was paid four times already on
2026-08-24 for a narrower reason and G2.5 says explicitly to decide the
grid-keying question before implementing re-ID-on-retag. I did not decide it;
I re-stated it next to the code that will need the decision, so it isn't lost
between here and G2.6's build.

**A finding worth surfacing, not just implementing around:** at the real
corpus's size (825 resolvable ids), running `plan_reid` produced 825 distinct
6-char groups for 825 nodes — every group has exactly one member
(`max_group_size: 1`). The hash space at 6 characters (36^6 ≈ 2.18 billion)
is so much larger than the corpus that random hashing produces no
clustering at all; the "supernode" layer is currently a no-op relabeling,
not a coarsening. That's expected given the model — grouping only becomes
real fan-in once G2.6 tags replace the hash — but it means anyone reading
`plan_reid`'s output today and expecting a genuinely zoomed-out view will not
get one. This is the honest state of the placeholder, not a bug in it.

## Real numbers, run against the live corpus

Ran a one-off script (not committed — scratch, per the hard boundary on
`bin/*.py`) that walks `nodes/`, parses frontmatter via the existing
`persistence.frontmatter.load_node_file`, and calls `plan_reid` on the
result. **Nothing was written back to any node file or grid ref** —
`plan_reid` only ever writes its own plan JSON, to `/tmp/agi_tree_plan_reid.json`
in this run.

- 826 `.md`/`.json` files scanned under `nodes/`.
- 1 file failed to parse as YAML frontmatter:
  `nodes/hypothesis/a00-1467544f-chain-600hop.md` — a malformed `evidence_runs:`
  block (bad indentation under a scalar key). Pre-existing corpus damage,
  unrelated to this change; excluded rather than fixed, since fixing corpus
  content is out of this node's scope.
- 825 nodes carried a resolvable `id` and were fed to `plan_reid`. No
  duplicate ids encountered in this pass (`load_directory`'s own
  first-wins/duplicate-warning behavior didn't need to trigger here).
- **`mapping` size: 825** (one new address per old id).
- **Supernode groups (6-char): 825.**
- **Max group size: 1.**
- **Groups over the 36-member cap: 0.**
- **References that would need rewriting if this mapping were applied:**
  `parents: 694`, `supersedes: 4`, `evidence_runs: 19`, **total: 717**.
  (`evidence_runs` counts only entries that resolve to a real node id in this
  corpus — most `evidence_runs` entries in this corpus are the `synthetic`
  sentinel goal:g3.1 already flags as not resolving to anything, so 19 is the
  count of the ones that *do* resolve, not the raw field count.)

I also hit one real corpus-shape surprise while writing the runner:
`evidence_runs` is a list in nearly every node but a bare scalar (`3`) in at
least one, which crashed a naive `for ev in n.get("evidence_runs")`.
`plan_reid` now treats any non-list value for `parents`/`evidence_runs` as
contributing zero references rather than raising — it counts, it doesn't
validate the corpus's shape, and a malformed field is a fact about that node,
not a reason to abort the whole plan.

## What I verified vs. assumed

Verified directly, with tests: hash determinism against a hardcoded known
seed (`test_mint_address_known_seed_is_a_constant`, so a hash-function
change is caught rather than silently reassigning every address); stability
under insertion (200→201, first 200 unchanged); collision-probe determinism
given a fixed `(seed, taken)`; `plan_reid`'s batch-level order independence
under real forced collisions; every minted address is alphabet-only and
passes `git check-ref-format --allow-onelevel` on a real `refs/grid/node/<id>`-shaped
ref (skipped gracefully if `git` isn't on `PATH`); `supernode()` truncation
round-trips both directly and through a second truncation; `plan_reid`
idempotence (two calls, same input, identical mapping); reference-count
correctness against a hand-built 3-node fixture with one of each reference
kind plus one dangling reference (correctly excluded); supernode-distribution
stats cross-checked against a manual grouping over 80 real mappings.

Assumed, not verified: that `blake2b` with `digest_size=8` gives enough
entropy headroom for the real deployed corpus size for the foreseeable
future — at 78 billion width-7 slots against corpora in the thousands, the
birthday-bound collision risk is negligible by a wide margin, but I did not
run a stress test at, say, 100k synthetic nodes to confirm the probe chain
stays short. Also assumed: that `parents`/`supersedes`/`evidence_runs` are
the complete set of reference kinds worth counting — I did not audit the
schema registry for any other field type that might embed a node id (e.g. a
future `blocks:` or `duplicates:` field would silently not be counted).

## Escalation not taken

No forbidden file was touched, no irreversible operation was run, and I
didn't hit a spec/reality contradiction that binds a future node beyond the
two G2.5 already records itself (the retag/grid-migration tension, and the
placeholder-grouping honesty above) — so no `SendMessage` was sent. The
empty-supernode-fan-in finding above is worth a future kid's attention when
G2.6 is built, but it doesn't block or contradict anything decided here.
<!-- THOUGHT:END -->