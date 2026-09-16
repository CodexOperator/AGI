export const meta = {
  name: 'harvest-review',
  description: 'Adversarial review of a merged round: one skeptic per kid experiment node (refute the recorded verdict against the bytes on disk), then a hypothesis-level judge that decides ACCEPT/DEMOTE and the hypothesis verdict. args: {hypothesis, nodes:[{key,node}], artifacts_dir, context, model?, effort?}',
  phases: [
    { title: 'Skeptics', detail: 'one adversarial reader per experiment node' },
    { title: 'Judge', detail: 'hypothesis-level ACCEPT / DEMOTE with a measured note' },
  ],
}

const ROOT = '/home/ubuntu/work/agi'
const A = args || {}
const HYP = A.hypothesis || 'hypothesis:d1-random-set-mean-ablation'
const NODES = A.nodes || [{ key: 'a00-01a81f78-81defb', node: 'experiment:a00-01a81f78-81defb' }, { key: 'a00-51318335-e170a9', node: 'experiment:a00-51318335-e170a9' }]
const ART = A.artifacts_dir || `${ROOT}/.agi/context/local-maxxing/d1/`
const CONTEXT = A.context || `The hypothesis node's testable_claim and falsifier are in ${ROOT}/.agi/nodes/hypothesis/${HYP.split(':')[1]}.md; read it. Verdict taxonomy: proved | disproved | inconclusive_lean_proved:N | inconclusive_lean_disproved:N | pending; proved/disproved require evidence_runs >= 1 AND the bytes to back them. Town frame (local-maxxing): decode on this box is bandwidth-bound, so a "decode lever" must be graded as a bytes-touched-per-token delta.`
const MODEL = A.model
const EFFORT = A.effort || 'high'
const opts = (o) => Object.assign({}, o, MODEL ? { model: MODEL } : {}, { effort: EFFORT })

const RULES = `HARD RULES: you are READ-ONLY. Never run git commit/push/add, never run write.py, never edit or create any file under ${ROOT}. Do not run the engine test suite. Do not dispatch anything. Read files with cat/sed/grep/python3 as needed. Your final output is DATA for an orchestrator, not prose for a human. Quote numbers exactly as they appear in the files you read, with the file path.`

const SKEPTIC = { type: 'object', properties: {
  node: { type: 'string' }, claimed_verdict: { type: 'string' },
  refuted: { type: 'boolean', description: 'true if the claimed verdict is NOT supported by the bytes on disk' },
  suggested_verdict: { type: 'string', description: 'proved | disproved | inconclusive_lean_proved:N | inconclusive_lean_disproved:N | pending' },
  reasons: { type: 'array', items: { type: 'string' }, description: 'measured, one sentence each, each citing a file path and a number' },
  numbers: { type: 'array', items: { type: 'string' }, description: '"<name>=<value> (<file>)"' },
  claim_vs_script: { type: 'string', description: 'does the script actually do what the testable_claim says? one sentence' },
  files_read: { type: 'array', items: { type: 'string' } },
}, required: ['node', 'claimed_verdict', 'refuted', 'suggested_verdict', 'reasons', 'numbers', 'claim_vs_script', 'files_read'] }

const JUDGE = { type: 'object', properties: {
  decision: { type: 'string', enum: ['ACCEPT', 'DEMOTE'] },
  hypothesis_verdict: { type: 'string', description: 'verdict for the hypothesis from the taxonomy' },
  note: { type: 'string', description: 'ONE line (<= 300 chars) to be written as a note on the hypothesis node: decision + measured reason + numbers' },
  reasons: { type: 'array', items: { type: 'string' } },
  per_experiment: { type: 'array', items: { type: 'object', properties: { node: { type: 'string' }, keep_verdict: { type: 'boolean' }, verdict: { type: 'string' }, why: { type: 'string' } }, required: ['node', 'keep_verdict', 'verdict', 'why'] } },
  what_was_established: { type: 'string', description: 'two sentences, measured: what the town now knows from this round that it did not before' },
}, required: ['decision', 'hypothesis_verdict', 'note', 'reasons', 'per_experiment', 'what_was_established'] }

phase('Skeptics')
const skeptics = (await pipeline(NODES, (n) => agent(
  `${RULES}\n\nYou are an adversarial skeptic. Try to REFUTE the verdict recorded on ${n.node}. Read ${ROOT}/.agi/nodes/experiment/${n.key}.md in full, then every artifact the node cites under ${ART}. Check: (1) the numbers in the node body equal the numbers in the results JSON/logs; (2) the script does what the node's testable_claim says (model, revision, what is ablated/measured, seeds, eval set size, noise floor actually measured or assumed); (3) whether the verdict string is justified by the taxonomy rules; (4) whether the node's testable_claim is the same claim the hypothesis asked for, or a narrower substitute; (5) whether any rescue number exists only off-disk (/tmp, narrated strings) rather than in committed bytes. Default to refuted=true if uncertain.\n\nContext: ${CONTEXT}`,
  opts({ label: `skeptic:${n.key.slice(0, 12)}`, phase: 'Skeptics', schema: SKEPTIC })))).filter(Boolean)
log(`skeptics: ${skeptics.map(s => `${s.node}: refuted=${s.refuted} -> ${s.suggested_verdict}`).join(' | ')}`)

phase('Judge')
const judge = await agent(
  `${RULES}\n\nYou are the hypothesis-level judge for the town master. Skeptics examined the experiment nodes of ${HYP}. Their findings (JSON):\n${JSON.stringify(skeptics, null, 1)}\n\nContext: ${CONTEXT}\n\nRead the hypothesis node and every experiment node yourself and spot-check any number a skeptic disputes against ${ART}. Decide: ACCEPT (the merge-up stands as harvested; the hypothesis gets a verdict the experiments jointly support) or DEMOTE (an experiment's verdict overstates its bytes, or the hypothesis's own claim was not actually decided). The hypothesis verdict must follow from what the bytes show about THE HYPOTHESIS'S claim, not the kids' narrower claims. Be exact: a demote needs a measured reason with numbers; an accept needs the same.`,
  opts({ label: 'judge', phase: 'Judge', schema: JUDGE }))
return { hypothesis: HYP, skeptics, judge }
