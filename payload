export const meta = {
  name: 'l4-plan-research',
  description: 'Map the seat/schema/goal/dispatch system, draft the L4 plan three ways, judge, synthesize, adversarially verify',
  phases: [
    { title: 'Understand', detail: 'five read-only mappers, each writes a map file' },
    { title: 'Design', detail: 'three independent plan drafts from different angles' },
    { title: 'Judge', detail: 'two judges score the drafts' },
    { title: 'Synthesize', detail: 'final plan body + banked questions' },
    { title: 'Verify', detail: 'three lenses, fix in place' },
  ],
}

const S = args.scratch
const COMMON = `Repo: /home/ubuntu/work/agi (branch season/s2), the agi thoughtgraph engine + its own graph under .agi/. You are READ-ONLY on the repo: never run git with a write verb (no add/commit/push/checkout/stash/reset/merge), never run grid.py, write.py, dispatch.py, send.py, rotate.py, driver.sh, level3.py, crons.py, workflow.py run, tmux, or the test suite (pytest / commands.py run tests); never create or edit any file inside the repo. Write ONLY under SCRATCH=${S} (mkdir -p it first). Prefer grep -n / sed -n / head over reading whole files; give a file:line anchor for every fact. Owner text is ONLY what appears verbatim inside .agi/nodes/doc/l4-owner-decisions.md, .agi/nodes/doc/l3-command-ladder-brief.md, .agi/context/l3-command-ladder-brief.md, .agi/context/season-ladder-and-morals-brief.md, or vision/goal/moral nodes; quote it exactly when you use it, with source line; label everything else "(prime proposal)". Never invent an owner decision. Do not paste whole files into your answer.`

const MAP_SCHEMA = { type: 'object', properties: {
  map_path: { type: 'string' }, summary: { type: 'string' },
  key_facts: { type: 'array', items: { type: 'string' } },
  gaps: { type: 'array', items: { type: 'string' } } },
  required: ['map_path', 'summary', 'key_facts'] }

const READERS = [
  { key: 'seats', prompt: `Map the SEAT system. Read: .agi/nodes/.geometry/seats.md (node config:seats — list EVERY row with its name, role, tier, harness, model, effort, status/idle fields, owning_goal, rotated_by, handoff_file, and every field name the rows carry); .agi/context/schemas/[config].md and any schema that validates seats; extensions/agi/bin/write_guard.py (exactly what it checks on config:seats rows and on node writes generally; who is a sanctioned writer; --strict); extensions/agi/bin/brief.py (how a seat/tier brief is rendered: profiles incl. survival, AGI_BRIEF_PROFILE, readings, the constitution head, what sections a seat's bootstrap contains and in what order, any measured token counts); the seat launch path (rotate.py spawn / loop / --seat / rotate-self, seat_pin, generation stamps, how a seat is launched and re-launched; the sanctuary-director brief under .agi/sessions/quorum/ or wherever seat briefs live). Write the full map to SCRATCH/understand/seats.md (tables where structure exists), then return JSON with map_path, a <=120-word summary, <=12 key_facts (each with file:line), and gaps.` },
  { key: 'schemas', prompt: `Map the SCHEMA / write-rule surface. Read every .agi/context/schemas/*.md: for each node type list required fields, spawn rules (allowed_parents / parent_shapes / min/max), and ANY existing field that names WHO may write it (actor, writer, author, owner, role). Then read how write.py enforces --actor (moral needs --actor owner), how write_guard.py decides a write is sanctioned, how links.py schema validates, and how schema_registry loads [name].md. Answer precisely: what is the smallest EXISTING mechanism through which a rule "node type X may only be written by role R" could be declared in a schema and enforced by write.py/write_guard.py (name the functions and file:line where the check would hook), and what the schema files for vision, overview, goal, outcome, bigger_outcome, config, doc currently say. Write the full map to SCRATCH/understand/schemas.md, then return JSON with map_path, a <=120-word summary, <=12 key_facts (file:line each), and gaps.` },
  { key: 'goals', prompt: `Map GOALS, LADDER and SEASON. (1) List every TOP-LEVEL goal node (ids goal:gN or goal:sN with no dot, from .agi/nodes/goal/ — also check .agi/nodes/deprecated/goal/ for retired ones) as a table: id, title, status, number of sub-goals, any field like goal_kind/perpetual/horizon; identify which goal is (or would be) the SANCTUARY goal (grep -ri sanctuary .agi/nodes/goal .agi/nodes/vision .agi/nodes/doc), which goal owns the seat system / ladder / rotation (grep for seats, ladder, rotation in goal titles), and which goal doc:l4-owner-decisions hangs under (its parents) — recommend the legal goal parent for a new doc:l4-plan node per .agi/context/schemas/[doc].md. (2) Read .agi/nodes/.geometry/ladder.md: current_season, tiers, plan/report types per tier, director_rotate_at, read order by role, roles named. (3) Read extensions/agi/bin/season.py: status/judge/rollover semantics and who is meant to run them. (4) How vision, overview, outcome, bigger_outcome nodes are minted today: count per type, example ids, their authors/edited_by fields, and which type of agent minted them (grep edited_by / authors). Write the full map to SCRATCH/understand/goals.md, then return JSON with map_path, a <=120-word summary, <=12 key_facts (file:line each), and gaps.` },
  { key: 'dispatch', prompt: `Map DISPATCH, DIRECTOR-KIDS and COMMS. Read extensions/agi/bin/dispatch.py --help output (run it, it is read-only) and its source for: tiers (parent/kid/other), --harness pi|claude-code, --target, --level, --branch, --prompt-file, --detach, ceilings (agent_timeout_mins, max kids), the AGI_BRIEF_PROFILE survival profile, how the brief is built for a parent (the target node's body IS the brief; testable_claim). Read extensions/agi/bin/spawn_budget.py (the tree-wide bound), extensions/agi/bin/send.py (send/read/peek, dm files under .agi/comms/season-2/, rooms, audience/report verbs), and grep -rn "director-kid\\|director_kid\\|director kid" across .agi/nodes .agi/context extensions/agi/briefs extensions/agi/bin (what a director-kid IS today, how sanctuary-director is realised: seat row, brief file, how it dispatches pi parents, how it reports to the prime). Also read .agi/nodes/doc/l3-command-ladder-brief.md sections about the perpetual seats layer (grep -n "perpetual\\|item 78\\|item 70\\|item 56\\|item 61\\|item 64\\|item 65\\|item 95\\|item 99\\|masters never build") and copy the owner's VERBATIM quotes on: what a director-kid does, what the masters do, what the quorum does, liaison, master sensei, "the masters never build again", roles self-selecting handoff slices, constitution scope. Write the full map to SCRATCH/understand/dispatch.md (quotes exact, each with source line), then return JSON with map_path, a <=120-word summary, <=12 key_facts (file:line each), and gaps.` },
  { key: 'owner', prompt: `Extract the OWNER'S WORDS on roles and constraints. Read .agi/nodes/doc/l4-owner-decisions.md WHOLE (it is ~29 KB) and .agi/nodes/doc/l3-command-ladder-brief.md (grep -n first for: role, seat, master, sensei, liaison, quorum, director, kid, parent, sonnet, opus, survival, budget, subscription, idle, slice, handoff, trim, diagram, verbatim, rotate, 0.47, perpetual, goal, vision, overview, webhook, alert, branch). Produce SCRATCH/understand/owner.md with: (a) a table ROLE -> every owner quote about that role (exact text, source file:line), for belam/prime, sanctuary master, master sensei, liaison, quorum seats (self-perpetuating, alive, all-is-one), sanctuary director, director-kids, pi parents, pi kids, drafting/review kids; (b) a list of STANDING CONSTRAINTS in force with exact quotes (survival mode, masters never build, quorum stays, rotate at 0.47, trim+diagram-max every role, owner verbatim lives in nodes, one round at a time, pi/OpenRouter does the work, Claude seats sit on context a little at a time, key floor, never delete nodes, plan mode); (c) the L4 BACKLOG items and the "still waiting on the owner" items as a checklist; (d) the exact text of the owner's L4 plan paragraphs (copy verbatim). Return JSON with map_path, a <=120-word summary, <=12 key_facts, and gaps (owner questions you saw left unanswered).` },
]

phase('Understand')
const maps = await parallel(READERS.map(r => () =>
  agent(`${COMMON}\n\nTASK (${r.key}): ${r.prompt}`, { label: `map:${r.key}`, phase: 'Understand', schema: MAP_SCHEMA, model: 'opus', effort: 'high' })))
const mapsOk = maps.filter(Boolean)
log(`maps written: ${mapsOk.length}/5`)
const mapDigest = mapsOk.map(m => `- ${m.map_path}: ${m.summary}\n  facts: ${m.key_facts.join(' | ')}\n  gaps: ${(m.gaps || []).join(' | ')}`).join('\n')

const STRUCTURE = `Write the plan as the BODY of a graph node doc:l4-plan, plain markdown, no frontmatter, no title line other than the H1 below. Diagram-max where structure exists (tables, ASCII arrow diagrams); keep negations, conditions, attributions and supersessions EXPLICIT in every diagram. Owner text quoted exactly and attributed; everything else labelled (prime proposal). Required sections, in this order and with these headings:
# L4 plan — who acts on what
## 0 Source — the owner's plan (pointers + exact key sentences, not a paraphrase)
## 1 Actor legend as schema rules — table: node type -> writer role(s) -> enforcement hook (EXISTING file:line, or PROPOSED with the file it lands in) -> what a violation looks like
## 2 The 2+2+1 role card — first the ROW SCHEMA (field names on config:seats rows: tracks[2] each = what + where + cost-to-read; tells[2] each = target role + trigger + channel; decides = one closed set; validation rules the write guard applies; how brief.py renders the card as the role's WHOLE bootstrap), then ONE CARD PER SEAT: belam (prime), sanctuary-master, master-sensei, liaison, quorum: self-perpetuating, alive, all-is-one, sanctuary-director (the sanctuary p-goal's director-kid), goal director-kid (template, one per perpetual goal), draft director-kid and review director-kid ("etc jobs, no goals"), and for contrast the non-seat pi parent and pi kid. Each card: TRACKS 2 / TELLS 2 (target + trigger) / DECIDES 1 (closed set), plus model tier (Sonnet | Opus | Fable | pi) with the reason
## 3 Perpetual goals — the rule (every top-level g goal is perpetual; one director-kid each; Sanctuary Master owns the count of active ones and the models), the current top-level goals as a table with the seat row each implies, what changes in ladder tier 1, and the migration from today's rows
## 4 The sanctuary p-goal's director-kid — always active; the masters' implementation hand; the recommendation inbox flow as a diagram; pi parents by default under survival mode, drafting workflows only when named
## 5 First L4 rounds — serialised, pi/OpenRouter, one hypothesis node per round whose testable_claim IS the assignment, a hard ceiling each, dependencies explicit, backlog items folded in where they fit (L4.01 the replace verb already LANDED); mark which rounds need the owner's go
## 6 Open questions — each with the prime's recommendation, to be banked in doc:l4-owner-decisions
## 7 What this plan does NOT do — survival mode holds until the owner lifts it; nothing dispatched or launched until the owner approves; no node deleted; no engine edit beyond the plan node and the handoff in the plan session`

const ANGLES = [
  { key: 'enforcement', lens: 'ENFORCEMENT-FIRST: every rule must be a check (schema field, write guard, brief renderer, links.py) rather than a brief line; design the exact fields, validators and render order; say what today\'s code already does and what is new.' },
  { key: 'economy', lens: 'ECONOMY-FIRST: minimise owner decisions and Claude-subscription spend; which seats can be Sonnet and idle; staccato cadence via triggers; cost-to-read of every tracks item; what survival mode permits; keep the plan short enough to be a seat\'s whole bootstrap.' },
  { key: 'migration', lens: 'MIGRATION-FIRST: get from today\'s seat rows, backlog and traps to the target state in serialised pi/OpenRouter rounds; dependencies, ceilings, what proves each round, what can go wrong (use the TRAPS CARRIED INTO L4 section), and where L3 lessons bind.' },
]

phase('Design')
const drafts = await parallel(ANGLES.map(a => () =>
  agent(`${COMMON}\n\nYou draft the L4 plan for the agi graph. Angle: ${a.lens}\n\nFIRST read the owner's verbatim plan: sed -n '126,200p' .agi/nodes/doc/l4-owner-decisions.md, and the backlog: sed -n '49,61p' of the same file, and the traps section (grep -n "TRAPS CARRIED" then read ~60 lines). THEN read the five maps under ${S}/understand/*.md (they carry file:line anchors — reuse them; verify any anchor you rely on with grep before quoting it).\n\nMap digest:\n${mapDigest}\n\n${STRUCTURE}\n\nWrite the complete draft to ${S}/drafts/${a.key}.md. Return JSON.`,
    { label: `draft:${a.key}`, phase: 'Design', model: 'opus', effort: 'high',
      schema: { type: 'object', properties: { draft_path: { type: 'string' }, word_count: { type: 'number' }, open_questions: { type: 'array', items: { type: 'string' } } }, required: ['draft_path', 'word_count'] } })))
const draftsOk = drafts.filter(Boolean)
log(`drafts: ${draftsOk.map(d => `${d.draft_path} (${d.word_count}w)`).join(', ')}`)

const CRITERIA = 'Score each draft 0-10 on: (1) OWNER FIDELITY — every owner statement quoted exactly and attributed, no invented owner decision, nothing the owner said is missing (check against sed -n 126,200p .agi/nodes/doc/l4-owner-decisions.md); (2) COMPLETENESS — all seven sections present, a 2+2+1 card for EVERY seat listed, closed decision sets, every tells has target+trigger; (3) ENFORCEABILITY — rules are checks with real hooks (verify 3 anchors with grep); (4) ECONOMY — minimal owner decisions, Claude spend conserved, staccato cadence explicit; (5) EXECUTABILITY — first rounds are serialised pi/OpenRouter with ceilings and dependencies and respect survival mode. Total 50.'
phase('Judge')
const judges = await parallel([1, 2].map(i => () =>
  agent(`${COMMON}\n\nYou are judge ${i} of 2 for three L4 plan drafts: ${draftsOk.map(d => d.draft_path).join(', ')}. ${CRITERIA} ${i === 1 ? 'Read the drafts in the listed order.' : 'Read the drafts in REVERSE order to counter position bias.'} For each draft give the five scores, a total, and <=80 words on its single best idea worth grafting and its worst defect. Write your full notes to ${S}/judge/judge${i}.md. Return JSON.`,
    { label: `judge:${i}`, phase: 'Judge', model: 'opus', effort: 'high',
      schema: { type: 'object', properties: { scores: { type: 'array', items: { type: 'object', properties: { draft_path: { type: 'string' }, total: { type: 'number' }, best_idea: { type: 'string' }, worst_defect: { type: 'string' } }, required: ['draft_path', 'total'] } }, notes_path: { type: 'string' } }, required: ['scores'] } })))
const judgesOk = judges.filter(Boolean)
const totals = {}
for (const j of judgesOk) for (const s of j.scores) totals[s.draft_path] = (totals[s.draft_path] || 0) + s.total
const ranked = Object.entries(totals).sort((a, b) => b[1] - a[1])
log(`ranking: ${ranked.map(([p, t]) => `${p.split('/').pop()}=${t}`).join(' > ')}`)
const winner = ranked.length ? ranked[0][0] : (draftsOk[0] && draftsOk[0].draft_path)
const grafts = judgesOk.flatMap(j => j.scores.map(s => `${s.draft_path.split('/').pop()}: best=${s.best_idea || ''} worst=${s.worst_defect || ''}`)).join('\n')

phase('Synthesize')
const synth = await agent(`${COMMON}\n\nSynthesize the FINAL L4 plan body. Winner draft: ${winner}. Other drafts: ${draftsOk.map(d => d.draft_path).filter(p => p !== winner).join(', ')}. Judges' notes: ${S}/judge/judge1.md and judge2.md; their one-line verdicts:\n${grafts}\n\nStart from the winner, graft the best ideas of the runners-up, remove every defect the judges named, and re-verify every owner quote against sed -n '126,200p' .agi/nodes/doc/l4-owner-decisions.md (exact bytes). Keep the seven-section structure exactly:\n${STRUCTURE}\n\nTarget length: as long as needed to be complete, as short as possible to be a bootstrap — prefer tables over prose. Write the final body to ${S}/final/l4-plan.md and the section-6 open questions ALSO as a standalone list with recommendations to ${S}/final/banked-questions.md (one item per line: "Q: ... | REC: ..."). Return JSON.`,
  { label: 'synthesize', phase: 'Synthesize', model: 'opus', effort: 'high',
    schema: { type: 'object', properties: { plan_path: { type: 'string' }, questions_path: { type: 'string' }, word_count: { type: 'number' }, seats_carded: { type: 'array', items: { type: 'string' } } }, required: ['plan_path', 'questions_path', 'word_count'] } })
log(`final: ${synth && synth.plan_path} (${synth && synth.word_count}w)`)

const LENSES = [
  { key: 'owner-fidelity', task: `Every string presented as owner text (quotes, "owner:", "verbatim") must appear byte-for-byte in a node file (.agi/nodes/doc/l4-owner-decisions.md or .agi/nodes/doc/l3-command-ladder-brief.md or a vision/goal/moral node) — verify each with grep -F; fix any drift to the exact bytes or relabel it (prime proposal). Every claim of the form "the owner decided/said/wants" must be traceable the same way. Nothing the owner said in the L4 PLAN section (lines 126-200) may be silently dropped or contradicted — add what is missing.` },
  { key: 'mechanism-reality', task: `Every file path, flag, field, command, node id, schema name and function the plan names must EXIST in the repo (verify with ls / grep) or be explicitly marked PROPOSED / NEW. Every file:line anchor must point at what it claims. Every "existing hook" must really exist. Fix or relabel; never leave a confident wrong pointer.` },
  { key: 'completeness-constraints', task: `Check: all seven sections present with the exact headings; a 2+2+1 card for EVERY seat named in section 2's list (belam, sanctuary-master, master-sensei, liaison, self-perpetuating, alive, all-is-one, sanctuary-director, goal director-kid, draft director-kid, review director-kid, pi parent, pi kid) with exactly 2 tracks / 2 tells (each with target AND trigger) / 1 decides that is a CLOSED set; section 5 rounds are serialised, pi/OpenRouter, each with a ceiling and a testable_claim-shaped assignment, and none dispatches before owner approval; survival mode is stated as in force; no node deletion anywhere; section 6 questions each carry a recommendation; the standalone banked-questions.md matches section 6 exactly. Fix in place.` },
]
phase('Verify')
const verdicts = await parallel(LENSES.map(l => () =>
  agent(`${COMMON}\n\nYou verify and FIX IN PLACE the final L4 plan at ${S}/final/l4-plan.md (and ${S}/final/banked-questions.md). You may edit files under ${S}/final only. Lens ${l.key}: ${l.task}\n\nWork through the whole document, not a sample. Return JSON listing what you fixed and what you could not fix (with the reason).`,
    { label: `verify:${l.key}`, phase: 'Verify', model: 'opus', effort: 'high',
      schema: { type: 'object', properties: { fixed: { type: 'array', items: { type: 'string' } }, left: { type: 'array', items: { type: 'string' } } }, required: ['fixed', 'left'] } })))

return {
  maps: mapsOk.map(m => m.map_path),
  drafts: draftsOk.map(d => d.draft_path),
  ranking: ranked,
  final: synth,
  verify: verdicts.filter(Boolean).map((v, i) => ({ lens: LENSES[i].key, fixed: v.fixed.length, left: v.left })),
}