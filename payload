export const meta = {
  name: 'agi-round-review',
  description: 'Review one agi round: per-target parent/kid outputs with claim re-verification, plus global repo checks',
  phases: [{ title: 'Review', detail: 'one reviewer per target + one global checks agent' }],
}
const iter = args.iter
const targets = args.targets
const RULES = `HARD RULES: you are READ-ONLY on this repo. Never run git commit/push/add/stash/checkout/reset, never run grid.py, never edit or create any file under .agi/nodes or anywhere in the repo, never run write.py. You may only READ files and run read-only inspection commands named below. Work from /home/ubuntu/work/agi. Return raw structured data via the StructuredOutput tool; no prose report.`
const TARGET_SCHEMA = {
  type: 'object',
  properties: {
    hypothesis: { type: 'string' },
    parent_agent: { type: 'string' },
    kid_agents: { type: 'array', items: { type: 'string' } },
    experiment_ids: { type: 'array', items: { type: 'string' } },
    verdict: { type: 'string' },
    confidence: { type: 'string' },
    evidence_runs: { type: 'string', description: 'the evidence_runs frontmatter value as written' },
    parent_accepted: { type: 'array', items: { type: 'string' }, description: 'parent Accepted lines, verbatim, trimmed' },
    parent_demoted: { type: 'array', items: { type: 'string' } },
    kid_struggles: { type: 'string' },
    kid_caveats: { type: 'string' },
    kid_feeling: { type: 'string' },
    files_changed: { type: 'array', items: { type: 'string' }, description: 'engine files this target changed (from git status/diff), not node files' },
    verify_reran: { type: 'array', items: { type: 'object', properties: { cmd: { type: 'string' }, ok: { type: 'boolean' }, note: { type: 'string' } }, required: ['cmd', 'ok', 'note'] } },
    overclaims: { type: 'array', items: { type: 'string' }, description: 'claims in the experiment body you could not reproduce, or that contradict repo reality' },
    open_gaps: { type: 'array', items: { type: 'string' }, description: 'what the brief asked for that is still not built' },
    summary: { type: 'string', description: 'max 60 words' },
  },
  required: ['hypothesis', 'parent_agent', 'experiment_ids', 'verdict', 'parent_accepted', 'parent_demoted', 'files_changed', 'verify_reran', 'overclaims', 'open_gaps', 'summary'],
}
const GLOBAL_SCHEMA = {
  type: 'object',
  properties: {
    git_status: { type: 'array', items: { type: 'string' }, description: 'git status --short lines' },
    diff_stat_tail: { type: 'string' },
    links_broken: { type: 'integer' },
    links_line: { type: 'string' },
    goals_check_ok: { type: 'boolean' },
    goals_check_line: { type: 'string' },
    guard_output: { type: 'string', description: 'write_guard.py check output, empty if silent' },
    suite_passed: { type: 'integer' },
    suite_failed: { type: 'integer' },
    suite_skipped: { type: 'integer' },
    suite_failures: { type: 'array', items: { type: 'string' }, description: 'failing test ids, if any' },
    unexpected_files: { type: 'array', items: { type: 'string' }, description: 'untracked files that are neither new nodes under .agi/nodes nor engine/test files' },
    summary: { type: 'string', description: 'max 50 words' },
  },
  required: ['git_status', 'links_broken', 'goals_check_ok', 'guard_output', 'suite_passed', 'suite_failed', 'suite_skipped', 'suite_failures', 'unexpected_files', 'summary'],
}
const reviewPrompt = (t) => `${RULES}
You review the agi graph round iter-${iter}, target ${t.hyp} (tmux window ${t.window}).
1. Read the brief: .agi/nodes/hypothesis/${t.hyp.replace('hypothesis:', '')}.md (the Agent Notes + ADDENDUM lines are the BUILD spec).
2. Under .agi/sessions/iter-${iter}/ find the parent dir whose brief/context/output names ${t.hyp} (grep -l "${t.hyp}" .agi/sessions/iter-${iter}/*/output.log .agi/sessions/iter-${iter}/*/*.md 2>/dev/null). From that parent's output.log extract the Accepted / Demoted lines verbatim and the kid agent ids. Also read the round log .agi/sessions/iter-${iter}/${t.window}.log if present.
3. Find the new experiment node(s) for this target: grep -l "${t.hyp}" .agi/nodes/experiment/*.md, keep those untracked or modified per git status --short. Read each: frontmatter verdict, confidence, evidence_runs, the body, and the kid's struggles/caveats/feeling lines (also in the kid's output.log under .agi/sessions/iter-${iter}/<kid>/).
4. RE-VERIFY the claims: run the VERIFY commands the brief and the experiment body name, as long as they are read-only (dry runs, --help, pytest on the specific test files named — run pytest only on those files, never the whole suite). Record each command, whether it reproduced the claimed output, and a short note. Check with git diff which engine files changed and whether the tests that were claimed red-first exist and pass.
5. List overclaims (claims not reproduced) and open_gaps (what the brief asked for that is still not built).
Be exact and terse. Verbatim lines trimmed to 200 chars.`
const globalPrompt = `${RULES}
Global checks for agi round iter-${iter}, in this order, from /home/ubuntu/work/agi (each is read-only or writes only derived files the round loop expects):
1. git status --short  (all lines) and git diff --stat | tail -1
2. python3 extensions/agi/bin/links.py links   -> the line with 'resolved' and 'broken'; broken count
3. python3 extensions/agi/bin/snapshot-goals.py --render --check  -> exit code 0 means ok; capture the last line
4. python3 extensions/agi/bin/write_guard.py check  -> capture all output (empty = silent = good)
5. python3 extensions/agi/bin/commands.py run tests  -> the pytest summary line: passed/failed/skipped counts and failing test ids if any (takes ~2 min)
6. Untracked files: classify each; report as unexpected anything that is not a new node file under .agi/nodes/ and not a file under extensions/ skills/ src/ tests.
Return the numbers exactly as printed.`
const ADVISOR_SCHEMA = {
  type: 'object',
  properties: {
    agents: { type: 'array', items: { type: 'object', properties: {
      agent_id: { type: 'string' }, tier: { type: 'string' }, target: { type: 'string' }, harness: { type: 'string' },
      finished: { type: 'boolean' }, num_turns: { type: 'integer' }, cost_usd: { type: 'number' },
      report_gist: { type: 'string', description: 'the agent final report compressed to <=80 words, keeping node ids, file:line cites and numbers' },
      nodes_minted: { type: 'array', items: { type: 'string' } },
      done_line: { type: 'string' }, caveats: { type: 'string' }, struggles: { type: 'string' },
      current_activity: { type: 'string', description: 'for a still-running agent: its last 3 tool uses in <=40 words' },
    }, required: ['agent_id', 'tier', 'finished', 'report_gist', 'nodes_minted'] } },
    room_posts: { type: 'array', items: { type: 'object', properties: { ts: { type: 'string' }, from: { type: 'string' }, gist: { type: 'string', description: '<=45 words' } }, required: ['ts', 'from', 'gist'] } },
    banked_for_prime: { type: 'array', items: { type: 'string' }, description: 'decisions or questions the agents say the prime or owner must take, one line each' },
    defects_found: { type: 'array', items: { type: 'string' }, description: 'each: defect, file:line cite, which g15 brief it belongs to or NEW' },
    gate_progress: { type: 'string', description: 'progress toward: one short-term subgoal under goal:g15 closed with a judged outcome and no human hand on a node; <=60 words' },
  },
  required: ['agents', 'room_posts', 'banked_for_prime', 'defects_found', 'gate_progress'],
}
const advisorPrompt = (aiter, since) => `${RULES}
Summarise the live ladder run under .agi/sessions/iter-${aiter}/ for the prime director. For every agent dir a00-*/ there: read agent.json (tier, target, harness); if output.log has a line with "type":"result", the agent finished — parse that JSON line (fields result, num_turns, total_cost_usd) and compress the result text to a gist keeping node ids, file:line cites and numbers, plus the DONE/caveats/struggles lines if present; if not finished, read the last ~40 lines of output.log and describe its current activity. List nodes each agent minted (grep the .agi/nodes tree for edited_by or authored ids, and git status --short untracked node files). Read every room file .agi/sessions/*/comms/room/tier3-quorum.md and summarise each post with ts >= ${since} (ts, from, gist). Collect: banked_for_prime (anything the agents say the prime/owner must decide), defects_found (with file:line and which hypothesis brief under goal:g15 it maps to — grep .agi/nodes/hypothesis/l3-*.md titles — or NEW), and gate_progress. Be terse and exact.`
phase('Review')
const jobs = [
  () => agent(globalPrompt, { label: 'global-checks', phase: 'Review', schema: GLOBAL_SCHEMA, model: 'sonnet', effort: 'low' }),
  ...targets.map(t => () => agent(reviewPrompt(t), { label: `review:${t.window}`, phase: 'Review', schema: TARGET_SCHEMA, model: 'sonnet', effort: 'medium' })),
]
if (args.advisor_iter) jobs.push(() => agent(advisorPrompt(args.advisor_iter, args.since || '2026-09-07T04:40'), { label: `ladder:${args.advisor_iter}`, phase: 'Review', schema: ADVISOR_SCHEMA, model: 'sonnet', effort: 'medium' }))
const results = await parallel(jobs)
return { iter, global: results[0], targets: results.slice(1, 1 + targets.length), ladder: args.advisor_iter ? results[1 + targets.length] : null }