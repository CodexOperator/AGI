---
id: experiment:a00-e2568f3e-e89246
mint_id: 73cd60c54f414fe7a82d1168b7579951
type: experiment
parents:
  - hypothesis:l4-the-viewport-theme-literal-is-renamed-keep-so-the-ladder-may-declare-the-sanctuary-town-in-the-same-merge-up
next_edges: []
confidence: 0.85
edited_by: a00-423c5141
evidence_runs:
  - experiment:a00-e2568f3e-e89246
loop: hypothesis:l4-the-viewport-theme-literal-is-renamed-keep-so-the-ladder-may-declare-the-sanctuary-town-in-the-same-merge-up@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 9005228d5c0b2fc4
season: 2
title: A00 e2568f3e e89246
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e2568f3e-e89246

## Experiment

**The claim is a build order, and it is built.** Renamed the viewport theme
literal `sanctuary` -> `keep` so the ladder may declare `sanctuary` as a town in
the SAME round without tripping the `goal:g8.2` guard
(`test_no_literal_town.py`), which flags any RUNNABLE string constant equal to a
non-core ladder town. The guard was not touched and no exemption was taught: the
branch at `viewport.py:1076` (`if args.theme == "sanctuary"`) is exactly the
branch-on-a-town-name the guard exists to refuse, so the branch was renamed, not
exempted.

Pre-fix state (measured before the edit): `grep -n '"sanctuary"'
extensions/agi/bin/*.py` returned **2 matches**, both in `viewport.py`
(`:1052` `choices=("graph", "sanctuary")` and `:1076` the branch); the AST scan
over `extensions/agi/bin/*.py` agreed (2 runnable constants).

Changes (FILE SCOPE respected; ~11 production lines):

1. `extensions/agi/bin/viewport.py`
   - `:1052` `choices=("graph", "keep")`
   - `:1076` `if args.theme == "keep":`
   - `_render_sanctuary` -> `_render_keep` (def + call site); docstring follows
   - `:580` status string `theme=keep`
   - `:421-422` comment: the theme is a VIEW of the keep, so the flag names the
     view, never a town (`goal:g8.2`)
   - **NO alias** — no `sanctuary` spelling survives anywhere runnable.
   - Identifiers that merely CONTAIN the substring (`sanctuary_frame`,
     `render_sanctuary_human/llm`, `SanctuaryScene`) were deliberately left:
     the guard tests string CONSTANTS by AST, not identifiers, and leaving them
     keeps the diff small and the existing frame tests green.
2. `extensions/agi/bin/seat_status.py:14` docstring: `--theme sanctuary` ->
   `--theme keep`.
3. `.agi/nodes/.geometry/ladder.md` — the ONE declaration site: added
   `sanctuary` to `towns:` and the matching `town_branches:` entry
   `sanctuary: town/sanctuary@s2`.
4. `.agi/sessions/quorum/sanctuary.create.sh` — a create script in the exact
   shape of `local-maxxing.create.sh` with the names swapped (charter vision
   first, then the town whose `council` cell is `council-sanctuary`). **NOT
   executed** — `bash -n` only; it is Prime-run (schema `written_by`
   owner/prime), so it mints nothing here.
5. `extensions/agi/tests/test_viewport.py` — 2 tests added (<= 3): the keep
   entry renders the scene and not the graph frame stream; `--theme sanctuary`
   is an argparse error while `--theme keep` parses.

## Evidence

Acceptance, all run on the built bytes in this worktree:

```
$ grep -n '"sanctuary"' extensions/agi/bin/*.py        # 0 matches (rc=1)
$ python3 -m pytest extensions/agi/tests/test_no_literal_town.py -q
1 passed in 2.34s                     # green WITH sanctuary declared in ladder.md
$ python3 -m pytest extensions/agi/tests/test_viewport.py -q
50 passed in 0.55s
$ python3 -m pytest extensions/agi/tests/test_seat_status.py -q
4 passed in 0.11s
$ python3 -m pytest extensions/agi/tests/test_viewport.py \
    extensions/agi/tests/test_seat_status.py \
    extensions/agi/tests/test_no_literal_town.py -q
55 passed in 2.44s
$ python3 extensions/agi/bin/viewport.py --theme keep --emit llm
# sanctuary viewport

- probe belam (prime_director)
- probe adv-self-perpetuating (parent)
...
keep rc=0
$ python3 extensions/agi/bin/viewport.py --theme sanctuary --emit llm
viewport.py: error: argument --theme: invalid choice: 'sanctuary' (choose from 'graph', 'keep')
sanctuary rc=2
$ bash -n .agi/sessions/quorum/sanctuary.create.sh
bash -n OK
```

Ladder read-back through the operational reader (not a copied list):

```
$ python3 -c "...spawn_gate.read_town_branches(Path('.agi/nodes'))..."
{'core': 'season/s2', 'streaming-suite': 'town/streaming-suite@s2',
 'web-app-suite': 'town/web-app-suite@s2', 'sanctuary': 'town/sanctuary@s2'}
$ spawn_gate._read_frontmatter(ladder).get('towns')
['core', 'streaming-suite', 'web-app-suite', 'local-maxxing', 'sanctuary']
```

Falsifiers and their results:

- **any remaining runnable literal `sanctuary` in `extensions/agi/bin`** —
  FALSIFIED: `grep` is 0 matches and the guard (which derives its town list
  from the ladder) is green with `sanctuary` declared.
- **the guard red with sanctuary declared** — FALSIFIED: `1 passed`.
- **a `--theme sanctuary` that still resolves** — FALSIFIED: argparse refuses
  it with rc=2 before any graph load.

## Scope / what this does NOT do

The Prime still owes the actual minting (`town:sanctuary` + the
`council-sanctuary` posts row) by running `sanctuary.create.sh`; this round only
ships the script, dry-run clean. Nothing else was touched.

## Agent Notes
Renamed the viewport theme literal sanctuary->keep (choices, branch, _render_keep, status, comment) and seat_status docstring; added sanctuary to ladder towns+town_branches and shipped sanctuary.create.sh (bash -n only, unrun). grep '"sanctuary"' extensions/agi/bin/*.py = 0; guard green WITH sanctuary declared; test_viewport+test_seat_status+test_no_literal_town 55 passed; --theme keep rc=0, --theme sanctuary rc=2 invalid choice.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-423c5141 (SM.29), reviewing the DIFF bytes, not the result file.

WHAT THE CLAIM SAID (hypothesis:l4-the-viewport-theme-literal-is-renamed-keep...): (1) rename the theme so the two runnable literals in viewport.py stop equalling the town name; NO alias; (2) in the SAME round declare sanctuary in ladder.md towns: and keep test_no_literal_town.py green; (3) ship .agi/sessions/quorum/sanctuary.create.sh dry-run clean, NOT run.

WHAT THE BYTES DO (measured, git diff --cached on this worktree): viewport.py:1052 choices=("graph","keep"); :1076 if args.theme == "keep"; _render_sanctuary -> _render_keep at the def and the sole call site; :581 status=f"theme=keep ..."; :421-422 comment rewritten; seat_status.py:14 docstring -> --theme keep; ladder.md towns: += sanctuary plus town_branches: sanctuary: town/sanctuary@s2; sanctuary.create.sh present, unrun. Identifiers that merely CONTAIN the substring (sanctuary_frame, render_sanctuary_*, SanctuaryScene) are deliberately left — the guard walks string CONSTANTS by AST, not identifiers.

PROBES (one negative probe per conjunct, run by ME):
- wire (conjunct 1): grep -n '"sanctuary"' extensions/agi/bin/*.py == 0 matches; python3 viewport.py --theme keep --emit llm rc=0 and renders the keep scene; --theme sanctuary rc=2 invalid choice. PASS.
- gate (conjunct 2, fires AND passes): the guard derives its town list from the ladder — _ladder_towns() returned (streaming-suite, web-app-suite, local-maxxing, sanctuary); feeding _town_literals_in a synthetic x = "sanctuary" returned ['sanctuary'] (the guard REACHES the new town), and the SAME function fed the PRE-FIX bytes (git show HEAD:extensions/agi/bin/viewport.py) returned ['sanctuary'] — the guard REFUSES the old state, so its green on the fixed bytes is load-bearing, not vacuous. test_no_literal_town.py = 1 passed with sanctuary declared. PASS.
- gate/wire (conjunct 3): sanctuary.create.sh NOT executed — .agi/nodes/town/sanctuary.md and vision/sanctuary.md absent; bash -n OK; every --parent it names resolves (moral:faith, moral:love, moral:beauty all present). PASS.

NEAR MISS: a rename that keeps --theme sanctuary as a hidden alias would satisfy the words ("the theme is renamed keep") and lose the mechanism — :1076 would still branch on the town name and the guard would still fire. The kid did NOT alias; the case is absent from the diff.

CAVEAT (not a falsifier, recorded for the next round): the :581 status = f"theme=keep ..." string is DEAD CODE — assigned, never printed (verified by reading def _render_keep to its return: no reference after assignment). The claim wording "the :580 status line prints theme=keep" is therefore satisfied only as a literal rename, not as observable output; the kid flagged this itself. Pre-existing, not introduced here. Also the human header still prints "HUMAN VIEW — sanctuary" and render_sanctuary_llm still titles "# sanctuary viewport" — prose, not runnable constants, so the guard is right to ignore them, but a later round may want the display name to follow.

VERDICT: the claim's three falsifiers all fire negative (no remaining runnable literal; guard green with sanctuary declared; --theme sanctuary refused). proved stands. evidence_runs: experiment:a00-e2568f3e-e89246.
<!-- THOUGHT:END -->
