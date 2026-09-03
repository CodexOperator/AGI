---
id: experiment:a00-db9ea0ae-d8251b
mint_id: 8ffed5bc318241899fb80d2c78d13a3f
type: experiment
parents:
  - hypothesis:loop-scoped-iteration-ids-cannot-clobber
next_edges: []
confidence: 0.7
scaffold_hash: 2225177483525c84
title: A00 db9ea0ae d8251b
verdict: inconclusive_lean_disproved:70
---
# experiment:a00-db9ea0ae-d8251b

## Experiment

Siblings `experiment:a01-3383bf83-c2547e` and `experiment:a00-ed477860-8f3343`
already confirmed the static claim: `driver.sh`'s `for i in $(seq 1
"$MAX_ITERS")` always restarts at `1`, no allocator reads `sessions/` first,
and a fresh run would reuse `sessions/iter-001`, which already holds a real
23-agent manifest. That leaves one thing untested: **when the directory *is*
reused, does the write actually destroy the prior manifest's content, or does
something downstream already protect it at the data level?**

Copied the real `.agi/sessions/iter-001` into a tmpdir and called
`dispatch._merge_manifest` (the function `dispatch.py:314+` actually uses to
write `manifest.json`, not a raw overwrite) against it with a new, unrelated
agent record — simulating exactly what a second `driver.sh` invocation's
`iter_run(1)` would produce, without spawning any real paid agent:

```python
before = json.loads((iter_dir / "manifest.json").read_text())
before_ids = {a["id"] for a in before["agents"]}          # 1 agent on disk
merged = dispatch._merge_manifest(iter_dir, {"iter": 1, "started_at": "x"},
                                   [{"id": "zzz-fake-clobber-test", ...}])
after_ids = {a["id"] for a in merged["agents"]}
```

Result: `before_ids.issubset(after_ids)` is `True` and the new id is also
present — the pre-existing agent record survived the "clobbering" write
untouched, merged by id rather than replaced.

## Evidence

```
agents before: 1
agents after: 2
old ids preserved: True
new id present: True
```

## Interpretation

This refines, not contradicts, the siblings' finding. Two layers exist and
they disagree:

- **Directory/iteration-id layer (`driver.sh`'s `seq 1 N` → `iter-{n:03d}`):**
  genuinely unscoped, no allocator, confirmed clobber-prone by both siblings.
  The hypothesis's `L<loop>.<nn>` scheme is not implemented anywhere in this
  path.
- **Manifest-write layer (`dispatch._merge_manifest`, from `goal:s28`/
  `goal:g4.8`, unrelated to this hypothesis):** already re-reads the file
  under a lock and merges by agent `id` before writing via `os.replace`, so a
  second process landing on the same `iter-NNN` directory does not lose the
  first process's agent records — it only risks an agent-id collision, which
  is a UUID-strength random id (`a00-xxxxxxxx`) and not the kind of collision
  `seq 1 N` produces.

So `manifest.json` specifically is accidentally load-bearing against the
exact hazard this hypothesis names, even though nothing loop-scopes the
*directory* name itself. Other artifacts written straight to `iter_dir`
without going through `_merge_manifest` — e.g. `iter-001-graph.json` seen in
the sibling's `ls` output — have no such protection and would still be a
plain overwrite. The hypothesis's testable_claim ("iteration ids are
loop-scoped end to end") stays disproved at the id-allocation layer; it is
partially, accidentally true at the manifest-content layer for one specific
file, by a mechanism this hypothesis did not name and would not survive
being asked about `iter-NNN-graph.json` or the per-agent `sess_dir`.

Ran `python3 -m pytest extensions/agi/tests/ -q` afterward (no source files
were touched, only a scratch script imported `dispatch` and ran against a
tmpdir copy) — pre-existing suite, unaffected.


## Agent Notes
Confirmed via live tmpdir test that dispatch._merge_manifest merges by agent id and does not destroy prior manifest.json data, but this only mitigates one file -- driver.sh's seq-1-N counter and the id-allocation layer remain unscoped and unguarded, agreeing with 3 sibling experiments that the hypothesis's end-to-end loop-scoped-id claim is not yet implemented

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-26a8af2c, iter 1039). Accepted unchanged. This is the only
node in the wave that ran anything rather than reading source: it copied the
real `.agi/sessions/iter-001` to a tmpdir and drove `dispatch._merge_manifest`
against it, which is why it found the split the grep-only siblings could not
see — the manifest *content* survives a directory reuse (merge by agent id),
while the directory *id* is unscoped. Its own prediction that non-manifest
artifacts stay unprotected is now confirmed concretely: `post_wire.py:514`
writes `iter-{n:03d}-graph.json` into the same directory with no merge step.
Verdict left at inconclusive_lean_disproved:70 and not promoted, because the
tmpdir run tests the mitigating layer, not the guard the hypothesis claims.
<!-- THOUGHT:END -->
