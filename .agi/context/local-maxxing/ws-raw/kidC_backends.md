# kidC backends + logprobs evidence

Runner: `.agi/context/local-maxxing/ws-raw/run_kidC.py` (2026-09-16)
`~/.venv-lm/bin/python run_kidC.py` — two CPU llama-servers (own
`--log-prompts-dir`: cap1/cap2), one `ws_raw.py` with
`--backend cpu=<:p1> --backend cpu2=<:p2> --backend gpu=http://127.0.0.1:18080`.
Full JSON: `kidC_results.json`; per-frame rows: `kidB_logprobs.jsonl`.

| # | check | command | result |
|---|---|---|---|
| 1 | header auth, no `key` field | `stream(url, frame, {"Authorization": "Bearer sk-ws-raw-test"})` | ADMITTED, 8/8 tokens raw + 8/8 chat; no-credential still `bad_key` |
| 2 | raw `n_probs=5` | 2 x `{"mode":"raw","params":{"n_probs":5,"n_predict":24,...}}` | 48/48 token frames, 5 entries each, argmax==emitted token; sha `a2b3547036649a62` == same request `n_probs=0` (both reqs) |
| 3 | chat `top_logprobs=3` | `{"mode":"chat","params":{"logprobs":true,"top_logprobs":3}}` | 24/24 content deltas carry `logprobs.content[0].top_logprobs` (3 entries) |
| 4 | backend switch cpu2 | raw frame `"backend":"cpu2"` | cap2 files 0->1, cap1 6->6: the bytes landed on the second server's capture dir only |
| 5 | GPU backend (ORDER 4) | chat frame `"backend":"gpu","key_env":"LOCAL_TOWN_KEY"` | LIVE: `ss -ltn` shows `127.0.0.1:18080`, unit active; admitted, 16 reasoning deltas / 0 content — Qwen3.5-9B thinks under `--jinja`, so its answer arrives as `{"reasoning":...}` |
| 6 | regression test | `~/.venv-lm/bin/python -m pytest extensions/agi/tests/test_ws_raw.py -q -o faulthandler_timeout=90` | 8 passed in 53.71 s |

Defect fixed: `extensions/agi/bin/ws_raw.py` `_auth_key` read
`ws.request_headers`, which does not exist on websockets 15.0.1's asyncio
`ServerConnection`; the handshake request is at `ws.request.headers`.
Tests 1 and 6 pin it.
