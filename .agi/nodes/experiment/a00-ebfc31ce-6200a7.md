---
id: experiment:a00-ebfc31ce-6200a7
mint_id: 4240a4d228cb4e17892e11c6b37742e6
type: experiment
parents:
  - hypothesis:l4-sb-status-reads-the-configured-stub
next_edges: []
confidence: 0.95
edited_by: a00-cdbed097
evidence_runs:
  - experiment:a00-ebfc31ce-6200a7
loop: hypothesis:l4-sb-status-reads-the-configured-stub@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ad85ce610bc5a6db
season: 2
title: A00 ebfc31ce 6200a7
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-ebfc31ce-6200a7

## Experiment

Deployment half of the g15 build order (the previous kid, a00-c6a65634, had
rewritten the wrapper TEMPLATE in `streamer-stub/bin/install-cli.sh` so the
generated wrapper resolves the stub at RUN time, but had NOT applied it to the
box -- the real `~/bin/sb-status` still hardcoded the install-time stub, leaving
two repo tests RED).

1. Confirmed the installer template was the fixed run-time-resolving one (the
   wrapper-no-absolute-path + `locations.streamer_stub` walk-up logic, with the
   install-time fallback spelled $HOME-relative). `streamer-stub` had no
   uncommitted changes, so the template edit had already landed via automation.
2. Re-ran the installer ONCE on the box:
   `bash /home/ubuntu/work/streamer-stub/bin/install-cli.sh` -- safe/idempotent;
   it rewrote `~/bin/sb-status` and re-pointed the brb/back/retract/panic/live
   symlinks at the same stub. The stream was never executed, only files in
   `~/bin` written.
3. Confirmed the new `~/bin/sb-status` body carries NO absolute stub path: the
   install-time fallback is now `_fb='work/streamer-stub'` (HOME-relative), and
   the run-time walk-up reads `locations.streamer_stub` from the nearest
   enclosing `.agi/config.json`.
4. Ran the repo test file:
   `python3 -m pytest extensions/agi/tests/test_commands.py -q`
   → `35 passed` in 1.93s. Both previously-red tests
   (`test_stream_fragment_argv_resolves_to_executable_files` and
   `test_real_fragment_sb_status_resolves_from_home_not_stub_depth`) are now
   GREEN.

No git was run by this kid (standing rule: the loop owns every commit; the
streamer-stub template change was already committed by automation, and the live
`~/bin/sb-status` rewrite is outside any repo).

## Evidence

Before: `~/bin/sb-status` body hardcoded the install-time path twice:
```
"/home/ubuntu/work/streamer-stub/bin/hold.sh" --status
"/home/ubuntu/work/streamer-stub/bin/panic.sh" --status
```

After installer re-run, the deployed wrapper body (HEAD) has no absolute path:
```
_fb='work/streamer-stub'
... walk up for .agi/config.json, read locations.streamer_stub ...
case "$_fb" in
  "~/"*) _fb="$HOME/${_fb#\~/}" ;;
esac
case "$_fb" in
  /*) stub="$_fb" ;;
  *)  stub="$HOME/$_fb" ;;
esac
"$stub/bin/hold.sh" --status
"$stub/bin/panic.sh" --status
```

Test run (real box, real wrapper):
```
$ python3 -m pytest extensions/agi/tests/test_commands.py -q
...................................                                      [100%]
35 passed in 1.93s
```
This is the exact falsifier flipped: the deployed wrapper no longer carries a
hardcoded stub path, and the two tests that read the REAL `~/bin/sb-status` are
green on the built bytes.

## Agent Notes
Deployed the fixed sb-status wrapper to the box: re-ran install-cli.sh once, new ~/bin/sb-status carries no absolute stub path (fallback HOME-relative work/streamer-stub, run-time walk-up for locations.streamer_stub), test_commands.py 35 passed on the real wrapper.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review a00-cdbed097 L4.197. Deployment half. Machine check: /home/ubuntu/bin/sb-status rewritten at 08:31:39, body names no absolute stub path and falls back to HOME-relative work/streamer-stub; I ran pytest extensions/agi/tests/test_commands.py -q on the real box -> 35 passed, so the two real-wrapper tests that were red on the previous node are green here. Near miss: reporting green from a fixture while the deployed wrapper stayed stale; here the deployed bytes are the fixed template and the real-wrapper tests are the ones that flipped. No deviation. Confidence 0.95.
<!-- THOUGHT:END -->

Parent review (a00-cdbed097): kept proved at 0.95. The deployed wrapper flips the stated falsifier (no hardcoded stub path) and the full test file is green on real bytes; the deployment step the previous node left open is closed.
