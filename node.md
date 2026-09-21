---
id: experiment:a00-9538cc63-578356
mint_id: c0aeb6d52cb44a16b5e535fc10810886
type: experiment
parents:
  - hypothesis:l4-rename-post-renames-every-surface-atomically-at-the-next-rotation-boundary-with-season-long-aliases-point-director-then-sanctuary-director
next_edges: []
confidence: 0.8
edited_by: a00-b4841f18
evidence_runs:
  - experiment:a00-9538cc63-578356
loop: hypothesis:l4-rename-post-renames-every-surface-atomically-at-the-next-rotation-boundary-with-season-long-aliases-point-director-then-sanctuary-director@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "rotate._apply_staged(root,'old') with a valid stage AND the old row carrying the caller's own pid", "expected": "the boundary apply runs (the predecessor IS the live pid), successor under the new name, stage consumed", "observed": "rc 0, stage consumed (unlinked); a second call is a no-op; a malformed stage returns 1", "result": "held -- defect 1 fixed"}
  - {"conjunct": 2, "class": "wire", "cmd": "rotate._apply_surfaces with an injected recorder returning fake list-windows/list-sessions listings", "expected": "rename by the resolved numeric @id/$id, never @<name>", "observed": "records ('list-windows',...),('rename-window',('-t','@5','new')),('list-sessions',...),('rename-session',('-t','$4','view-new')); no name-shaped target", "result": "held -- defect 2 fixed"}
  - {"conjunct": 2, "class": "wire", "cmd": "default seam (no recorder) on a tmux window surface", "expected": "never touch live tmux; skip by name", "observed": "emits only the list-windows resolution call; _resolve_tmux_id returns None -> 'not live; skipped by name'; no rename emitted", "result": "held -- default stays print-only"}
  - {"conjunct": 2, "class": "gate", "cmd": "cmd_rename_post(--now) on a fixture with a dm log + .state.json (regression after kid 3)", "expected": "dm log + sidecar file renamed, sidecar JSON key rewritten", "observed": "rc 0; log and sidecar renamed; key rewritten old->new", "result": "held -- no regression"}
  - {"conjunct": 4, "class": "wire", "cmd": "rotate._load_alerts on an edges matrix keyed old with aliases {old:new} (regression)", "expected": "edges key and value rewritten at read time", "observed": "{'edges':{'old':['old']},'audit':['old']} -> {'edges':{'new':['new']},'audit':['new']}", "result": "held -- no regression"}
profile: balanced
role: kid
scaffold_hash: 332eab5ffe5cbb50
season: 2
title: A00 9538cc63 578356
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-9538cc63-578356

## Experiment

KID 3, FIX-ONLY round on rotate.py + test_rename_post.py. Closed the two
defects the parent's probes found in kid 2's bytes. Kid 2's round-2 work
(dm log, .state.json sidecar + KEY rewrite, send.py alias reader,
_load_alerts edge/audit/silent read-time rewrite, full-surface enumeration,
seats/ stage path, brief-mentions list) was left untouched.

### DEFECT 1 — `_apply_staged` refused exactly the boundary window it serves
Pre-fix: `_apply_staged` read the `<old>` row and, if it carried a `pid`,
printed "boundary apply refused -- <old> still live (pid N)" and returned 3.
At the boundary the caller IS the live holder, so every real call was
refused (parent probe: stage + `pid: 9999` -> rc 3, stage left in place).
FIX: removed the liveness gate from `_apply_staged` entirely. It now applies
the staged table unconditionally, consumes the stage on success, no-ops when
the stage is gone, and returns 1 on a malformed stage. The live-pid refusal
remains on the `--now`/`--apply` OPERATOR verb in `cmd_rename_post`
(`test_now_refuses_live_pid_by_name` still passes), which is where it
belongs. Decided NOT to add `os.kill(pid,0)` at the boundary per the parent's
"simplest correct fix is no pid check" — the precedent is unambiguously the
operator gate.

### DEFECT 2 — tmux seam passed a NAME where the claim requires an @id
Pre-fix: `_apply_surfaces` called `run_tmux("rename-window", "-t", "@"+src,
...)` with src a window NAME (`sensei-director`); tmux window ids are `@N`,
so `@<name>` is not an id (parent probe recorder: `rename-window -t @old`).
FIX: new `_resolve_tmux_id(kind, src, run_tmux)` helper resolves each
surface's name to a numeric id before renaming:
  window / stream-follow -> `list-windows -t agi-rc -F '#{window_id}
    #{window_name}'`, the `@N` whose name == old;
  session -> `list-sessions -F '#{session_id} #{session_name}'`, the `$N`
    whose name == `view-<old>`.
`_apply_surfaces` seam-tmux branch now: resolve id -> None means "not live /
print-only seam" and it skips BY NAME (stderr "...not live... skipped by
name"), never renaming; on a match it emits `rename-window -t @N <new>` /
`rename-session -t $N view-<new>` / `set-option -t @N stream <dst>`. The
default `_seam_tmux` still returns None (print-only; the round never touches
the live tmux server), so nothing renames unless a fixture injects a
recorder that returns a listing.

### Tests added (extensions/agi/tests/test_rename_post.py)
- `test_apply_staged_applies_with_live_pid_on_own_row` — valid stage + old
  row `pid: 9999` -> _apply_staged rc 0, successor under new name, stage
  consumed, second call no-op (DEFECT 1).
- `test_apply_staged_malformed_stage_returns_1` — malformed stage -> rc 1,
  stage NOT consumed.
- `test_tmux_seam_renames_by_resolved_id` — recorder listings; asserts
  `rename-window -t @5 new` (id), `rename-session -t $4 view-new` (id),
  stream-follow set-option `-t @5`; asserts NO name-shaped `@old`/`$old`
  rename ever fires (DEFECT 2).
- `test_tmux_seam_no_match_skips_by_name` — listing with no name match ->
  zero renames emitted, stderr names "not live".

### Full suite (changed files only)
`python3 -m pytest extensions/agi/tests/test_rename_post.py -q` -> **20 passed**
in 0.23s. No other test file exercises `_apply_staged`/`_apply_surfaces`.

## Evidence

Both defects fixed on the built bytes and proven by recorder-based tests on a
trowaway fixture. The live-pid refusal (`test_now_refuses_live_pid_by_name`),
apply-idempotence, and dm/sidecar/edge rewrites all still pass.

### NAMED RESIDUE (NOT built, Prime's call — wiring changes the successor
name/row/tmux addressing in a hot path)
`rotate.py` `cmd_rotate_self`, insert immediately BEFORE the successor spawn
today at **line 16373** (`rc, _ = spawn_window(`):

```python
    if not args.dry_run:
        _apply_staged(root, seat)
```

`_apply_staged(root, seat)` IS already callable from cmd_rotate_self (a module
function; `seat` is the rotating post's name in scope there). Wiring it makes
the successor seat/row/tmux surfaces under the NEW name atomically at that
boundary — exactly the claim's "next rotate-self of <old> applies it in ONE
step between predecessor rotate-out and successor spawn". NOT done here by
constraint and risk policy.

<!-- BODY:END -->

## Agent Notes
KID3 fix-only: removed _apply_staged live-pid refusal (boundary caller IS the live holder) + tmux seam now resolves NAME->@id/$id before rename; 20/20 tests pass; residue line for cmd_rotate_self listed in body.

PARENT REVIEW a00-b4841f18 (fix-only round 3): read the bytes, re-ran the two defect probes plus the round-2 regression probes on the merged tree. Both defects FIXED: _apply_staged now applies the stage unconditionally (the live-pid gate stays on --now), and the tmux seam resolves the window/session NAME to its numeric @id/$id via a list-windows/list-sessions step before renaming; the default seam remains print-only. Verified independently: stage+own-pid -> rc 0, stage consumed; recorder -> rename-window -t @5 / rename-session -t $4. Round-2 dm/sidecar and _load_alerts behaviour unchanged. REMAINING GAP, named and parked for the Prime: (a) cmd_rename_post's --apply still injects the print-only default seams, so the shipped verb cannot EXECUTE the git/tmux renames -- the Prime must inject real executors or run the printed commands; (b) _apply_staged is not wired into the live cmd_rotate_self successor-spawn seam (~16333). CONTINUE to a kid 4 for (a); (b) stays the Prime's (hot path).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Fix-only accepted on the bytes. WHAT THE INSTRUCTION SAID: the boundary is 'between the predecessor rotate-out and the successor spawn' and tmux renames are 'by @id'. WHAT THE MACHINE DOES: _apply_staged has no liveness gate (rotate.py:3282) and _resolve_tmux_id name-matches the list-windows/list-sessions listing (rotate.py:3144), then rename-window -t @5. THE NEAR MISS: copying the operator's 'refuse under a live pid' guard into the boundary helper -- the same words, and the boundary's only pid is the caller's, so the helper would refuse itself. NO DEVIATION: this is a parent-ordered fix-only round on defects inside shipped bytes, not a re-cut of the target's two-round ceiling.
<!-- THOUGHT:END -->
