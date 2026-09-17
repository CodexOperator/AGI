# Camber Cloud — XS / 24 GB GPU price quote (conjunct 6)

Quoted 2026-09-16 from the public pricing page; captured with `curl -sL` and parsed.

## Source
- https://www.cambercloud.com/pricing — accessed 2026-09-16
- GPU model crosscheck: https://docs.cambercloud.com/docs/nodes-pricing/ — accessed 2026-09-16
- Credit-to-USD: AWS Marketplace "Camber Research Cloud"
  https://aws.amazon.com/marketplace/pp/prodview-oeuojqxhlhrh6 — accessed 2026-09-16

## On-Demand GPUs (verbatim from cambercloud.com/pricing, GPU section)

> Some engines support GPU-accelerated execution, which you can enable by setting the
> `with_gpu` attribute to True.
> Engine size | Cost in credits per hour | Number of CPU cores | System Memory (GB)
> XSMALL | 3 | 5 | 50
> medium | 12 | 25 | 220
> large | 24 | 50 | 440

Engine **XSMALL** = **1 × NVIDIA L4 GPU, 24 GB VRAM** (per docs nodes-pricing, On-Demand GPU
XSMALL = 1 L4; the L4 is a 24 GB card), 5 CPU cores, 50 GB system RAM.

**Cost: 3 credits/hour.** AWS Marketplace lists Camber Usage Credits at **$1.00 each**
("Camber Usage Credits ... $1.00"), i.e. billing granularity is **per-hour credit
consumption**, pay-as-you-go.

## The "XS 24 GB" mapping (honest note)

The owner's ceiling says "Camber XS 24 GB". The public pricing page has **no literal "XS"
tier** — the On-Demand GPU engine sizes are **XSMALL / medium / large**. The L4-24 GB engine
is **XSMALL**. So "XS 24 GB" ≈ Camber On-Demand **XSMALL (1× L4, 24 GB)**.

## Round-2 (2-epoch QLoRA) estimate

Corpus (this build): **sum ≈ 1,798,090 tokens** (tiktoken cl100k_base proxy, ESTIMATE — the
Qwen3.5 tokenizer is not shipped offline here).
Two epochs → ≈ **3,596,180 tokens**.
Assumed QLoRA throughput on a 1× L4 (24 GB) for a small kid-size model: **~1,500 tok/s**
(ESTIMATE, low-end for training).
Time ≈ 3.596e6 / 1500 ≈ **2,400 s ≈ 0.67 h** on the XSMALL engine.
Cost ≈ 0.67 h × 3 credits/h × $1.00 ≈ **~$2.00**, well inside the 3 GPU-hours/month budget.

## Falsifier check
The page DOES show a 24 GB (L4) engine and a price (3 credits/h ⇒ ~$3/h via the $1
credit), so the round-2 ask has a number. Caveat: the tier is named "XSMALL" not "XS", and
the USD figure rests on the AWS-Marketplace 1-credit = $1.00 conversion, which is the
closest public $-denomination Camber publishes.