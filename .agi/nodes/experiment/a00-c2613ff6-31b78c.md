---
id: experiment:a00-c2613ff6-31b78c
mint_id: 7a7ecebee5d1476486460e00c33f65bf
type: experiment
parents:
  - hypothesis:l4-workflow-residue-sub-floor-marker-dead-code-and-truncation
next_edges: []
confidence: 0.85
edited_by: a00-93b7761e
evidence_runs:
  - experiment:a00-c2613ff6-31b78c
loop: hypothesis:l4-workflow-residue-sub-floor-marker-dead-code-and-truncation@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "PARENT probe, in-process: provisioning.check_key_floor with (A) one sub-floor cap; (B) TWO sub-floor caps; (C) a sub-floor cap followed by a cap-above-floor whose remaining is below it; (D) empty listing; (E) available()=False", "expected": "A (True, <marker>) with marker byte-identical to the one stderr line; B (True, <marker>), TWO stderr lines, marker = the FIRST; C still (False, <refusal>) and no 'sub-floor' in it; D and E still (True, None) -- a silent path must stay silent", "observed": "A True + stderr_matches=True + 1 line; B True + 'agi-a' in marker + 2 stderr lines; C False + 'agi-b' in msg + no 'sub-floor'; D True/None; E True/None", "result": "pass"}
  - {"conjunct": 1, "class": "wire", "cmd": "PARENT probe: drove dispatch.main() in-process with provisioning.check_key_floor -> (True, 'MARKER-SUB-FLOOR-PROBE') and check_account_floor -> (False, 'ACCOUNT-PROBE-REFUSES'), so main returns BEFORE any spawn/mint/scaffold", "expected": "the marker reaches stderr as a notice on the LIVE dispatch path, before the account-floor refusal", "observed": "stderr carried 'notice: MARKER-SUB-FLOOR-PROBE' then 'ERR: ACCOUNT-PROBE-REFUSES', RC 1, zero spawns", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "PARENT probe: grep -rn _parse_last_json extensions/ skills/ src/; then import workflow/dispatch/provisioning/cli/send in a fresh interpreter and test hasattr", "expected": "no production caller and no dangling import after removal", "observed": "2 hits, both the deletion comment in workflow.py:1323/1328; hasattr(workflow,'_parse_last_json') False; all five modules import clean", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "PARENT probe: _preview_detail at exactly the budget, at budget+1, and on a 7989-char multi-line blob; then a real RunView('k',[{'label':'only'}])._set('only','unstructured',blob) with the tree captured from its io buffer", "expected": "exactly-at-budget is whole; budget+1 elides by exactly 1 with the exact marker; the blob renders ONE line shorter than the blob with no embedded newline; state['detail'] keeps the WHOLE text", "observed": "budget 200: 200 chars whole; 201 -> 'x'*200 + '… (+1 chars)'; blob 7989 -> tree_line_len 229, no newline, state_len 7989 (whole)", "result": "pass"}
  - {"conjunct": 5, "class": "gate", "cmd": "PARENT probe: _resolve_stage_timeout matrix -- stage 3/no manifest; no stage/absent; no stage/manifest 42; stage 3/manifest 600; stage None/manifest 42; and the case the kid never tried: stage 3 with manifest timeout_s=0; then the refusals: manifest 0, stage 0 vs manifest 600, -1, '600', True", "expected": "resolve by PRESENCE: a stage value wins over the manifest, an absent value falls to 600; and a manifest-level 0 must NOT poison a stage that declares its own positive budget", "observed": "3; 600; 42; 3; 42; stage 3 + manifest 0 -> 3 (allowed). Refusals raise ValueError naming timeout_s for: manifest 0, stage 0, -1, '600', True", "result": "pass"}
  - {"conjunct": 5, "class": "wire", "cmd": "PARENT probe: a TWO-stage manifest (the kid's own fixtures were single-stage, where 'before any stage' cannot be told from 'at the only stage'): stage 'first' with no timeout_s, stage 'second' with timeout_s=0, driven through the real run_workflow with subprocess.run captured; control: first 600 / second 4", "expected": "the refusal fires BEFORE the first stage is dispatched (seen == [], no stage marked running or run in the tree), and a positive budget still reaches subprocess.run(timeout=...)", "observed": "rc != 0, seen == [], stderr names 'second' and timeout_s, no [~] or [✓] in the tree; control rc 0 with seen == [600, 4]", "result": "pass"}
  - {"conjunct": 4, "class": "gate", "cmd": "PARENT probe: parse the edited node's frontmatter probes list and list (conjunct, class); then re-ran the hermeticity claim INDEPENDENTLY -- env -u OPENROUTER_API_KEY -u ANTHROPIC_API_KEY pytest test_workflow.py -q -p <my own guard patching socket.socket.connect/connect_ex/create_connection> -k 'pi or lenient or unstructured or revoke or timeout'", "expected": "numbering aligned to the parent hypothesis's conjunct list with hermeticity at 3 and a probe of its own; and the pi-return tests pass with no credentials and every outbound connect refused", "observed": "conjuncts [0,1,1,2,3,4,5,6] -- 0 is the re-cut, 1 revoke x2, 2 schema, 3 hermeticity (NEW, executed), 4 sub-floor, 5 timeout, 6 tree/tracking; my own guard run: 26 passed, 45 deselected", "result": "pass"}
profile: balanced
role: kid
scaffold_hash: 3a7fb4927149c126
season: 2
title: A00 c2613ff6 31b78c
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c2613ff6-31b78c

## Experiment

BUILD ORDER on `hypothesis:l4-workflow-residue-sub-floor-marker-dead-code-and-truncation`. Five conjuncts, each re-measured on this worktree's bytes before editing (the brief's line numbers had drifted, as it warned). All five were IMPLEMENTED, not merely measured. Every claim below cites a `file:line` on the current bytes or a command I ran with its real output.

Files touched (named in prose — no git command was run):

- `extensions/agi/bin/provisioning.py` — conjunct 2
- `extensions/agi/bin/dispatch.py` — conjunct 2 (the notice surface)
- `extensions/agi/bin/workflow.py` — conjuncts 3, 4, 6
- `extensions/agi/tests/test_provisioning.py` — conjunct 2 tests
- `extensions/agi/tests/test_workflow.py` — conjuncts 3, 4, 6 tests
- `.agi/nodes/experiment/a00-e9f2167d-babbe4.md` — conjunct 5 (via `write.py` only)

No file outside that scope was touched. No unexpected files were seen in the tree.

### Conjunct 2 — the sub-floor skip is visible in the RETURN VALUE

Pre-fix (`provisioning.py:400-408`): the sub-floor branch printed one stderr line and `continue`d; the only exits were `(True, None)` and `(False, <message>)`.

Fix: the sentence is built ONCE into `marker`, printed to stderr, remembered in `skipped`, and returned — `return True, skipped` at `provisioning.py:422`. `(True, None)` is now reserved for the genuinely silent paths. Scanning still continues past a skip, so a later key whose remaining is below the floor still refuses; when several caps are skipped the first marker is returned (stderr names every one). Docstring updated at `provisioning.py:355-367`.

The one live caller (`grep -rn "check_key_floor" extensions/ --include=*.py` → `dispatch.py:2072`, plus the definition and prose mentions; every other hit is a test):

```python
        _hkey_ok, _hkey_msg = provisioning.check_key_floor(cfg, root)
        if not _hkey_ok:
            print(f"ERR: {_hkey_msg}", file=sys.stderr)
            return 1
        # conjunct (2) ... ok=True still means dispatch proceeds, but a
        # (True, <marker>) return NAMES a skipped sub-floor minted key. A
        # marker returned to a caller that ignores it is the falsifier, so it
        # reaches a surface here as a NOTICE, before the account-floor block.
        if _hkey_ok and _hkey_msg:
            print(f"notice: {_hkey_msg}", file=sys.stderr)
```

(`dispatch.py:2072-2081`.) `ok=True` still means dispatch proceeds — unchanged.

### Conjunct 3 — `_parse_last_json` removed

Pre-removal grep, the exact output:

```
extensions/agi/tests/test_workflow.py:169:    render_stage_prompt, _parse_last_json, _effort_to_thinking,
extensions/agi/tests/test_workflow.py:215:def test_parse_last_json_tolerates_preamble_and_trailing_glue():
extensions/agi/tests/test_workflow.py:216:    assert _parse_last_json("ok here\n{\"slug\": \"x\", \"v\": 1}\n thanks") == \
extensions/agi/tests/test_workflow.py:219:        _parse_last_json("no braces here")
extensions/agi/bin/workflow.py:1291:def _parse_last_json(text: str):
```

Definition plus one unit test of it, and no production caller. Removed the function (replaced by a comment at `workflow.py:1323-1330` explaining that `_balanced_brace_spans` / `_resolve_lenient_return` supersede it), removed it from the test import list, deleted the test. Post-removal grep:

```
$ grep -rn "_parse_last_json" extensions/
extensions/agi/bin/workflow.py:1323:# _parse_last_json was DELETED here (hypothesis:l4-workflow-residue-sub-floor-
extensions/agi/bin/workflow.py:1328:# depth-aware AND string-aware; `_parse_last_json`'s `find("{") /
```

The only remaining hits are the deletion note itself.

### Conjunct 4 — the tree PREVIEWS a multi-KB blob

Fix: `_TREE_DETAIL_PREVIEW_CHARS = 200` (`workflow.py:919`) and `_preview_detail()` (`workflow.py:922-933`), used by `RunView._tree` (`workflow.py:1003`). **Budget justification:** a tree line is read by a human watching a live run and by a parent harvesting it; 200 chars is about one terminal line at 200 columns — enough to identify WHAT a stage returned (its first sentence) and no more. It is an order of magnitude below the >= 4000-char returns the falsifier names, so such a return cannot dominate the tree. `state[lb]["detail"]` is NOT touched — only the render is cut — so the tracking row's `returns` still holds the whole text.

New test `test_tree_previews_a_multi_kb_detail_while_tracking_keeps_it_whole` (numeric on both sides): a 10990-char unstructured return renders exactly one `└─ [?] only` line of length `len("└─ [?] only — ") + 200 + len("… (+10790 chars)")`, shorter than the blob, with no embedded newline; `rows[0]["returns"]["only"]` is the whole 10990 chars.

### Conjunct 6 — `timeout_s = 0` defined and reachable

Fix: `_resolve_stage_timeout(stage, manifest)` (`workflow.py:1536-1571`) resolves by PRESENCE, never truthiness. Definition (a) chosen and documented there: a non-positive or non-numeric budget is INVALID, and `run_workflow` refuses the run by name before anything is dispatched or minted (`workflow.py:1646-1658`, `return 4` with one stderr line naming the key and the stage). Refusing is observable; `subprocess.run(timeout=0)` silently kills every stage, and "wait forever" is indistinguishable from a hung stage. The resolved budgets are hoisted into `stage_timeouts` and the in-loop lookup is `stage_timeouts[st["label"]]` (`workflow.py:1698`). `_DEFAULT_STAGE_TIMEOUT_S = 600` names the historical default in one place.

### Conjunct 5 — experiment `a00-e9f2167d-babbe4` renumbered, hermeticity probed

Edited through `write.py` only, never by hand. Original probes were numbered 1..6 with probe 1 = the re-cut, so revoke (labelled 2, should be 1), schema (labelled 3, should be 2) diverged from the parent hypothesis's conjunct list, and conjunct (3) hermeticity had NO probe. Renumbered to the parent's numbers; the re-cut probe moved to `"conjunct": 0, "class": "wire"`. The new `"conjunct": 3` probe was EXECUTED (see Evidence). `verdict`, `confidence`, `parents`, `evidence_runs` and the body are untouched; `probes` and `thought` only.

## Evidence

### Red first, then green

Conjunct 2, with the source temporarily restored to its pre-fix bytes (same worktree, edit tool only — no git):

```
$ python3 -m pytest extensions/agi/tests/test_provisioning.py -q -k "g_sub_floor"
>       assert ok is True and msg is not None, (
            "a skipped sub-floor cap must be VISIBLE in the return value")
E       AssertionError: a skipped sub-floor cap must be VISIBLE in the return value
E       assert (True is True and None is not None)
extensions/agi/tests/test_provisioning.py:1589: AssertionError
1 failed, 2 passed, 79 deselected in 0.30s
```

After restoring the fix:

```
$ python3 -m pytest extensions/agi/tests/test_provisioning.py -q -k "g_sub_floor or above_floor_cap"
4 passed, 78 deselected in 0.15s
```

Conjuncts 4 and 6, same method (source reverted, tests run, source restored):

```
$ python3 -m pytest extensions/agi/tests/test_workflow.py -q -k "timeout or tree_previews"
FAILED test_manifest_timeout_zero_is_refused_by_name_before_any_stage
FAILED test_stage_timeout_zero_overrides_manifest_600_and_is_refused
FAILED test_negative_stage_timeout_is_refused_not_passed_through
FAILED test_tree_previews_a_multi_kb_detail_while_tracking_keeps_it_whole
E       AssertionError: (11004, 10990)
E       assert 11004 < 10990
4 failed, 3 passed, 64 deselected in 0.53s

$ python3 -m pytest extensions/agi/tests/test_workflow.py -q -k "timeout or tree_previews"
7 passed, 64 deselected in 0.30s
```

### The suite

```
$ python3 -m pytest extensions/agi/tests/test_workflow.py extensions/agi/tests/test_provisioning.py -q
148 passed, 5 skipped in 79.75s (0:01:19)

$ python3 -m pytest extensions/agi/tests/test_workflow.py extensions/agi/tests/test_provisioning.py \
    extensions/agi/tests/test_adapters.py extensions/agi/tests/test_dispatch.py \
    extensions/agi/tests/test_commands.py -q
339 passed, 5 skipped, 2 warnings in 83.21s (0:01:23)
```

(The two warnings are a pre-existing `datetime.utcnow()` DeprecationWarning in `node_writer.py:1244`, unrelated to this round.)

### Conjunct 5 — the hermeticity probe, executed

```
$ grep -n "_mutation_guard" extensions/agi/bin/provisioning.py
639:def _mutation_guard(op: str) -> None:
711:    _mutation_guard("mint")
789:    _mutation_guard("revoke")

$ (test -e .env && echo present || echo absent)
absent

$ env -u OPENROUTER_API_KEY -u ANTHROPIC_API_KEY python3 -m pytest \
    extensions/agi/tests/test_workflow.py -q -k "pi or lenient or unstructured or revoke"
20 passed, 51 deselected in 69.77s (0:01:09)
```

And with a one-off pytest plugin (`-p sockguard`) refusing every outbound connect, so the claim is proved by a guard rather than by the tests' own higher-level stubs (pattern: `conftest.py:526` `_no_pin_socket`):

```
$ PYTHONPATH=/tmp env -u OPENROUTER_API_KEY -u ANTHROPIC_API_KEY \
    python3 -m pytest extensions/agi/tests/test_workflow.py -q -p sockguard \
    -k "pi or lenient or unstructured or revoke"
20 passed, 51 deselected in 74.34s (0:01:14)
```

The plugin patches `socket.socket.connect`, `socket.socket.connect_ex` and `socket.create_connection` (leaving `socket.socket` itself intact, because `ssl` subclasses it at import time — patching the class broke the interpreter with `TypeError: function() argument 'code' must be code, not str`).

### The `write.py` edit of `a00-e9f2167d-babbe4`

Dry-run first (`--dry-run`) — printed the full 8-probe list under `set probes = [...]` plus `RING-GATE PREVIEW: admitted (written_by + ring quorum + freshness satisfied); dry-run writes nothing` — then the same command without `--dry-run` → `updated: experiment:a00-e9f2167d-babbe4`. Read back from the file:

```
entries 8 types {'dict'}
```

with `probes[].conjunct` = `[0, 1, 1, 2, 3, 4, 5, 6]`. `thought` was written with `write.py experiment:a00-e9f2167d-babbe4 "thought $(cat /tmp/thought.txt)"`; the `THOUGHT` block at `a00-e9f2167d-babbe4.md:87` now records what the previous version said and why this one differs.

### One deviation, named

The order for conjunct 5 said only to renumber and add a probe. I also REWROTE the `observed`/`expected` of the conjunct-5 (timeout) and conjunct-6 (tree) probes, because this same round changed that behaviour on purpose: a probe still certifying `declared 0 -> [0]` and `the tree inlines the whole 1120 chars` is false on the built bytes. The rewrite is recorded in the node's `thought`. If the parent prefers the parent-review measurements preserved verbatim, that is the one thing to revert.

## Agent Notes
All five conjuncts BUILT and green: sub-floor skip now returns its stderr sentence as a marker (provisioning.py:422) and dispatch prints it as a notice (dispatch.py:2072-2081); _parse_last_json removed (zero callers proved by grep); RunView._tree previews detail at _TREE_DETAIL_PREVIEW_CHARS=200 with an exact +N elision while tracking keeps the whole text; timeout_s resolved by presence, 0/negative/non-numeric refused by name before any stage or mint (workflow.py:1536-1658); experiment a00-e9f2167d-babbe4 renumbered to the parent conjuncts with a new executed hermeticity probe (20 passed with keys cleared and every outbound connect refused), edited only through write.py. Red-first captured for conjuncts 2, 4, 6. Suite: 148 passed/5 skipped on workflow+provisioning, 339 passed/5 skipped across adapters/dispatch/commands.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
RENUMBERED (SD.08, experiment a00-93b7761e-ba5b62). WHAT THE PREVIOUS VERSION SAID, condensed: this node's probes were the SD.06 parent review's (a00-f2da57da) — seven executed probes over the round's five conjuncts, all pass, verdict proved; the review's own words live in the previous grid version of this file (grid.py payload experiment:a00-c2613ff6-31b78c --version N-1) and are not restated here. WHAT THIS VERSION DIFFERS IN: the probe ordinals. Measured pre-fix on the current bytes, the probes list carried conjunct values [2,2,3,4,6,6,5] — every one of them exactly +1 against the parent hypothesis's own (1)-(5) list (sub-floor marker, dead-code removal, tree preview, experiment renumbering, zero timeout), because the parent's list is (1)-(5) and this node's were written as if the list were (2)-(6) with the renumbering step at 5. This round renumbered them to [1,1,2,3,5,5,4]: sub-floor gate+wire -> 1, dead-code removal -> 2, tree preview -> 3, experiment/hermeticity -> 4, timeout matrix+two-stage wire -> 5. NOTHING ELSE ON THE NODE CHANGED: verdict, confidence, parents, evidence_runs and the body are untouched, and the probe cmd/expected/observed/result text is byte-identical (the renumbering is ordinals only, not a re-measurement). The parent's five conjuncts and the sites that cite them (dispatch.py, provisioning.py, workflow.py, test_workflow.py) were renumbered in the same round by experiment a00-93b7761e-ba5b62, which is the node that cites this edit as its conjunct (1). Reversible in one command; the previous version is the grid.
<!-- THOUGHT:END -->
