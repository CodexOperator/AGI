export const meta = {
  name: 'agi-deep-search',
  description: 'Multi-lens deep investigation — one reader per lens on the same ground truth, an adversarial refuter per lens (default: refuted), then a ranker of survivors. Question, facts, lenses and refute_n all arrive through args; no investigation-specific text lives here.',
  phases: [
    { title: 'Read', detail: 'one reader per lens, findings to scratch files' },
    { title: 'Refute', detail: 'one adversarial refuter per lens, default to refuted' },
    { title: 'Synthesize', detail: 'one ranker merges survivors into a ranked mechanism list' },
  ],
}
// args: {question, facts, lenses:[{slug,instruction}], refute_n, scratch} — the ONLY channel
// by which this workflow knows what it is investigating. Defaults below are neutral
// placeholders; a reader points this at a real question purely through args (hypothesis:
// l3-deep-search-workflow-harness-agnostic).
const QUESTION = (args && args.question) || 'the investigation question (pass via args)'
const FACTS = (args && args.facts) || 'measured ground truth the agents must explain (pass via args)'
const REFUTE_N = (args && args.refute_n) || 3
const SCRATCH = (args && args.scratch) || '/tmp/agi-deep-search'
const LENSES = (args && args.lenses) || [
  { slug: 'mechanism', instruction: 'trace the concrete mechanism that produces the phenomenon' },
  { slug: 'cause', instruction: 'find the root cause and any competing or simpler explanation' },
]
const safeQuestion = String(QUESTION).replace(/[\n\r]/g, ' ').slice(0, 500)
const safeFacts = String(FACTS).replace(/[\n\r]/g, ' ').slice(0, 1500)
const READER_SCHEMA = { type: 'object', properties: { slug: { type: 'string' }, found: { type: 'integer' } }, required: ['slug', 'found'] }
const REFUTE_SCHEMA = { type: 'object', properties: { slug: { type: 'string' }, admitted: { type: 'integer' }, refuted: { type: 'integer' } }, required: ['slug', 'admitted', 'refuted'] }
const SYNTH_SCHEMA = { type: 'object', properties: { ranked: { type: 'array' }, top_mechanism: { type: 'string' } }, required: ['ranked', 'top_mechanism'] }
const readerPrompt = (l) => `You are one reader in a multi-lens investigation. Ground truth you MUST explain, not re-litigate: ${safeFacts}

The question under investigation: ${safeQuestion}

Your lens is '${l.slug}': ${l.instruction}

Read the relevant code/history and gather findings that EXPLAIN the phenomenon. Different lenses find different things on purpose; do not try to match other lenses. For every finding that claims to explain the phenomenon, keep one JSON record with: a concrete mechanism, the evidence (file:line where possible), and a confidence 0..1.

Write your findings to ${SCRATCH}/read-${l.slug}.json as an ARRAY of {"mechanism":"...","evidence":"...","confidence":0.0} objects (mkdir -p ${SCRATCH} first, overwrite if present). Return {slug, found} via StructuredOutput — no prose report.`
const refuterPrompt = (l) => `You are the adversarial refuter for lens '${l.slug}' in a multi-lens investigation. The question: ${safeQuestion}. Ground truth (do not re-litigate): ${safeFacts}

Read every findings file ${SCRATCH}/read-*.json (each lens wrote an ARRAY of {"mechanism","evidence","confidence"}). For EACH finding that claims to explain the phenomenon, try to kill it: check the cited evidence, look for a competing or simpler explanation, and DEFAULT TO REFUTED whenever the evidence is weak, ambiguous or unverified. Admit as a survivor only a finding whose explanation survives genuine adversarial pressure. Keep at most ${REFUTE_N} admitted findings for your lens; refute the rest.

Write your survivors to ${SCRATCH}/refute-${l.slug}.json as an ARRAY of {"mechanism":"...","evidence":"...","confidence":0.0,"why_survives":"..."} (mkdir -p ${SCRATCH} first, overwrite if present). Return {slug, admitted, refuted} via StructuredOutput — no prose report.`
const synthPrompt = `You synthesize a multi-lens investigation. The question: ${safeQuestion}. Ground truth: ${safeFacts}

Read every survivor file ${SCRATCH}/refute-*.json (each lens wrote an ARRAY of {"mechanism","evidence","confidence","why_survives"}). Merge duplicates across lenses, rank the distinct mechanisms by weighted confidence and breadth of independent evidence, and produce a ranked list of the TOP ${REFUTE_N} mechanisms most likely to explain the phenomenon. For each ranked mechanism give a concrete fix and, where code can be tested, a red-first test that would fail before the fix and pass after.

Return {ranked:[{mechanism,evidence,confidence,fix,red_first_test}], top_mechanism} via StructuredOutput — no prose report.`

phase('Read')
const reads = (await parallel(LENSES.map(l => () => agent(readerPrompt(l), { label: `read:${l.slug}`, phase: 'Read', schema: READER_SCHEMA, model: (args && args.model) || 'sonnet', effort: (args && args.effort) || 'medium' })))).filter(Boolean)
log(`${reads.length}/${LENSES.length} readers done`)
phase('Refute')
const refutes = (await parallel(LENSES.map(l => () => agent(refuterPrompt(l), { label: `refute:${l.slug}`, phase: 'Refute', schema: REFUTE_SCHEMA, model: (args && args.model) || 'sonnet', effort: (args && args.effort) || 'high' })))).filter(Boolean)
log(`${refutes.length}/${LENSES.length} refuters done`)
phase('Synthesize')
const synth = await agent(synthPrompt, { label: 'synthesize', phase: 'Synthesize', schema: SYNTH_SCHEMA, model: (args && args.model) || 'sonnet', effort: (args && args.effort) || 'high' })
return { question: safeQuestion, reads, refutes, ranked: synth }
