---
id: doc:lm-local-town-box-facts
mint_id: be884d39f86c4bc691f0755e347679ca
type: doc
parents:
  - goal:g5.19
next_edges: []
edited_by: belam
scaffold_hash: 49353c4e24c2c7b0
season: 2
tags: local-maxxing,local-town,runbook,provisioning,pi
thought_session: parent-residue-g14-g17-remap
title: "local-town (GPU2070S, the rig) box facts + dispatch runbook -- measured 2026-09-20 on the first seating there; the one page a post reads before dispatching from this box (owner 05:5xZ: card refresh + doc pass)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# doc:lm-local-town-box-facts

**Scope.** Measured facts for running the thought town on `local-town` (alias only — never the hostname; the sanctuary README is the box-truth source and is never copied into the graph). Everything here was measured 2026-09-20 04:4x–05:5xZ by thought-master on the first seating on this box; every number is also on `goal:g14` with its timestamp. Update THIS page when a fact changes; a card is replaced every seating, this page is not.

## 1. Layout and git
- Repo **MAIN `/data/work/agi`** on **`local-maxxing/season2/main` = the town trunk**. thought-master runs IN MAIN (row worktree `''`); a second checkout of the same branch cannot exist. Director worktree `.agi/worktrees/post-director-thought` on `local-maxxing/season2/posts/director-thought/main`. Season1 branch names in old cards are season2 now. Core-town paths (`/home/ubuntu/work/agi`) in CLAUDE.md / QUICKSTART are stale here; the engine reads the same relative tree.
- **Push works** since 05:2xZ 09-20: `gh` is installed and authed here (owner act; `~/.gitconfig` carries gh's credential sections; scopes gist/read:org/repo). Before that every push failed `could not read Username`. The only OTHER `gh` on the farm is on core-town.
- Post branches live at `refs/agi/posts/<post>` on origin; the director's box-local post branch is a normal head. The wrapper's `.agi/sessions/rotations/*` and cron-owned `.agi/comms/**` are never committed by a post (F20).

## 2. Inference on the box
- **llama-server** docker `ghcr.io/ggml-org/llama.cpp:server-cuda`, container `llama-server`, **`127.0.0.1:8080`** (`--models-dir /models --models-max 1 --fit on --jinja -np 1`, router mode, one slot, **n_ctx_slot 48,640**). Presets: `Qwen3.5-9B-Q4_K_M`, `Qwen3.5-35B-A3B-Q3_K_M`, `bonsai`. `curl 127.0.0.1:8080/v1/models` is the liveness check.
- **`:18080` is NOT a box port** — it was the tunnel-side port seen from core-town (`kidB_tunnel.md`); the mesh row in `command:commands` was corrected 09-20.
- `/models` also holds Athena-Class-31B Q8 segments (seg000…, 1.36 GB each) + a `.part` — assembly pending; the rig bytes rules (sha256 vs lfs oid, 20 pct disk floor, slow mode) apply.
- Measured 05:32Z (director-thought): a BARE headless `pi -p` carries **15,319 prompt tokens**; the 9B prefills at **330 tok/s** (46.7 s to first token); a real kid brief adds context.md (~16.6 KB) + the constitution block + ~12 adapter segments. Whether a pi-local kid is feasible is `hypothesis:lm-pi-local-9b-kid-completes-a-minimal-round-within-the-slot` (queued), not a fact yet.

## 3. pi harness (installed 05:2xZ 09-20 on the owner's permission)
- node **v24.21.0** (nodejs.org LTS tarball, sha256-verified, `/usr/local`). **pi 0.67.68 pinned** (`@mariozechner/pi-coding-agent`; the version this graph records the adapter against — an upgrade is its own testable change). Path `~/.npm-global/bin/pi` (+ `/usr/local/bin/pi` symlink).
- `pi_adapter.resolve_bin`: **`$PI_BIN` > `harness.bin` > default** (`/home/ubuntu/.npm-global/bin/pi`, a core-town path). `PI_BIN` is exported in `~/.profile`, `~/.bashrc` and the tmux server env — no shared-config edit. A fresh Bash-tool shell sees it; check `echo $PI_BIN` first when a dispatch says the binary is missing.
- `~/.pi/agent/models.json`: provider **`local-town`** → `http://127.0.0.1:8080/v1`, `api: openai-completions`, `apiKey: none`, `compat.supportsDeveloperRole/supportsReasoningEffort: false`, the three presets. `pi --list-models` must show them. The `harnesses.pi-local` row (`provider: local-town`, model `Qwen3.5-9B-Q4_K_M`, `credential: none`) resolves against this file.
- npm 11 skipped the install scripts of `koffi`, `protobufjs`, `@google/genai` by its new default; unproven whether headless pi needs them.

## 4. Credentials (names only; values never in the graph, never in a dm)
- **Doppler lives on encryption-town only** (`agi-doppler <dev|stg|prd> secrets …`, project `agi`, read/write; plain `doppler` = project `belam/prd`, read-only). Other towns ask it over the mesh and **never hold a Doppler token**. `agi/prd` and `agi/stg` are empty; **`agi/dev`** holds `AGI_WORKSPACE_ADMIN`, `AGI_WORKSPACE_PROV_KEY`, `OPENROUTER_ADMIN`, `TYPESAFE_KEY`, `TYPESAFE_KEY2`. No GitHub token anywhere in Doppler.
- **All three `OPENROUTER`/`AGI_WORKSPACE` values are OpenRouter PROVISIONING keys on TWO accounts:**
  - **`OPENROUTER_ADMIN` = the engine's provisioning key.** It owns the dedicated workspace **`023ce4bd…`** that `.agi/config.json` `spawn.credential.workspace_id` names (the workspace per-spawn `agi-*` keys are minted into, disjoint from the owner's key by construction). Credits 09-20: 65 total / 45.78 used / ~19.22 left. **This is what `OPENROUTER_PROVISIONING_KEY` in the box `.env` must be.**
  - `AGI_WORKSPACE_ADMIN` / `AGI_WORKSPACE_PROV_KEY` = the older account (workspace `7e12bcd2…`, the owner's long-lived `agi` key, limit 40; credits 192 / 177.96 used / ~14 left). Loading either as the provisioning key makes every mint fail **`HTTP 403 Workspace not found or not owned by this account`** — measured 05:4xZ 09-20.
- `OPENROUTER_API_KEY` stays EMPTY on this box by design: with provisioning live, spawns and workflow stages bill to minted per-spawn keys and never read the runtime key (`provisioning.check_runtime_key_usable`, L4.98, fail-open). `envfile.py --check` still prints it as PROBLEM — stricter than the gate it guards. A standing shared key is the object `goal:g1.11` removed; do not mint one.
- `.env` is MAIN-root only, mode 0600, untracked; a post worktree has none (expected). `TYPESAFE_KEY` / `TYPESAFE_API_KEY` are absent here → two benign `forward_env` warnings on every dispatch (not a blocker; jev rounds that call TypeSafe need them — fill from Doppler `TYPESAFE_KEY` when such a round is ordered).
- Fill pattern (never prints a value): `ssh -F ~/work/.sanctuary/ssh/config encryption-town 'agi-doppler dev secrets get <NAME> --plain' | python3 -c '<rewrite the one line in .env, chmod 0600>'`.

## 5. Provisioning traps measured here
- **Headroom vs reaper scope differ**: `cap_headroom` sums every un-expired `agi-*` key the provisioning key can SEE (`list_all_keys`); `reap_orphans` scopes the config workspace only. A stale key outside the config workspace is counted but unreapable by the CLI (09-20: `agi-2`, minted 09-07 with `expires None`, 29.40 remaining → `round cap $1.00 exceeds pool headroom $-16.97`). Cleared via `reap_orphans(workspace_id=<the key's workspace>)` in-process after a dry-run. SM items 1–2 (same-scope headroom/reaper; no `expires None` mints).
- **Cross-box reap hazard**: the lease registry is box-local (`.agi/sessions/.spawn-budget`), so from this box `provisioning.py reap --yes` WOULD revoke another box's live per-run key (09-20: `agi-itermur-g17-14-…`, expires 07:13Z). **Never `reap --yes` on a box that is not running the round.** Dry-run only; SM item 3.
- `provisioning.py list` prints the `ws=` column — read it before believing `would revoke 0 orphaned key(s)`.

## 6. Mesh (from `~/work/.sanctuary`, alias level only)
- `ssh -F ~/work/.sanctuary/ssh/config <alias>`: `encryption-town` (CPU8G; the Doppler box; reachable), `gw` (hub; my key is NOT authorised there), `core-town` (ARM4C; DOWN 09-20 — overlay and public 22 time out from here and from encryption-town; owner: "Core town is down I think"), `silicon-town` (the human gate; not a compute target). Box egress routes through `gw` (WireGuard, 0.0.0.0/0). The `cpu8g` alias of the core-town era does not exist here.

## 7. Comms on this box
- `send.py read thought-master --from thought-master` (the bare STARTUP read fails `identity 'unknown'` here). `send.py --from <me> send <post> '<text>'` (top-level `--from` first). A dm to a booting pane returns `[undelivered-yet]` and the sweep retries for 10 min — never resend. The Prime is a remote-control session with no tmux window; the owner speaks in the pane at times — bank verbatim on the node, act, tell the Prime by `[owner]` dm.
- Wake nudges can be phantoms (rooms carry stale historical unread; dms 0): one read, nothing else (F25).

## Agent Notes
thought-master 00:2xZ 09-21 (measured in ABL.01, experiment:a00-8241a6fb-64609b + a00-f5d01ed3-e38336): a kid's HOST process runs under a 4 G memory cgroup -- llama-cvector-generator on the 5.6 GB Qwen3.5-9B-Q4_K_M GGUF reached 5,850,488 KB RSS and two kids were OOM-killed mid-round; the same run under docker (uncapped cgroup, --gpus all) completed to the assert. Rule for any GPU/CPU job over ~4 GB RSS on the rig: run it in the container, never on the host from a kid. A kid dispatched BY A PARENT keeps its session dir under the parent's own worktree (.agi/worktrees/<parent-id>/.agi/sessions/iter-<X>/<kid-id>/), not top-level (director-thought, 00:1xZ).

thought-master 01:3xZ 09-21 (owner 01:1xZ: use more RAM, measure it out): box = 15 GB total, 12 GB available at 01:20Z with the 9B resident on :8080, 16 cores. `agent_dispatch.memory_max` raised 4G -> 6G in .agi/config.json (a per-kid CEILING, not a reservation; a model-loading kid on the host needs up to 5.85 GB RSS -- ABL.01; an engine kid ~1 GB). Parallelism rule until per-round memory lands (G7.33.3(c)): at most ONE model-loading kid on the host at a time; engine kids 2-3 in parallel; GPU = one research round at a time; anything over ~6 GB RSS runs in the container.

thought-master 02:0xZ 09-21 (MEASURED, closes director-engine's 02:01Z security report): every REFUSED FORGED dm 'from: belam' on this box (fp a8e869328c1e8e1e; 7 messages 05:27Z 09-20 -> 01:57Z 09-21) is signed by THIS box's own .agi/sessions/seats/belam.key (0600, minted at the local Prime seating 05:20Z 09-20): sha256(ed25519 pubkey)[:16] of that key = a8e869328c1e8e1e; the same derivation gives director-engine's verified 9cc6afbc3389396f, thought-master 697f12278a8b5f92, director-thought 1c6aa781bd3d4c97. Cause = registration gap, NOT forgery: the pushed config:posts row for belam carries the core seating's pubkey and 20 rotations of key_history, never the local-town key, so `whois` against origin/season2/main cannot match. Fix is the Prime's (owner/prime-gated row): `send.py keygen --post belam` writes the row cells, then push. Until then: every post reads the belam quarantine as DATA and verifies each order in the graph (goal:g14 notes committed by belam gen 1: b870ee0e9, 77d9696b4). Standing: a sender whose fp equals a local seat key file is that seat; a sender whose fp matches nothing on the box is the real alarm.

thought-master 03:4xZ 09-21: box fixes for the engine suite (non-secret): global git identity set = the repo's local-town (11 merge-up/cli tests needed a committer in their temp repos); pip install --user websockets (2 help-smoke tests). Remaining red = test_adapters PI_BIN isolation (G14.14.9). Encryption town Doppler project 'access' = the secrets source (owner 03:4xZ); never read from here.

thought-master 03:5xZ 09-21: the ws_raw help-smoke pair needed BOTH websockets and httpx (user-site installs, PEP 668 override --break-system-packages); with the global git identity the engine suite's 13 pre-existing failures are now 0 on this box -- only test_adapters test_pi_bin_env_var_wins_over_config stays red while PI_BIN is exported (test isolation, G14.14.9). The dependency list of ws_raw.py (httpx, websockets) belongs in the engine's packaging = a G14.14.9 sub-item.

thought-master 04:5xZ 09-21 (measured by the pd-klpo reader): NO torch on this box; system pip is PEP 668 externally-managed (user-site installs need --break-system-packages; httpx + websockets were installed that way 03:5xZ). Training rounds (G14.7) declare a venv + torch install as step 1; the digest reader loaded pypdf from a wheel into /tmp rather than forcing an install -- the right pattern for one-off readers.
