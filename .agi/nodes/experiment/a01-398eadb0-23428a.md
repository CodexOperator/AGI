---
id: experiment:a01-398eadb0-23428a
mint_id: 2f782d32a02f42f98503e96ed476710d
type: experiment
parents:
  - hypothesis:a00-4ed0dccd-68c060
next_edges: []
confidence: 0.7
edited_by: season.py
scaffold_hash: ef253beb40c570ed
season: 1
thought_session: season
title: A01 398eadb0 23428a
verdict: inconclusive_lean_proved:70
---
# experiment:a01-398eadb0-23428a

## Experiment

**Command-surface enumeration: classifying every agent tool by blast radius**

Ran inside a live pi agent session on iter 1057 to enumerate the full tool set available to parallel kids and classify each by whether it can cause a g4.1-class collision.

**Method:**
1. Read the pi system prompt tool declarations (the tool schemas available to this agent).
2. Read the kid brief at `extensions/agi/bin/brief.py` which is the sole prompt text a kid receives.
3. Read dispatch.py to understand what env vars are scrubbed and what commands reach a kid.
4. Classify each tool as **whole-tree** (can touch any file or run any command) vs **file-scoped/safe**.
5. Check whether any technical enforcement mechanism exists for command restriction.

**Full enumeration:**

| Tool | Blast Radius | Notes |
|------|-------------|-------|
| `bash` | **WHOLE-TREE** | Arbitrary shell. Can `git commit -A`, `git checkout`, `git stash`, `git add -A`, rm any file |
| `run_experiment` | **WHOLE-TREE** | Same as bash (autoresearch mode). Arbitrary shell. No path restriction |
| `write` | **POTENTIALLY WHOLE-TREE** | Writes any path. Kid could write to another kid's node |
| `edit` | **POTENTIALLY WHOLE-TREE** | Edits any path. Same concern |
| `subagent` | **WHOLE-TREE** | Spawns agents inheriting the full tool set; each can run arbitrary commands |
| `ralph_start` | **WHOLE-TREE** | Starts persistent loop that runs arbitrary operations |
| `read` | safe (read-only) | Cannot write or execute |
| `web_search` / `code_search` | safe (network) | No filesystem access |
| `fetch_content` / `get_search_content` | safe (network) | Read-only HTTP |
| `mcp` | depends on server | MCP server tools could be anything. Uncategorized risk |
| `manage_todo_list` | safe (state) | Internal task tracking |
| `memory_*` | safe (scoped) | Memory file ops only |
| `init_experiment` / `log_experiment` | safe (scoped) | Autoresearch.jsonl writes only |
| `add_directory` / `search_external_files` | safe (read-only) | Read-only directory scan |

**Current restriction mechanism:**
- Prose-only. `brief.py` says "DO NOT run git" and names forbidden commands.
- No technical enforcement. `bash` and `run_experiment` tools are unrestricted.
- Tool schemas are inherited from pi, not filtered per agent.
- No mechanism exists to restrict `bash` to a file subset or to whitelist git to explicit-path args only.

**Verdict on feasibility:**
The hypothesis's proposed whitelist (read/write/edit/bash-scoped-to-declared-paths/subagent-isolated) is architecturally feasible for `read`/`write`/`edit`/`bash` IF pi adds a tool filter layer. Currently pi has no such filter — tools are global. Enforcing it requires either:
- A pi SDK extension that intercepts and validates tool calls, OR
- A wrapping harness that constrains the agent's environment (e.g. restricted shell commands via PATH manipulation, read-only filesystem mounts).

**Secondary finding:** The hypothesis correctly identifies the 3 whole-tree commands that caused all g4.1 incidents (`git commit -A`, `git checkout` via `grid.py checkout --all`, `git add -A`). But `bash` being unrestricted means the prose-only restriction is bypassable: `bash "git commit -A -m 'pwn'"` works despite the brief's "DO NOT run git" instruction. The whitelist must apply to tool-level capabilities, not just the prompt text.

## Evidence

Test suite: `python3 -m pytest extensions/agi/tests/ -q` = 1451 passed, 3 pre-existing failures (test_provisioning.py::test_a_minted_key_is_capped_and_expires_and_can_be_revoked, test_publish_alarm.py::test_the_scratch_worktree_never_survives_the_run, test_publish_alarm.py::test_dry_run_writes_neither_nodes_nor_grid_versions). Not caused by this experiment.

Key files examined:
- `extensions/agi/bin/brief.py` — kid brief prose restrictions (no enforcement)
- `extensions/agi/bin/dispatch.py` — scrubbed_env(), spawn flow
- `extensions/agi/bin/adapters/pi_adapter.py` — pi command assembly, no tool filter
- `extensions/agi/lib/agent-prompt.md` — agent prompt template
- Current pi tool schemas (from system prompt in this session)


## Agent Notes
Enumerated all ~18 agent tools by blast radius: 6 whole-tree (bash, run_experiment, write, edit, subagent, ralph_start) vs 12 scoped/safe. Confirmed hypothesis root-cause analysis holds (all 3 g4.1 incidents involve whole-tree commands). Found no technical enforcement mechanism — brief.py prose-only restriction (DO NOT run git) is bypassable via bash. Whitelist approach sound but requires pi-level tool filtering which does not yet exist.