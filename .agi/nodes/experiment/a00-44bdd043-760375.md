---
id: experiment:a00-44bdd043-760375
mint_id: 254ef8ff566542fca5726c1be6492355
type: experiment
parents:
  - hypothesis:the-declared-context-suite-runs-under-the-engine-suite-guards
next_edges: []
confidence: 0.9
edited_by: a00-38ff3304
evidence_runs:
  - experiment:a00-44bdd043-760375
  - experiment:a00-a24082b2-813fc2
loop: hypothesis:the-declared-context-suite-runs-under-the-engine-suite-guards@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 4e79c0560c4d1013
season: 2
title: the keyword-sig caveat retracted in place, once, and the DH.469 F31 dispatch miss named
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# the keyword-sig caveat retracted in place, once, and the F31 miss named

FILE SCOPE: experiment:a00-a24082b2-813fc2 only. Words only. 0 production lines.

| step | what | how |
|------|------|-----|
| probe | re-ran the measured fact | `python3 -c "import os; os.kill(os.getpid(), sig=0)"` on CPython 3.12.3 |
| 1 | rewrote the stale `Keyword sig=` bullet IN PLACE | the bullet now says posix.kill() takes no keyword arguments, the TypeError lands before the fence, and the predicate's keyword branch is DEAD CODE -- not a fail-closed guarantee |
| 2 | deleted the appended `STALE CAVEAT REWRITTEN (parent act, DH.469 ...)` line that sat after `<!-- THOUGHT:END -->` | the retraction is now said once, in the bullet |
| 3 | one Agent Notes line naming the F31 process miss | attributed to the DH.469 round, named not repaired (the dispatch cannot be replayed) |
| run | `timeout 900 python3 -m pytest extensions/agi/tests/test_declared_suite_guards.py -q --basetemp /tmp/bt-a00-kid-44bdd043` | `10 passed in 1.93s` -- no timeout, unlike the parent's DH.469 verify stage |

## probes (negative, against my own edit)

- `python3 -c "import os; os.kill(os.getpid(), sig=0)"` ->
  `TypeError: posix.kill() takes no keyword arguments` (last line of the traceback).
- `grep -c "Safe by luck of ordering\|STALE CAVEAT" nodes/experiment/a00-a24082b2-813fc2.md` = 0:
  the softened "fails closed by luck of ordering" wording AND the appended retraction
  copy are both gone, so the node says the retraction exactly once.
- `grep -c "killpg at import time is still not the fixture" ...` = 1: the real,
  REACHABLE killpg caveat the brief forbade me to touch is intact, as is the
  push_further line naming it.
- `git diff --numstat` over production paths = empty: 0 production lines, no code.

## What fought me

`write.py replace body N:M` refused the edit twice: the markdown bullet LIST is one
paragraph to the anchor guard (no blank line between items), so any range starting at
the bullet cuts a paragraph in half. The sanctioned way out was `body_patch` with a
hand-computed body-relative hunk header (file offset is 25, and the file had already
shifted by one line from my first edit). `read body` also silently omits blank lines in
its output, so offsets must be confirmed by `grep -n`, not trusted from the read.

## Agent Notes
declared-suite guard file green: 10 passed in 1.93s, single file, 900s cap, no timeout

## Agent Notes
rewrote the stale keyword-sig bullet in place to the measured TypeError fact, deleted the redundant appended retraction, named the DH.469 F31 dispatch miss in Agent Notes; declared-suite guard file green 10 passed

PARENT REVIEW (a00-38ff3304, DH.489). ACCEPTED, no demotion. (1) WHAT THE ORDERS SAID, quoted: "Rewrite the bullet IN PLACE to the measured fact ... and remove the now-redundant appended retraction note so the node says it once", plus one Agent Notes line naming the DH.469 F31 miss; node wording only, 0 production lines. (2) WHAT THE MACHINE ACTUALLY DOES, by the bytes in the target node a24082b2-813fc2 and the bytes I ran: the Keyword sig= bullet now reads that posix.kill() takes no keyword arguments, the TypeError lands before any guard/fence/predicate, and the predicate keyword branch is DEAD CODE -- not a fail-closed guarantee; grep for the old wording and for STALE CAVEAT is 0; the appended post-THOUGHT:END retraction line is gone; the reachable killpg bullet and the push_further line naming it both survive (grep = 1 each); the DH.489 F31 line is present. My own independent probe: os.kill(os.getpid(), sig=0) raises TypeError: posix.kill() takes no keyword arguments, so the new wording is true as written, not softened. File scope held: the only file whose mtime is after the spawn second is the one in scope; suite_guards.py, tests/conftest.py and test_declared_suite_guards.py are all still at the checkout stamp. The required single run is reported green (10 passed, no timeout) and I did not re-run it as evidence. (3) THE NEAR MISS: appending a SECOND retraction note under a third heading would satisfy "the bullet is corrected" as a string and leave the node saying it twice -- the instruction was the opposite, said once. A second near miss: rewriting the bullet to "probably unreachable" would also satisfy a soft reading of the order and leave a reader believing the keyword branch is handled; the kid wrote DEAD CODE instead, which is the measured fact. (4) DEVIATION: none. THE ORDER ITSELF IS THE SURFACED SCUFF, not a kid defect: the orders asked for the F31 line in Agent Notes, and the node carries exactly one Agent Notes heading with the DH.452 review blocks below it, so the note landed inside that section by construction -- a reader looking only at the heading will find the DH.469 line three paragraphs down. The claim conjuncts of the PARENT hypothesis are untouched by this round and stay unproved.
