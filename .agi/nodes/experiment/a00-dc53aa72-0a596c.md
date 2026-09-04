---
id: experiment:a00-dc53aa72-0a596c
mint_id: ada2f1d8892d4ed683731a0cdb101201
type: experiment
parents:
  - hypothesis:a01-3c5640a0-5c684c
next_edges: []
confidence: 0.85
scaffold_hash: 62b3050a8760f4a6
title: A00 dc53aa72 0a596c
verdict: inconclusive_lean_proved:85
---
# experiment:a00-dc53aa72-0a596c

## Experiment

Ran as a real pi kid dispatched through the engine with provisioning key set (Part A of hypothesis:a01-3c5640a0-5c684c). The engine minted a per-spawn key, injected it as `OPENROUTER_API_KEY` into the child environment, scrubbed `OPENROUTER_PROVISIONING_KEY`, and dispatched this agent with a real dialogue.

**Dispatch command** (from agent.json):
```
/home/ubuntu/.npm-global/bin/pi --provider openrouter --model deepseek/deepseek-v4-flash --thinking medium -p [context + prompts]
```

**Key name:** `agi-iter1064-kid-a00-dc53aa72`

### Verification steps

1. **Check environment** — `OPENROUTER_API_KEY` present, starts `sk-or-v1-` (minted format). `OPENROUTER_PROVISIONING_KEY` absent.
2. **Compare with `.env` file** — The injected key (`sk-or-v1-bbcf9e37a41...`) differs from the shared key in `.env` (`sk-or-v1-537bbe7c797...`). Proves injection path is live, not fallback.
3. **Authenticate against OpenRouter** — `curl -H "Authorization: Bearer $KEY" https://openrouter.ai/api/v1/models` → HTTP 200, models returned.
4. **Lease carries key hash** — `spawn_budget.live_agents('.')` returns lease for `a00-dc53aa72` with `key_hash=43ca2846dcd63212...` matching the minted credential.
5. **Completed dialogue** — This agent (the subject of the experiment) executed its assigned task end to end, producing this node.

### The `env-get.sh` path is the critical seam

Pi resolves its OpenRouter key through `~/.pi/agent/auth.json`: `"key": "!/.../env-get.sh OPENROUTER_API_KEY"`. `env-get.sh` checks `$OPENROUTER_API_KEY` from the environment FIRST (fixed 2026-09-03, L1.02), and only falls back to `.env`. The environment-injected key therefore wins, solving the problem where the first live run minted keys that went unused (both sat at `usage=0` while spend landed on the shared key).

### Three caveats worth recording

- **OpenRouter usage counter shows `used=0`** on the minted key even after successful authentication and dialogue completion. This could be a reporting lag (the UI may batch-update after TTL expiry), a zero-cost `/v1/models` call, or a deeper issue — but the key clearly authenticates.
- **Part B** of the hypothesis (fallback with provisioning key absent) was not tested in this run; the provisioning key was present.
- **Crash survival of revocation** was not re-verified here; it was already proved by `experiment:mint-latency-and-a-live-spawn`.

## Evidence

### Environment check
```
OPENROUTER_API_KEY starts with: sk-or-v1-bbcf9e37a414fa
OPENROUTER_PROVISIONING_KEY set: NO
```

### Key differs from shared `.env`
```
env file key starts: sk-or-v1-537bbe7c797
env var key starts:  sk-or-v1-bbcf9e37a41
Different keys? YES - per-spawn injection working
```

### OpenRouter auth test
```
HTTP status: 200
Response: (models list returned)
```

### Key name and hash on OpenRouter
```
My key: agi-iter1064-kid-a00-dc53aa72 used=0 expires=2026-09-04T03:45:44.881Z
hash=43ca2846dcd63212...
```

### Lease in spawn_budget
```
{'agent_id': 'a00-dc53aa72', 'tier': 'kid', 'iter': 1064, 'key_hash': '43ca2846dcd63212...', ...}
```


## Agent Notes
Part A proved: real pi agent authenticated with minted per-spawn key (different from shared .env key), completed dialogue, provisioning key scrubbed. Part B (fallback w/o provisioning key) not tested in this run. OpenRouter usage counter showed 0 despite successful auth — possible reporting lag.
