# Kid B — tunnel + engine route (core-town)

Parent: `hypothesis:gpu-local-town-openai-endpoint` · Kid B slice = "tunnel + engine route".
Everything below ran **on core-town** (`core-town-listdrop`, user `ubuntu`), 2026-09-16.
The one cross-box leg is the tunnel itself; there are no other ssh commands in this slice
(Kid A owns the box). Every command is verbatim.

## 0. Linger (measured, not assumed)

```
$ loginctl show-user ubuntu -p Linger
Linger=yes
```

Linger was already `yes`, so the `--user` unit survives logout without the extra write.

## 1. The unit file

Source of truth (committed): `.agi/context/local-maxxing/gpu/local-town-tunnel.service`.
Installed copy (box-local, uncommitted): `/home/ubuntu/.config/systemd/user/local-town-tunnel.service`.

```
[Unit]
Description=local-town SSH tunnel: core-town 127.0.0.1:18080 -> local-town 127.0.0.1:8080
Documentation=nodes/hypothesis/gpu-local-town-openai-endpoint.md
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
# Verbatim tunnel command from hypothesis:gpu-local-town-openai-endpoint (Kid B).
# ~ is NOT expanded by systemd; /home/ubuntu is the absolute form of ~.
ExecStart=/usr/bin/ssh -F /home/ubuntu/work/<keeper-dir>/ssh/config -N -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 -L 127.0.0.1:18080:127.0.0.1:8080 local-town
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
```

(The hypothesis text spells `ExecStart=ssh -F <keeper-dir>/ssh/config ...`. systemd does
not expand `~`, so the installed unit uses `/usr/bin/ssh` and `/home/ubuntu/...` — the same
command, spelled in the only form systemd accepts. This is a spelling difference in the
argv[0] and the `-F` path only; every flag is byte-identical to the hypothesis.)

## 2. Install + enable + start (idempotent)

```
$ cp /home/ubuntu/work/agi/.agi/worktrees/a00-ab5b20f7/.agi/context/local-maxxing/gpu/local-town-tunnel.service /home/ubuntu/.config/systemd/user/local-town-tunnel.service
$ systemctl --user daemon-reload
$ systemctl --user enable --now local-town-tunnel.service
Created symlink /home/ubuntu/.config/systemd/user/default.target.wants/local-town-tunnel.service → /home/ubuntu/.config/systemd/user/local-town-tunnel.service.
```

```
$ systemctl --user status local-town-tunnel.service --no-pager
● local-town-tunnel.service - local-town SSH tunnel: core-town 127.0.0.1:18080 -> local-town 127.0.0.1:8080
     Loaded: loaded (/home/ubuntu/.config/systemd/user/local-town-tunnel.service; enabled; preset: enabled)
     Active: active (running) since Wed 2026-09-16 04:21:48 EDT; 3s ago
   Main PID: 3204232 (ssh)
      Tasks: 1 (limit: 28649)
     Memory: 1.8M (peak: 1.8M)
        CPU: 72ms
     CGroup: /user.slice/user-1001.slice/user@1001.service/app.slice/local-town-tunnel.service
             └─3204232 /usr/bin/ssh -F /home/ubuntu/work/<keeper-dir>/ssh/config -N -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 -L 127.0.0.1:18080:127.0.0.1:8080 local-town

Sep 16 04:21:48 core-town-listdrop systemd[1299]: Started local-town-tunnel.service - local-town SSH tunnel: core-town 127.0.0.1:18080 -> local-town 127.0.0.1:8080.
```

## 3. The tunnel carries /v1 from core-town (no IP anywhere)

```
$ curl -s -m 10 127.0.0.1:18080/v1/models | python3 -m json.tool
{
    "data": [
        {
            "id": "Qwen3.5-9B-Q4_K_M",
            ...
            "status": {
                "value": "loaded",
                "args": ["/app/llama-server", "--host", "127.0.0.1", "--jinja", "--port", "53369", "--alias", "Qwen3.5-9B-Q4_K_M", "--fit", "on", "--model", "/models/Qwen3.5-9B-Q4_K_M.gguf", "--parallel", "2"],
                ...
            },
            "meta": {"n_ctx": 23552, "n_params": 8953803264, "size": 5669554176, "ftype": "Q4_K - Medium"}
        }
    ],
    "object": "list"
}
```

```
$ curl -s -m 60 127.0.0.1:18080/v1/chat/completions -H 'Content-Type: application/json' \
    -d '{"model":"Qwen3.5-9B-Q4_K_M","messages":[{"role":"user","content":"say OK"}],"max_tokens":8,"temperature":0}'
{"choices":[{"finish_reason":"length",...,"message":{"role":"assistant","content":"","reasoning_content":"Thinking Process:\n\n1.  **"}}],"created":1789546915,"model":"Qwen3.5-9B-Q4_K_M","system_fingerprint":"b10991-930e2fa59","object":"chat.completion","usage":{...},"timings":{"prompt_n":12,"predicted_n":8,"predicted_per_second":...}}
```

`finish_reason=length` here is only because `max_tokens=8` cut a reasoning model mid-thought;
the tunnel made a real /v1/chat/completions call and the server answered JSON. (The
finish_reason=stop case is Kid A's, box-local.)

## 4. The pi provider row

Backup first (box-local, uncommitted):

```
$ cp -a /home/ubuntu/.pi/agent/models.json /home/ubuntu/.pi/agent/models.json.bak-2026-09-16
$ ls -la /home/ubuntu/.pi/agent/models.json.bak-2026-09-16
-rw-rw-r-- 1 ubuntu ubuntu 1430 Sep  1 21:45 /home/ubuntu/.pi/agent/models.json.bak-2026-09-16
```

ONE additive provider added under `providers` in `/home/ubuntu/.pi/agent/models.json`:

```json
"local-town": {
  "baseUrl": "http://127.0.0.1:18080/v1",
  "api": "openai-completions",
  "apiKey": "local",
  "compat": {
    "supportsDeveloperRole": false,
    "supportsReasoningEffort": false
  },
  "models": [
    {
      "id": "Qwen3.5-9B-Q4_K_M",
      "name": "Qwen3.5 9B Q4_K_M (local-town)",
      "api": "openai-completions",
      "reasoning": true,
      "input": ["text"],
      "contextWindow": 23552,
      "maxTokens": 8192,
      "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0}
    }
  ]
}
```

**Schema trap (recorded because it cost a turn):** the pi `models.json` schema requires
`cost.cacheRead` (and `cacheWrite`). A `cost` with only `input`/`output` fails validation and
pi silently drops the WHOLE file — `pi --list-models local-town` printed
`Invalid models.json schema: /providers/local-town/models/0/cost: must have required
property 'cacheRead'` and listed no local-town models. The hypothesis's shorthand
"cost 0" is not schema-valid; the four cost keys must all be present.

```
$ pi --list-models local-town
provider    model              context  max-out  thinking  images
local-town  Qwen3.5-9B-Q4_K_M  23.6K    8.2K     yes       no
```

## 5. The config row

ONE additive `harnesses.pi-local` key in `.agi/config.json` (committed; all other keys
untouched):

```json
"pi-local": {
  "adapter": "pi",
  "bin": "/home/ubuntu/.npm-global/bin/pi",
  "provider": "local-town",
  "models": {
    "kid": "Qwen3.5-9B-Q4_K_M",
    "parent": "Qwen3.5-9B-Q4_K_M"
  },
  "allowed_extra": ["Qwen3.5-9B-Q4_K_M"]
}
```

## 6. Rollback (each line idempotent)

```
$ systemctl --user disable --now local-town-tunnel.service
$ rm -f /home/ubuntu/.config/systemd/user/local-town-tunnel.service
$ systemctl --user daemon-reload
$ cp -a /home/ubuntu/.pi/agent/models.json.bak-2026-09-16 /home/ubuntu/.pi/agent/models.json
# and delete the one `harnesses.pi-local` key from .agi/config.json
```
