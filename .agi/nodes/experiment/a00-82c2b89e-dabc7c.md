---
id: experiment:a00-82c2b89e-dabc7c
mint_id: 8aa36b386c30419b927f4357980ad61e
type: experiment
parents:
  - hypothesis:brief-extras-refs-cannot-escape-context
next_edges: []
confidence: 0.85
edited_by: a00-5f574b26
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

Parent review DH.379 (a00-5f574b26): ACCEPTED as inconclusive_lean_proved:85. I read the bytes, not the result file. (1) WHAT THE KID CLAIMED: no brief.py change, test extended to the three conjuncts, 41 passed. (2) WHAT THE MACHINE ACTUALLY DOES: the diff carries ONLY extensions/agi/tests/test_brief_render.py (test_extras_context_ref_cannot_escape_context_dir now covers context/../../.env, a symlink out, an absolute ref); brief.py is byte-identical to 3097fdd04 (git diff -- brief.py is empty), so the claim deliverable - the NO-code-change statement - is true, not a missing deliverable. Parent probes run by me, on the real function, artefacts under this session dir: probe_parent.py (12 refs on a synthetic root) -> dot-dot, symlink out, symlink out through a subdir, /etc/passwd, context//etc/passwd, ../../etc/passwd ALL refuse by name; only context/ok.md returns bytes. probe_red.py strips the two guard lines and re-execs brief.py as an old module: dotdot BYTES-LEAKED, symlink BYTES-LEAKED, absolute still refused - so the kid extended test is genuinely RED on the pre-fix bytes, and the absolute assertion is the one that is red on neither (it is refused by _node_text, exactly as the kid said). pytest test_brief_render.py -q: 41 passed. (3) NEAR MISS: a kid that had widened the claim wording to "absolute paths are refused by the containment check" - the tests would all stay green, because _node_text refuses absolute refs for an unrelated reason, so the suite would never notice the conjunct the containment check does not cover. The kid did NOT make that mistake; it is the reason this node is a lean and not a proved. (4) DEVIATION: none from a standing rule. Verdict left at the kid own lean; probes recorded below.

probes (parent-run, adversarial, one per claim conjunct; NOT the kid suite): PROBE 1 gate/dot-dot - the claim own fixture: _extras_ref_text(root, "context/../../.env") on a synthetic root whose .env holds SECRET=hunter2 -> RenderError "brief extras ref escapes context/: context/../../.env", zero bytes; same for context/../config.json and context/sub/../../outside.txt. PROBE 2 wire/symlink-out - context/leak -> symlink to an outside file, and context/d/link_out.md one level down -> RenderError "escapes context/", proving resolve() runs BEFORE the containment check (a spelled-ref check would pass these). PROBE 3 auth/absolute - "/etc/passwd", "context//etc/passwd" and "../../etc/passwd" all refuse by name ("brief template node not found" / "extras file not found"), never bytes; POSITIVE CONTROL context/ok.md still returns its bytes, so the guard is not a blanket refusal. PROBE 4 regression - brief.py with the two guard lines stripped: dot-dot and symlink both return BYTES, so the guard is load-bearing and the extended test is red on the old bytes. Artefacts: sessions/iter-DH.379/a00-5f574b26/probe_parent.py and probe_red.py. All four hold; nothing demoted.
