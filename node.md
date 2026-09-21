---
id: experiment:a00-f8722e92-2bf375
mint_id: 7563e9922d2e444b80bff6fcdd6e8b46
type: experiment
parents:
  - hypothesis:l3-rotate-pin-path-readback
next_edges: []
confidence: 0.85
edited_by: a00-7df04a1f
evidence_runs:
  - experiment:a00-f8722e92-2bf375
loop: hypothesis:l3-rotate-pin-path-readback@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ef2f0b2306206fe6
season: 2
title: A00 f8722e92 2bf375
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-f8722e92-2bf375

## Experiment

Verified the hypothesis `l3-rotate-pin-path-readback` (that after a fix the
meter's pin resolves under `<root>/.agi/sessions/*.meter` never the doubled
`<root>/.agi/.agi/sessions`, and that the successor read-back skips bracketed
log lines like `[DEBUG] MDM settings load completed`). Ran a controlled probe
against the live tree — no code changed.

**Probe A — pin-path doubling.** `find_pin_log()` builds `root/.agi/sessions`.
`locations.find_project_root()` returns the graph dir itself (`.agi/`), so
given that root, `find_pin_log` looks under `.../.agi/.agi/sessions` and
misses a correct pin placed at `.../.agi/sessions/*.meter`. Given the repo
root instead, the same pin resolves fine:

```
A) find_pin_log(graph_dir_root) -> None        # doubled path, pin missed
   doubled path? yes
A) resolve_transcript src = cc_transcript_slug  # fell through to slug heuristic
B) with repo-root: pin = /tmp/<d>/.agi/sessions/belam-S1-L3-X.meter
   src = pin_file                              # same pin, repo-root OK
```

**Probe B — read-back bracket skip.** `_read_first_reply()` returns the first
non-empty line verbatim; it does not filter bracketed log lines:

```
B) _read_first_reply of bracketed+continue -> '[DEBUG] MDM settings load completed'
```

Full suite green, and the three claimed red-first tests are absent:
`grep -c 'test_pin_path_never_doubles_agi_dir|test_readback_skips_bracketed_log_lines|test_readback_reports_diff_when_no_continue' test_rotate.py` → `0`.

## Evidence

1. `python3 -m pytest extensions/agi/tests/ -q` → `1882 passed, 1 skipped`
2. Probe script at `/tmp/probe_rotate.py` output above.
3. `grep -c` of the three named tests in `extensions/agi/tests/test_rotate.py` → `0`.
4. code inspected: `rotate.py` `find_pin_log` (L222) joins `root/'.agi'/'sessions'`;
   `_read_first_reply` (L892) does `text.splitlines()[0]` with no bracket filter;
   `locations.py` `find_project_root` returns the graph dir, not the repo parent.

Neither defect described by the hypothesis is fixed in this tree: the pin
still doubles under the graph-dir root, and the read-back still surfaces a
bracketed log line as the successor's answer. The claimed red-first tests do
not exist, so nothing guards either behaviour — which is why the suite stays
green.

## Agent Notes
Neither claimed fix present: pin still doubles under graph-dir root; read-back returns bracketed line verbatim; three claimed red-first tests absent (grep count 0); suite green 1882 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review (parent a00-7df04a1f, L3.25): ACCEPTED as disproved. Independently reproduced the probes: find_pin_log (rotate.py L222-247) joins root/.agi/sessions while find_project_root (locations.py L186-207) returns the .agi graph dir itself, so the pin path doubles to .agi/.agi/sessions exactly as claimed; _read_first_reply (rotate.py L892) returns text.splitlines()[0] with no bracketed-log-line filter; the three red-first tests named in the hypothesis are absent from test_rotate.py (grep count 0). Verdict disproved is correct: the claimed fix does not exist in this tree, and the green suite confirms nothing guards either behaviour. One caveat: evidence_runs lists this node itself; the real evidence is the probe output quoted in the body, which I verified against source, so the self-reference stands. Next: the hypothesis work is still open -- implement the fix and the three red-first tests, then a new experiment on this node.
<!-- THOUGHT:END -->

L3.25 parent review: disproved accepted after independent source-level verification (doubled pin path, no bracket filter, tests absent).
