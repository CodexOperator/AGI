# Trove — Camber Cloud XS slice (camber-xs)

Read date: 2026-09-18 (UTC). READ-ONLY. All figures MEASURED (quoted from page) unless marked ESTIMATE.
Anonymization: our boxes = ARM4C / GPU2070S / CPU8G. No host names/IPs/key ids recorded.

## 1. The XS GPU node — Camber "XSMALL" with GPU (owner's "24 GB VRAM" claim VERIFIED)

Source: https://docs.cambercloud.com/docs/nodes-pricing/ (page "Last updated: Sep 25, 2025"), read 2026-09-18.
Quoted table, section "GPU Node Sizes → On-demand GPUs":

| Node size | # L4 GPUs | CPU cores | System Memory (GB) | credits/hr |
|---|---|---|---|---|
| **XSMALL** | **1** | **8** | **32** | **1.5** |
| MEDIUM | 4 | 48 | 192 | 6 |
| LARGE | 8 | 192 | 768 | 12 |

- MEASURED: GPU model = **NVIDIA L4**. Source: https://docs.cambercloud.com/docs/compute/ ("Last updated: Feb 18, 2026"): "Available GPU: NVIDIA L4 (24GB VRAM)".
- MEASURED: VRAM = **24 GB** per L4 → owner's "24 GB stated" is CORRECT for XSMALL (1 GPU).
- MEASURED: "**1 Camber Credit equals 1 U.S. dollar.**" → XSMALL GPU = **$1.50/hr**.
- MEASURED: "Credits are used when a [job status] is `RUNNING`" (nodes-pricing).
- ESTIMATE (arithmetic): $1.50/hr ÷ 3600 s = $0.0004167/s; ÷60 = $0.025/min.
- **Next size up = MEDIUM**: 4× L4 (96 GB VRAM total), 48 cores, 192 GB, **$6.00/hr**. ESTIMATE: $6/1.5 = exactly **4×** XSMALL price for 4× GPU / 6× cores / 6× RAM. Per-GPU price flat at $1.50/GPU-hr across XSMALL/MEDIUM/LARGE (12/8 = 1.5) → no bulk discount at on-demand tier.

## 2. CPU node sizes (same page) — for arithmetic / fallback

Source: https://docs.cambercloud.com/docs/nodes-pricing/ ("CPU Node Sizes").
| Size | cores | RAM GB | credits/hr |
|---|---|---|---|
| XMICRO | 1 | 4 | 0.04 |
| MICRO | 2 | 8 | 0.08 |
| XXSMALL | 4 | 16 | 0.16 |
| XSMALL | 8 | 32 | 0.32 |
| SMALL | 16 | 64 | 0.64 |
| MEDIUM | 32 | 128 | 1.28 |
| LARGE | 64 | 256 | 2.56 |

- MEASURED: a GPU XSMALL costs 1.5 cr/hr vs CPU XSMALL 0.32 cr/hr → ESTIMATE: GPU premium ≈ **$1.18/hr** over the same-core CPU node.
- CAUTION: a second, DIFFERENT node table exists on the marketing page (see §4) — the docs table above is the authoritative/dated one.

## 3. Billing granularity, free credits, storage

- MEASURED: "Each user starts with 100 free Camber credits when they sign up for the free trial." (nodes-pricing) = ESTIMATE **$100**.
- MEASURED: billed while job `RUNNING` (nodes-pricing) → idle/queued time is NOT billed. Granularity unit NOT stated on page (see §5 open).
- MEASURED: Object storage via Stash: "1 TB | 23" credits/month (nodes-pricing) = ESTIMATE $23/TB/month.
- MEASURED: Free plan $0; Pro $20/mo ($216/yr); Team $50/seat/mo ($540/yr) — Source: https://www.cambercloud.com/pricing JSON-LD offers, read 2026-09-18.

## 4. Marketing pricing page (cambercloud.com/pricing) — CONFLICTING legacy engine table

Source: https://www.cambercloud.com/pricing, read 2026-09-18. Search-indexed text shows an engine table:
`xmicro 1cr/6GB/0.125core; MICRO 2cr/12GB/0.25; XXSMALL 4cr/24GB/0.5; XSMALL 8cr/45GB/1; SMALL 16cr/90GB/2 …`
- MEASURED (via search snippet of same URL, 2026-09-18) but NOT confirmable in page body (page is JS/Wix, curl returned only JSON-LD).
- WARNING: this table's XSMALL (8 cr/hr) contradicts docs XSMALL GPU (1.5 cr/hr) and docs CPU XSMALL (0.32 cr/hr). Treat marketing page as STALE/ambiguous; use docs/nodes-pricing for the XS slice.

## 5b. Job-level API — YES, it exists (container-job model, not just interactive box)

- MEASURED: Python SDK job submit — Source https://docs.cambercloud.com/docs/compute/ (2026-02-18):
  `job = camber.mpi.create_job(command="python train.py", node_size="SMALL", num_nodes=2, with_gpu=True)`
- MEASURED: CLI equivalent — Source search snippet of https://docs.cambercloud.com/docs/camber-cli/job/ (2026-09-18): flags `--cmd` (required), `--engine` (mesa, ... flow, gromacs ...), `--gpu`, `--num-nodes`, `--params`, `--size` (required: xxsmall, xsmall, small, medium, large, xlarge).
- MEASURED: engines expose `create_job(...)`; Nextflow engine "deployed on Kubernetes as execution platform" — Source https://docs.cambercloud.com/docs/reference/python-api/nextflow/.
- MEASURED: engines are "container technologies" / "Camber containerizes HPC compute environments" — Source AWS Marketplace listing (read 2026-09-18).
- CONCLUSION: job-level API present (SDK + CLI). A container job can be submitted non-interactively; no evidence of a plain public REST endpoint.

## 6. HPC queue variant (different SKU — 16 GB T4, NOT the 24 GB L4)

Source: search snippet of https://docs.cambercloud.com/docs/hpc/our-systems/ (read 2026-09-18):
| Queue | vCPUs | RAM | GPU | Max Instances |
|---|---|---|---|---|
| cpu-queue | 16 | 32GB | - | 20 |
| mem-queue | 16 | 128GB | - | 20 |
| gpu-queue | 16 | 64GB | 1x NVIDIA **T4 (16GB VRAM)** | 20 |
- MEASURED: also "Files stored in `/camber/home/<user>/outputs` ... automatically synchronized with your stash `./hpc-outputs`"; "Automated provisioning with home and scratch directories".
- NOTE: this is a SEPARATE HPC-cluster product line from the on-demand XSMALL L4 node. Do not conflate.

## 7. Billing risk / granularity — READ THIS BEFORE THE 3 GPU-HOUR BUDGET

- MEASURED: vendor states only "Credits are used when a job status is `RUNNING`" (nodes-pricing + pricing). **No per-second/per-minute unit is published** on any page read.
- MEASURED (real user report, GitHub issue #43, CamberCloud-Inc/community, read 2026-09-18): "6+ hours billed for ~10 minutes of use, likely due to core-scaling on a 64GB RAM instance".
- INTERPRETATION: billing may be **core-hour** based (cores × wall-time) rather than node-hour, and may round up. For the 3 GPU-hr/month cap this is the single biggest risk: an 8-core XSMALL left RUNNING accrues 8 core-hours/hr even if the GPU is idle.
- RECOMMENDATION: verify granularity with vendor before spending; always tear the node down; prefer CLI/SDK one-shot jobs over an interactive box.

## 8. Spin-up time
- MEASURED (vendor, AWS Marketplace listing): "Within minutes, individual research groups can get up and running" (cold-start wording, not a hard number).
- MEASURED (marketing https://www.cambercloud.com/research): "scale ... in seconds".
- CONCLUSION: no published hard spin-up figure. ESTIMATE for budget planning: **1–3 min** per node (unverified). Budget it: 3 GPU-hr budget loses ~2–5% to provisioning if 10 jobs at 1–3 min.

## 5. Open items (not yet found, flagged not invented)

- Billing granularity unit (per-second / per-minute / per-hour) — NOT stated on nodes-pricing. TODO next pages.
- Disk size per node, network/egress pricing — NOT on the pages read so far.
- Spin-up / provisioning minutes — vendor says "within minutes" (AWS Marketplace listing, unverified body) and "in seconds" (marketing); no hard number yet.
- Quotas / concurrency cap per account — not found.
- Image / CUDA / driver stack — not found; compute page only names L4.
