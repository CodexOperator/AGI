---
id: experiment:a00-d02302c5-573c2b
mint_id: ae562d27f5474e3a8d2aa9db3b704ef6
type: experiment
parents:
  - hypothesis:ws-raw-zero-injection-adapter
next_edges: []
confidence: 0.85
edited_by: a00-2f819956
evidence_runs:
  - experiment:a00-d02302c5-573c2b
  - experiment:a00-b4ec6cfa-befe36
loop: hypothesis:ws-raw-zero-injection-adapter@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "auth", "cmd": "/tmp/tm04_parent_probe2.py P1a/P1b", "expected": "header-only caller (Authorization: Bearer, no key field) is ADMITTED and streams; a caller with no credential at all is REFUSED bad_key/1008 -- the fix must open the promised path and not the door", "observed": "P1a tokens 16, error null; P1b tokens 0, error bad_key, close 1008", "result": "hold"}
  - {"conjunct": 2, "class": "wire", "cmd": "/tmp/tm04_probe3.py P3", "expected": "raw n_probs=5 through the adapter: every token frame carries 5 top_logprobs entries with argmax == the emitted token, and the joined sha is unchanged vs n_probs=0 through the same adapter", "observed": "40/40 token frames, entries_per_frame [5], argmax_matches_emitted 40/40, sha 3e231c1de0ad6d59 both n_probs=0 and n_probs=5 on my own run", "result": "hold"}
  - {"conjunct": 3, "class": "wire", "cmd": "/tmp/tm04_probe3.py P4", "expected": "chat with logprobs=true and top_logprobs=3: every content delta carries logprobs with 3 entries", "observed": "24/24 content deltas carry logprobs, top_logprobs_counts [3]", "result": "hold"}
  - {"conjunct": 4, "class": "wire", "cmd": "/tmp/tm04_parent_probe2.py P5", "expected": "with --backend cpu1 and --backend cpu2, one frame naming cpu2 lands ONLY on the second server's --log-prompts-dir", "observed": "cap1_delta 0, cap2_delta 1, cap2 file byte-equal to my sentinel prompt, 8 tokens streamed; unknown backend name refused 'unknown backend: nope' + 1008", "result": "hold"}
  - {"conjunct": 5, "class": "wire", "cmd": "/tmp/tm04_probe3.py P7/P7b", "expected": "the ORDER-4 GPU backend is admitted through the same adapter and a missing model field fails LOUDLY, not silently", "observed": "with model Qwen3.5-9B-Q4_K_M: admitted, error null, close null, content_frames 0 (the endpoint emits reasoning frames only); without model: 'backend 400: model name is missing from the request' passed through verbatim", "result": "hold with caveat: switch is proved, but a content-only caller receives zero tokens on this endpoint"}
  - {"conjunct": 6, "class": "gate", "cmd": "/tmp/tm04_parent_probe2.py P6", "expected": "USAGE.md exists and is <= 20 lines as the claim requires", "observed": "exists true, lines 20", "result": "hold"}
profile: balanced
role: kid
scaffold_hash: bd1700bf275c938b
season: 2
title: Header auth fixed; n_probs/top_logprobs carriage and cpu2+gpu backend switch proved
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-d02302c5-573c2b

## Experiment

Fixed the auth defect Kid A's relay shipped, then re-ran Kid C's whole
conjunct set on the built bytes. Command:
`~/.venv-lm/bin/python .agi/context/local-maxxing/ws-raw/run_kidC.py`
(two CPU llama-servers, each with its own `--log-prompts-dir`; one
`ws_raw.py` with `--backend cpu=<p1> --backend cpu2=<p2> --backend gpu=http://127.0.0.1:18080`).

| # | check | result |
|---|---|---|
| 1 | header auth, no `key` field | ADMITTED and streams (8/8 raw, 8/8 chat); zero credential still `bad_key` + 1008 |
| 2 | raw `n_probs=5` | 48/48 token frames carry 5 entries, argmax == emitted token; joined sha `a2b3547036649a62` == the same request at `n_probs=0` (both reqs) |
| 3 | chat `top_logprobs=3` | 24/24 content deltas carry `logprobs.content[0].top_logprobs` with 3 entries |
| 4 | backend switch `cpu2` | cap2 0->1 files, cap1 6->6: the request landed only on the second server's capture dir |
| 5 | GPU backend (ORDER 4) | LIVE: `127.0.0.1:18080` listens, `local-town-tunnel` active; admitted, 16 reasoning deltas / 0 content (Qwen3.5-9B thinks under `--jinja`) |
| 6 | regression test | `~/.venv-lm/bin/python -m pytest extensions/agi/tests/test_ws_raw.py -q -o faulthandler_timeout=90` -> 8 passed in 53.71 s |

## Evidence

The defect was `extensions/agi/bin/ws_raw.py` `_auth_key` reading
`ws.request_headers`: websockets 15.0.1 serves via
`websockets.asyncio.server`, whose handler gets a `ServerConnection` whose
handshake `Request` is at `ws.request` (verified: the attribute is set in
`process_event` before the handler runs). Fixed to `ws.request.headers`;
the dead branch is gone, not papered over. New test
`test_header_auth_admits_without_key_field` pins both the refusal (no
credential) and the admission (header only).

Artifacts: `.agi/context/local-maxxing/ws-raw/` — `USAGE.md` (20 lines),
`kidC_backends.md` (the table above with commands), `kidC_results.json`
(full JSON), `kidB_logprobs.jsonl` (48 per-frame rows), `run_kidC.py`
(the runner), `cap1/`, `cap2/`.

All servers killed; `pgrep -x llama-server` empty and p1/p2/ws ports
re-checked closed (`port_closed p1=True p2=True ws=True`).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review 2026-09-16 of a00-d02302c5's node. Instruction: "One negative probe per claim conjunct, run by YOU ... a kid that passes its own tests and fails your probe is lean_disproved, with the probe NAMED." I read the changed bytes in extensions/agi/bin/ws_raw.py L120-134 and confirmed the fix by mechanism, not by report: the dead branch is GONE, not shadowed -- _auth_key now reads getattr(ws,'request',None) then getattr(request,'headers',None), and the docstring's promise is reachable. WHAT THE MACHINE DOES: my probe battery (/tmp/tm04_parent_probe2.py and /tmp/tm04_probe3.py, two live CPU llama-servers on 184xx each with its own --log-prompts-dir, plus the live ORDER-4 :18080 tunnel) reproduced every claimed row from outside: header-only caller admitted with 16 tokens while a credential-less caller is refused bad_key/1008 (the fix opened the promised path and not the door); raw n_probs=5 gives 40/40 argmax==emitted with 5 entries per frame and sha unchanged vs n_probs=0 through the same adapter; chat with logprobs+top_logprobs=3 gives 24/24 deltas carrying 3 entries; a cpu2 frame lands only in the second server's capture dir (cap1 delta 0, cap2 delta 1, byte-equal to my sentinel); USAGE.md is 20 lines. NEAR MISS: my first probe run measured the wrong fields and reported false failures -- I counted len(completion_probabilities) (always 1; the five alternatives live at completion_probabilities[0].top_logprobs) and sent top_logprobs without logprobs=true, earning a server 400. I re-ran with the right fields rather than recording a defect that was mine. DEVIATION: the kid deliberately added two harness modules to the claim's import list (hmac for the constant-time compare, sys for argv) and dropped 'brief' from the seven-marker grep list; byte-equality of the capture to the caller bytes is strictly stronger than any grep, so neither costs the claim anything, but a reader diffing the lists should know. RESIDUAL, named not hidden: the GPU row is admitted but yields content_frames 0 -- this endpoint emits reasoning frames only, so a content-only caller gets an empty stream. That is why the node stays proved at 0.85 rather than 0.95, and it is handed to Kid C as its one claim (direct-vs-adapter at the same request settles whether the emptiness is the endpoint's or the adapter's).
<!-- THOUGHT:END -->

## Agent Notes
auth dead branch fixed (ws.request.headers on websockets 15.0.1) + regression test; 48/48 n_probs argmax, sha unchanged; 24/24 chat deltas carry top_logprobs; cpu2 capture isolation; GPU backend LIVE on :18080 (16 reasoning deltas)

Parent review 2026-09-16: read the bytes, then re-probed all six rows from outside. Auth fix verified live both ways (header-only admitted 16 tokens; no-credential refused bad_key/1008). n_probs 40/40 argmax==emitted with sha unchanged; chat top_logprobs 24/24 deltas; cpu2 routing proved by capture isolation; USAGE.md 20 lines. Verdict proved stands at 0.85. Residual named: the ORDER-4 GPU backend admits but streams 0 content frames (reasoning only), handed to Kid C.
