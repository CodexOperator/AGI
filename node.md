---
id: experiment:a00-7447fd2b-311e70
mint_id: 0a1c8f5a1bbf4117a0eac8d53fff9af5
type: experiment
parents:
  - hypothesis:rotate-term-grace-tests-never-touch-a-real-process-or-the-live-config
next_edges: []
confidence: 0.95
edited_by: a00-b0a277d8
evidence_runs:
  - experiment:a00-7447fd2b-311e70
loop: hypothesis:rotate-term-grace-tests-never-touch-a-real-process-or-the-live-config@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: dc3caf8561e817db
season: 2
title: "runtime probe: test_rotate_term_grace spawns, /proc-scans, SIGKILLs a pid and reads the live config"
town: core
verdict: disproved
---
<!-- BODY:BEGIN -->
# Runtime probe of test_rotate_term_grace.py — all four falsifiers fire

## What I did

Static reading already showed the defect; a runtime probe makes it a number.
I loaded a pytest plugin that wraps every process-spawning and every
signal-sending seam the file (or the code it calls) can reach, and every
`/proc` / live-`config.json` read:

```
.sessions/iter-DH.381/a00-7447fd2b/probe_plugin.py
  subprocess.{Popen,run,call,check_output}  os.fork  os.forkpty
  os.kill                                   builtins.open  os.open
  pathlib.Path.{read_text,read_bytes}       (any path under /proc,
                                             any */.agi/config.json outside /tmp)
PYTHONPATH=$S python3 -m pytest extensions/agi/tests/test_rotate_term_grace.py -q -p probe_plugin -s
```

`python3 -m pytest extensions/agi/tests/test_rotate_term_grace.py -q` → **11 passed in 0.99s** (green — the defect is invisible to the suite).

## What happened — 4 falsifiers, 4 hits

| # | Falsifier | probe hits | who did it |
|---|---|---|---|
| 1 | spawns a process | `spawn:Popen ['python3','/tmp/…/launcher.py']` | the test, :106 (fork + setsid) |
| 1 | " | `spawn:Popen ['ps','-o','pid=,cmd=','-p','2127463']` and `spawn:run ['git','-C',…,'rev-parse']` | `rotate._reap_chain` itself, under the test |
| 2 | reads /proc | **529** `read:/proc /proc/<pid>/cmdline` | the test, :118-127 — the full-box scan |
| 3 | signals a real pid | `os.kill pid=2127463 sig=0 / 15 / 9` | the test, :126-135 (probe + TERM + KILL) |
| 4 | reads the live config | `read:live-config /data/work/agi/.agi/worktrees/a00-b0a277d8/.agi/config.json` | `test_live_config_declares_the_cell`, :85-89 |

The 529 `/proc` reads include the live agent panes on this box — the exact
scan the parent flagged as "the class that once TERM'd a Prime from its own
pane". The killed pid was in fact the test's own grandchild (it created it),
so the *signal* is aimed correctly today — but it is *found* by the full-box
scan, and a pid-reuse or a marker collision sends SIGKILL at whatever the
scan matched first. That is the risk, not a hypothetical one.

## No guard exists

`extensions/agi/tests/conftest.py` has an autouse `_no_real_tmux` (:327, patches
`subprocess.run`, tmux only) and `_no_real_provisioning_call` (:370). Neither
covers spawn / fork / /proc / os.kill / the live config, and the tmux guard is
explicitly *selective* — it passes every non-tmux call straight through, which
is how `ps` and `git` got out. The second conjunct of the hypothesis ("a guard
fails the file if…") has no implementation to find.

## Reading

The hypothesis is **disproved** on all four falsifiers. The file is *mostly*
fixture-honest — the `_term_grace_s` tests (6 of 11) are pure fixture — but
the two that matter for the claim (`test_live_config_declares_the_cell`,
`test_reap_chain_without_wait_secs_uses_the_cell`) are exactly the two that
reach out. Both pass, so CI is green and the class of harm is unbounded.

## Next step (not done here — measurement only, 0 production lines)

```
rewrite test_reap_chain_without_wait_secs  -> fake the pid/kill/ps seams;
                                              no fork, no /proc, no ps
move the live-config assertion out of this file (config-cell test lives
                                              where the cell is owned)
add an autouse conftest guard: fail on subprocess.Popen/os.fork, on any
                              /proc read, on os.kill of a non-fixture pid
```
That is engine work on `extensions/agi/tests/conftest.py` + the test file —
a build under a new hypothesis, not a patch under this one.

## Evidence

- probe plugin + raw hit log: `.agi/sessions/iter-DH.381/a00-7447fd2b/probe_plugin.py`, `hits.txt`
- `hits.txt` summary: `529 read:/proc · 3 spawn:Popen · 2 spawn:run · 3 os.kill · 1 read:live-config`
- `pytest … -q` → `11 passed in 0.99s`
- `git diff --numstat -- extensions/` → empty (this round changed no production bytes)

## Agent Notes
runtime probe plugin: 529 /proc reads, os.kill TERM+KILL on a live pid, a forked sleeper + ps/git spawns, and the live .agi/config.json read all occur in a green (11 passed) run; no conftest guard covers spawn//proc/kill/live-config

PARENT REVIEW (a00-b0a277d8, DH.381) -- ACCEPTED, verdict disproved stands.

Deliverables vs diff: `git status --porcelain` and `git diff --numstat` are EMPTY in my worktree, which matches the node's own claim ("this round changed no production bytes"). The named artifacts (sessions/iter-DH.381/a00-7447fd2b/{probe_plugin.py,hits.txt}) exist; the report did not overclaim a file the bytes lack. Title is the kid's own words.

probes (run by the parent, not the kid, one per claim conjunct):

1. wire -- the call site reaches the live seams. /tmp/probe_parent.py patched os.fork, subprocess.Popen, os.kill, builtins.open, os.open and ran the file: `11 passed in 0.99s` AND `subprocess.Popen ['/usr/bin/python3', '.../test_reap_chain_without_wait_s0/launcher.py']` x1, `Popen ['ps','-o','pid=,cmd=','-p','2152545']` x2, `Popen ['git','-C',...,'rev-parse',...]` x4, `os.kill pid=2152545 sig=0` x14, `sig=SIGTERM` x1, `sig=SIGKILL` x2, plus 3 /proc/<pid>/stat reads. The real spawn is not a description of the source; it is a hit in a run.

2. wire (pathlib half) -- /tmp/probe_parent2.py wrapped pathlib.Path.read_bytes/read_text: `499 hits`, first of them `/proc/1/cmdline`. NEAR MISS worth keeping: probe 1 counted only 3 /proc reads because Path.read_bytes reaches C-level io.open and never touches builtins.open. A probe that patches only builtins.open UNDERCOUNTS a pathlib read by ~170x and would have read as "the /proc scan is minor". This is the one place the kid's 529 and my 499 differ -- same class, both far above any threshold.

3. gate -- conjunct "a guard fails the file if any test spawns a process, reads /proc, signals a real pid or reads the live config". I dropped extensions/agi/tests/test_zzz_parent_guard_probe_tmp.py (tmp_path, no repo write kept: file removed after the run) that forks a real detached process, read_bytes every /proc/<pid>/cmdline and os.kill(pid, 0) -- every forbidden act in the claim's own list. Result: `1 passed in 0.12s`, PYTEST_EXIT=0. The gate does not exist. conftest.py's autouse fixtures (:326 _no_real_tmux, :369 _no_real_provisioning_call, :565 _no_openrouter) cover tmux, provisioning and the API key; none of them names spawn, /proc, os.kill or the live config, and _no_real_tmux is documented as selective (it passes non-tmux calls through), which is exactly how `ps` and `git` escaped.

Standing-rule deviation: none. I ran read-only git (status/diff) because the review section of the brief requires reading the kid diff; the no-git rule governs commits.

Residue carried forward, not ridden: the fix (fake the pid/kill/ps seams, move the live-config assertion to the cell's owning test, add the autouse guard) is NOT done. It is engine work under its own build; this round is measurement only.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT RE-VERSION of a00-7447fd2b's experiment node: accepted unchanged in verdict, hardened in provenance.

(1) WHAT THE BRIEF SAID: "A kid's tests are its CLAIM, not your evidence... run one negative probe per claim conjunct yourself and record them as probes:". (2) WHAT THE MACHINE DOES: the node as filed carried no `probes:` field and no parent-run evidence -- its only backing was the kid's own plugin at sessions/iter-DH.381/a00-7447fd2b/probe_plugin.py. My three probes are independent artifacts (/tmp/probe_parent.py, /tmp/probe_parent2.py, and a temporary test file under extensions/agi/tests/ that I deleted in the same command), and they hit the same seams from a different instrument: 499 /proc cmdline reads, one real Popen of a fork+setsid launcher, 2 `ps` + 4 `git` spawns from rotate._reap_chain itself, 17 os.kill calls (14 probes + TERM + 2 KILL) against pid 2152545, and a green 1-passed run for a test that did every forbidden act. (3) NEAR MISS: a parent that reads the kid's hits.txt, sees "529 /proc reads, all four falsifiers fire", and records the node as proved-by-the-kid -- the number is right and the evidence is still the kid's, which is precisely the failure mode the parent-task node names. The number is only evidence when a second instrument reproduces it. (4) DEVIATION: none; the standing no-git rule is about commits and the review section mandates reading the diff.

The claim survives both of its conjuncts' falsification, so `disproved` stands at confidence 0.95. What does NOT stand is any implication that the round closed something: the defect is measured, unfixed, and the guard the claim names does not exist to stop the next one.
<!-- THOUGHT:END -->
