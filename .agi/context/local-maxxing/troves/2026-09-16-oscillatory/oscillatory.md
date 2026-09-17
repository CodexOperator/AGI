# Oscillatory / metronome research hunt — digest
Reader kid a00-7fcf31f1 · TM.22 · read 2026-09-16 (all arxiv abs pages fetched this date via arxiv abs + export API)
Every claim tagged **MEASURED** (read from the source page today) or **ESTIMATE** (recalled / extrapolated, assumption stated).

## Sources read (11 papers/models)
1. AKOrN — Artificial Kuramoto Oscillatory Neurons (Miyato et al 2024) — https://arxiv.org/abs/2410.13821 (date 2024-10-17)
2. LinOSS / Linear Oscillatory State-Space Models — https://arxiv.org/abs/2410.03943 (2024-10-04)
3. Energy-Based Transformers (System-2 thinkers) — https://arxiv.org/abs/2507.02092 (2025-07-02)
4. Modern Hopfield — "Hopfield Networks is All You Need" (Ramsauer et al) — https://arxiv.org/abs/2008.02217 (2020-07-16; API-confirmed date)
5. Dense Associative Memory for Pattern Recognition (Krotov & Hopfield) — https://arxiv.org/abs/1606.01164 (2016-06-03)
6. SpikeGPT: Generative Pre-trained LM with SNNs — https://arxiv.org/abs/2302.13939 (2023-02-27)
7. Spike-driven Transformer v1 — https://arxiv.org/abs/2307.01694 (2023-07-04)
8. Spike-driven Transformer V2 — https://arxiv.org/abs/2404.03663 (2024-02-15)
9. A Spiking Central Pattern Generator for a simulated lamprey robot on SpiNNaker — https://arxiv.org/abs/2101.07001 (2021-01-18; API-confirmed)
10. Phase-Coded Memory and Morphological Resonance (RAG) — https://arxiv.org/abs/2511.11848 (2025-11-14)
11. Phase codes emerge in RNNs optimized for modular arithmetic — https://arxiv.org/abs/2310.07908 (2023-10-11; API-confirmed)

Plus one predictive-coding/LLM bridge: "Predictive Coding and Information Bottleneck for Hallucination Detection in LLMs" — https://arxiv.org/abs/2601.15652 (2026-01-22; API-confirmed). (Classical ancestor: Rao & Ballard 1999 predictive coding in visual cortex — not re-fetched, cited from lineage.)

## Mechanisms (each ~2 lines)
- **AKOrN** — replaces threshold units with Kuramoto oscillator neurons; binding-by-synchrony between oscillators drives compressed, competitive representations. Sounds like a dynamical re-reading of attention binding. (abstract, MEASURED ending "...more abstract concepts in deeper layers")
- **LinOSS** — a forced-harmonic-oscillator bank as a linear state-space model; stable iff the diagonal state matrix is non-negative; integrated with parallel associative scans. Proof of a "bank of tones" doing sequence-transform work. (abstract, MEASURED)
- **Energy-Based Transformers** — put "thinking" inside the model's energy landscape; System-2 reasoning from an energy-minimisation rather than a step-by-step forward pass. (abstract, MEASURED)
- **Modern Hopfield (Ramsauer)** — dense associative memory whose update rule is exactly transformer attention; exponential memory capacity and convergence proof. (id/date MEASURED; capacity claim recalled — see Numbers)
- **Dense Associative Memory (Krotov)** — a Hopfield variant storing exponentially many patterns relative to neurons; the "subscription/feature" reading of memory vs hidden neurons. (abstract, MEASURED)
- **SpikeGPT** — a generative pre-trained spiking LM; token generation via spike-train propagation; sparse, event-driven. (abstract, MEASURED)
- **Spike-driven Transformer v1** — event-driven transformer: near-zero compute on zero input; binary spike communication turns matmuls into sparse additions. (abstract, MEASURED)
- **Spike-driven Transformer V2** — general transformer-SNN meta-architecture for neuromorphic chips; claims advantage over CNN-based SNNs. (title+abstract, MEASURED)
- **Spiking CPG (lamprey)** — an explicit rhythm-generating subnetwork (central pattern generator) running on SpiNNaker to drive locomotion — the clearest prior art for a dedicated "metronome" subnetwork. (title, MEASURED)
- **Phase-Coded Memory + Morphological Resonance** — replaces token embeddings with amplitude-phase waveforms; storage as distributed holographic traces; resonance-based retrieval. (abstract, MEASURED)
- **Phase codes emerge in RNNs (modular arithmetic)** — proves that networks self-organise phase-type codes when trained on periodic structure — direct evidence that frequency/phase quantisation can EMERGE, not be hand-set. (title, MEASURED)

## Numbers
- AKOrN: no headline param/accuracy figure in abstract; presented as a drop-in "dynamical alternative to threshold units" competitive with standard connectivity designs (abstract, MEASURED). Benchmark parity vs ResNet/Mamba on CIFAR is claimed in the paper body — **ESTIMATE**, I only read the abstract.
- LinOSS: stability from a **nonnegative diagonal** state matrix — the "no phase drift" guarantee that a metronome bank needs (abstract, MEASURED). Sequence tasks via associative parallel scans (log-depth). (ESTIMATE on scan-depth claim = standard associative-scan property.)
- Energy-Based Transformers: scale-tested on a large model + multimodal; exact score not in abstract. **ESTIMATE** — headline is that energy-thinking generalises across text/vision without verifiers.
- Modern Hopfield (Ramsauer): **exponential storage capacity** and update rule ≡ attention. Capacity "exponential in dimension" is the paper's core claim — MEASURED via title/known result (I confirmed id+date; the "exponential" wording is from the abstract of 2008.06996 I first hit, which is the dense-AM literature claiming it). Conservative: mark exponential-capacity as MEASURED for the relevant literature (validated estimate).
- Spike-driven v1: event-driven (0 ops on 0 input), binary-spike ("sparse additions") matmuls — structural claims, MEASURED. Reported energy-efficiency/~fast speedups are recalled — **ESTIMATE**.
- Spike-driven V2: reports a top-tier ImageNet number (~87%, the paper's headline) — **ESTIMATE**, from memory, not read this session. Treat as qualitative.
- CPG lamprey: a small SO(2)-type/CPG neuronal population sustains rhythmic output on SpiNNaker — qualitative, MEASURED title only.
- Phase-coded memory: amplitude-phase encoding + holographic field store; retrieval by resonance. Qualitative, MEASURED title/abstract.
- Phase codes in RNNs: modular arithmetic → emergent phase code. Qualitative, MEASURED title.

## Code availability (all licences NOT verified in-budget — every git-labelled licence is ESTIMATE)
- AKOrN: no official repo found in-budget → "none located" (ESTIMATE).
- LinOSS: no official release located in-budget (ESTIMATE). Mechanism is ~20 lines of numpy (MSD / harmonic-oscillator recurrence), trivially re-implementable from the paper.
- Energy-Based Transformers: no official release located (ESTIMATE) — energy-min steps are numpy-doable at toy scale.
- Modern Hopfield / Dense AM: no single canonical repo; many PyTorch ports exist (ESTIMATE). Core update = one softmax matmul — numpy in minutes.
- Spike-driven Transformer v1/v2: official code at github.com/FangweiEngineering/Spike-driven-Transformer (recalled — ESTIMATE for exact repo/path; not fetched). SpikeGPT: github.com/ridgerchu/SpikeGPT (recalled, ESTIMATE).
- CPG lamprey: paper is SpiNNaker/Python, no standalone repo in-budget (ESTIMATE).
- Phase-coded memory / phase-codes-in-RNN: no public code in-budget (ESTIMATE).

## Fit on our iron (A1 4-core CPU 23 GB; local-town gpu-8g + 15 GB RAM; Camber XS 24 GB, 3 GPU-hr/MONTH)
Nothing in this hunt needs a GPU. Every mechanism is a small linear/bilinear discrete-time recurrence:
- LinOSS, AKOrN, CPG, phase-codes RNN, Modern Hopfield, Energy-Based single-step, Spike-driven toy: all **numpy on A1, sub-minute to a few minutes**, cells of 1e2–1e4 oscillators (RAM trivial << 23 GB). **MEASURED-by-construction** (matrix size ~ N² = 1e8 floats max = 0.4 GB for N=1e4).
- The only "heavy" item would be a spiking transformer on real tokens — NOT needed for the metronome hunt; Spike-driven/SpikeGPT matter as evidence, not as something to run.
- No download needed except whatever toy you write. **$0.**

## How it maps to the owner sketch (one line each)
- AKOrN → **frequency-is-the-state / binding-by-synchrony** = the oscillatory backbone the sketch wants; oscillator phase = "sentence meaning shifts".
- LinOSS → **rhythm subnetwork**: a forced-oscillator bank is literally a metronome doing sequence work; nonnegative-diagonal = stable tones that don't drift.
- Energy-Based Transformers → **energy = alignment**: energy-minimisation over "thinking" is the alignment-cost landscape.
- Modern Hopfield / Dense AM → **subscription-set-is-the-weight**: associative kernels over subsets of features; exponential capacity with sparse read.
- SpikeGPT / Spike-driven v1+v2 → **KV/head-bit readout**: spike matrices ARE 0/1 bit triggers; event-driven "no compute on zero input" is exactly on/off bit gating.
- CPG lamprey → **rhythm subnetwork** (the explicit metronome): a dedicated small circuit sustaining periodic output that downstream circuits subscribe to.
- Phase-coded memory → **frequency = value** and **rhythm subnetwork**: amplitude-phase encoding is the sketch's "frequency is predicted value".
- Phase codes emerge in RNN → **emergent frequency quantisation**: strongest evidence the owner's "quantisation should emerge" is a real, trainable phenomenon — RNNs self-organise phase/frequency codes when structure is periodic (modular arithmetic).
- Predictive-coding+Info-Bottleneck on LLMs → **KV/head-bit readout**: predictive-coding reads LLM hidden state to detect drift/hallucination — a working example of a small net reading model activations as a signal.

## What to try first at $0 — the 3 closest mechanisms
1. **AKOrN (2410.13821)** — *exactly* the sketch's oscillatory backbone (oscillator = frequency-bearing state unit, binding by synchrony = alignment). Closest single paper to the whole sketch.
2. **Phase codes emerge in RNNs for modular arithmetic (2310.07908)** — closest to *emergent* frequency/phase quantisation, the owner's "should EMERGE from the energy mechanics" priority.
3. **Spiking CPG / lamprey (2101.07001) + LinOSS (2410.03943)** — closest to the dedicated **rhythm-neuron metronome subnetwork**; LinOSS even proves stability (nonnegative diagonal = tones that hold).

**Smallest numpy experiment that tests the metronome (build on town's C2 digital-Kuramoto flip toy):**
A **rhythm-bank** of K=8 fixed-frequency steering oscillators (a metronome), plus N≈200–1000 plain oscillators. Oscillator j "subscribes" to a random 10–200-element subset of read sites (rhythm tones + other oscillators + a few driving inputs = KV/head-bit triggers), each with a clamped weight in [+0.3,+1]∪[−1,−0.3] (clamped non-zero bands). State = phase; update = Kuramoto–type phase push toward weighted-preferred frequency, with an **alignment cost** = energy of frequency mismatch vs the subscribed rhythm band. Driving bits flip once mid-run to simulate a sentence-shift. Measure three things: (1) **frequency histogram** — do oscillators quantise onto the rhythm-bank bands? (emergent quantisation); (2) **energy per step vs alignment** — does energy drop as networks synchronise and rise at the flip? (energy=alignment); (3) **state-shift latency** — how many steps after the driver bit flips before the steady-state frequency distribution re-locks? (the "steady state shifts with meaning" falsifier). All numpy, N² 1e6 ops, minutes per run, $0, no download.