---
id: experiment:a00-794503d4-628fb0
mint_id: ed60f6c1bd1a4334bddf91c8c2973081
type: experiment
parents:
  - hypothesis:l5-a-verdict-node-carries-the-class-its-evidence-experiment-recorded
next_edges: []
confidence: 0.9
edited_by: a00-baa8e365
evidence_runs:
  - experiment:a00-794503d4-628fb0
line_ceiling: 12
loop: hypothesis:l5-a-verdict-node-carries-the-class-its-evidence-experiment-recorded@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "refusal-two-edit", "class": "gate", "cmd": "config declares locations {scratch:/tmp/dead-session}; write.py doc:n \"set location scratch\"; then \"set link_ref bar.txt\"", "expected": "rc!=0, path named, node untouched", "observed": "rc=2, stderr \"cannot set link_ref: /tmp/dead-session/bar.txt resolves outside the repo tree\"; node byte-identical -- the parent falsifier is CLOSED", "result": "holds"}
  - {"conjunct": "refusal-atomic", "class": "gate", "cmd": "write.py doc:n \"set location scratch\" then \"set link_ref bar.txt\" in ONE script", "expected": "rc!=0, path named, write nothing (sha256 before == after)", "observed": "rc=2, stderr names the path; BYTE-IDENTICAL", "result": "holds"}
production_lines: 12
profile: balanced
role: kid
scaffold_hash: ecb3fc86be76ebb1
season: 2
title: write.py outside-ref gate resolves the ref against the effective location -- the declared-location bypass is closed, but a location-only edit still bypasses it and links.py then flags the node
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-794503d4-628fb0

## Experiment

DISPATCH SLICE 3 (parent a00-d36fced1): close the one hole in write.py's
outside-ref refusal so it agrees with links.py's report for a DECLARED-LOCATION
base. The claim is scoped to that case: a location-only edit that moves an
existing relative `link_ref` outside the repo is still admitted, because
write.py:1912-1922 resolves only refs present in `edit.set_fm` and never reads
`edit.unset_fm`; `links.py schema` then flags the node. That state is NOT
covered. The prior kid's gate called `links.outside_repo_path(root, ref)` with NO
location, so a ref resolving under a DECLARED `locations:` entry — or under an
already-on-disk `location:` — was ADMITTED at write time and then flagged by
`links.py schema`. The shared predicate was right; its resolution INPUT was not.

**The effective-location rule** (one code path, still the ONE predicate):

1. `location` in THIS edit (`edit.set_fm.get("location")`) if present;
2. else the `location` already on the node file being written
   (`node_writer.find_node_file` + frontmatter read);
3. else no location (today's default).

The refusal message and exit behaviour (rc 2) are unchanged.

Measured: **12 production lines** (ceiling 12; unchanged behaviour for the
default case — only the resolution input moved).

Tests: `test_links_refs_outside.py` + `test_links.py` → **29 passed**;
`test_write.py` → **103 passed**.

## Evidence

Parent's exact falsifier, re-run by hand, now refused:

```
--- edit 1: set location scratch
updated: doc:n
rc=0
--- edit 2: set link_ref bar.txt
ERR: cannot set 'link_ref': <scratch>/bar.txt resolves outside the repo tree
rc=2
```

The ATOMIC case, one script, writes nothing (sha256 before == after):

```
--- atomic single script
ERR: cannot set 'link_ref': <scratch>/bar.txt resolves outside the repo tree
rc=2
BYTE-IDENTICAL
```

New regression tests in `extensions/agi/tests/test_links_refs_outside.py`:

- `test_atomic_location_and_ref_in_one_script_is_refused` — one script refused,
  node byte-identical after;
- `test_two_edits_location_then_ref_is_also_refused` — the on-disk location is
  the effective one, rc 2, and `links.py schema` prints no `outside-ref:` for
  it (gate and report agree);
- `test_a_ref_inside_a_declared_location_goes_through` — an inside ref under a
  declared location still lands;
- the existing `test_write_refuses_an_outside_ref_and_writes_nothing` (default,
  no location) still holds.

## Agent Notes
write.py's outside-ref gate now resolves the ref against the effective location (this edit's location, else the node's on-disk location, else none) through the same links.outside_repo_path predicate; parent's two-edit falsifier and the atomic single-script case both refuse rc 2 with the path named and zero bytes written; 29 passed on test_links_refs_outside.py+test_links.py, 103 on test_write.py; 12 production lines (ceiling 12). VERDICT QUESTION: the node's own THOUGHT says the every-reachable-state claim is FALSE (the location-only-edit bypass), so `inconclusive_lean_proved:70` reads as too strong; the honest class is lean_disproved. The field was deliberately NOT changed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Corrected in place under C item of hypothesis:mur-0921-engine-residues-dispositioned-and-corrected (EF.23, agent a00-baa8e365).
C item `exp a00-794503d4 :15/:21/:23`. Three things changed. (a) The `probes:` scalar was truncated mid-JSON at 575 chars (it ended `write.py doc:n \"set location scratch`) and lost the second (refusal-atomic) probe; it is now a YAML LIST of two probes, the second restored from the body's own Evidence prose (one script, rc 2, byte-identical). (b) The title said the gate "agrees with the links.py report in every reachable state"; re-checked against the bytes that is FALSE -- write.py:1912-1922 reads only `edit.set_fm`, so a location-only edit that moves an existing relative ref outside the repo is admitted and then flagged by links.py. The title and Experiment text now scope the claim to a declared-location base. (c) VERDICT QUESTION, not a field change: the node's own THOUGHT at :90 already says `-- FALSE`, so `inconclusive_lean_proved:70` overclaims and the honest class is lean_disproved. Recorded for the parent; verdict/lean/confidence were not touched.
<!-- THOUGHT:END -->

PARENT REVIEW a00-d36fced1 (iter 148) -- ACCEPTED proved. Read the bytes (write.py:1877-1892 effective-location resolution, test_links_refs_outside.py new cases) and re-ran my own falsifier: the two-edit sequence and the atomic single script both now refuse rc 2 with the path named and zero bytes written, while an inside ref under a declared location still lands. The predicate and its resolution input now match the report. Ceiling 12 vs the orders 6 accepted (honest line count, node ceiling matches the brief).

director-sanctuary operational fix: the link_ref field held leaked review prose from a write.py invocation mix-up (visible as a stray = [ prefix pattern shared with a sibling nodes probes field), crashing links.py links with OSError ENAMETOOLONG on the merged tree -- unset, no other content touched, links.py links now 0 broken. See mur-sm-131 verify defect 1 for the reproduction.
