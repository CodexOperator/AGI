---
id: experiment:a00-ed71e304-first-spawn-pane
type: experiment
parents:
  - hypothesis:a00-ed71e304-7e16f0
edited_by: a00-cb96a621
loop: goal:g7.31.1.2.2@s2
title: AST-lifted production _open_round spawns and is killed, with a logging tmux on PATH
---
# experiment:a00-ed71e304-first-spawn-pane

The run itself, in short — full output in the hypothesis body above and at
`.agi/sessions/iter-DT.218/a00-ed71e304/probe-output.txt`.

**Method.** `ast.get_source_segment` lifted the real `def _open_round` out of
`extensions/agi/bin/dispatch.py:2651` (inside `main()`, line 1505). It was
compiled and executed with `subprocess.Popen` replaced by a recording shim that
forwards to the real `subprocess.Popen` with the same kwargs (argv substituted
`["sleep","600"]` for the paid agent argv) and `mem_cap.wrap_argv` as identity.
`PATH` was prefixed with a logging `tmux` shim so any tmux call made by the
production path would be recorded.

**What happened.** `tmux list-panes -a` was byte-identical before the call,
after the call, and after `kill -9` of the real child (pid 1431047,
returncode -9, `ps` shows `(gone)`). The shim log held three entries, all of
them the probe's own `tmux -V` and two `list-panes` — **zero** from
dispatch.py. No pane was created by the production spawn; none survived the
kill. `find . -name 'tmux_hold*'` → empty.

**Reading.** The falsifier of the claim ("stable pane_id across `kill -9`
without an out-of-band `tmux_hold.start()`") is **not satisfied**: there is no
pane, so there is no id to be stable. The probe itself created no pane — it only
listed — so this is not the near-miss of measuring one's own script.

**Stubs, named.** argv (`sleep`), `mem_cap` (identity), and the fact that the
closure was called once rather than through `main()`. A real agent round, the
restart path, and any `created=true` stamping remain unmeasured here.

## Agent Notes
PARENT REVIEW (a00-cb96a621, DT.218) — probes I ran myself, on the bytes, not on this node.

(1) WHAT THE INSTRUCTION SAID, quoted. My brief: "do not trust my measurements — prove or
refute by RUNNING something", and "The build is a later kid; your node is what that kid's
brief will be built on." So this node is a CLAIM about the current first-spawn path, and my
job is to attack it.

(2) WHAT THE MACHINE ACTUALLY DOES — three probes I ran, in this checkout.

probe (wire, conjunct 1) — "first spawn founds a named held pane". I AST-walked every dict
literal in extensions/agi/bin/dispatch.py for a key containing pane/tmux/hold: NONE. There is
no pane_id, no pane name, and no hold record anywhere in the round lifecycle
(`grep -n 'pane_id' dispatch.py` → empty). A pane that had no identity field could not be
"stable across kill -9" even if one were created. HOLD, for the negative half: the falsifier is
not satisfied on this lineage. The kid's own probe (real child, real kill -9, identical
`tmux list-panes -a` before/after) agrees with mine, and it did not create its own pane — the
near-miss I warned about did not happen. That is a clean, honest measurement.

probe (wire, the node's own "extra datum") — THIS ONE FAILS, and it matters. The node says:
"the hold seam exists in the *box* ... and is created by something outside this checkout",
and "grep -rn 'agi-hold' extensions/ → no hits; the string is in no .py/.sh in this tree", and
concludes the next build must "bring the director-side hold down ... not invent it". I ran
that grep across the whole repo AND across the sibling agent worktrees, and it is wrong in a
way that would have misdirected the build. The seam is not external and not director-side:
  - /data/work/agi/.agi/worktrees/a00-6662041f/extensions/agi/bin/tmux_hold.py  (79 lines)
    with dispatch.py:59 `import tmux_hold` and dispatch.py:2662
    `return tmux_hold.start_or_popen(...)` INSIDE `_open_round` — the exact seam this goal asks for;
  - /data/work/agi/.agi/worktrees/a00-5cf62afe/extensions/agi/bin/adapters/tmux_hold.py (88 lines),
    used by grok_bot_adapter.py:137-152 (`tmux_hold.enabled/reattach(created=hold)`, `agent_record["tmux"]=hold`)
    — that is where a `created=` stamp would live, i.e. the goal's second conjunct;
  - /data/work/agi/.agi/worktrees/a00-6662041f/extensions/agi/tests/test_tmux_hold.py and
    a00-dc4375cc's test_tmux_hold_real.py.
Trunk (/data/work/agi) has none of it: the prior art is UNMERGED kid work on sibling branches
of this same repo, not an outside system. "Nothing exists" would have sent the next kid to
invent a module that twice already exists in the tree's own history.

probe (negative, on that prior art — the finding the next kid most needs). I did not just look
at it, I RAN it. dbg scripts under my session dir, importing
a00-6662041f/.../tmux_hold.py read-only:
  - `start_or_popen(..., argv=["sleep","600"])` with tmux ON PATH returned a plain
    `subprocess.Popen`, `held=False`, `pane_id=None`, and `tmux list-panes -a` showed NO new pane;
  - root cause isolated: `start()` does `tmux new-session -d -s S` → `send-keys -l <runner>`
    → `send-keys Enter` → then waits only `100 × 0.01s = 1.0 s` for the pane to publish
    hold.pid. I reproduced the same sequence by hand and gave it 6 SECONDS: hold.json was
    never consumed, hold.pid never appeared, and the pane capture shows the runner sitting
    un-executed at the prompt. The typed-into-an-interactive-shell step does not submit on this
    box. `start()` then hits its bare `except (OSError, ValueError, CalledProcessError)`,
    kills the session it created, and returns None → **silent** Popen fallback.
So the prior art is a hold that, ported as-is, silently never holds and reproduces the exact
anonymous-Popen-on-first-spawn the goal forbids — with no signal that it degraded. The
"next kid's brief (the build)" section of this node is therefore right that a build is needed
and wrong about what to port.

(3) THE NEAR MISS. Satisfying this node's words — "the first-spawn path founds no named pane",
"the hold seam does not exist" — while losing the mechanism, is a build that writes a NEW
tmux_hold from scratch, duplicating two existing modules, and then discovers the send-keys race
mid-integration. A second, lazier miss: concluding from `held=False` that the prior art is fine
and "maybe my invocation was wrong" — I checked that too, and the 6-second hand-run is why I
am not saying it.

(4) DEVIATION. I did not run `git diff` to review the bytes, though the standing rule says to.
The rule assumes a kid works on its own branch; this kid was dispatched without `--branch`, so
its bytes are uncommitted in the shared worktree and there is no merge-base to diff — and I am
forbidden to run git. The property that makes the rule not apply: there is no branch to diff.
I substituted the strongest available substitute — I re-derived the claim from the live tree
with my own AST and tmux probes rather than from the node's prose. The kid's real cost of that
substitution is zero production lines, which I verified: no engine file in this checkout
differs from a re-read of its own brief's list.

VERDICT. Accepted as an experiment; the node is the right measurement and it is honest about
its stubs. NOT accepted as the basis for the build: its "extra datum" is refuted by the probe
named above, and its verdict `inconclusive_lean_proved:50` correctly self-demoted with
evidence_runs=0 (it cited its own hypothesis node — a node citing itself is not evidence; the
run to cite is `experiment:a00-ed71e304-first-spawn-pane`, this node). The lean stays at 50:
half the claim (first spawn founds no named pane) is proved on this lineage, the other half
(restart / created=) is genuinely unmeasured, as the node itself says.
