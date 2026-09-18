---
id: experiment:a00-cf8addbe-8374f0
mint_id: b8b74f9c03e148b3962e669a70378b2e
type: experiment
parents:
  - hypothesis:l4-same-harness-handback-a-claude-code-caller-gets-one-exact-native-workflow-call-every-engine-js-is-registered-and-a-hook-closes-the-record
next_edges: []
confidence: 0.85
edited_by: director-sanctuary
evidence_runs:
  - experiment:a00-cf8addbe-8374f0
line_ceiling: 60
loop: hypothesis:l4-same-harness-handback-a-claude-code-caller-gets-one-exact-native-workflow-call-every-engine-js-is-registered-and-a-hook-closes-the-record@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 86
profile: balanced
role: kid
scaffold_hash: fd09c81cf0c2b7cc
season: 2
title: "Native handback: seam, one exact Workflow call, 8 links, note hook"
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-cf8addbe-8374f0

## Experiment

Built the three conjuncts of hypothesis:l4-same-harness-handback on the live
bytes, then proved them on the repo suite.

**Conjunct 1 (detection, `extensions/agi/bin/workflow.py`).** Added
`CLAUDE_CODE_SEAM_VARS = (CLAUDECODE, CLAUDE_CODE_SESSION_ID,
CLAUDE_CODE_MESSAGING_SOCKET)` and the pure helper
`_claude_code_seam_present(env=None)` (defaults to `os.environ`, takes an
explicit mapping so both branches are assertable in-process). The
`harness != "pi"` branch is now gated explicitly on `harness ==
"claude-code"` and, when the seam is present, writes ONE line to `out`
instead of the SM.120 stderr notice:

    Workflow({"name": "agi-round-review", "args": {"targets": [...]}})

The `name` is the REGISTERED script stem — `manifest["script"]` minus `.js` —
never `f"agi-{key}"`. Verified on the live registry: `key=review ->
agi-round-review.js` and `key=drafting -> agi-brief-drafting.js`, so a
key-formatted name would print two links that do not exist. `args` is the same
`args: dict` parameter `_mint_run_key` used. Every line below (`stage_resolved`
loop, `summary()`, `_track_run`, `return 0`) is unchanged; the seam-absent path
keeps the SM.120 stderr line byte-for-byte.

**Conjunct 2 (registration, `workflow.py link`).** New `link_workflows`
subcommand (name `link`; NOT `register`, which stays the retired refusal
locked by `test_register_refuses_naming_author_verb`). For every manifest
`script` with no same-named entry under `<repo>/.claude/workflows/`, it
creates the relative symlink `../../extensions/agi/workflows/<script>`,
idempotent (second run creates 0), refusing by name when a path exists and is
not a symlink pointing at the right target. Run FOR REAL against this repo:
`[linked] 8 workflow link(s) created`, then `[linked] 0` on the re-run; all 12
manifests' scripts now resolve to live symlinks (4 pre-existing + 8 new,
git-tracked).

**Conjunct 3 (record, `extensions/agi/hooks/workflow_note.py`).** New
PostToolUse hook: reads the Claude Code envelope on stdin, requires
`tool_name == "Workflow"`, reads `tool_input.name`, takes the first present of
`runId`, `run_id`, `id` from `tool_response` (assumed shape; no real sample
exists here), reverse-maps the name to the config key by scanning the
manifests for `script == <name>.js`, resolves
`<shared root>/sessions/workflows/<key>.jsonl`, picks the LAST row with
`harness_id == []` (the row carries NO `args` field, so correlation by args is
impossible), and shells out to the existing `workflow.py note <run_key>
--harness-id <id>`. `plan_note` is pure (a test drives it directly); `_note` is
the one subprocess seam. Any missing/malformed field, an unrelated project,
and a swallowed `note` refusal all print a NAMED one-line stderr message and
return 0 — never a traceback, never non-zero.

**`~/.claude/settings.json` was NOT written** (per the SM.121 brief: the live
file is global to every concurrent agent, so prepare + disclose only).

### The exact new settings.json entry

```json
{
  "matcher": "Workflow",
  "hooks": [
    {
      "type": "command",
      "command": "python3 /home/ubuntu/work/agi/extensions/agi/hooks/workflow_note.py",
      "timeout": 10,
      "statusMessage": "agi workflow note..."
    }
  ]
}
```

Appended to the existing `PostToolUse` array; existing `PreToolUse`,
`SessionStart`, `UserPromptSubmit`, and the Bash/gitnexus `PostToolUse` entry
are untouched. Diff (tmp copy, reproduced under
`.agi/sessions/iter-121/a00-cf8addbe/`):

```diff
@@ -24,6 +24,17 @@
             "statusMessage": "Checking GitNexus index freshness..."
           }
         ]
+      },
+      {
+        "matcher": "Workflow",
+        "hooks": [
+          {
+            "type": "command",
+            "command": "python3 /home/ubuntu/work/agi/extensions/agi/hooks/workflow_note.py",
+            "timeout": 10,
+            "statusMessage": "agi workflow note..."
+          }
+        ]
       }
     ],
     "SessionStart": [
```

## Evidence

Three shipped tests that call `run_workflow(..., "claude-code", ...)`
directly (`test_claude_code_path_feeds_the_same_view`,
`test_real_cc_run_appends_exactly_one_row`, `test_claude_code_path_mints_nothing`)
now clear the three seam vars via `_clear_cc_seam(monkeypatch)` — without that
they inherit `CLAUDECODE=1` from the Bash tool and silently hit the new branch.

`python3 -m pytest extensions/agi/tests/test_workflow.py -q` -> **93 passed in
114.95s**. New coverage: seam helper both branches; native seam prints exactly
one call with `agi-round-review` / `agi-brief-drafting` (never the key form);
no-seam still prints the stderr notice and no call; `link` creates all 12 and
is idempotent; `link` refuses a non-symlink by name; hook reverse-map, ordered
id keys, named skips on four unrecognised payloads, and `main` notes once via
the `_note` seam then stays 0 on malformed stdin and an unrelated cwd.

Production lines: `git diff --numstat 4c366d29e -- extensions/agi/bin/workflow.py`
= 86 added / 10 removed (the hook script is separate, 190 lines, plus the 8
symlinks which are git objects). Headroom: 86 < 120 (2x), so no re-brief.

> Note: the loop's clean-tree requirement committed the in-progress bytes as
> WIP checkpoint `ced593fc1` while this round ran, so `git diff HEAD` reads
> clean for `workflow.py`; the measurement is against the last real commit
> `4c366d29e` (SM.120).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Independently reviewed: reran the cited suite fresh, 93 passed in 115.58s, matches the reported result exactly. Confirmed workflow.py (seam vars, _claude_code_seam_present, link_workflows, harness=="claude-code" branch) and hooks/workflow_note.py already at HEAD via the gen3 WIP commit ced593fc1 -- this node and the tests were the only remaining bytes, not a fabrication. Confirmed all 12 .claude/workflows/ symlinks resolve, 8 dated to this round, 4 pre-existing. One correction for the record: the card carried "the registration verb is workflow.py register" from sanctuary-master -- ground truth is link, not register; register is a separate pre-existing verb (new-manifest registration, its own refusal test, test_register_refuses_naming_author_verb) untouched by this round. The card was stale, not the code; noting here so it is not repeated. Accepting the verdict as delivered (inconclusive_lean_proved:85) -- evidence supports it and the hedge is honest: the hook payload shape (runId/run_id/id) is untested against a real Workflow tool_response, and settings.json was correctly left uninstalled since it is a shared global file.
<!-- THOUGHT:END -->

## Agent Notes
Built conjunct 1 (explicit claude-code seam gate; native handback prints Workflow({"name": <script-stem>, "args": <resolved args>})), conjunct 2 (new workflow.py link verb, 8 real symlinks created, 12 resolve, idempotent), conjunct 3 (workflow_note.py PostToolUse hook, pure plan_note + one _note seam). Fixed three shipped claude-code tests to clear the ambient seam. pytest test_workflow.py: 93 passed. settings.json entry prepared + diffed, not installed.
