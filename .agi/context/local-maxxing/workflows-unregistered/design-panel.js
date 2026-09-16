export const meta = {
  name: 'design-panel',
  description: 'Judge panel for ONE hypothesis node draft: N independent drafters from distinct angles, then a judge that scores (decidable/grounded/cheap/bridges), spot-checks sources, and synthesizes the final draft + the one-line dispatch order. args: {topic, sources, angles:[{key,text}], slug_prefix, model?, effort?}',
  phases: [
    { title: 'Draft', detail: 'one drafter per angle' },
    { title: 'Judge', detail: 'score, synthesize, emit the order line' },
  ],
}

const ROOT = '/home/ubuntu/work/agi'
const A = args || {}
const TOPIC = A.topic || 'chain 2: "digital Kuramoto in flip mode" — N byte-neurons (8-bit fixed cascades from E3) as oscillators whose IMPULSE is a bit FLIP, coupled by nearest-flip coupling, sweeping coupling strength K and measuring the Kuramoto order parameter R — a numpy toy on CPU.'
const SOURCES = A.sources || `Sources to read (all under ${ROOT}): the owner's verbatim research lines (sed -n 110p .agi/nodes/goal/g14.md); .agi/context/local-maxxing/e3/e3_lut.py and e3_results.json; the trove survey regions you grep to in .agi/context/local-maxxing/trove-survey-2026-09-14.md; .agi/nodes/doc/local-maxxing-trove-survey-2026-09-14.md; .agi/nodes/vision/local-maxxing*.md; a prior hypothesis node and its kid experiment nodes as the deliverable shape. Hardware: 4-core arm-cloud, 23 GB, no GPU, shared (load 1-5); CPU-only numpy; a script must finish in < 20 min wall-clock. Budget: $2 OpenRouter cap per round.`
const ANGLES = A.angles || [
  { key: 'physics', text: 'physics-first: define the unit precisely from the sources, derive the decisive measurement, make the claim a sharp statement with seeds and a noise floor' },
  { key: 'engineering', text: 'engineering-first: start from what the town can USE, design the smallest measurement whose outcome changes a decision; make the falsifier bite' },
]
const PREFIX = A.slug_prefix || 'c2-'
const MODEL = A.model
const EFFORT = A.effort || 'high'
const opts = (o) => Object.assign({}, o, MODEL ? { model: MODEL } : {}, { effort: EFFORT })

const RULES = `HARD RULES: you are READ-ONLY. Never run git commit/push/add, never run write.py, never edit or create any file under ${ROOT}. Do not run the engine test suite. Do not dispatch anything. Pilot scripts go in a mktemp -d directory, never the repo. Your final output is DATA for an orchestrator, not prose for a human.`

const DRAFT = { type: 'object', properties: {
  slug: { type: 'string', description: `kebab-case node slug, starts with "${PREFIX}"` },
  title: { type: 'string' },
  testable_claim: { type: 'string', description: 'ONE sentence, with a number and a threshold, decidable on the town iron within the ceiling' },
  falsifier: { type: 'string', description: 'ONE sentence: the measurement that would disprove it' },
  tests: { type: 'string', description: 'kid split: Kid A / Kid B / Kid C, each ONE claim with a number; the parent spawns >= 2 real kids and authors NO experiment node itself' },
  file_scope: { type: 'string', description: 'exact paths the round may create/edit' },
  ceiling: { type: 'string', description: 'cap: $, hardware, wall-clock, max runtime per script' },
  body_md: { type: 'string', description: 'markdown body: ## Measured lines (each with a source path or URL and date) / ## CLAIM / ## FALSIFIERS / ## TESTS / ## FILE SCOPE / ## CEILING / ## Bridge. <= 60 lines.' },
  sources: { type: 'array', items: { type: 'string' } },
  order_line: { type: 'string', description: 'the ONE-line dispatch order to the director, <= 400 chars, starting with "[TM] hypothesis:<slug> — "' },
}, required: ['slug', 'title', 'testable_claim', 'falsifier', 'tests', 'file_scope', 'ceiling', 'body_md', 'sources', 'order_line'] }

const JUDGE = { type: 'object', properties: {
  scores: { type: 'array', items: { type: 'object', properties: { draft: { type: 'integer' }, decidable: { type: 'integer' }, grounded: { type: 'integer' }, cheap: { type: 'integer' }, bridges: { type: 'integer' }, total: { type: 'integer' }, weakest_point: { type: 'string' } }, required: ['draft', 'decidable', 'grounded', 'cheap', 'bridges', 'total', 'weakest_point'] } },
  winner: { type: 'integer' }, why: { type: 'string' }, final: DRAFT,
}, required: ['scores', 'winner', 'why', 'final'] }

phase('Draft')
const drafts = (await pipeline(ANGLES, (a) => agent(
  `${RULES}\n\nYou are drafting ONE hypothesis node for the local-maxxing town. TOPIC: ${TOPIC}\nYour angle: ${a.text}\n\n${SOURCES}\n\nProduce a draft with: a testable_claim that is ONE sentence with a number and a threshold, a falsifier, a Kid A / Kid B / Kid C split where each kid's deliverable is ONE measured claim (the parent must spawn >= 2 real kids and author NO experiment node itself — a standing process rule), an exact file scope, a ceiling, and a body that also states the BRIDGE: what a proved result feeds next and what a disproved one kills. Ground every measured line in a file you actually read (path + what it says). Do not pad: a chain is as long as its evidence.`,
  opts({ label: `draft:${a.key}`, phase: 'Draft', schema: DRAFT })))).filter(Boolean)
log(`drafts: ${drafts.map(d => d.slug).join(', ')}`)

phase('Judge')
const judge = await agent(
  `${RULES}\n\nYou are the judge for the town master. ${drafts.length} independent drafts of a hypothesis node on the TOPIC below were produced (JSON below). TOPIC: ${TOPIC}\nScore each 1-5 on: decidable (one numeric claim a script settles), grounded (every measured line traces to a file the drafter read — spot-check by reading the files yourself: ${SOURCES}), cheap (inside the ceiling), bridges (a result changes what the town does next). Then SYNTHESIZE the final draft: start from the winner, graft the best of the others, tighten the claim to one sentence with a number and a threshold, keep the Kid A/B/C split (each kid ONE measured claim; parent spawns >= 2 real kids, authors no experiment node), the file scope, the ceiling, and the ONE-line order to the director. The body_md must be <= 60 lines with the sections ## Measured lines / ## CLAIM / ## FALSIFIERS / ## TESTS / ## FILE SCOPE / ## CEILING / ## Bridge, every measured line citing a path or URL. Slug must start with "${PREFIX}".\n\nDRAFTS:\n${JSON.stringify(drafts, null, 1)}`,
  opts({ label: 'judge', phase: 'Judge', schema: JUDGE }))
return { drafts, judge }
