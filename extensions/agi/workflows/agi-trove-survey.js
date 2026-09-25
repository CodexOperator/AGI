export const meta = {
  name: 'agi-trove-survey',
  description: 'Survey the local-maxxing research trove (owner repos, papers, literature, hardware), critique each reading, then a 3-vision hypothesis panel + judge',
  phases: [
    { title: 'Read', detail: 'one reader per source' },
    { title: 'Critique', detail: 'adversarial critic per reading' },
    { title: 'Panel', detail: 'three vision angles propose hypothesis chains' },
    { title: 'Judge', detail: 'dedup, rank by knowledge-per-token, completeness critic' },
  ],
}
const S = args.scratch
const ROOT = (args && args.project_root) || '.'
const COMMON = `You are a research reader for the "local-maxxing" town of an AI research graph. READ-ONLY: never modify any repo, never install packages, never run training, never rent GPUs, never call paid APIs. You may run small read-only shell commands (ls, cat, grep, wc, python3 -c for JSON inspection) and use WebFetch/WebSearch (load via ToolSearch "select:WebFetch,WebSearch"). Quote sources with URL/path + date. Mark every number as MEASURED (from a file/page you read) or ESTIMATE. Never invent results.
Context the owner gave (verbatim-ish): the town's aim is to maximize the usefulness of ABSOLUTELY TINY models across all layers of the system; everything must run on CPU + ordinary RAM (this box: 4-core ARM arm64 arm-cloud, 23 GB RAM, ~7 GB free, no GPU; a second headless box: 8 GB unified RAM, old Intel HD iGPU; Camber Cloud GPU: ONE extra-small 24 GB VRAM instance, hard budget 3 GPU-HOURS PER MONTH). Three visions: (1) there is always a more efficient way to infer on lighter hardware; (2) there is always a smarter way to infer that scores higher on benchmarks over time; (3) two or more tiny models cooperating are exponentially smarter than the sum. Town moral: not tokens saved, but KNOWLEDGE and WISDOM extracted per token spent, failures included. The owner wants many hypotheses chased in parallel, coalesced into further hypothesis sets sequentially, before any MVP. Owner's specific threads: the dead-head "coherence" pruning equation applied to head pruning AND to generating coupled-oscillator maps, imported into a spiking-neural-network architecture; a neuron-as-transistor-byte model (each neuron = a byte; fires by how many/which bits are set, in what order; bits map to upstream neurons' output bits; broadcast/subscribe; one bit out per tick); KV-cache compression + efficient streaming papers folded in; recurrent looped transformers (depth recurrence); candidate model line "qwen3.8 50b" (exact id unknown — resolve it).`

const READ_SCHEMA = { type: 'object', properties: {
  source: { type: 'string' },
  summary: { type: 'string', description: '<=400 words, dense' },
  key_facts: { type: 'array', items: { type: 'string' }, description: 'each tagged MEASURED or ESTIMATE with the path/URL' },
  reusable_assets: { type: 'array', items: { type: 'string' }, description: 'code, data, equations, results we can reuse directly, with paths' },
  failures_and_lessons: { type: 'array', items: { type: 'string' } },
  hypothesis_seeds: { type: 'array', items: { type: 'object', properties: { claim: { type: 'string' }, falsifier: { type: 'string' }, cpu_experiment: { type: 'string' }, est_cost: { type: 'string' } }, required: ['claim', 'falsifier', 'cpu_experiment'] } },
  open_questions: { type: 'array', items: { type: 'string' } },
}, required: ['source', 'summary', 'key_facts', 'reusable_assets', 'failures_and_lessons', 'hypothesis_seeds', 'open_questions'] }

const DEFAULT_SOURCES = [
  { key: 'dead-head-paper', prompt: `Read the dead-head paper repo at ${S}/dead-head (paper.tex, README.md, data/README.md, the JSON result files' top-level keys and headline numbers, Makefile). Extract: the exact coherence equation(s) and their definitions; what "dead head" means operationally; the measured results per model (gpt2, gpt2-medium, open_llama_7b, qwen2.5-0.5b) — how many heads pruned, quality delta, timing; the compute needed to run the method (does it need a GPU? could it run on CPU for a 0.5B model?). Then think hard about the owner's idea: could the same coherence quantity define coupling strengths between heads/neurons, i.e. generate a coupled-oscillator (Kuramoto-style) map? State precisely what would have to be true. Seeds must be CPU-runnable on 0.5B-class models.` },
  { key: 'modularNN', prompt: `Read the owner's modularNN pipeline at ${S}/machinelearning/modularNN (README.md, examples/README.md, ingestion/pipeline.py, the encoding/ and framing/ modules' docstrings, tests list, any results/artifacts summaries; also ${S}/machinelearning/CLAUDE.md, AGENTS.md, log.md). Extract what the pipeline actually does end-to-end, what encoders exist (spike encodings? rate/latency/delta?), what runs on CPU, what is finished vs scaffold, test count and status. Which parts are reusable for tiny-model / SNN experiments now, with paths.` },
  { key: 'snn-experiments', prompt: `Read the owner's spiking-neural-network work: ${S}/machinelearning/spikyNN, ${S}/machinelearning/snn_standard_model (TODO.md, reports/SNN_Progress_Report.md, experiment_plan.py, experiment_infrastructure.py, colab/README.md, any results JSON/CSV summaries), ${S}/machinelearning/snn_applied_finance (README files, snn_energy_topology/*.py docstrings, run_p2_experiments.py, and SKIM the conversations/ folder: read the LAST 3 critic files fully and grep the rest for 'result', 'fail', 'conclusion'), and ${S}/Simple-Spiking-Net-Demo. Extract: neuron models used (LIF? params), encodings, surrogate gradients, topologies, energy models, what was measured, what failed and WHY (the owner says pricing prediction had little success), what infrastructure is reusable. Then map the owner's neuron-as-transistor-byte idea onto what exists: which files would a bit-threshold neuron replace or extend.` },
  { key: 'looped-transformer', prompt: `Fetch and digest https://www.alphaxiv.org/abs/2609.recurrent-looped-transformer (try also https://www.alphaxiv.org/overview/2609.recurrent-looped-transformer, arxiv.org/abs/2609.xxxxx equivalents via WebSearch "recurrent looped transformer 2026"). If the exact page will not load, find the actual paper by search and say exactly which paper you read. Extract: the architecture (depth recurrence, how many loops, shared weights?), parameter count vs effective depth, benchmark results vs same-param and same-compute baselines, inference cost per token, whether loop count can be varied at inference (adaptive compute), training recipe and its cost, any released weights/code. Then digest it into an autoresearch-style chain of 4-6 hypotheses, each with claim/falsifier/CPU experiment on a tiny model (<=1B), each building on the previous. Also search for related 2025-2026 work: "looped transformers", "Ouro", "recurrent depth", "Huginn", "latent reasoning depth recurrence".` },
  { key: 'kv-cache-streaming', prompt: `Literature sweep (WebSearch + WebFetch, 2024-2026): KV-cache compression and efficient streaming inference for small models on CPU — e.g. StreamingLLM/attention sinks, H2O, SnapKV, PyramidKV, KV quantization (KIVI, KVQuant), TurboQuant, cross-layer KV sharing (YOCO, CLA, MLA), token merging, sliding-window + global. For each: mechanism, measured memory/throughput gain, quality loss, whether llama.cpp / vLLM-CPU / candle / mlc already implement it (name the flag). Output a ranked table of what is worth testing on a 4-core ARM box with ~7 GB free RAM for a 0.5B-4B model. Seeds: hypotheses testable with llama.cpp on CPU in under 1 CPU-hour each.` },
  { key: 'tiny-models-cpu', prompt: `Literature + practical sweep (WebSearch + WebFetch, dated 2026): (1) the current best OPEN models at 0.3B, 0.5-1B, 1.5-2B, 3-4B, 7-8B parameters (Qwen3.x small, Gemma 3/4 small, SmolLM3, Llama 3.2/4 small, Phi-4-mini, MiniCPM, etc.) with benchmark numbers (MMLU/GSM8K/HumanEval/IFEval) from their model cards, quoted with URLs; (2) RESOLVE what the owner's "qwen3.8 50b" most plausibly is (Qwen3.5/3.8? a 50B? Qwen3-Next-80B-A3B? Qwen3-30B-A3B?) — list candidates with real ids, dense/MoE, active params, bytes at 4-bit, licence; (3) realistic CPU throughput on a 4-core ARM arm64 (arm-cloud) with llama.cpp Q4_K_M for 0.5B/1.5B/4B/8B and for A3B MoEs — find measured numbers from llama.cpp discussions/benchmarks on Ampere/Graviton, tag ESTIMATE otherwise; (4) which tiny models fit the second box (8 GB unified); (5) OpenRouter price of deepseek-v4-flash and a tiny hosted model for comparison. Seeds: the first 5 benchmark-on-CPU experiments that establish a baseline ceiling for tiny models on this hardware.` },
  { key: 'ensembles', prompt: `Literature sweep (WebSearch + WebFetch, 2023-2026) on the third vision: multiple small models cooperating outperforming a bigger model — mixture-of-agents, LLM-Blender/ranking, self-consistency and majority voting scaling laws for small models, debate, speculative decoding with tiny drafts (throughput not quality), routing/cascades (FrugalGPT, RouteLLM), test-time compute scaling with small models (e.g. "smaller models with search beat larger" — Snell et al 2024, Beeching et al), process reward models, and any 2026 results on ensembles of 1-4B models vs 30-70B. For each: the measured gain, the condition under which it holds, and where it fails (correlated errors). Be honest about the "exponential" claim: what evidence supports super-additivity and what refutes it. Seeds: CPU-runnable experiments (a few tiny models on this box) that would measure super-additivity directly.` },
  { key: 'oscillators-bitneurons', prompt: `Literature sweep (WebSearch + WebFetch) for prior art on the owner's neuron-as-transistor-byte + coupled-oscillator SNN idea: BitNet b1.58 / 1-bit LLMs and their CPU inference (bitnet.cpp) with measured numbers; binary/ternary neural nets; XNOR nets; oscillatory neural networks and Kuramoto-model computing (ONNs, oscillator-based Ising machines); coupled-oscillator attention or "synchrony as attention" work; spiking transformers (SpikeGPT, Spikformer, SpikingBERT), spike-driven attention; neuromorphic bit-serial / event-driven designs (Loihi, SpiNNaker) implementable in software; Hopfield/modern Hopfield as attention; "binding by synchrony". Also CPU-side: bit-packed integer kernels (popcount, AVX/NEON) for binary matmul. For each: what it is, measured results, what is reusable in software on a CPU. Then assess the owner's proposal frankly: what is novel, what has prior art, which parts are testable cheaply, and the biggest risk (e.g., no gradient path; hand-wired mappings do not scale). Seeds: the smallest CPU experiments that would prove or kill each piece.` },
  { key: 'graph-prior-art', prompt: `Read the project's own graph for prior local-maxxing work, at /${ROOT} (READ ONLY). Use grep -rl over .agi/nodes/ for: 'local-maxxing', 'g14', 'dead-head', 'dead head', 'coherence', 'quantiz', 'llama.cpp', 'ollama', 'tiny model', 'small model', 'spiking', 'Camber', 'CAMBER', 'fine-tune', 'classifier'. List every matching node id with its title line and status, and summarize what was actually done vs planned. Also: is llama.cpp, ollama, or any local inference binary installed on this box (which llama-cli llama-server ollama; ls ~/.cache/huggingface ~/.ollama 2>/dev/null; pip list 2>/dev/null | grep -iE 'torch|llama|transformers|onnx|numpy|snntorch|norse')? Report MEASURED. Read .agi/nodes/goal/g14.md, g14.1-g14.4.md, .agi/nodes/vision/local-maxxing.md, .agi/nodes/town/local-maxxing.md fully. What does the graph's schema for hypothesis/experiment/verdict require (.agi/context/schemas/[hypothesis].md, [experiment].md, [verdict].md, [doc].md — quote required fields)?` },
]

const CRIT_SCHEMA = { type: 'object', properties: {
  source: { type: 'string' },
  unsupported_claims: { type: 'array', items: { type: 'string' } },
  errors_found: { type: 'array', items: { type: 'string' } },
  missing_angles: { type: 'array', items: { type: 'string' } },
  strongest_seed: { type: 'string' },
  weakest_seed: { type: 'string' },
  confidence: { type: 'number', description: '0-1 that the reading is reliable' },
}, required: ['source', 'unsupported_claims', 'errors_found', 'missing_angles', 'strongest_seed', 'weakest_seed', 'confidence'] }

const SOURCES = (args && args.sources) || DEFAULT_SOURCES
const ANGLES = (args && args.angles) || DEFAULT_ANGLES
phase('Read')
const readings = await pipeline(SOURCES,
  s => agent(`${COMMON}\n\nTASK (${s.key}): ${s.prompt}\nReturn the structured reading.`, { label: `read:${s.key}`, phase: 'Read', schema: READ_SCHEMA }),
  (r, s) => r ? agent(`${COMMON}\n\nYou are an ADVERSARIAL CRITIC. A reader produced this reading of source "${s.key}":\n${JSON.stringify(r, null, 1)}\n\nSpot-check it: re-open 2-4 of the cited paths/URLs yourself and verify the quoted numbers and claims. Flag anything unsupported, hype-driven, or that contradicts the source. Name angles the reader missed. Judge which hypothesis seed is strongest (highest knowledge-per-token on CPU) and which is weakest. Default to skepticism.`, { label: `critique:${s.key}`, phase: 'Critique', schema: CRIT_SCHEMA }).then(c => ({ key: s.key, reading: r, critique: c })) : null,
)
const good = readings.filter(Boolean)
log(`readings: ${good.length}/${SOURCES.length}`)

const digest = good.map(g => `### ${g.key}\nSUMMARY: ${g.reading.summary}\nKEY FACTS: ${g.reading.key_facts.join(' | ')}\nREUSABLE: ${g.reading.reusable_assets.join(' | ')}\nLESSONS: ${g.reading.failures_and_lessons.join(' | ')}\nSEEDS: ${g.reading.hypothesis_seeds.map(h => `[${h.claim} // falsifier: ${h.falsifier} // exp: ${h.cpu_experiment} // cost: ${h.est_cost || '?'}]`).join(' ')}\nOPEN: ${g.reading.open_questions.join(' | ')}\nCRITIC (conf ${g.critique?.confidence}): unsupported=${(g.critique?.unsupported_claims||[]).join(' | ')} errors=${(g.critique?.errors_found||[]).join(' | ')} missing=${(g.critique?.missing_angles||[]).join(' | ')} strongest=${g.critique?.strongest_seed} weakest=${g.critique?.weakest_seed}`).join('\n\n')

const PANEL_SCHEMA = { type: 'object', properties: {
  angle: { type: 'string' },
  chains: { type: 'array', items: { type: 'object', properties: {
    chain_title: { type: 'string' },
    why_this_first: { type: 'string' },
    hypotheses: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'string' }, claim: { type: 'string' }, falsifier: { type: 'string' }, experiment: { type: 'string' },
      hardware: { type: 'string', description: 'this box CPU / 8GB box / Camber XS minutes' },
      est_cost: { type: 'string' }, builds_on: { type: 'string' }, knowledge_if_fails: { type: 'string' },
    }, required: ['id', 'claim', 'falsifier', 'experiment', 'hardware', 'est_cost', 'knowledge_if_fails'] } },
  }, required: ['chain_title', 'why_this_first', 'hypotheses'] } },
  coalescence_points: { type: 'array', items: { type: 'string' }, description: 'where chains merge into a second-order hypothesis set before any MVP' },
  critique_of_owner_plan: { type: 'array', items: { type: 'string' } },
}, required: ['angle', 'chains', 'coalescence_points', 'critique_of_owner_plan'] }

const DEFAULT_ANGLES = [
  { key: 'efficiency', text: 'VISION 1 — there is always a more efficient way to infer on lighter hardware: quantization (incl. sub-4-bit, ternary), KV-cache compression, looped/recurrent depth, head pruning via coherence, CPU kernels, the 8 GB box, Camber minutes as the rarest resource.' },
  { key: 'smarter', text: 'VISION 2 — there is always a smarter way to infer that scores higher on benchmarks over time: test-time compute, self-consistency, distillation into tiny models, graph-routed specialists (goal:g14 lattice), fine-tuning slots with the corpus this graph already has, benchmark ceilings for tiny models rising month over month.' },
  { key: 'cooperation', text: 'VISION 3 — two or more tiny models cooperating are exponentially smarter than the sum: ensembles, debate, routing, speculative decoding, mixture-of-agents, spiking/oscillator coupling as a cooperation mechanism between model-neurons (the owner\'s byte-neuron pub/sub idea), the graph as the coordinator.' },
]

phase('Panel')
const panel = (await parallel(ANGLES.map(a => () => agent(`${COMMON}\n\nYou are one seat of a three-seat hypothesis panel. Your angle: ${a.text}\n\nHere is the critiqued digest of the whole research trove:\n${digest}\n\nPropose 3-5 hypothesis CHAINS (each 3-6 hypotheses building on one another, autoresearch style: each hypothesis has a measured claim, a falsifier, and the experiment that decides it). Constraints: ~all experiments run on this 4-core ARM box (or the 8 GB box); Camber GPU is 3 hours/month TOTAL — name where a single 10-30 minute Camber burst would be decisive, and nowhere else; no MVP, research only; maximize KNOWLEDGE per token, so every hypothesis states what we learn if it FAILS. Include at least one chain that touches the owner's spiking/oscillator/byte-neuron thread frankly (even if the honest first hypothesis is a kill-test). Name coalescence points where chains merge into a second-order hypothesis set. Give 3-6 frank critiques of the owner's plan (things that are likely wrong, prior art, or a cheaper path).`, { label: `panel:${a.key}`, phase: 'Panel', schema: PANEL_SCHEMA })))).filter(Boolean)
log(`panel seats: ${panel.length}/3`)

const JUDGE_SCHEMA = { type: 'object', properties: {
  ranked_chains: { type: 'array', items: { type: 'object', properties: {
    rank: { type: 'number' }, chain_title: { type: 'string' }, vision: { type: 'string' }, score_knowledge_per_token: { type: 'number' },
    first_hypothesis: { type: 'string' }, first_experiment: { type: 'string' }, hardware: { type: 'string' }, est_cost: { type: 'string' }, why: { type: 'string' },
    full_chain: { type: 'array', items: { type: 'string' } },
  }, required: ['rank', 'chain_title', 'vision', 'score_knowledge_per_token', 'first_hypothesis', 'first_experiment', 'hardware', 'est_cost', 'why', 'full_chain'] } },
  duplicates_merged: { type: 'array', items: { type: 'string' } },
  coalescence_plan: { type: 'array', items: { type: 'string' } },
  camber_burst_plan: { type: 'array', items: { type: 'string' }, description: 'the only uses of the 3 GPU-hours/month, in priority order, with minutes' },
  round0_baseline: { type: 'array', items: { type: 'string' }, description: 'the measurements to take on this box BEFORE any chain runs' },
  critiques_of_owner_plan: { type: 'array', items: { type: 'string' } },
  what_is_missing: { type: 'array', items: { type: 'string' } },
}, required: ['ranked_chains', 'duplicates_merged', 'coalescence_plan', 'camber_burst_plan', 'round0_baseline', 'critiques_of_owner_plan', 'what_is_missing'] }

phase('Judge')
const judged = await agent(`${COMMON}\n\nYou are the JUDGE + COMPLETENESS CRITIC. Three panel seats proposed hypothesis chains:\n${JSON.stringify(panel, null, 1)}\n\nThe critiqued trove digest:\n${digest}\n\nDedup and merge overlapping chains; rank the top 8-12 chains by KNOWLEDGE-PER-TOKEN (a chain whose first hypothesis is cheap, decisive, and informative when it fails ranks high); keep every hypothesis's falsifier. Produce: the round-0 baseline measurements to take on this box before anything else; the ONLY planned uses of Camber's 3 GPU-hours/month (minutes each, priority order); the coalescence plan (which chains merge into second-order hypothesis sets, and when); the merged frank critiques of the owner's plan; and what is still missing from the whole survey (a source not read, a claim unverified, a vision with no chain).`, { label: 'judge', phase: 'Judge', schema: JUDGE_SCHEMA, effort: 'high' })

return { readings: good, panel, judged }