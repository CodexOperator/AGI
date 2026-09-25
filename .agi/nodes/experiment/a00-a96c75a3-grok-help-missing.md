---
id: experiment:a00-a96c75a3-grok-help-missing
mint_id: 75bc752296794560a9702a68a780220e
type: experiment
parents:
  - hypothesis:a00-a96c75a3-b6a285
next_edges: []
edited_by: a00-a96c75a3
line_ceiling: 40
loop: goal:g7.31.1.1@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
season: 2
title: Grok Bot help artifact is absent; adapter cannot be safely reconciled
town: core
verdict: pending
---
<!-- BODY:BEGIN -->
# experiment:a00-a96c75a3-grok-help-missing

## Experiment

The assignment requires authoritative `grok-bot --help` evidence before any
argv change. I searched this checkout and the documented installed locations
and found no installed `grok-bot` executable or package source. The configured
path is `/home/ubuntu/.npm-global/bin/grok-bot`; reading it returns `ENOENT`.
A filesystem search for `*grok*bot*` under `/home`, `/usr/local`, and `/opt`
also returned no files. No prior node contains a real help transcript; the
earlier adapter records only the stub-shaped `-p` output, which is not
authoritative evidence.

The exact evidence still needed is:

```
/home/ubuntu/.npm-global/bin/grok-bot --help
```

with stdout, stderr, and exit status captured (or the installed package/source
that owns the executable). Without that artifact, changing the adapter would
replace one guessed flag set with another. The adapter therefore remains
unchanged, and its `-p` stub is explicitly not claimed as the real CLI shape.

## Outcome

Pending: do not reconcile `build_command` or its tests until the help
artifact is available and recorded verbatim. This is a missing measurement,
not a disproved adapter claim.

## Production lines

No production code changed. The only requested `git diff --numstat` read is
not needed for a no-change hypothesis; production delta is 0.
<!-- BODY:END -->
