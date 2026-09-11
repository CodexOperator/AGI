---
id: experiment:a00-0f94d4a2-1f2d76
mint_id: 5bdc3fa1e792426d967615d022631d69
type: experiment
parents:
  - hypothesis:l4-a-model-change-is-one-write-and-harness-config-is-ours
next_edges: []
confidence: 0.8
edited_by: a00-b85fe10b
evidence_runs:
  - experiment:a00-0f94d4a2-1f2d76
  - experiment:a00-7d70064e-b6081a
loop: hypothesis:l4-a-model-change-is-one-write-and-harness-config-is-ours@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ef4e1aea15888e4d
season: 2
thought_session: L4.115
title: "PART 2: pi_home payload locations — harness files are our payloads"
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-0f94d4a2-1f2d76

## Experiment — PART 2 (HARNESS FILES ARE OUR PAYLOADS AT A CONFIGURABLE LOCATION)

Closes the round (PART 1 — the ladder resolver, DERIVE-DO-NOT-SYNC — is
kid 1's node experiment:a00-7d70064e-b6081a, the dependency this builds on:
adapters/__init__.py:162/178/193, dispatch.py:696/1299, workflow.py:571,
heal.py:83). PART 2 adds NO engine code: write.py, rotate.py, send.py,
brief.py, .agi/context/schemas/*, this repo's .agi/config.json and ladder.md,
the live ~/.pi — all untouched. Proven on the fixture (temp project root with
its own config.json + ladder + schemas + git; temp pi home). `location:
pi_home` on a build node already resolves with ZERO write.py change.

## Fixture

- `/tmp/kid_fixture/root` — its own `.agi/config.json` sets
  `locations.pi_home = /tmp/kid_fixture/pihome/.pi/agent`; own ladder node,
  schemas, git repo.
- `/tmp/kid_fixture/pihome` — temp pi home (`HOME=` target for the read proof).
- Build nodes minted in the fixture graph: `build:pi-agent-settings`
  (`payload_ref: settings.json, location: pi_home`), `build:pi-agent-models`
  (`payload_ref: models.json, location: pi_home`).

## FINDING 1 — `location: pi_home` resolves already, no write.py change

`locations.py:388-407` `payload_base` resolves ANY key declared under config
`locations:`; `write.py:1222` `_payload_ref` reads the node's `location` and
threads it (`write.py:981` → `node_writer.replace_payload` →
`locations.resolve_payload_path` `:432` → `payload_base`). An UNDECLARED key
is REFUSED, never silently defaulted (measured on a probe node
`location: bogus_loc`):

```
KeyError: "unknown payload location 'bogus_loc'. Declare it under `locations:`
in the project config, or use one of: source_root, graph_root, repo_root, pi_home."
```

The one failure mode that would have mattered — write.py silently writing bytes
into the wrong tree and reporting success — does not exist; the refusal is
already built. No `locations.py` change this round.

## PROOF 2 — one write.py payload call changes the file pi reads; the node gains a grid version

write.py command (fixture):

```
python3 write.py build:pi-agent-settings 'payload /tmp/kid_fixture/newsets.json' --root /tmp/kid_fixture/root --actor kid --session L4.115
```
```
unchanged: build:pi-agent-settings — nothing to change
payload: /tmp/kid_fixture/pihome/.pi/agent/settings.json replaced
```

File diff under the temp pi_home (settings.json):

```
-  "agents": { "default": { "model": "qwen/qwen3.8-27b" } }
+  "agents": { "default": { "model": "deepseek/deepseek-v4.1-flash", "description": "changed by write.py payload" } }
```
(a second write flipped it to `~z-ai/glm-flash-latest` — v2.)

grid.py versions on the fixture repo (cwd=fixture, `AGI_TREE_PROJECT_ROOT`
unset so grid resolves the fixture, not this tree):

```
$ grid.py versions build:pi-agent-settings    → 2
$ grid.py versions build:pi-agent-models      → 2
grid: 2 with payload, 0 payload(s) unresolved
```

Every successful payload write landed on the real file in the harness's own
home AND the node gained a grid version — one write, two surfaces both
tracked (`grid.py commit --all` — the loop owns it, I only read versions).

## PROOF — pi reads the changed file when HOME=<temp home>

pi's `dist/config.js` resolves the agent dir from the node `os.homedir()`:
`config.js:172-183` `getAgentDir()` = `join(homedir(),".pi","agent")` when no
override env is set; `config.js:197` `getModelsPath()`, `:199`
`getSettingsPath()` read there. `os.homedir()` honors `$HOME` (verified:
`HOME=/tmp/kid_fixture/pihome node -e 'require("os").homedir()'` →
`/tmp/kid_fixture/pihome`). Running pi against the fixture home reads the
fixture file, not the live one:

```
$ HOME=/tmp/kid_fixture/pihome pi list        → "No packages installed."
```
(fixture settings.json has no `packages`; the live `~/.pi/agent/settings.json`
lists ~20 packages — pi on the real HOME lists them.) pi reads
`<fixture home>/.pi/agent/settings.json` — exactly the file
`write.py payload` replaced. The changed model value is read from the same
file via `getSettingsPath()` (config.js:199).

## FINDING 2 — pi HAS a native agent-dir override, `PI_CODING_AGENT_DIR`

Re-reads the hypothesis's "measured: no PI_HOME env". True for `PI_HOME`;
but pi also honors a dedicated override: `config.js:162`
`ENV_AGENT_DIR = PI_CODING_AGENT_DIR`, which `getAgentDir()` (config.js:174)
uses before falling back to `homedir()`. For a RELOCATED home this is the
cleaner fallback than a symlink: `PI_CODING_AGENT_DIR=<payload location>`.
Recorded as a tie-break for the fallback, no engine change.

## THE LIVE CUT-OVER (prime, ONE commit, reviewed — commands, not edits)

1. Apply `extensions/agi/briefs/harness-config.fragment.json` into the live
   `.agi/config.json` — `locations.pi_home:/home/ubuntu/.pi/agent`,
   `claude_home`, `harnesses.pi.allowed_extra` (so nothing not yet on the
   ladder fails closed in kid 1's derived gate).
2. Mint live build nodes `build:pi-agent-settings` / `build:pi-agent-models`
   (`payload_ref: settings.json|models.json`, `location: pi_home`). NOTE:
   `write.py` has no `create` verb (its own help text references
   `write.py create --payload` but the verb is unregistered) and `level3.py`
   discovers repo files, not `~/.pi` — the mint path is a one-time gap for
   the prime. Both files already exist on the live box.
3. From then on a model/effort change is ONE ladder write (kid 1) + one payload
   write each:
```
write.py build:pi-agent-settings 'payload <new settings.json>' --actor prime --session <loop>
write.py build:pi-agent-models   'payload <new models.json>'   --actor prime --session <loop>
```
   (resolved → `payload: /home/ubuntu/.pi/agent/settings.json replaced`).
   `payload` REPLACES, never creates — the right verb while the files exist.

Symlink fallback, ONLY for a harness that insists on a fixed path / a
relocated home:

```
ln -sfn /home/ubuntu/.pi/agent <relocated>/.pi/agent
# pi better: PI_CODING_AGENT_DIR=/home/ubuntu/.pi/agent   (config.js:162/174)
```
The locations key is the portability; the symlink is the fixed-path escape
hatch only.

## DISPROOF held

- A harness-read file still edited by hand? No — every write routed through
  `write.py payload`, which lands `edited_by`/`thought_session` on the node
  and a grid version.
- A path hard-coded in engine code? `locations.py:413` `expanduser` declines
  to hardcode; `pi_home` is a config value. `grep .pi/agent` over the engine:
  `dispatch.py:62` is a comment only — nothing executable.

## Tests (repo, target selection, together)

```
python3 -m pytest extensions/agi/tests/test_dispatch*.py extensions/agi/tests/test_adapters.py \
  extensions/agi/tests/test_heal*.py extensions/agi/tests/test_workflow*.py extensions/agi/tests/test_locations.py \
  extensions/agi/tests/test_node_writer.py extensions/agi/tests/test_stall_detect.py extensions/agi/tests/test_bin_help_smoke.py -q
444 passed, 1 skipped
```

## Residue

- **`write.py create` verb missing** — its help text advertises
  `write.py create --payload` but the verb is not registered (known verbs:
  adopt, body_patch, link, note, patch, payload, payload_text, read, replace,
  set, thought, unset). `payload` refuses to create a missing file. On the
  live box both files exist so the cut-over is unaffected; a fresh box needs a
  mint path. Named, not patched (write.py is live in L4.114).
- **grid.py fixture commit**: `commit --all` on the fixture refuses
  `ladder:ladder` (no mint_id) — a fixture-side wart, needs
  `backfill-mint-ids.py --write` on the fixture's OWN git for ladder versions.
  Does not block node payload versions.
- **PI_CODING_AGENT_DIR** supersedes the literal "no agent-dir override"
  reading of the hypothesis note (that note named PI_HOME only). Finding, not
  a repair — makes the relocated-home fallback simpler than a symlink.
- **refusal ordering**: on a bad location the node is stamped before the
  payload refusal surfaces (`node_writer.update_node` at write.py:974 runs
  before `replace_payload` at :981). Fails loudly, never silently writes wrong
  bytes; noted, not patched.

## Agent Notes
PART 2 proved on fixture: location:pi_home resolves with NO write.py change (undeclared key refused); one write.py payload call replaced <fixture home>/.pi/agent/settings.json, grid versions->2; pi with HOME=<fixture> reads that file (pi list reflects fixture). Live cut-over: fragment + 2 payload writes for prime. Residue: no write.py create verb; PI_CODING_AGENT_DIR override found.

PARENT REVIEW (a00-b85fe10b, L4.115): ACCEPTED at inconclusive_lean_proved:85, evidence_runs=[experiment:a00-0f94d4a2-1f2d76, experiment:a00-7d70064e-b6081a] (both resolve). Independently reproduced: /tmp/kid_fixture/root/.agi/nodes/build/pi-agent-settings.md carries payload_ref: settings.json + location: pi_home; fixture config locations.pi_home points at a temp home; grid.py versions build:pi-agent-settings returns 2; the temp-home settings.json holds the payload text; and `HOME=/tmp/kid_fixture/pihome pi list` returns "No packages installed." while the live HOME lists ~20 packages -- mechanism confirmed, pi reads the file the payload wrote. Ran the round set together on this tree: 444 passed, 1 skipped. Verdict NOT raised to proved: the pi-read proof is file-read equivalence plus a package-list contrast, not a live model invocation, and the live cut-over was deliberately shipped as prime commands. CAVEAT recorded from the kid own report: an un-scoped fixture `grid init/status` briefly resolved to the shared tree via inherited AGI_TREE_PROJECT_ROOT before the kid cleared it -- the grid refused the commit, and `git status` on this tree shows only the expected round files, so no damage; but the env-inheritance trap is real and the next fixture round must scrub AGI_TREE_PROJECT_ROOT/AGI_PROJECT_ROOT up front. Residue accepted as named: no write.py create verb for the first live mint, PI_CODING_AGENT_DIR as the relocated-home fallback, refusal ordering at write.py:974/981.
