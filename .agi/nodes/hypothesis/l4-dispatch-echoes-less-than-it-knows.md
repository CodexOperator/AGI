---
id: hypothesis:l4-dispatch-echoes-less-than-it-knows
mint_id: d87f63ba046c421ea9ab94609cc53263
type: hypothesis
parents:
  - goal:g1.11
next_edges: []
edited_by: belam-S1-L4-V
scaffold_hash: 6f77954d1e0f6c94
season: 2
testable_claim: "OWNER 2026-09-10 ('Go for both a and b as described'; measurement on goal:g17.1). THE DEFECT: a dispatch.py spawn's console output — the child env, the per-spawn provider-key mint, GIT_CONFIG_* hooks wiring, the bypassPermissions flag and the whole brief — was classified by Opus 5's safeguards as violative cyber content, which downgraded the seat that read it to opus-4-8 for the rest of its session. The same output is also the loudest thing on a seat's pane, and the pane is what the livestream (goal:g18.1) will show. Two problems, one cause: dispatch echoes more than any reader needs. CLAIM: dispatch.py's console output is reduced to a reader's contract — per spawn ONE line naming agent id, tier, iter, target node, harness, model, branch/worktree and the per-spawn key's NAME and cap (never its value, never a prefix); the env is never printed; the brief is never printed in full (--dry-run keeps its truncated preview, which already exists — trap 0aj); anything a debugger needs goes to the spawn's session dir as spawn.json (env with key values REDACTED to their last 4 characters, the full brief, the argv) where a reader opens it on purpose. envfile.py's forbidden-pattern check extends to dispatch's stdout in the suite: a test spawns with --dry-run and a real-shaped fake key in the env and asserts no key-shaped string reaches stdout. PROVED BY: (a) the suite test above; (b) a live --dry-run on the real tree whose stdout, pasted, contains no key material and no env dump; (c) the seat pane during a real dispatch, captured, shows the one-line contract per spawn; (d) spawn.json in the session dir carries the redacted env and the full brief for the debugger. DISPROVED BY: any key value or prefix, or any env variable's value, on dispatch's stdout after this lands. HARD RULES: dispatch.py is a build node, edit through write.py; do not change what is SPAWNED, only what is PRINTED — the child's env is untouched; the reaper's log lines and the DONE parser's lines are contracts other code reads — keep their shape; redaction is by name pattern (KEY, TOKEN, SECRET, PASSWORD) and by value shape (sk-, sk-or-v1-), both; --verbose may restore the full echo for a human who asks for it, and it defaults off."
thought_session: f3b92df1
title: dispatch.py prints what a reader needs, never the spawn env or key material — a smaller dox surface and fewer classifier hits
---
<!-- BODY:BEGIN -->
# hypothesis:l4-dispatch-echoes-less-than-it-knows

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
