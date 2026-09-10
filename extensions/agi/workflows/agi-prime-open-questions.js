export const meta = {
  name: "agi-prime-open-questions",
  description: "Authored via workflow.py author (L4.105 rewrite: one repeated investigate + one repeated refute through the author verb (hypothesis:l4-workflow-authoring-is-a-harness-tool))",
  phases: [
    { title: "Investigate" },
    { title: "Refute" },
  ],
}

const MODEL = (args && args.model) || "sonnet"
const EFFORT = (args && args.effort) || "medium"

const fill = (t, ctx) => String(t).replace(/\{([A-Za-z_][A-Za-z0-9_]*)\}\/g, (_, k) => (k in ctx && ctx[k] != null ? ctx[k] : ''))

const ITEMS = (args && args["questions"]) || []

const INVESTIGATE_TMPL = "You are a READ-ONLY investigator for the Prime director of the agi graph.\n\nHARD RULES: never write, edit or create any file. Never use write.py, Edit or Write. Never git commit/add/checkout/merge/push. Never run pytest or 'commands.py run verify' or 'driver.sh' (the suite window is held by the Prime). Never dispatch agents or spawn anything. Allowed: git log/show/diff/merge-base/rev-list, cat, sed -n, grep, find, ls, and python3 -c for PARSING only. Repo: /home/ubuntu/work/agi, branch season/s2. The graph is .agi/. The engine is extensions/agi/.\n\nGREP PROVES PRESENCE; ONLY A STRUCTURAL ASSERTION PROVES SHAPE. Quote the exact lines with file:line for every claim. If you cannot ground a claim in bytes you actually read, say so explicitly rather than inferring.\n\nTHE QUESTION YOU MUST INVESTIGATE (this is question key {key}):\n{question}\n\nRespond with EXACTLY ONE JSON object and nothing else, matching this schema: {\"answer\":\"direct answer, 1-3 sentences\",\"evidence\":[\"each: file:line plus the exact quoted bytes that ground the claim\"],\"still_live\":true,\"recommendation\":\"the single smallest correct action, or 'none'\",\"ungrounded\":\"anything you could NOT verify, stated plainly, else 'none'\"}."
const INVESTIGATE_SCHEMA = {"type": "object", "properties": {"answer": {"type": "string"}, "evidence": {"type": "array", "items": {"type": "string"}}, "still_live": {"type": "boolean"}, "recommendation": {"type": "string"}, "ungrounded": {"type": "string"}}, "required": ["answer", "evidence", "still_live", "recommendation", "ungrounded"]}
const REFUTE_TMPL = "You run the ADVERSARIAL CHECK on an investigator's finding about the agi repo (question key {key}).\n\nThe ORIGINAL QUESTION:\n{question}\n\nThe FINDING BEING CHECKED:\nANSWER: {answer}\nstill_live: {still_live}\nEVIDENCE CITED:\n{evidence}\nRECOMMENDATION: {recommendation}\nTHEY COULD NOT VERIFY: {ungrounded}\n\nTry to REFUTE it. Go back to the actual bytes at every file:line they cited and check that the quoted text is really there and really says what they claim. Look specifically for: a claim that rests on a grep coming back clean without checking the callee (trap 0ab); a diff taken against a moved tip instead of the merge-base (trap 0ae); presence asserted where the real property is validity or shape; an inference run backwards (a dead pid proves stopped; a live pid proves nothing). Default to refuted=true if you are uncertain. If it holds up, say refuted=false and which single piece of evidence is load-bearing.\n\nRespond with EXACTLY ONE JSON object and nothing else, matching this schema: {\"refuted\":true,\"why\":\"...\",\"corrected\":\"the corrected claim if refuted, else 'n/a'\"}."
const REFUTE_SCHEMA = {"type": "object", "properties": {"refuted": {"type": "boolean"}, "why": {"type": "string"}, "corrected": {"type": "string"}}, "required": ["refuted", "why", "corrected"]}

phase("Investigate")
const results = await pipeline(
  ITEMS,
  it => agent(fill(INVESTIGATE_TMPL, it), { label: `investigate:${it.key}`, phase: "Investigate", schema: INVESTIGATE_SCHEMA, model: MODEL, effort: EFFORT }),
  (finding, it) => {
    if (!finding) return null
    return agent(fill(REFUTE_TMPL, { ...it, ...finding }), { label: `refute:${it.key}`, phase: "Refute", schema: REFUTE_SCHEMA, model: MODEL, effort: EFFORT }).then(v => ({ key: it.key, finding, refute: v }))
  },
)
return results.filter(Boolean)
