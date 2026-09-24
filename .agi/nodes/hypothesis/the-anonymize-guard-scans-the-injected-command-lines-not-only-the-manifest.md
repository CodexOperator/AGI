---
id: hypothesis:the-anonymize-guard-scans-the-injected-command-lines-not-only-the-manifest
mint_id: cfe258ec4e3c45679c48a65b313df2c2
type: hypothesis
parents:
  - goal:g1.25.5
next_edges: []
assigned: "director-engine (leaf goal:g1.25.5, round C2: the mesh about under the anonymize guard)"
ceiling: 1 kid, 10-12 production lines per conjunct, pi parent (scope, never spend)
confidence: 0.7
edited_by: director-engine
scaffold_hash: ffea91306d8decc7
season: 2
testable_claim: After the fix, the anonymize guard scans both texts command:commands renders -- render_manifest and the INJECTION.md command lines of render_for_injection -- through one helper, so a box label or dotted-quad address in any about fails it, including an about the manifest shadows with a reason (today mesh-gw and verify-suite), proved by a committed mutant test red against the manifest-only guard, with test_commands_manifest.py and test_commands.py green (test-only).
title: "The anonymize guard scans the injected command lines, not only the manifest -- a box label in any about, shadowed or not, fails a test (goal:g1.25.5 round C2; assigned: director-engine)"
town: local-maxxing
---
# hypothesis:the-anonymize-guard-scans-the-injected-command-lines-not-only-the-manifest

# hypothesis:the-anonymize-guard-scans-the-injected-command-lines-not-only-the-manifest

**Assigned: director-engine** (leaf goal:g1.25.5, round C2; the owner's cli-maxxing, goal:g1.25) · build loop · one `[merge-up]` to thought-master. Dispatch AFTER C1 (hypothesis:the-choice-surface-derives-proposable-from-declared-side-effects) merges.

## Measured (bytes verified by a read-only triage pass for director-engine 22:4xZ 09-23 on the post tip d5696ac1de (every file:line read))
```
guard     test_commands_manifest.py:858 _BOX_LABELS; :861-870 scans commands.render_manifest(root) only (:866) -- R-EF45 M1,
          untouched since EF.45
reach     manifest() takes a commands: entry's `about` as its purpose only when its manifest: override declares neither purpose
          nor reason (commands.py:220, :241-244): the four mesh abouts EF.45 rewrote (commands.md:162, :170, :178, :186) ARE in the
          manifest and scanned -- the residue is narrower than filed
gap       mesh-gw's about (commands.md:194) and verify-suite's (:116) are shadowed by their reasons (:2743, :3004): absent from
          render_manifest, present in render_for_injection (commands.py:514-547; about at :538, :544) -> briefing.py:274-276,
          :336-337 -> INJECTION.md, which no test scans on the live node (test_commands.py:177-193 read a synthetic one)
live      probe on the tip: 0 box labels, 0 dotted quads in either render -- the widened live guard is green pre-fix, so the red
          is a mutant
```

## CLAIM
After the round, the anonymize guard scans BOTH texts command:commands renders -- `commands.render_manifest` and the INJECTION.md command lines of `commands.render_for_injection` -- through one helper over the one `_BOX_LABELS` list and the one dotted-quad pattern, so a box label or address in any `about` fails it, including an `about` the manifest shadows with a `reason` (today mesh-gw's and verify-suite's). A committed mutant test builds a tmp node whose `commands:` entry plants a `_BOX_LABELS` token and a dotted quad in its `about` behind a `manifest:` override carrying a reason, shows the manifest alone does not carry them, and asserts the guard names both -- red when the helper is narrowed back to the manifest (the pre-fix guard). The live guard stays green on today's node. Test-only: nothing under bin/, no node edit.

## Dispatch line
config-max: none / template-max: none -- the `about` lines stay the node's / code: none in bin/ -- the guard reads the second render commands.py already produces

## FALSIFIERS
- the mutant passes the guard, or the new test is green against the manifest-only guard
- the live guard red on today's commands.md -- fixed in the data under the owner's anonymization rule, never by exempting a token
- a second copy of the label list or the address pattern; an existing assertion relaxed
- any of the named test files red; a change outside FILE SCOPE

## TESTS
test_commands_manifest.py (the guard, the mutant) · test_commands.py -- those files only, under `env -u TMUX -u TMUX_PANE`

## FILE SCOPE
extensions/agi/tests/test_commands_manifest.py -- nothing under extensions/agi/bin/, never .agi/nodes/.geometry/commands.md

HAZARD: the mutant lives in tmp_path only -- never write a box label or an address into the live node, a commit message or a dm; never run `commands.py run mesh-*` (it opens a shell on a farm box)
HAZARD: test_commands_manifest.py is shared with C1 (its gate at :848-855 sits beside this guard) and rounds B/D -- dispatch after C1 merges

## CEILING
1 kid · 10-12 production lines per conjunct · pi parent · scope, never spend (owner 09-23 14:xZ)
