# ws_raw — raw token stream, zero injection

WS_RAW_KEY=secret \                       # static key; caller sends it as frame `key` or `Authorization: Bearer`
  ~/.venv-lm/bin/python extensions/agi/bin/ws_raw.py --port 18431 \
  --backend cpu=http://127.0.0.1:18430 \
  --backend gpu=http://127.0.0.1:18080 \
  --backend cpu2=http://127.0.0.1:18440

One frame (JSON), then one ws frame back per SSE event:
  {"mode":"raw","backend":"cpu","key":"secret","prompt":"Count to twenty.",
   "params":{"temperature":0,"seed":7,"n_predict":32,"n_probs":5}}
  {"mode":"chat","backend":"gpu","key":"secret","key_env":"LOCAL_TOWN_KEY",
   "messages":[{"role":"user","content":"hi"}],"params":{"max_tokens":32,"model":"Qwen3.5-9B-Q4_K_M"}}

Frames: `{"token":...}` / `{"reasoning":...}` / `{"token":"","done":true,...}` / `{"error":...,"close":1008}`.
GPU backend (`--jinja`) thinks first: a content-only caller gets 0 content frames; consume `{"reasoning":...}` (measured direct == adapter, 16/16 reasoning, sha e3b0c442).
Cancel = close the socket; the backend slot frees within 2 s. Key: frame `key` or `Authorization: Bearer <key>` on the handshake (websockets 15: ws.request.headers).
Unknown top-level key or non-allowlisted param -> `{error}` + close 1008. `chat_template_kwargs` is the caller's (it renders, captured).
Backends: any `--backend name=base_url`; gpu rides the ORDER-4 tunnel `127.0.0.1:18080 -> local-town:8080`
(`systemctl --user status local-town-tunnel`), base_url WITHOUT `/v1` (the adapter appends the endpoint).
