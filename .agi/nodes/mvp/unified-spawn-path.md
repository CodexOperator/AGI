---
id: mvp:unified-spawn-path
mint_id: 1646a6b2322244b886c6ce467a573d7c
type: mvp
parents:
  - goal:g4.6
next_edges:
  - outcome:a00-c8365a0c-85a6d1
confidence: 0.7
edited_by: season.py
season: 1
status: open
thought_session: season
title: "One spawn path: harnesses declared in config, adapters behind them"
---
# mvp:unified-spawn-path

**This is a design node, not code** (see `[mvp].md`, revised 2026-09-01). It
states the minimum the subsequent `build` nodes must satisfy, and the falsifier
that says whether they did.

## 1. The seam

`dispatch.py` keeps everything it does today **except** command construction and
child-environment construction. Those two move behind an adapter chosen by name
from config. Shared and staying shared: target selection, `--target` aiming, the
spawn gate, node scaffolding, the manifest, `post_wire`, the evidence gate.

## 2. Config — the whole customization surface

```jsonc
"harnesses": {
  "pi": {
    "adapter": "pi",                       // -> bin/adapters/pi_adapter.py
    "bin": "/home/ubuntu/.npm-global/bin/pi",   // $PI_BIN still wins if set
    "provider": "openrouter",
    "thinking": "medium",
    "models": { "kid": "z-ai/glm-5.3-flash", "parent": "qwen/qwen3.8-27b" },
    "env_scrub": ["ANTHROPIC_*", "CLAUDE_CODE_*"]
  },
  "claude-code": {
    "adapter": "claude_code",
    "models": { "kid": "claude-sonnet-5", "parent": "claude-opus-5" }
  }
},
"spawn": { "harness": "pi", "parallel": 1 }
```

**Adding a harness is one config entry plus one adapter file.** No edit to
`dispatch.py` — that is the falsifier, not a slogan.

**Legacy config must keep resolving.** When `harnesses` is absent, synthesize
`harnesses.pi` from today's `agent_dispatch` (`provider`, `model`, `thinking`,
`claude_max_parallel`) so every existing project runs unchanged. This repo has
paid for that rule repeatedly — `agi-tree.config.json`,
`autoresearch-tree.config.json` and `$AUTORESEARCH_TREE_PROJECT_ROOT` all still
resolve. Same discipline here.

## 3. Adapter interface — the minimum, and no more

`extensions/agi/bin/adapters/<name>_adapter.py`:

```python
NAME: str

def build_command(*, harness: dict, tier: str, context_file: str,
                  agent_id: str, iter_n: int, sess_dir: Path,
                  scaffold: dict | None) -> list[str]:
    """The argv that starts one agent. The ONLY place a harness's CLI shape
    is known."""

def child_env(*, harness: dict, base: dict[str, str]) -> dict[str, str]:
    """The environment that argv runs in, including the scrub."""
```

Two functions. Anything a third function would need is either shared (and
belongs in `dispatch.py`) or is `goal:g4.7`'s (`is_alive`, `restart`) and is
**out of scope here** — declared in the docstring, not implemented.

`pi_adapter.py` is `pi_model_args` + `_build_pi_args` + `_scrubbed_env`
**moved, not rewritten**. Their existing tests must pass against the moved
code with assertions unchanged; a rewrite that needs the tests edited has
changed behaviour and is out of scope.

`claude_code_adapter.py` is declared in config and **not implemented this
pass** — the owner's call: pi is the primary platform now that OpenRouter is
reachable. It should exist as a stub that raises a clear `NotImplementedError`
naming `goal:g4.6`, so the config entry is honest rather than aspirational.

## 4. Tier is a parameter

`build_command(tier=...)` selects `harness["models"][tier]`. `parent` and `kid`
differ in model and in brief, and in nothing else. This is what finally connects
`goal:g4`'s per-tier model knob to code — `cc_dispatch.kid_model` and
`parent_model` have existed for weeks with **no reader anywhere**
(`experiment:a00-763e629b-5c04ad` confirmed this by grep).

A tier that is not in `models` is an error naming the tier and the harness,
never a silent fallback to the other tier's model. Tiering the model is the
entire point of having tiers.

## 5. Completion is a graph event

**The finish signal is the scaffolded node acquiring real content.** Not a pid,
not a manifest field, not `cli.py done`.

```python
def is_complete(root: Path, node_id: str) -> bool:
    """True once the node's body differs from the scaffold placeholder."""
```

Why this and not what exists: today "done" is `cli.py done` writing
`agent.json` while `heal.py` polls a pid. Both are the pi process model wearing
a general name. A Claude Code kid has no pid to poll. Worse, a kid that wrote
its node and then died looks *identical* to one that never started — the
2026-08-31 field note ("check the filesystem before resuming; kids often die
after the node file landed, losing only their report") is that failure, already
observed, handled by hand.

**Three consequences the build must honour:**

- **The kid writes its `verdict`, `confidence` and `evidence_runs` into its own
  node frontmatter.** `post_wire` reads the node. This makes the 2026-09-01
  drop-bug structurally impossible rather than fixed: verdict data stops
  travelling through `agent.json` → `heal.py` → manifest → `post_wire`, a
  four-hop path where one hop carried one field and silently dropped the rest.
- **`cli.py done` still works and is still worth running** — it announces, it
  applies the evidence gate at write time, and it is how a kid reports
  `caveats`/`struggles`. It is demoted from *the definition of done* to *one
  way to announce it*.
- **From the agent's own point of view the finish step is identical on every
  harness:** write your node. That is the unification the brief can finally
  state without naming a runtime, and it is a prerequisite for `goal:g1.9`'s
  assembled brief.

## 6. Out of scope, named so it is not quietly attempted

Healing (`goal:g4.7`) · the Claude Code adapter's body · the iomap system ·
`closed_chains.txt` (`goal:g4.3` H4b) · brief assembly (`goal:g1.9`).

## 7. Falsifier

1. **Add a third harness with no edit to `dispatch.py`** — one config entry,
   one adapter file. Spawn a kid on it. Any change required outside those two
   files means the seam is in the wrong place.
2. **`grep` the shared path for branches keyed on harness name: zero**, outside
   the single adapter lookup.
3. **The moved pi tests pass with assertions unchanged.**
4. **A kid that writes its node and is then killed before reporting is still
   counted complete**, on any harness. This is the one that proves completion
   stopped being process inspection; the others only prove the code moved.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Written by the delegator on 2026-09-01 as the design a kid can build against,
because the owner's budget constraint makes the expensive tier's job "get the
seam right once" and the cheap tier's job "fill it in".

The seam is drawn at two functions on purpose. The temptation is a richer
adapter — spawn, poll, heal, parse — and that is how a "unified" path grows a
per-harness copy of the loop inside it, which is exactly the failure
`goal:g4.3`'s invariant names. Two functions is the smallest interface that
still lets a harness be added without touching shared code, and `is_alive` is
deliberately named-and-excluded so its absence reads as a decision.

The completion clause is the owner's, and reframes more than it looks like.
Once "done" is a graph event, `heal.py`'s finished-detection dissolves rather
than being ported (which is why `goal:g4.7` is `horizon`, waiting on this),
the verdict stops travelling through a four-hop marshalling path that was
silently dropping three of its four fields until this morning, and the brief
can describe finishing without naming a runtime. One change closing three open
problems is usually a sign the abstraction was missing rather than that the
change is clever.

Confidence 0.7, not higher: the placeholder-comparison test for "acquired real
content" is the weak joint. A kid that writes a node whose body happens to
match the scaffold, or a scaffold template that changes, would both break it,
and the honest alternative — hashing the scaffold at write time and storing the
hash — is one more field this node does not currently require.
<!-- THOUGHT:END -->