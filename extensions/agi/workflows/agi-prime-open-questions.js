export const meta = {
  name: 'prime-l4v-open-questions',
  description: 'Read-only verification of three prime-tier open questions: commit-guard inertness, seat-branch ahead=4 shape, suite-lock placement',
  phases: [
    { title: 'Investigate', detail: 'one read-only agent per question' },
    { title: 'Refute', detail: 'adversarial check of each finding' },
  ],
}

const RO = `
HARD RULES for this task — you are a READ-ONLY investigator for the Prime director of the agi graph.
- NEVER write, edit or create any file. NEVER use write.py, Edit or Write. NEVER git commit, git add, git checkout, git merge, git push.
- NEVER run pytest or 'commands.py run verify' or 'driver.sh' — the suite window is held by the Prime and a bare pytest walks past its lock. Running one is the exact defect under investigation.
- NEVER dispatch agents (dispatch.py) and never spawn anything.
- Allowed: git log / git show / git diff / git merge-base / git rev-list, cat, sed -n, grep, find, ls, and python3 -c for PARSING only.
- Repo: /home/ubuntu/work/agi, branch season/s2. The graph is .agi/. The engine is extensions/agi/.
- Trap 0ae: 'git diff season/s2..BRANCH' is NOT a change list — always diff against the MERGE-BASE (git merge-base season/s2 BRANCH), never against a moved tip.
- Trap 0ab: when a grep comes back clean, check the CALLEE before concluding a mechanism is absent.
- GREP PROVES PRESENCE; ONLY A STRUCTURAL ASSERTION PROVES SHAPE. Quote the exact lines with file:line for every claim.
- If you cannot ground a claim in bytes you actually read, say so explicitly rather than inferring.
`

const FINDING = {
  type: 'object',
  properties: {
    answer: { type: 'string', description: 'Direct answer to the question, 1-3 sentences.' },
    evidence: {
      type: 'array',
      description: 'Each item: file:line plus the exact quoted bytes that ground the claim.',
      items: { type: 'string' },
    },
    still_live: { type: 'boolean', description: 'True if the hazard/condition described in the question is still true on this tree today.' },
    recommendation: { type: 'string', description: 'The single smallest correct action, or "none".' },
    ungrounded: { type: 'string', description: 'Anything you could NOT verify, stated plainly. "none" if all grounded.' },
  },
  required: ['answer', 'evidence', 'still_live', 'recommendation', 'ungrounded'],
}

const VERDICT = {
  type: 'object',
  properties: {
    refuted: { type: 'boolean', description: 'True if the finding is wrong, overclaimed, or ungrounded.' },
    why: { type: 'string' },
    corrected: { type: 'string', description: 'The corrected claim if refuted, else "n/a".' },
  },
  required: ['refuted', 'why', 'corrected'],
}

const QUESTIONS = [
  {
    key: 'commit-guard',
    label: 'commit-guard-inert',
    prompt: `${RO}

QUESTION 1 — is the agent git-commit guard still INERT on this repo?

An audience request dated 2026-09-07 (three days old, in .agi/sessions/inbox/prime.md) claimed:
"hooks/agent-git/pre-commit scopes itself by comparing git rev-parse --show-toplevel against AGI_PROJECT_ROOT; dispatch.py:755 sets AGI_PROJECT_ROOT to locations.find_project_root() = /home/ubuntu/work/agi/.agi while .git is at /home/ubuntu/work/agi, so the != test is always true and the hook always exits 0 (allow). claude-code kids are masked by the adapter deny-rule; pi kids have no belt at all."

Determine whether that is STILL TRUE on this tree TODAY. Specifically:
(a) Find the pre-commit hook file(s) under the engine (look for hooks/agent-git/, and anything installing them). Read the scoping comparison verbatim.
(b) Find where AGI_PROJECT_ROOT is set for spawned agents (grep dispatch.py and any spawn path). Read the exact assignment.
(c) Determine whether find_project_root() returns the .agi directory or the repo root today (read bin/locations.py — do not guess).
(d) Check whether some OTHER belt now covers pi kids: write_guard.py, the 'tier kid may not commit' guard in cli.py, per-kid branching (--branch), or anything else. Trap 0ab applies — check the callee.
Then state whether a pi kid on this tree can still land a raw 'git commit -A'.`,
  },
  {
    key: 'seat-branch',
    label: 'seat-branch-ahead-4',
    prompt: `${RO}

QUESTION 2 — what are the 4 commits on seat/sanctuary-director@s2 that are not on season/s2?

Facts already measured by the Prime: 'git rev-list --count season/s2..seat/sanctuary-director@s2' = 4, and 'git rev-list --count seat/sanctuary-director@s2..season/s2' = 4.

The predecessor's handoff card contains a CONTRADICTION and your job is to settle it with bytes: one line says "MERGE-UPS 5-15 ALL ACCEPTED (latest 762a496c2)" and a bullet immediately below says "MERGE-UP 13 IS PENDING on seat/sanctuary-director@s2: 306b77bb6 (the conditional pre-flight, 59 tests, 6 new none edited)".

Determine, using the MERGE-BASE (trap 0ae):
(a) List the 4 commits (hash, author date from 'git log --format', subject) that are ahead.
(b) Is 306b77bb6 among them, or is it already an ancestor of season/s2? Answer with 'git merge-base --is-ancestor' semantics, stated explicitly.
(c) Classify the 4: are they FINISHED work awaiting a merge-up, or IN-FLIGHT commits of a round still running (round L4.104 has live per-spawn keys right now)? Ground the classification in the commit subjects/bodies and in whether each round's node/experiment files look complete.
(d) Name the files each commit touches (name only, do not read them all) and flag anything touching .agi/nodes/ under a deprecated path, anything touching .geometry/, and any deletion.
Set still_live = true only if there is genuinely finished, unmerged work the Prime should be reviewing NOW.`,
  },
  {
    key: 'suite-lock',
    label: 'suite-lock-placement',
    prompt: `${RO}

QUESTION 3 — where does the suite lock live, and where do the tests actually run?

The Prime must rule on this framing, raised by sanctuary-director gen VI: "anything that guards a resource by locking one of its callers guards nothing against the others." The observed defect: 'commands.py run verify-suite' acquires .agi/sessions/verify-suite.lock, but a bare 'pytest extensions/agi/tests/' walks straight past it, and one did during the previous session (2542 passed, no lock, no stamp).

Determine:
(a) Exactly where the lock is acquired and released — file:line, the lock file path, and whether it is advisory (flock) or a lockfile-with-pid. Read verification.py and commands.py.
(b) Every code path that can run the engine's tests. Enumerate them: commands.py run verify --suite, verification.py --suite, anything in driver.sh, any cron line in .agi/nodes/.geometry/crons.md, any Makefile/CI. For each, say whether it passes through the lock.
(c) Does extensions/agi/tests/ have a conftest.py today? If yes, what session-scoped fixtures does it define? Quote its top-level content list.
(d) Assess the minimal correct fix WITHOUT implementing it: could a session-scoped autouse fixture in extensions/agi/tests/conftest.py acquire the same lock so a BARE pytest also respects it? Name the concrete obstacles you can see in the bytes (e.g. does anything already run pytest inside pytest; would a nested acquisition self-deadlock; does the test suite itself invoke commands.py run verify-suite as a subprocess anywhere — grep for that, it would self-deadlock).
Your recommendation should be the smallest change that moves the lock to the resource, or a statement that it cannot be done safely and why.`,
  },
]

const results = await pipeline(
  QUESTIONS,
  q => agent(q.prompt, { label: q.label, phase: 'Investigate', schema: FINDING }),
  (finding, q) => {
    if (!finding) return null
    return agent(`${RO}

ADVERSARIAL CHECK. Another investigator answered this question about the agi repo:

QUESTION KEY: ${q.key}
ANSWER: ${finding.answer}
still_live: ${finding.still_live}
EVIDENCE THEY CITED:
${(finding.evidence || []).map(e => '- ' + e).join('\n')}
RECOMMENDATION: ${finding.recommendation}
THEY COULD NOT VERIFY: ${finding.ungrounded}

Try to REFUTE it. Go back to the actual bytes at every file:line they cited and check that the quoted text is really there and really says what they claim. Look specifically for:
- a claim that rests on a grep coming back clean without checking the callee (trap 0ab);
- a diff taken against a moved tip instead of the merge-base (trap 0ae);
- presence asserted where the real property is validity or shape;
- an inference run backwards (a dead pid proves stopped; a live pid proves nothing).
Default to refuted=true if you are uncertain. If it holds up, say refuted=false and say which single piece of evidence is load-bearing.`,
      { label: `refute:${q.key}`, phase: 'Refute', schema: VERDICT })
      .then(v => ({ key: q.key, finding, verdict: v }))
  },
)

return results.filter(Boolean)
