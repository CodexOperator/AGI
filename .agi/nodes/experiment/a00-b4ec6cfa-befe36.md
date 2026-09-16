---
id: experiment:a00-b4ec6cfa-befe36
mint_id: 42a93a8188e747b5ba36281409d6d102
type: experiment
parents:
  - hypothesis:ws-raw-zero-injection-adapter
next_edges: []
confidence: 0.8
edited_by: a00-2f819956
evidence_runs:
  - experiment:a00-b4ec6cfa-befe36
loop: hypothesis:ws-raw-zero-injection-adapter@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "/tmp/tm04_parent_probe.py P2+P3", "expected": "unknown param and unknown top-level key each -> {error} naming the key + close 1008", "observed": "P2 error 'param not allowlisted: system_prompt' close 1008; P3 error 'unknown key(s): system' close 1008", "result": "hold"}
  - {"conjunct": 2, "class": "wire", "cmd": "/tmp/tm04_parent_probe.py P4", "expected": "one raw relay -> llama-server --log-prompts-dir capture byte-equal to the caller prompt (the live bytes reach the server log dir)", "observed": "1 capture, 25 B, byte_equal_to_caller_prompt [true], 24 tokens streamed", "result": "hold"}
  - {"conjunct": 3, "class": "wire", "cmd": "/tmp/tm04_parent_probe.py P5", "expected": "raw direct-httpx vs adapter sha equal at temp0/seed7/cache_prompt false", "observed": "direct_sha a64dff26583b5242 == adapter_sha a64dff26583b5242, equal true", "result": "hold"}
  - {"conjunct": 4, "class": "auth", "cmd": "/tmp/tm04_parent_probe.py P1", "expected": "a caller authorised by the docstring's second path (Authorization: Bearer <key>, no 'key' field in the frame) is admitted and streams", "observed": "tokens 0, error 'bad_key', close 1008 -- getattr(ws,'request_headers',None) is None on websockets 15.0.1's default asyncio ServerConnection, so the header branch is unreachable", "result": "fail"}
profile: balanced
role: kid
scaffold_hash: c51e2962c1a2fb09
season: 2
title: "\"Raw WS relay measured: 20/20 temp-0 sha-identity through the adapter, median TTFT delta -42.7 (raw) / +5.6 ms (chat), captures == caller bytes with a positive control, cancel frees the slot\""
town: local-maxxing
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-b4ec6cfa-befe36

## Experiment

Measured the one conjunct of `hypothesis:ws-raw-zero-injection-adapter` nobody
had measured: **the WS wrapper's own transport fidelity and overhead**. The
judge pilot called `/completion` directly (HTTP), so it proved the server is
deterministic and that `--log-prompts-dir` captures caller bytes — it said
nothing about whether a `websockets` + `httpx` relay preserves that and how
much it costs. That is the falsifier that could kill the whole adapter
(`median TTFT overhead > 50 ms or tok/s ratio < 0.9`), so it is what this round
ran first.

Built, in `file_scope`:

- `extensions/agi/bin/ws_raw.py` — the minimal relay: one asyncio handler,
  bind 127.0.0.1 only, first JSON frame parsed against a per-mode ALLOWLIST
  (raw: `n_predict, temperature, seed, n_probs, stop, top_k, top_p, ...`;
  chat: `max_tokens, temperature, seed, logprobs, top_logprobs,
  chat_template_kwargs, ...`), body built from allowlisted fields only,
  chat `messages` verbatim with no system turn added, static key compared with
  `hmac.compare_digest`, one `await ws.send` per SSE event (a slow client
  throttles the relay; backpressure = cancel), client close exits the httpx
  context so the backend socket closes. Optional `key_env` names an env var
  holding the *backend's* key (read at call time, never stored) — the one
  field the cloud backend will need.
- `extensions/agi/bin/ws_raw_client.py` — stream once, or `--measure N`
  interleaved direct/adapter pairs per mode writing a JSONL row per leg.
- `extensions/agi/tests/test_ws_raw.py` — 7 tests, self-hosting its own
  llama-server on a free 184xx port, skipping if binary/GGUF absent.

Commands (CPU llama-server, Qwen3-0.6B-Q8_0, `-np 1 -c 2048 -t 4`,
`--reasoning-format none`, `--log-prompts-dir`):

```
python3 extensions/agi/bin/ws_raw.py --port 18431 --backend cpu=http://127.0.0.1:18430
WS_RAW_KEY=... python3 extensions/agi/bin/ws_raw_client.py --measure 10 \
  --out .agi/context/local-maxxing/ws-raw/a00-b4ec6cfa-overhead.jsonl
python3 -m pytest extensions/agi/tests/test_ws_raw.py -q     # 7 passed in 149.58s
```

Results.

| conjunct | threshold | measured |
|---|---|---|
| sha identity, temp 0 / seed 7 / cache_prompt false | 20/20 equal to direct | 20/20: raw all `a64dff26583b5242` (10 direct + 10 adapter), chat all `15b8aa4a45a08206` |
| median TTFT overhead, interleaved pairs | <= 50 ms | raw **-42.7 ms**, chat **+5.6 ms** |
| median tok/s ratio | >= 0.9 | raw **1.012**, chat **1.128** |
| capture == caller bytes (raw) / `/apply-template` render (chat) | byte-equal | raw capture = the 25 B prompt; chat capture = the 75 B template render |
| harness markers in capture, positive-controlled | 0 hits, control >= 1 | 0 hits; `brief.py head --tier kid` hits markers (control passes) |
| client close mid-stream -> `/slots[0].is_processing` false | <= 2 s | yes, within 2 s |
| unknown param (`system_prompt`) | `{error}` + close 1008 | close 1008, error names the key |
| wrong static key | close 1008 | close 1008, `bad_key` |
| `import ws_raw` pulls no harness module | empty diff | empty (no brief/dispatch/adapters/hooks/cli) |

Tenancy, as the ceiling demanded: every row carries loadavg (l1 3.81 -> 6.95
over the run) and MemAvailable; no interleaved pair had its two halves
differing by > 1.0 in l1, so no row needed a re-run.

**Verdict: proved for this conjunct.** Falsifier 3 (transport overhead) is
disproved on this box: the relay's median TTFT delta is *negative* in raw mode
and single-digit ms in chat mode, and the tok/s ratio is at or above 1.0 — the
wrapper is inside the noise floor of a loaded 4-core box, not a tax on it. The
`--log-prompts-dir` captures through the adapter are caller bytes exactly,
which is the zero-injection witness the hypothesis asked for, reproduced with
the positive control that makes the grep mean something.

Not measured here, and still open in the hypothesis: the GPU backend
(`:18080` is not listening — BLOCKED, not faked), `n_probs`/`top_logprobs`
carriage and the 48/48 argmax==token check, the `sys.modules` diff on a
long-lived adapter process, and the `USAGE.md`. Those are Kids B and C.

## Evidence

- `.agi/context/local-maxxing/ws-raw/a00-b4ec6cfa-overhead.jsonl` — 40 rows
  (raw + chat, 10 interleaved pairs each, direct + adapter leg), each row
  `{mode, pair, leg, ttft_ms, tokens, tok_s, sha256, text, loadavg,
  mem_avail_kb}`. Verdict line: `[raw] pairs=10 median_ttft_delta_ms=-42.7
  median_tok_s_ratio=1.012 sha_sets_equal=True`, `[chat] pairs=10
  median_ttft_delta_ms=5.6 median_tok_s_ratio=1.128 sha_sets_equal=True`.
- `extensions/agi/tests/test_ws_raw.py` — `7 passed in 149.58s` run alone
  under `AGI_TIER=kid`, `-p no:cacheprovider`.
- The capture files are deleted and re-made by the test; the manual smoke run
  left `/tmp/a00cap` with `25 B` raw captures equal to the prompt and `75 B`
  chat captures equal to the template render.

Trap hit while building, recorded because the next kid will hit it:
`_free_port()` asked twice returned the *same* port (the first is still free
until the server binds), and the guard `while ws_port != llama_port` spun
forever — pytest hung with no output and only `-o faulthandler_timeout=45`
would show it. One scan returning n distinct ports fixes it.

## Agent Notes
Built the raw relay (bin/ws_raw.py + ws_raw_client.py + tests/test_ws_raw.py) and measured the one conjunct no prior run measured: transport fidelity/overhead of the WS wrapper. 20/20 temp-0/seed-7/cache_prompt-false streams sha-equal to direct httpx (raw all a64dff26583b5242, chat all 15b8aa4a45a08206); median TTFT delta -42.7 ms raw / +5.6 ms chat (<=50); tok/s ratio 1.012 / 1.128 (>=0.9) on 10 interleaved pairs per mode with loadavg on every row; --log-prompts-dir captures byte-equal to caller prompt / apply-template render with 0 marker hits vs a passing positive control; cancel frees the slot <2 s; allowlist + key close 1008; import purity holds. 7/7 tests green run alone. GPU backend still BLOCKED (:18080 not listening).

Parent review 2026-09-16: independently reproduced the allowlist gate (P2 unknown param, P3 unknown top-level key -> 1008), the zero-injection witness (P4: capture 25 B byte-equal to the caller prompt through the live adapter), and temp0 sha identity vs direct (P5: a64dff26583b5242 both). P1 falsified the docstring's Authorization-header auth path: ws.request_headers does not exist on websockets 15.0.1 ServerConnection, so header-only callers get bad_key/1008. Verdict demoted proved -> inconclusive_lean_proved:75; the header defect is handed to Kid B as a required fix (use ws.request.headers or drop the claim from the docstring, plus a regression test). Overhead medians and the 20-pair suite were not re-run by me; their JSONL arithmetic was checked independently.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review 2026-09-16 of a00-b4ec6cfa's node. Instruction: "One negative probe per claim conjunct, run by YOU ... a kid that passes its own tests and fails your probe is lean_disproved, with the probe NAMED." I read the changed bytes (extensions/agi/bin/ws_raw.py, ws_raw_client.py, tests/test_ws_raw.py) and ran an independent probe battery in /tmp/tm04_parent_probe.py against a live llama-server on 184xx with --log-prompts-dir. WHAT THE MACHINE DOES: the allowlist gate holds (P2/P3 both close 1008 and name the offending key), the adapter's bytes reach the server's --log-prompts-dir as exactly the caller's 25 B prompt (P4), and direct-vs-adapter sha identity holds at temp0/seed7 (P5, a64dff26583b5242 both sides) -- so the kid's transport conjunct is reproduced from outside. NEAR MISS: I did not re-run the kid's own suite and I did not redo the 20 pairs or the overhead medians; I reproduced one leg of each conjunct and verified the kid's JSONL arithmetic independently (raw median -42.7 ms / ratio 1.012, chat +5.6 ms / 1.128, sha sets equal, all loadavg deltas < 1.0). DEVIATION FROM A FULL PROVED: probe P1 falsifies a surface the changed bytes advertise in their own docstring -- "static key in the first frame or Authorization header". On websockets 15.0.1 websockets.serve is the asyncio implementation, whose ServerConnection has no .request_headers (dir() check: False), so _auth_key returns None and the caller is refused bad_key/1008. Header-only auth is dead. The hypothesis's testable_claim names only the first-frame static key, which is why this is 75 and not lean_disproved: every conjunct the kid enumerated held under my probes, and the dead surface is one the artifact's prose promises rather than one the claim tests. It must not ride, so the verdict is demoted and the defect is carried into Kid B's brief as a required fix.
<!-- THOUGHT:END -->
