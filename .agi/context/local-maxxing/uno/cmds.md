# UNO step 1 — CPU-XSMALL billing-granularity probe: every command, verbatim

Run 2026-09-18 ~06:44–06:54Z by kid a00-8614c12a (parent = hypothesis:lm-uno-diffusion-draft-on-l4).
Box aliases only (ARM4C). No host names, GPU model names or CPU model names recorded.
The API key VALUE never appears below — only the env var names.

## 0. Key present? (step 1 gate)
```
[ -n "$CAMBER_CLOUD_API_KEY" ] && echo set
# -> set
```
Key IS in the dispatch env. Proceeded.

## 1. Install the Camber CLI (none was present; `which camber` empty)
```
curl -sL https://cli.cambercloud.com/install-v2.sh -o /tmp/camber-install.sh
bash /tmp/camber-install.sh          # installs to ~/.camber/bin, no sudo
~/.camber/bin/camber version
# -> Camber 1.0.40 - 2118c7a
```

## 2. Auth — name bridge
The CLI reads `CAMBER_API_KEY`; the project key is `CAMBER_CLOUD_API_KEY`
(doc:config:secrets). Bridged in the shell, not by changing the key:
```
export PATH="$HOME/.camber/bin:$PATH"
export CAMBER_API_KEY="$CAMBER_CLOUD_API_KEY"
camber me
# -> Email shaelaran@gfl.guide / Username jsualsiialls / Stash stash://jsualsiialls/
```

## 3. Help (exact flags, never guessed)
```
camber --help
camber job --help
camber job create --help
camber job get --help
camber job list --help
camber team --help
```
`job create` flags: `--cmd --engine --gpu --num-nodes --path --size` (size one of
xxsmall,xsmall,small,medium,large). `job get/list` take `--output json`. NO billing flag.

## 4. Baseline
```
camber job list --output json       # -> total 0 (clean account)
camber team list --output json      # -> Worthy Default Team (1 team)
camber me --output json             # -> no credit/balance field
```

## 5. The one job (CPU XSMALL, one-shot, NOT GPU, NOT interactive)
```
yes | camber job create --cmd "sleep 300 && echo camber-probe-ok" \
  --engine base --size xsmall --num-nodes 1 --path "stash://jsualsiialls/"
# -> Job created successfully. Status: Submitted. Job ID: 27649
```
`--gpu` omitted (=false). `--size xsmall` = CPU XSMALL (0.32 credits/h per docs).

## 6. Observe lifecycle
```
camber job get 27649 --output json
camber job get 27649
camber job logs 27649
camber job list --output json
```
Final object (06:52Z):
```
created_at  2026-09-18T06:45:25Z
started_at  2026-09-18T06:47:08Z   (RUNNING begins)
finished_at 2026-09-18T06:52:26Z
job_status  COMPLETED
```
RUNNING wall = finished - started = **318 s**. Pending spin-up = 103 s (not billed per docs).

## 7. Billing hunt — CLI/SDK has NO credits surface
Every path below 404s (`{"message":"Not Found"}`) or 401s with the account key:
```
for p in credits user/credits v1/credits me user teams billing usage account \
         jobs/27649 v1/jobs/27649 api/jobs/27649 api/v1/jobs/27649 \
         v2/jobs/27649 openapi.json docs swagger.json; do
  curl -s -o /tmp/po -w '%{http_code}\n' -H "authorization: Bearer $CAMBER_CLOUD_API_KEY" \
    "https://api-v2.cambercloud.com/$p"; done
```

## 8. Real API base route found via Go HTTP/2 debug
```
GODEBUG=http2debug=2 camber job get 27649 2>&1 | grep ':path'
# -> :path = "/api/cli/jobs/27649",  authorization: Bearer <key>
curl -s -H "authorization: Bearer $CAMBER_CLOUD_API_KEY" \
  https://api-v2.cambercloud.com/api/cli/jobs/27649
curl -s -H "authorization: Bearer $CAMBER_CLOUD_API_KEY" \
  https://api-v2.cambercloud.com/api/cli/me
```
CLI API prefix is `/api/cli/`. `me` and `jobs/{id}` return no credit/cost field.
`/api/cli/credits`, `/api/cli/usage`, `/api/cli/billing`, `/api/cli/account`,
`/api/cli/teams/{id}/usage` all 404.

## 9. Where credits DO live (web app, not the key)
Scraped the web-app JS bundles (`app.cambercloud.com/assets/*.js`):
- page routes `/personal-usage`, `/team-management/${id}/usage`
- generated clients call `user/teams`, `teams/subscription`
- host is the SAME `api-v2.cambercloud.com` but the prefix is `/api/`:
```
curl -s -H "authorization: Bearer $CAMBER_CLOUD_API_KEY" \
  https://api-v2.cambercloud.com/api/user/teams
# -> 401 {"message":"unauthorized - invalid token"}
```
The `/api/*` usage surface requires a Clerk browser session token, NOT the
Camber API key. So per-job credits are **not readable with this account key**.

## 10. Teardown — verified, not assumed
```
camber job list --output json   # -> total 1, the single job 27649, status COMPLETED
```
No running job, no GPU job, no interactive box. Nothing left RUNNING.

## Finding
Job lifecycle + wall-clock are readable via CLI. Credits charged are NOT. The
0.03 USD cap was respected (job ran, one-shot, torn down). Billing granularity
is therefore UNDETERMINED from this key; needs the owner/parent to read the
Teams→Usage tab once.

# UNO step 2 — one-shot GPU XSMALL (job 27689): commands and result

Run 2026-09-18 13:24-13:32Z by kid a00-cb88d326. Aliases only; no host/IP/GPU model names.
The whole remote script was base64'd into the single `--cmd`, so nothing was uploaded anywhere.

## Submit (one job, one-shot, no interactive box)
```
export CAMBER_API_KEY="$CAMBER_CLOUD_API_KEY"        # step-1 auth bridge
B64=$(base64 -w0 work.sh)                            # script incl. run_arm.py + prompts.jsonl
yes | camber job create --cmd "echo $B64 | base64 -d > \$HOME/uno-work.sh && timeout -s TERM 2820 bash \$HOME/uno-work.sh" \
  --engine base --gpu --size xsmall --num-nodes 1 --path "stash://jsualsiialls/"
# -> Job 27689
```
## Inside (on the rental, exact)
```
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv $HOME/uno-work/dlvenv --python 3.10 && uv pip install --python $HOME/uno-work/dlvenv/bin/python "huggingface-hub>=0.34,<1" hf_transfer
# download in background:
HF_HUB_ENABLE_HF_TRANSFER=1 snapshot_download("s-sahoo/uno-qwen3-8B", local_dir=.../uno-bundle, max_workers=8)
uv venv $HOME/uno-work/venv --python 3.10
uv pip install --python $PYBIN torch==2.11.0 --index-url https://download.pytorch.org/whl/cu128
uv pip install --python $PYBIN 'https://github.com/lesj0610/flash-attention/releases/download/v2.8.3-cu12-torch2.11/flash_attn-2.8.3%2Bcu12torch2.11cxx11abiTRUE-cp310-cp310-linux_x86_64.whl'
uv pip install --python $PYBIN transformers==4.55.0 safetensors==0.5.3 numpy==1.26.4 "tqdm>=4.67,<5" "xxhash>=3.5,<4" triton==3.6.0 "huggingface-hub>=0.34,<1"
git clone --depth 1 https://github.com/ifm-ai/uno $HOME/uno-work/uno-src && uv pip install --python $PYBIN -e $HOME/uno-work/uno-src --no-deps
$PYBIN run_arm.py --bundle .../uno-bundle --prompts .../prompts.jsonl --out .../rows.jsonl
```
## Timings observed (job 27689)
```
MARK nproc=8 mem_kb=31623604 ; disk 100G 23% used ; python3 = 3.11.7 (uv fetched 3.10.12)
MARK torch_ready 54s ; fa2_ready 69s ; deps_ready 73s ; cuda True dev_mem_MiB 22563
MARK repo_ready 134s ; download_done 154s (16 GiB bundle)
MARK arm_base_FAILED -> torch.OutOfMemoryError during load_model: 21.69 GiB allocated of 22.03 GiB (96 MiB MLP weight copy failed)
MARK arm_uno_FAILED -> ValueError: trying to initialize the default process group twice!
job wall started->finished = 251 s; created->finished = 483 s
```
## Teardown
```
camber job list --output json   # -> no RUNNING job (27689 COMPLETED; 27649 step-1 COMPLETED)
```

# UNO retry — one-shot GPU XSMALL (job 27711): commands and result

Run 2026-09-18 17:22:19–17:26:07Z by kid a00-79309500. Aliases only; no host/IP/GPU model names.
Whole remote script base64'd into one `--cmd`; nothing uploaded to any shared place.

## Submit (ONE job, one-shot, internal timeout 840 s)
```
export CAMBER_API_KEY="$CAMBER_CLOUD_API_KEY"
B64=$(base64 -w0 work.sh)
yes | camber job create --cmd "echo $B64 | base64 -d > \$HOME/uno-work.sh && timeout -s TERM 840 bash \$HOME/uno-work.sh" \
  --engine base --gpu --size xsmall --num-nodes 1 --path "stash://jsualsiialls/"
# -> Job 27711
```
## Fixes this round (vs job 27689)
- ONE subprocess per arm (`run_arm.py` per arm), so a failed arm cannot poison the next.
- `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`; `max_model_len 4096`, `max_num_batched_tokens 1024`.
- PATCH `nano_vllm_uno/engine/model_runner.py`: wrap `load_model` with `torch.set_default_device("cpu")` then restore `"cuda"`.
- Always-fits fallback arm downloaded: `IFM/K2-Horizon-0.9B` + `IFM/K2-Horizon-0.9B-Uno`.
## Timings observed
```
MARK torch_ready 52s ; fa2_ready 68s ; deps_ready 71s ; repo_ready 126s ; patch_applied
MARK download_exit 0 158s ; 8B 136s ; K2 base 16s ; K2 Uno 3s
MARK base8 weight_load_device cpu pre_alloc_gib=15.28 ; weight_load_done alloc_gib=15.28 peak_gib=15.28
MARK k2base weight_load_done alloc_gib=2.04 peak_gib=2.04
```
The 8B base OOM is FIXED: peak 15.28 GiB (was 21.69 of 22.03 GiB in job 27689).
## Where it stopped
Both arms died in `ModelRunner.warmup_model` -> `@torch.compile` RMSNorm -> inductor -> triton builds
`cuda_utils.c` and fails: `/usr/include/python3.10/Python.h: No such file or directory`.
The `engine=base` image has no Python 3.10 headers; uv's 3.10 lives under `~/.local/share/uv/python`.
```
MARK base8_exit 1 s=34 ; MARK k2base_exit 1 s=44
MARK nvsmi_max_mib 15886
```
No token, no METRIC tok_s, no IDENT — rows null, never fabricated.
## Teardown
```
camber job list --output json   # -> total 3, running [] (27649, 27689, 27711 all COMPLETED)
```
## Next-round one-liner
`export C_INCLUDE_PATH="$(dirname "$(find $HOME/.local/share/uv/python -name Python.h | head -1)")"`
before the arms; then the same job returns base-vs-Uno tok/s and the identical check.
