---
id: experiment:a00-82c2b89e-dabc7c
mint_id: 8aa36b386c30419b927f4357980ad61e
type: experiment
parents:
  - hypothesis:brief-extras-refs-cannot-escape-context
next_edges: []
confidence: 0.85
edited_by: a00-82c2b89e
evidence_runs:
  - experiment:a00-82c2b89e-dabc7c
loop: hypothesis:brief-extras-refs-cannot-escape-context@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 9b52199f1646919d
season: 2
title: all three escape conjuncts of _extras_ref_text refuse on the real bytes
town: core
verdict: inconclusive_lean_proved:85
---
# experiment:a00-82c2b89e-dabc7c

# all three escape conjuncts of `_extras_ref_text` refuse on the real bytes

## What I ran

Probed the real `extensions/agi/bin/brief.py` (tip 3097fdd04) on a synthetic
graph root, one negative probe per conjunct of the claim. Probe lives at
`.agi/sessions/iter-DH.379/a00-82c2b89e/probe_extras.py`; output below is
verbatim (`probe_out.txt`).

```
A positive: context/ok.txt                 BYTES!!  'OK\n'
A positive: context/sub/deep.txt           BYTES!!  'DEEP\n'
A positive: symlink staying inside         BYTES!!  'OK\n'
B dot-dot, the claim's own fixture         REFUSED  brief extras ref escapes context/: context/../../.env
B dot-dot one level, graph-side .env       REFUSED  brief extras ref escapes context/: context/../.env
B dot-dot via subdir                       REFUSED  brief extras ref escapes context/: context/sub/../../outside.txt
C absolute path ref                        REFUSED  brief template node not found: /tmp/tmpmpkjnue4/.env
C absolute, real system file               REFUSED  brief template node not found: /etc/hostname
C absolute spelled context-prefixed        REFUSED  brief extras file not found: context//etc/hostname
D symlink out -> .env                      REFUSED  brief extras ref escapes context/: context/leak-env
D symlink out -> outside.txt               REFUSED  brief extras ref escapes context/: context/leak-out
E dir inside context                       REFUSED  brief extras file not found: context/sub
F dot-dot that lands back inside           BYTES!!  'OK\n'
```

## What the probes say

| conjunct | outcome | where the refusal comes from |
|---|---|---|
| dot-dot (`context/../../.env`, the claim's OWN fixture) | refuses by name, no bytes | the `is_relative_to` check, brief.py:2374 |
| symlink out of `context/` | refuses by name, no bytes | `resolve()` follows the link FIRST, then the same check |
| absolute path ref | refuses by name, no bytes | **NOT** the containment check — see below |

The positive controls (A, and F's `context/sub/../ok.txt`, which resolves
back inside) still read bytes, so the guard is not refusing indiscriminately.

## The one thing that is weaker than the claim's wording

The claim says the function "refuses **by name** any ref whose resolved path
leaves context (dot-dot segments, **absolute paths**, symlinks out)". For an
absolute ref that is structurally unreachable: the `context/` branch is entered
only when `ref.startswith("context/")`, and a string cannot be both absolute
and `context/`-prefixed. An absolute ref therefore falls to `_node_text` and
is refused as an unknown NODE ("brief template node not found: /etc/hostname"),
not as a path that tried to escape. The bytes are refused, so no leak — but
the refusal is a different one than the claim describes, and if the
`context/` prefix guard were ever widened (e.g. accepting `context` without
the slash, or a `file:` scheme) the absolute case would fall straight into the
read path un-checked for that reason. A conjunct, not a leak; recorded so a
later reader does not read "absolute paths" as "proved by the containment
check".

## Code change

**None to `brief.py`** — no probe failed, so there was nothing to fix. The one
edit is to the TEST: `test_extras_context_ref_cannot_escape_context` covered
only dot-dot, so conjuncts 2 and 3 were untested in the suite even though the
code already held. Extended the same test with the claim's own `.env` fixture,
a symlink out of `context/`, and an absolute ref. Production lines: **0**
(test files are excluded from the ceiling).

```
$ python3 -m pytest extensions/agi/tests/test_brief_render.py -q
41 passed in 1.66s
```

## Verdict reading

All three conjuncts hold against the real bytes; the escape-guard is real and
is not a blanket refusal. The hypothesis is **proved in substance** with one
wording caveat (absolute refs are refused by `_node_text`, not by the escape
check). Node deliverable; nothing left to build.

## Agent Notes
Probed all three escape conjuncts on the real brief.py bytes: dot-dot (claim's own context/../../.env fixture), symlink out of context/, and an absolute ref all refuse by name with no bytes returned; positive controls still read. Absolute refs are refused by _node_text (unreachable in the context/ branch), not by the containment check. No code fix needed; extended the existing test to cover the two untested conjuncts (41 passed, production lines 0).
