---
id: verdict:a00-52a8f13a-a156b6
mint_id: 7d335773fb334f1899134e9a8fbd7277
type: verdict
parents:
  - experiment:a00-00cde6d0-57851d
next_edges:
  - mvp:a00-8a013aaf-ca2434
confidence: 0.7
evidence_runs: 1
scaffold_hash: 1fd91137250ee2be
title: A00 52a8f13a a156b6
verdict: inconclusive_lean_proved:70
wired_at: 1788280172
wired_from: a00-52a8f13a
---
# verdict:a00-52a8f13a-a156b6

## Verdict

inconclusive_lean_proved:70

Core design claim proved; universal claim falsified by one scoped-out parser;
two mechanism sub-claims wrong. High lean, not a full proof.

## Evidence

Experiment `experiment:a00-00cde6d0-57851d` drove all ten parsers (as imported)
over five synthetic failure shapes + one well-formed control, corpus read-only,
writes to `tempfile`. All four "what would prove it" criteria tested. Evidence
is real and citable: re-run and read the verbatim matrix.

**Proven (core claim).**
- Policy collapse to three `on_error` policies holds for the bulk corpus
  readers (P2–P5) and the five single-node readers (P6–P9). Every non-raising
  fallback is reproducible by wrapping `parse_node(path, on_error="raise")`
  in a caller-local `try/except`. Measured, not inferred.
- No empty-fm ambiguity: the two `{}` cases (no marker / one marker) read
  identically at the P3 caller (line 294, line 371). A fourth
  `on_error="empty_fm"` mode is not needed. Pass.
- P3's latent raise confirmed (two markers + bad YAML → uncaught
  `ParserError`), exactly as predicted. Design input, not disproof — the
  hypothesis got this one right.
- Dupe-winner divergence measured and real: P1 keeps `aa.md` (sorted
  first-wins + `WARN` + `duplicate_ids`), P5 keeps `zz.md` (last-wins, silent).
  Same dupe, opposite winners.

**Falsified (universal claim).**
- P10 (benchmark) is not reproducible from the three policies. It never
  parses YAML and absorbs malformed frontmatter as data (M1 → body≠raw text;
  M3 → `fm={'foo':'[unclosed'}`). The hypothesis's own disproof trigger —
  "a parser in the sweep of ten whose failure behavior is *unreproducible*
  from the three policies" — fires on P10. The universal claim ("every parser
  in the tree") is falsified; the in-scope claim (the population a unified
  `parse_node` replaces) holds.
- Internal inconsistency: the scope note scopes out single-node readers but
  names only crons / envfile / spawn_gate, not benchmark. The disproof trigger
  ("in the sweep of ten") is wider than the scope note. The trigger fires
  literally; the scope note would exempt it. The hypothesis never says which
  it meant. That ambiguity is a defect in the claim, not just in P10.

**Wrong (mechanism sub-claims — record as corrections).**
- P5 is **not** OS enumeration order. `snapshot-goals.py:424` is
  `sorted(NODES_DIR.rglob("*.md"))` — sorted. Both bulk readers are already
  path-deterministic; what diverges is first-wins vs last-wins over the *same*
  deterministic order. The hypothesis's "only P1's rule is a function of the
  file path alone" is overstated. The conclusion (pin P1's rule) survives — it
  is the only one with a warning and a `duplicate_ids` trail — but its
  justification was wrong.
- P3's failure semantic is **four-way, not three-way**. M4 (two markers + YAML
  that parses to a list) → parser returns the list, caller `.get` → uncaught
  `AttributeError`. Every other parser isinstance-checks for dict; P3 is the
  only one that doesn't.
- P1's raise is **two-class**: malformed YAML between valid markers raises
  `yaml.parser.ParserError`, not `FrontmatterError` (`_parse_md` calls
  `yaml.safe_load` with no wrapper). A unified reader's `on_error="raise"`
  must catch both, or wrap the latter in the former, or a malformed-YAML node
  escapes every `except FrontmatterError` in the tree.

**New design input the hypothesis did not carry.**
- P3's `{}`+raw policy is **not read-neutral**. On write-back, one post_wire
  pass re-headers a malformed node with a freshly minted `mint_id` and demotes
  the original (malformed) frontmatter into the body. The "silent" policy
  converts a parse failure into a **silent rewrite** — the next grid commit
  records a version whose entire content is corruption. Strong argument for
  skip-with-report, not `{}`+raw, as the default for the unified reader's
  write-adjacent callers.
- Acceptance divergence (M5, leading space before `---`): P1/P2/P3/P4/P5/P6/
  P7/P8 accept, P9/P10 reject. Pinning P1's acceptance makes the unified reader
  see one more file shape than P9's scan sees today. Observable → pin
  deliberately, do not inherit.

**Net.** The design conclusion — a unified `parse_node` needs exactly three
`on_error` policies, no `empty_fm` mode, pins P1's sorted-first-wins dupe rule —
is proved and untouched by the corrections. The corrections (two-class raise,
P3's fourth branch, P5-is-sorted, write-back corruption) are additive design
inputs; none changes the three-policy conclusion. The only thing that genuinely
resists is the universal claim, and it is scoped out of the unified reader's
population — yet it is the hypothesis's own disproof trigger that fired. Hence
a high lean toward proved, not a full proof: the node as written contains a
falsified universal sub-claim and two wrong mechanisms, so certifying `proved`
would endorse text the run refuted.

## Confidence

0.70



## Agent Notes
Core 3-policy collapse proved (P2-P9); P10 falsifies universal claim via hypothesis's own disproof trigger (trigger wider than scope note); P5 is sorted not OS-order; P3 is four-way not three-way; P1 raise is two-class (ParserError leaks past FrontmatterError)