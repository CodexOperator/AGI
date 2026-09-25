export const meta = {
  name: "agi-recovery-survey",
  description: "Authored via workflow.py author (Prime belam gen 21, 2026-09-16: a re-seated Prime learns a bounded window by NAME (survey:{key} -> adversarial refute:{key} over args.areas [{key,brief}]) instead of reading the bytes itself)",
  phases: [
    { title: "Survey" },
    { title: "Refute" },
  ],
}

const MODEL = (args && args.model) || "sonnet"
const EFFORT = (args && args.effort) || "high"

const fill = (t, ctx) => String(t).replace(/\{([A-Za-z_][A-Za-z0-9_]*)\}/g, (_, k) => (k in ctx && ctx[k] != null ? ctx[k] : ''))

const ITEMS = (args && args["areas"]) || []
const ROOT = (args && args.project_root) || '.'

const SURVEY_TMPL = "You are a recovery reader for the Prime director of the agi graph, who was re-seated on 2026-09-16 after two dead sessions and must learn what happened since commit c062cfc18 without reading the bytes itself. READ-ONLY on the agi repo at /" + ROOT + " (branch season2/main): never edit, commit, push, stash or checkout; never run the test suite, rotate.py, dispatch.py, send.py, write.py, workflow.py or any tmux command; never ask a human (there is none). Node ids map to files: goal:g14.3 = .agi/nodes/goal/g14.3.md; hypothesis:<slug> = .agi/nodes/hypothesis/<slug>.md; experiment:<id> = .agi/nodes/experiment/<id>.md; retired siblings live under .agi/nodes/deprecated/<type>/; config:<name> = .agi/nodes/.geometry/<name>.md; owner verbatim = .agi/nodes/doc/l4-owner-decisions.md (grep -n it, read ranges with sed -n, never whole). Tag every number MEASURED (the command + the value) or INFERRED; never stamp a time from a felt clock; a grep proves presence, only a structural read proves shape.\n\nAREA {key}: {brief}\n\nRead the named sources (git log/show/diff --stat, sed -n ranges, grep -n) and return: findings (max 1400 chars: one line per fact, newest first, each with its commit sha or file:line), numbers (max 400 chars: the counts/ids/shas the Prime must carry forward), open_items (max 700 chars: unfinished, blocked or contradictory things, each with where it is recorded), sources_read (max 300 chars: the commands/files you actually read)."
const SURVEY_SCHEMA = {"type": "object", "properties": {"findings": {"type": "string", "description": "max 1400 chars"}, "numbers": {"type": "string", "description": "max 400 chars"}, "open_items": {"type": "string", "description": "max 700 chars"}, "sources_read": {"type": "string", "description": "max 300 chars"}}, "required": ["findings", "numbers", "open_items", "sources_read"]}
const REFUTE_TMPL = "You are an ADVERSARIAL VERIFIER for the Prime director of the agi graph. READ-ONLY on the agi repo at /" + ROOT + " (branch season2/main): never edit, commit, push, stash or checkout; never run the test suite, rotate.py, dispatch.py, send.py, write.py, workflow.py or any tmux command; never ask a human (there is none). Node ids map to files: goal:g14.3 = .agi/nodes/goal/g14.3.md; hypothesis:<slug> = .agi/nodes/hypothesis/<slug>.md; experiment:<id> = .agi/nodes/experiment/<id>.md; retired siblings live under .agi/nodes/deprecated/<type>/; config:<name> = .agi/nodes/.geometry/<name>.md; owner verbatim = .agi/nodes/doc/l4-owner-decisions.md (grep -n it, read ranges with sed -n, never whole). Tag every number MEASURED (the command + the value) or INFERRED; never stamp a time from a felt clock; a grep proves presence, only a structural read proves shape.\n\nA reader surveyed AREA {key} ({brief}) and reported:\nFINDINGS: {findings}\nNUMBERS: {numbers}\nOPEN ITEMS: {open_items}\nSOURCES: {sources_read}\n\nRe-derive every MEASURED claim from the bytes yourself (git show <sha> --stat, sed -n on the file, grep -n the node). Default to refuted when you cannot reproduce a claim. Return: verified (max 600 chars: claims you reproduced, each with the command), refuted (max 600 chars: claims that failed, with what the bytes say instead), corrected_digest (max 1400 chars: the reader's findings rewritten with your corrections applied, newest first, shas kept -- this is the only text the Prime reads), owner_line (max 300 chars: one plain sentence a human owner should hear about this area)."
const REFUTE_SCHEMA = {"type": "object", "properties": {"verified": {"type": "string", "description": "max 600 chars"}, "refuted": {"type": "string", "description": "max 600 chars"}, "corrected_digest": {"type": "string", "description": "max 1400 chars"}, "owner_line": {"type": "string", "description": "max 300 chars"}}, "required": ["verified", "refuted", "corrected_digest", "owner_line"]}

phase("Survey")
const results = await pipeline(
  ITEMS,
  it => agent(fill(SURVEY_TMPL, it), { label: `survey:${it.key}`, phase: "Survey", schema: SURVEY_SCHEMA, model: MODEL, effort: EFFORT }),
  (finding, it) => {
    if (!finding) return null
    return agent(fill(REFUTE_TMPL, { ...it, ...finding }), { label: `refute:${it.key}`, phase: "Refute", schema: REFUTE_SCHEMA, model: MODEL, effort: EFFORT }).then(v => ({ key: it.key, finding, refute: v }))
  },
)
return results.filter(Boolean)
