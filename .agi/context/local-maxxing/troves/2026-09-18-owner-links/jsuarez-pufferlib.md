# X-THREAD: @jsuarez — PufferLib 5.0 "train agents in under a second"
Slice X-THREADS / local-maxxing town. READ-ONLY (no key, no install, no clone). Read 2026-09-18Z.
Tag legend: MEASURED = quoted from a page/file read here; ESTIMATE = inference.

## 0. The post (pointer)
- Post: https://x.com/jsuarez/status/2099511202431021236 — @jsuarez (Joseph Suarez, MIT PhD, Neural MMO / PufferAI), created **Mon Sep 14 14:50:52 +0000 2026** (MEASURED, fxtwitter `created_at`), 161,768 views, 1,821 likes (MEASURED). JSON via `https://api.fxtwitter.com/jsuarez/status/2099511202431021236`.
- Text is a single line: "**Releasing PufferLib 5.0: Train agents in under a second**" + a 30.2 s mp4. **No card, no `urls` facets** (MEASURED — the only outbound is the video; the artifact is named in the text).

## 1. What is claimed (MEASURED, verbatim)
- "Releasing PufferLib 5.0: **Train agents in under a second**" (post, 2026-09-14).
- README (github.com/PufferAI/PufferLib, fetched 2026-09-18): "a fast and sane reinforcement learning library that can **train tiny, super-human models in seconds**" (MEASURED).
- Prior public milestones (MEASURED, puffer.ai/blog index): PufferLib 2.0 "Reinforcement Learning at **1M sps**"; 3.0 "Better Reinforcement Learning at **4M sps**"; 4.0 engineering/recurrent-network posts.

## 2. The artifact it points to
- Repo: **`github.com/PufferAI/PufferLib`** (created 2022-09-17; pushed 2026-09-13; **6,451 stars**; ~926 MB, API-viewed not cloned). MEASURED, GitHub API 2026-09-18.
- Release: **tag `5.0-experiments`, name "5.0 Experiments", published 2026-09-13T00:26:10Z** (MEASURED, GitHub releases API). Assets: `puffer5_experiments.zip` (10 downloads), `puffer5_models.zip` (50 downloads).
- Release body (MEASURED, verbatim): "Experiments and pretrained models for PufferLib 5.0. Unzip puffer5_experiments -> copy env folders to logs/ … We ship demo files for a few of the coolest environments. **You can reproduce the rest from scratch quite easily on a single GPU.** The file name tells you the `--policy.hidden_size` and `--policy.num_layers` to use for eval."
- Docs: **https://puffer.ai/** (blog index + citation). Papers: arXiv 2406.12905 (PufferLib, 2024); RLJ vol 6 pp.1378–1388 (PufferLib 2.0, 2025). MEASURED.

## 3. The headline number (and what is NOT verified)
- Headline: "**under a second**" (post + video only). **The release body does NOT state a per-environment wall-clock** and the repo README says "in seconds" (plural) — so the "under a second" figure is **MEASURED as a post claim, UNVERIFIED as a repo number**. Flag: video-only evidence; treat as ESTIMATE-class until reproduced.
- Release ships **pretrained 5.0 models** (`puffer5_models.zip`, 50 downloads) — so the "under a second" may mean *eval/verify of a shipped model*, not *training from scratch* (ESTIMATE — the post says "Train", the release body leans "eval/reproduce").
- **GPU dependency (MEASURED, release body):** "reproduce the rest from scratch quite easily on a **single GPU**." This is the key caveat for a GPU-less town.
- Config surface is large: ~90 `config/*.ini` envs (breakout, cartpole, craftax, nmmo3, pokerl-ish, drone, chess, go…), including a `config/minimal.ini` and `config/benchmark.ini` (MEASURED, repo tree).

## 4. Town chain it touches
- **GPU-less compute** (primary): the interesting test is whether "tiny super-human models in seconds" survives on **CPU-only** 4-core ARM. The release body explicitly assumes a GPU, so this is a direct falsifier target.
- **Local inference / lighter hardware** (secondary): tiny policies (hidden_size/num_layers encoded in filenames) are exactly "absolutely tiny models".
- **Two tiny models cooperating** (tertiary): PufferLib ships many env-specific tiny policies; a **policy-pool/selector** (CARBS, 0.4 policy store) is a cooperating-experts mechanism worth mining (MEASURED, puffer.ai credits "CARBS integration", "0.4 policy pool/store/selector").
- Not typed decisions, not oscillators — this thread is compute/RL, not the decision or oscillator chains.

## 5. Hypothesis seeds (smallest experiment)
- **P1 (ARM4C, 4-core arm-cloud, 23 GB, no GPU) — CPU-only breakout.** Shallow-clone PufferLib, `puffer train breakout` with CPU vectorisation (`--vec.num-threads 4`), no CUDA; measure wall-clock to a scoring agent and compare against "under a second". Est cost **$0.00**, **~30–60 min**. Falsifier: CPU-only never reaches the claim (release body predicts this).
- **P2 (THIS box) — eval-only timing.** Load a shipped 5.0 tiny policy (`puffer5_models.zip`) and time one eval/rollout pass on CPU. Isolates "under a second" as *eval* vs *train*. Est cost **$0.00**, **~20 min**.
- **P3 (local-town, ssh alias, 8 GB GPU + 15 GB RAM) — GPU repro of the 5.0 claim.** `puffer train breakout` on the local-town GPU; measure seconds-to-train and peak VRAM. Est cost **$0.00** (own box), **~30–45 min**. Camber XS (24 GB) NOT needed.
- All seeds are $0: PufferLib is free/open-source; no paid API anywhere in this thread.

## 6. Open questions
- Exact per-env "under a second" workload is video-only — no repo number, no benchmark file read here (MEASURED absence).
- "Train agents" vs "eval shipped models": the release body's "reproduce … on a single GPU" and shipped `puffer5_models.zip` make this ambiguous. Resolve before citing.
- Repo is 926 MB; a shallow clone is the max allowed and was NOT performed here (API view only).
