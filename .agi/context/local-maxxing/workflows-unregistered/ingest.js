export const meta = {
  name: 'ingest',
  description: 'Treasury ingestion for a research town: per source a reader writes the digest file + idea seed and a critic refutes it against the source (pipeline), then one agent per owner hunch builds on the critiqued digests (barrier), then a synthesizer ranks the first research rounds. Nodes are minted afterwards by the town master (doc:<key> link_ref -> digest, idea:<key> the seed). args: {date, sources:[{key,url,hint}], hunches:[{id,text,focus}], papers_dir?, town?, model?, effort?}',
  phases: [
    { title: 'Digest', detail: 'reader writes the digest file, critic checks it against the source' },
    { title: 'Hunches', detail: 'one agent per owner hunch, built on the critiqued digests' },
    { title: 'Synthesize', detail: 'rank the first research rounds' },
  ],
}

const ROOT = '/home/ubuntu/work/agi'
const A = args || {}
const PAPERS = A.papers_dir || `${ROOT}/.agi/context/local-maxxing/papers`
const DATE = A.date || 'undated'
const SOURCES = A.sources || []
const HUNCHES = A.hunches || []
const MODEL = A.model
const EFFORT = A.effort || 'high'
const opts = (o) => Object.assign({}, o, MODEL ? { model: MODEL } : {}, { effort: o.effort || EFFORT })
if (!SOURCES.length) log('ingest: no args.sources — nothing to digest')

const RULES = `HARD RULES: you may write EXACTLY ONE file in the repo — the digest file named in your task under ${PAPERS}/ — and nothing else. Never run git add/commit/push, never run write.py, never touch .agi/nodes, never run the engine test suite, never dispatch anything. Scratch downloads go to a \`mktemp -d\` directory, never into the repo. Tools: curl -sL -A 'Mozilla/5.0' for pages; pdftotext -layout for PDFs; arXiv HTML lives at https://arxiv.org/html/<id> and abs metadata at https://arxiv.org/abs/<id>; alphaxiv abs pages accept a .pdf suffix; a GitHub repo README is at https://raw.githubusercontent.com/<org>/<repo>/HEAD/README.md; a HF dataset's metadata is at https://huggingface.co/api/datasets/<id>. If a fetch fails, say so exactly (URL + HTTP code) and digest what you could reach — NEVER summarize a source from memory; every number you write must be quoted from bytes you fetched, with its URL. Your final output is DATA for an orchestrator, not prose for a human.`
const READONLY = RULES.replace(/you may write EXACTLY ONE file in the repo[^.]*\./, 'you are READ-ONLY: write nothing in the repo.')

const TOWN = A.town || `The town (local-maxxing, goal:g14: "the smallest model that can do the job, everywhere"): decode on the swarm box (arm-cloud 4c, 23 GB, no GPU) is bandwidth-bound — every lever is graded as a bytes-touched-per-token delta. Cluster (hardware only; never write addresses): local-town = x86-8c 8c/16t, 16 GB, gpu-8g, 339 GB /data; encryption-town = i5 2c/4t, 8 GB, 352 GB /data (archive); gigabit LAN between them; WireGuard overlay to the swarm box. Standing threads: E3 byte-neuron LUT (bit FLIP = impulse), chain 2 digital Kuramoto in flip mode, D1 mean-ablation on Qwen2.5-0.5B, a recurrent looped transformer as the intended architecture, and powering the swarm's own parents/kids off OpenRouter in bursts. The owner's standing angle on every source: compute-cost tricks that the bit-wise oscillator SNN + looped transformer might supercharge — assess frankly, with a falsifier.`

const IDEA = { type: 'object', properties: {
  slug: { type: 'string', description: 'kebab-case, starts with "lm-"' }, title: { type: 'string', description: '<= 80 chars' },
  lever: { type: 'string', description: 'ONE sentence: the mechanism and what cost it saves' },
  buys: { type: 'string', description: 'what the town could do with it on ITS iron' },
  first_falsifier: { type: 'string', description: 'the cheapest measurement that would kill the idea' },
  cheapest_test_on_our_iron: { type: 'string', description: 'the first experiment, which box, rough wall-clock and $' },
}, required: ['slug', 'title', 'lever', 'buys', 'first_falsifier', 'cheapest_test_on_our_iron'] }

const DIGEST = { type: 'object', properties: {
  key: { type: 'string' }, title: { type: 'string', description: 'the source real title, quoted' }, url: { type: 'string' },
  kind: { type: 'string', enum: ['paper', 'blog', 'repo', 'dataset', 'model', 'other'] },
  fetched: { type: 'string', description: 'what was actually fetched: URL, HTTP code, bytes, pages/lines' }, date_published: { type: 'string' },
  summary: { type: 'array', items: { type: 'string' }, description: '3-6 measured lines with quoted numbers' },
  numbers: { type: 'array', items: { type: 'string' }, description: '"<what>=<value> (<where in source>)"' },
  relevance: { type: 'string' }, idea: IDEA, tags: { type: 'array', items: { type: 'string' } }, digest_file: { type: 'string' },
}, required: ['key', 'title', 'url', 'kind', 'fetched', 'summary', 'numbers', 'relevance', 'idea', 'tags', 'digest_file'] }

const CRITIQUE = { type: 'object', properties: {
  key: { type: 'string' }, grounded: { type: 'integer', description: '1-5: 5 = every claim traces to bytes in the source' },
  errors: { type: 'array', items: { type: 'string' } }, unsupported_numbers: { type: 'array', items: { type: 'string' } },
  corrected_idea: IDEA, keep_digest: { type: 'boolean' }, note: { type: 'string', description: 'one line for the node' },
}, required: ['key', 'grounded', 'errors', 'unsupported_numbers', 'corrected_idea', 'keep_digest', 'note'] }

const HUNCH = { type: 'object', properties: {
  hunch: { type: 'string' }, slug: { type: 'string', description: 'kebab-case, starts with "lm-hunch-"' }, title: { type: 'string' },
  reading: { type: 'array', items: { type: 'string' } },
  actionable: { type: 'array', items: { type: 'object', properties: { claim: { type: 'string' }, falsifier: { type: 'string' }, cheapest_test: { type: 'string' }, iron: { type: 'string' }, cost: { type: 'string' }, sources: { type: 'array', items: { type: 'string' } } }, required: ['claim', 'falsifier', 'cheapest_test', 'iron', 'cost', 'sources'] } },
  dead_ends: { type: 'array', items: { type: 'string' } },
  body_md: { type: 'string', description: 'the idea node body, <= 50 lines: ## Owner hunch (verbatim) / ## What the sources say / ## Actionable claims / ## Dead ends / ## First round' },
}, required: ['hunch', 'slug', 'title', 'reading', 'actionable', 'dead_ends', 'body_md'] }

const SYNTH = { type: 'object', properties: {
  ranked_first_rounds: { type: 'array', items: { type: 'object', properties: { idea_slug: { type: 'string' }, hypothesis_claim: { type: 'string' }, falsifier: { type: 'string' }, why_first: { type: 'string' }, iron: { type: 'string' }, cost: { type: 'string' } }, required: ['idea_slug', 'hypothesis_claim', 'falsifier', 'why_first', 'iron', 'cost'] } },
  cross_cutting: { type: 'array', items: { type: 'string' } },
  owner_line: { type: 'string', description: 'ONE line (<= 400 chars) for the owner' },
}, required: ['ranked_first_rounds', 'cross_cutting', 'owner_line'] }

phase('Digest')
const pairs = await pipeline(SOURCES,
  (s) => agent(`${RULES}\n\n${TOWN}\n\nTASK: digest ONE source for the town's research treasury and write the digest to ${PAPERS}/${s.key}.md (markdown; sections: # <title> / ## Provenance (URL, HTTP code, bytes, date fetched ${DATE}) / ## Summary (measured lines) / ## Numbers / ## Relevance / ## Idea seed). If that file already exists, do NOT overwrite it: read it, spot-check two numbers, and APPEND "## Idea seed (${DATE})". Source key: ${s.key}. URL: ${s.url}. Owner hint (verbatim where quoted): ${s.hint || ''}\n\nThe idea seed is what a hypothesis will hang from — make its lever ONE mechanism with a number, its first_falsifier a measurement the town can run, and its cheapest test sized to the iron above. Return the DIGEST object.`,
    opts({ label: `read:${s.key}`, phase: 'Digest', schema: DIGEST })),
  (d, s) => d ? agent(`${RULES}\n\n${TOWN}\n\nYou are an adversarial critic. A reader digested source ${s.key} (${s.url}) into ${d.digest_file} and returned:\n${JSON.stringify(d, null, 1)}\n\nRe-fetch the source yourself and REFUTE: every number in the digest and the idea seed must appear in the source; every mechanism claim must be the source's, not the reader's; the lever must be a cost-saving mechanism the source demonstrates; the cheapest test must run on the town's iron. APPEND one section "## Critique (adversarial, ${DATE})" to the digest file listing each error with the correction (your ONE allowed write) and return the CRITIQUE object with a corrected_idea. Default to skepticism: an unsupported number is an error.`,
    opts({ label: `critique:${s.key}`, phase: 'Digest', schema: CRITIQUE, effort: s.kind === 'blog' ? 'medium' : EFFORT })).then(c => ({ source: s, digest: d, critique: c })) : null,
)
const done = pairs.filter(Boolean)
log(`digests: ${done.length}/${SOURCES.length}; grounded: ${done.map(p => `${p.source.key}=${p.critique ? p.critique.grounded : '?'}`).join(' ')}`)
const missing = SOURCES.filter(s => !done.find(p => p.source.key === s.key)).map(s => s.key)
if (missing.length) log(`MISSING digests: ${missing.join(', ')}`)
const seeds = done.map(p => ({ key: p.source.key, url: p.source.url, file: p.digest.digest_file, title: p.digest.title, idea: (p.critique && p.critique.corrected_idea) || p.digest.idea, grounded: p.critique ? p.critique.grounded : null, relevance: p.digest.relevance, numbers: p.digest.numbers }))

phase('Hunches')
const hunches = (await parallel(HUNCHES.map(h => () => agent(
  `${READONLY}\n\n${TOWN}\n\nOWNER HUNCH ${h.id} (verbatim, ${DATE}): "${h.text}"\nFocus: ${h.focus || ''}\n\nThe treasury's critiqued digests (read the files; each ends with an adversarial critique — trust the critique over the summary where they differ):\n${JSON.stringify(seeds, null, 1)}\n\nTASK: extract ACTIONABLE WISDOM from this gut feeling — not agreement, not dismissal. 2-3 claims a kid could decide on the town's iron for under $2 of API tokens or under 20 min of CPU/GPU, each with its falsifier and the number from a source that motivates it; the dead ends the evidence already argues against (with the number); and the idea node body.`,
  opts({ label: `hunch:${h.id}`, phase: 'Hunches', schema: HUNCH }))))).filter(Boolean)
log(`hunches explored: ${hunches.map(h => h.slug).join(', ')}`)

phase('Synthesize')
const synth = await agent(
  `${TOWN}\n\nREAD-ONLY (write nothing in the repo). You are the synthesizer for the town master. Inputs: (a) ${seeds.length} critiqued idea seeds:\n${JSON.stringify(seeds, null, 1)}\n(b) ${hunches.length} explored owner hunches:\n${JSON.stringify(hunches.map(h => ({ slug: h.slug, title: h.title, actionable: h.actionable, dead_ends: h.dead_ends })), null, 1)}\n\nRank the first 5 research rounds the town should run next (each = one hypothesis under one idea; ONE numeric claim; falsifier; iron; cost). Rank by: decidable on our iron for <= $2 or <= 20 min; changes what the town does next; builds on existing evidence rather than starting cold. Name the genuine cross-cutting compositions the numbers support — and say plainly which owner compositions the numbers do NOT yet support. Finish with the one line for the owner.`,
  opts({ label: 'synth', phase: 'Synthesize', schema: SYNTH }))
return { seeds, critiques: done.map(p => p.critique).filter(Boolean), hunches, synth, missing }
