---
id: experiment:a00-d9d3fcc1-grok-tip-measure
mint_id: 6bfa324200c042d1b4c4d5e669aa1d20
type: experiment
parents:
  - hypothesis:a00-d9d3fcc1-943a40
next_edges: []
edited_by: a00-dd8fbaa9
line_ceiling: 400
loop: goal:g7.25.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 162
profile: balanced
role: kid
scaffold_hash: e63370238acd7ea4
season: 2
title: "Experiment: five probes on the landed tip — load, hash, resolve-by-name, dispatch gate, config gate"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-d9d3fcc1-grok-tip-measure

## Experiment

**Testable claim (measured on THIS tip, adapter landed):** On this tip, with
`extensions/agi/bin/adapters/grok_bot_adapter.py` present, `adapters.load('grok_bot')`
succeeds on the TREE bytes with all five `adapters.REQUIRED` callable; the file
sha256 is the canonical `66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c`;
`adapters.resolve(real cfg, 'grok-bot')` refuses by name because the
`harnesses.grok-bot` row is absent (Belam-owned); and `dispatch.py` has zero grok
hits. On THIS tip the config row is therefore the **sole remaining cell for
`resolve` — but only because the adapter was landed first**, which DT.21's "sole
remaining gap" wording did not say. It was false on the tip it was written on,
where the adapter file was absent.

### What was done

1. Copied the canonical adapter byte-for-byte from
   `.agi/sessions/iter-DT.22/a00-dd8fbaa9/grok_bot_adapter.canonical.py` to
   `extensions/agi/bin/adapters/grok_bot_adapter.py` (162 lines). sha256 verified equal.
2. `level3.py --mint-missing-only` did **not** discover the new file — the scan
   reads `git ls-files`, and the file is untracked on this tip (no commit allowed
   for a kid). So the build node was minted by hand with `write.py create build`,
   `parents: [mvp:bin-modules]` (the map's `extensions/agi/bin/ | mvp:bin-modules`
   prefix), as anticipated by the brief. Node id `build:bin-adapters-grok-bot-adapter`
   (goal:s29 `[mvp]` shape). A first attempt under an agent-prefixed slug was
   deprecated and moved to `.agi/nodes/deprecated/build/` rather than deleted.
3. Ran all five probes below on the tip bytes.

### Probes

```yaml
probes:
  - conjunct: wire
    class: experiment
    cmd: "cd extensions/agi/bin && python3 -c \"import adapters; m=adapters.load('grok_bot'); print(m.NAME, [callable(getattr(m,f)) for f in adapters.REQUIRED])\""
    expected: "grok-bot [True, True, True, True, True]"
    observed: "grok-bot [True, True, True, True, True]"
    result: pass
  - conjunct: wire
    class: experiment
    cmd: "sha256sum extensions/agi/bin/adapters/grok_bot_adapter.py"
    expected: "66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c"
    observed: "66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c  extensions/agi/bin/adapters/grok_bot_adapter.py"
    result: pass
  - conjunct: auth
    class: experiment
    cmd: "python3 -c \"import json,sys; sys.path.insert(0,'extensions/agi/bin'); import adapters; adapters.resolve(json.load(open('.agi/config.json')), 'grok-bot')\""
    expected: "AdapterError naming grok-bot and the declared set"
    observed: "AdapterError: no harness 'grok-bot' in config; declared: ['claude-code', 'copilot-cli', 'pi', 'pi-local']"
    result: pass
  - conjunct: gate
    class: experiment
    cmd: "grep -Ein grok extensions/agi/bin/dispatch.py"
    expected: "rc=1, no output"
    observed: "rc=1, no output"
    result: pass
  - conjunct: gate
    class: experiment
    cmd: "sha256sum .agi/config.json (before and after all work)"
    expected: "equal hashes — config.json never written"
    observed: "before == after == da08e30344d55554a0c831efa890253ca1594d2cd5ff053fcfe26ad7f1d8e459"
    result: pass
```

## Evidence

- **wire (load):** `grok-bot [True, True, True, True, True]` — the module loads from
  TREE bytes (`extensions/agi/bin/adapters/`), declares `NAME = "grok-bot"`, and all
  five `adapters.REQUIRED` are callable.
- **wire (hash):** `66b7891f…826081c`, byte-identical to the canonical copy.
- **auth (resolve):** `AdapterError: no harness 'grok-bot' in config; declared:
  ['claude-code', 'copilot-cli', 'pi', 'pi-local']` — a named refusal, not an
  ImportError. The `harnesses` block exists on this config, so the legacy
  synthesis path is not in play.
- **gate (dispatch):** zero grok hits in `dispatch.py` (rc=1).
- **gate (config):** `.agi/config.json` sha256 unchanged across the whole round:
  `da08e30344d55554a0c831efa890253ca1594d2cd5ff053fcfe26ad7f1d8e459`. The
  `harnesses.grok-bot` row was NOT added.

**Correction to DT.21's claim.** On this tip the config row is the sole remaining
cell for `resolve` — but the adapter had to be landed first for that to be true.
DT.21 landed the adapter only on a side branch, so on `core/season2/main` (and this
branch, cut from it) the "sole remaining gap" sentence described a state that did
not exist here. Measured, not assumed.

**Build-node side effect, stated plainly.** `level3.py --mint-missing-only` minted
**203** census build nodes on this tip in addition to the hand-minted grok node
(the scan had a backlog of tracked engine files with no build node). That is the
sanctioned ADDITIVE-ONLY scan doing its job, but it is a large graph delta for a
single-kid round and the parent should expect it in the commit.

production_lines: 162 (the adapter copy; measured per-file by `wc -l` because the
new file is untracked and `git diff --numstat` shows nothing for it).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-dd8fbaa9, DT.22). The probes listed in this body are the KID own; the parent ran eight independent negative probes (parent_probes.py in the round scratch dir) and all held: the load probe reads the tree file itself, the corrupt-copy probe proves the REQUIRED check is live, the hash probe is byte-identical, the resolve probe shows the real config refusing by name and an in-memory row resolving, dispatch.py is grok-free, config.json is byte-identical to HEAD, the build/mvp chain resolves, and the base tip 7d35ae4f9 has no adapter file. This closes the node own caveat: the hand-minted build node was untracked, and the parent done commits it via --owns. One residue is named and left for the director, not committed here: level3.py --mint-missing-only also left 203 unrelated census build nodes untracked under .agi/nodes/build/; they are foreign to this round (their basenames carry no agent id) and are neither accepted nor rejected by this review.
<!-- THOUGHT:END -->
