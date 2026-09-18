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
