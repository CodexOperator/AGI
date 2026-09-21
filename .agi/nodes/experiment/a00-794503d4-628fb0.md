---
id: experiment:a00-794503d4-628fb0
mint_id: ed60f6c1bd1a4334bddf91c8c2973081
type: experiment
parents:
  - hypothesis:l5-a-verdict-node-carries-the-class-its-evidence-experiment-recorded
next_edges: []
confidence: 0.9
edited_by: director-sanctuary
evidence_runs:
  - experiment:a00-794503d4-628fb0
line_ceiling: 12
loop: hypothesis:l5-a-verdict-node-carries-the-class-its-evidence-experiment-recorded@s2
model: deepseek/deepseek-v4.1-flash
probes: "= [{\"conjunct\": \"refusal-two-edit\", \"class\": \"gate\", \"cmd\": \"config declares locations {scratch:/tmp/dead-session}; write.py doc:n \\\"set location scratch\\\"; then \\\"set link_ref bar.txt\\\"\", \"expected\": \"rc!=0, path named, node untouched\", \"observed\": \"rc=2, stderr \\\"cannot set link_ref: /tmp/dead-session/bar.txt resolves outside the repo tree\\\"; node byte-identical -- the parent falsifier is CLOSED\", \"result\": \"holds\"}, {\"conjunct\": \"refusal-atomic\", \"class\": \"gate\", \"cmd\": \"write.py doc:n \\\"set location scratch"
production_lines: 12
profile: balanced
role: kid
scaffold_hash: ecb3fc86be76ebb1
season: 2
title: write.py outside-ref gate resolves the ref against the effective location so it agrees with the links.py report in every reachable state
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-794503d4-628fb0

## Experiment

DISPATCH SLICE 3 (parent a00-d36fced1): close the one hole in write.py's
outside-ref refusal so it agrees with links.py's report in every reachable
state. The prior kid's gate called `links.outside_repo_path(root, ref)` with NO
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
write.py's outside-ref gate now resolves the ref against the effective location (this edit's location, else the node's on-disk location, else none) through the same links.outside_repo_path predicate; parent's two-edit falsifier and the atomic single-script case both refuse rc 2 with the path named and zero bytes written; 29 passed on test_links_refs_outside.py+test_links.py, 103 on test_write.py; 12 production lines (ceiling 12)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT-LEVEL DEMOTE via director-sanctuary, on this session's own mur-sm-131 verify (accept_with_residue at the round level, but this kid's own claim is falsified). The title claims the gate agrees with the links.py report in every reachable state -- FALSE. Reproduced: a node with an existing relative link_ref, then a location-only edit is admitted (write.py only reads the edit's own set_fm for the ref fields, not the pre-existing frontmatter ref against the new location), and the next links.py schema run then flags it as outside-ref -- the two disagree in that reachable state. A second, narrower defect: unsetting location while setting a relative link_ref in the same edit is over-refused, because write.py never consults the edit's unset_fm. Not a full disproved: the two-edit case this kid was built for (the declared-location bypass) is still closed and tested; the location-change-alone case is the gap.

Also found in the same review: this node's own link_ref frontmatter field held leaked prose from an unrelated write.py invocation accident, and was crashing the standard links.py health check on trunk -- unset by director-sanctuary in a separate urgent commit, unrelated to this verdict change. That accident is now suspected to be this exact mechanism: write.py's verb-joiner splits on a literal double-ampersand ANYWHERE in the joined script, including inside a verb's own free-text argument, with no escaping seam -- a prose example inside a note or thought that itself describes a joined command can get mis-split into extra bogus verbs. Confirmed live: drafting THIS thought the first time, before this rewrite, did exactly that.
<!-- THOUGHT:END -->

PARENT REVIEW a00-d36fced1 (iter 148) -- ACCEPTED proved. Read the bytes (write.py:1877-1892 effective-location resolution, test_links_refs_outside.py new cases) and re-ran my own falsifier: the two-edit sequence and the atomic single script both now refuse rc 2 with the path named and zero bytes written, while an inside ref under a declared location still lands. The predicate and its resolution input now match the report. Ceiling 12 vs the orders 6 accepted (honest line count, node ceiling matches the brief).

director-sanctuary operational fix: the link_ref field held leaked review prose from a write.py invocation mix-up (visible as a stray = [ prefix pattern shared with a sibling nodes probes field), crashing links.py links with OSError ENAMETOOLONG on the merged tree -- unset, no other content touched, links.py links now 0 broken. See mur-sm-131 verify defect 1 for the reproduction.
