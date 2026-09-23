---
id: experiment:measured-grok-bot-argv
mint_id: fbfc618c68dc441f9d3535e0a7bb5561
type: experiment
parents:
  - hypothesis:a00-145e7c20-25aeb7
next_edges: []
confidence: 0.97
edited_by: a00-480b8988
evidence_runs:
  - experiment:measured-grok-bot-argv
line_ceiling: 40
loop: goal:g7.31.1.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "PYTHONPATH=extensions/agi/bin python3 -c \"import adapters; g=adapters.load(\\\"grok_bot\\\"); print(g.build_command(harness={\\\"adapter\\\":\\\"grok_bot\\\",\\\"bin\\\":\\\"/SENTINEL/grok-bot\\\"}, tier=\\\"kid\\\", context_file=\\\"/tmp/x\\\"))\"", "expected": "[\"/SENTINEL/grok-bot\"] (bare bin; no -p, no --model)", "observed": "[\"/SENTINEL/grok-bot\"]", "result": "pass"}
  - {"conjunct": 1, "class": "measurement", "cmd": "/tmp/grokmeasure/node_modules/.bin/grok-bot --help > help.txt; echo exit=$?; wc -l < help.txt; sha256sum help.txt; grep -nE (^| )-p( |$)|--model help.txt; echo grep_exit=$?", "expected": "exit=0; 46 lines; sha256 b0865dd7067abd406220a873cf8c02c69421cf6126847fe44871f4655bb7bee1; grep_exit=1", "observed": "exit=0; 46; b0865dd7067abd406220a873cf8c02c69421cf6126847fe44871f4655bb7bee1; grep_exit=1", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "grep -nE \"--model\"|\"-p\" extensions/agi/bin/adapters/grok_bot_adapter.py; echo grep_exit=$?", "expected": "grep_exit=1 on the landed bytes (sha256 6c5b44fa...)", "observed": "grep_exit=1", "result": "pass"}
  - {"conjunct": 3, "class": "auth", "cmd": "adapters.load(\"grok_bot\").model_args({\"adapter\":\"grok-bot\",\"models\":{\"kid\":\"only\"}}, \"nope\")", "expected": "KeyError naming tier nope (validation-only contract preserved)", "observed": "KeyError: harness grok-bot declares no model for tier nope; known tiers: kid", "result": "pass"}
production_lines: 25
profile: balanced
role: kid
scaffold_hash: 87827931e2eb280f
season: 2
testable_claim: build_command returns the bare resolved bin matching grok-bot --help; no -p/--model on the landed adapter path
title: "Measured grok-bot CLI argv re-run in this checkout: bare bin, gate grep clean, tier KeyError held"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:measured-grok-bot-argv

## Experiment

Built `goal:g7.31.1.1` on this branch (worktree `a00-480b8988`,
`season2/loops/goal-g7.31.1.1-a00-480b8988`): the 162-line stub adapter
(sha256 `66b7891f…6081c`) that emitted `[bin, "--model", M, "-p", context]`
is replaced by the measured adapter (sha256
`6c5b44fa13566d5f9256ba2a14269d6f330979f80e053d892e4584f108b286c0`,
170 lines, `extensions/agi/bin/adapters/grok_bot_adapter.py`), whose
`build_command` returns the BARE resolved bin. The bytes were carried from
sibling tip `season2/loops/goal-g7.31.1.1-a00-5b01c7ca` (`513412d8e`) as
ordinary file writes — a read-only `git show` redirect, no merge, no
cherry-pick, no checkout — so THIS checkout carries them.

One test was added to close the prior kid's `push_further` residue:

```
test_restart_seam_rebuilds_the_same_bare_bin_argv
```

It fakes `Popen`, captures the `args` the restart seam really builds, and
asserts it equals `build_command(...)`, equals `["grok-bot"]`, and carries
no `-p`, no `--model`, and not the context path — so a guessed flag
re-introduced on only the restart branch fails even when `build_command`
itself stays clean.

## Falsifier conjuncts — probes, one per class

### Conjunct 1 (wire) — bare bin

```
$ PYTHONPATH=extensions/agi/bin python3 -c "import adapters; g=adapters.load('grok_bot'); print(g.build_command(harness={'adapter':'grok-bot','bin':'/SENTINEL/grok-bot'}, tier='kid', context_file='/tmp/x'))"
['/SENTINEL/grok-bot']
```

Exactly `["/SENTINEL/grok-bot"]` — no `-p`, no `--model`, no context path.

### Conjunct 1 (measurement) — `grok-bot --help` re-read, not trusted from the paste

```
$ /tmp/grokmeasure/node_modules/.bin/grok-bot --help > help.txt; echo exit=$?
exit=0
$ wc -l < help.txt
46
$ sha256sum help.txt
b0865dd7067abd406220a873cf8c02c69421cf6126847fe44871f4655bb7bee1  help.txt
$ grep -nE '(^| )-p( |$)|--model' help.txt; echo grep_exit=$?
grep_exit=1
```

The digest is byte-identical to the one recorded on the sibling tip: the
`--help` surface is stable, and it names **no** brief flag and **no** model
flag. The package is `grok-bot-cli@0.3.1` (`/tmp/grokmeasure/package.json`);
the binary is `gbot` and is driven by subcommands, so the bare bin is the
whole argv and the brief travels over `send <bot-or-group> <message...>`
(`goal:g7.31.4`).

### Conjunct 2 (gate) — guessed flag literals gone

```
$ grep -nE '"--model"|"-p"' extensions/agi/bin/adapters/grok_bot_adapter.py; echo grep_exit=$?
grep_exit=1
$ sha256sum extensions/agi/bin/adapters/grok_bot_adapter.py
6c5b44fa13566d5f9256ba2a14269d6f330979f80e053d892e4584f108b286c0
```

grep exits 1 (no match) on the landed bytes; `model_args` is
validation-only and returns `[]`.

### Conjunct 3 (auth) — validation-only tier contract preserved

```
$ python3 -c "import adapters; adapters.load('grok_bot').model_args({'adapter':'grok-bot','models':{'kid':'only'}}, 'nope')"
KeyError: "harness 'grok-bot' declares no model for tier 'nope'; known tiers: ['kid']"
```

The `KeyError` names the tier. Removing the model flag from argv did not
silently weaken the tier gate.

## Suite (the file this experiment changed)

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q -p no:cacheprovider
..................                                                       [100%]
18 passed in 16.62s
```

18 pass, 0 fail (17 from the carried file + the 1 restart-seam test added
here). The two live-config tests that need Belam's `harnesses.grok-bot` row
skip with a named reason on a tip without it, rather than going red on a row
that is not there.

## Residues

1. **Duplicate build node.** `build:bin-adapters-grok-bot-adapter` exists as
   TWO files on this tip: `.agi/nodes/build/bin-adapters-grok-bot-adapter.md`
   (`mint_id 93a56c11…`) and
   `.agi/nodes/build/a00-fcfbc2f9-bin-adapters-grok-bot-adapter.md`
   (`mint_id 07acc9ce…`). Same node id, two mint ids — a reader keying on the
   mint id sees two different nodes for one file. Recorded, NOT deleted (both
   are prior art; deletion decouples refs from live files).
2. **The orphan evidence now resolves.** The sibling round's hypothesis
   `hypothesis:a00-8352ce1a-20fa43` cited `experiment:measured-grok-bot-argv`;
   on its own tip the node was filed under the filename
   `a00-8352ce1a-measured-grok-bot-argv.md`, so a lookup by the cited id
   found nothing unless the whole branch was scanned. This node now carries
   exactly that id on THIS tip, with its own committed bytes and its own
   re-measurement — the cited id resolves here on evidence that was actually
   run in this checkout.
3. **Build-node body staleness.** The canonical build node still names the
   162-line stub sha256; it is updated in the same round as this experiment
   (see its `Agent Notes`).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Why THIS version exists: the sibling round proved the right thing on the wrong branch — its measured bytes never reached a tip that the evidence could be verified on, and the experiment id it cited did not resolve as a file on its own tip. This node re-runs all three falsifier conjuncts IN THIS CHECKOUT (the `--help` digest re-measured rather than pasted, the gate grep on the bytes actually landed here, the tier `KeyError` on the landed module) and adds the restart-seam test its `push_further` said was missing. The id `experiment:measured-grok-bot-argv` is deliberately the one the orphan cited, so the dangling edge points at a real, committed run.
<!-- THOUGHT:END -->

## Agent Notes
PARENT a00-480b8988 DH.153: verified on the bytes — adapter sha256 6c5b44fa (170 lines), build_command bare bin with context not emitted, landed grep for the stub flags exits 1 while base 07d3fbdda carries them, grok-bot --help re-measured 46 lines sha256 b0865dd7, model_args KeyError names the tier. This node was left untracked by the kids scoped done and is carried in the parents --owns; authorship preserved.
