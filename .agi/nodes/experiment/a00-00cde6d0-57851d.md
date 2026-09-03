---
id: experiment:a00-00cde6d0-57851d
mint_id: 8bbf5dcf28ed43dd98195cc0c4fa2a16
type: experiment
parents:
  - hypothesis:a00-6b4ad6b2-a60b78
next_edges:
  - verdict:a00-52a8f13a-a156b6
confidence: 0.75
evidence_runs: 1
scaffold_hash: 8c6538ac4c4faef4
title: A00 00cde6d0 57851d
verdict: inconclusive_lean_proved:75
wired_at: 1788279774
wired_from: a00-00cde6d0
---
# experiment:a00-00cde6d0-57851d

## Experiment

Differential failure-semantics run over all ten parsers named by the
hypothesis, testing its four "what would prove it" criteria. One script,
`/tmp/g13-policy-collapse.py` (path may not survive; method below, output
verbatim under Evidence), run 2026-09-01 from `/home/ubuntu/work/agi` with
`python3 /tmp/g13-policy-collapse.py`. Real corpus untouched; every write
went to a `tempfile.mkdtemp` dir.

**Synthetic shapes** (five failure cases, one well-formed control):
`W` well-formed; `M1` one marker (`---\nfoo: [unclosed\nno closing marker\n`);
`M2` no markers (`just text\n`); `M3` two markers + invalid YAML between
them; `M4` two markers + YAML that parses but is a **list** (`- a\n- b`);
`M5` leading space before the opening `---` (acceptance probe, not a failure).

**Parsers driven, as imported:** P1 `graph_core.persistence.frontmatter.load_node_file`;
P2 `graph_core.loader.load_directory` (one file per fresh dir); P3
`post_wire._read_frontmatter` (text in); P4 `stitch._parse_frontmatter` (text
in); P5 `snapshot-goals.load_existing_nodes` with `NODES_DIR` monkeypatched to
a one-file dir; P6 `crons._parse_frontmatter`; P7 `envfile._parse_frontmatter`;
P8 `verify_unified._read_frontmatter`; P9 `spawn_gate._read_frontmatter`;
P10 `benchmark._parse_frontmatter` (text in; `benchmark` imports an `ollama`
guard that `sys.exit(1)`s when the package is missing, so the script stubs
`sys.modules["ollama"]` first — the function under test is pure line-based
Python). **One extra shape the hypothesis did not anticipate:** `M4` — frontmatter
that is valid YAML but not a mapping.

**What happened.** All four criteria were tested; three passed, one passed
with a correction, and the run produced three findings the hypothesis did not
carry: (a) P1's own raise is a **two-class raise** — malformed YAML between
valid markers raises `yaml.parser.ParserError`, *not* `FrontmatterError`;
(b) P3's failure is **four-way**, not the three-way the hypothesis modeled —
`M4` slips through P3's parser as a list and explodes at the caller with
uncaught `AttributeError`; (c) P3's `{}+raw` policy is **not read-neutral** —
its caller writes the result back, and one post_wire pass re-headers a
malformed node with a freshly minted `mint_id` and demotes the original file
(its own `---` included) to body text.

### Criterion 1 — Policy collapse: 9/10, with one scoped exception

For M1/M2/M3/M4 the unified `parse_node`-as-P1 plus a caller-local
`except Exception` fallback reproduces: P2 (absent, silent), P3
(`{}, raw` — for M1/M2 only; M3/M4 raise, see below), P4 (`None`), P5
(absent, silent), P6/P7 (raise, re-wrapped in `CronsError`/`SecretsError`),
P8/P9 (`None`). All ten agree on `W`'s frontmatter.

**P10 (benchmark) is the one parser whose behavior is not reproducible from
the three policies** — the hypothesis's disproof trigger, but for a parser
itself scoped out of the unified reader's replacement population. It never
parses YAML, so it has no YAML failure class at all: on M1 it returns
`( {}, "no closing marker" )` (body ≠ raw text) and on M3 it returns
`( {"foo": "[unclosed"}, "body M3" )` — it absorbs malformed frontmatter as
*data*. Its sole consumer (`_build_judge_prompt`) reads only `parents` for
prompt decoration, so the garbage is invisible today; it becomes visible the
moment the corpus contains a malformed node with a `parents:` line. The
universal claim ("every parser in the tree") is falsified by P10; the
in-scope claim (the population a unified `parse_node` replaces) holds.

### Criterion 2 — No empty-fm ambiguity: pass, plus a write-side cost

P3 on M2 (no markers) and M1 (one marker) both return `fm={}`; both caller
sites read identical values — `confidence=None, verdict=None,
evidence_runs=None` at line 294, `next_edges=[]` at line 371. No branch
distinguishes "malformed" from "no frontmatter", so no `on_error="empty_fm"`
mode is needed. **But** the `{}+raw` fallback's cost is on the write side,
not the read side: `post_wire._write_node` (→ `snapshot-goals.write_frontmatter`)
run on P3's result for M1 produced:

```
'---\nmint_id: 6848715e8ba541359dd45cadb23a123e\n---\n\n---\nfoo: [unclosed\nno closing marker\n'
```

One wire pass re-headers the malformed node with a fresh minted `mint_id`,
drops its original (malformed) frontmatter into the body, and leaves it
malformed-in-a-new-way. The "silent" policy is therefore not benign: it
converts a parse failure into a **silent rewrite**, which the next grid
commit will record as a version whose entire content is corruption. Strong
design argument for `skip`-with-report over `{}+raw` as the default for the
unified reader's write-adjacent callers.

### Criterion 3 — P3's latent raise: confirmed, and P1 shares it

P3 on M3 raises `yaml.parser.ParserError` **uncaught** in `post_wire`, exactly
as the hypothesis predicted for the untested case. New: P1 shows the same gap —
`load_node_file` on M3 raises `ParserError`, not `FrontmatterError`, because
`_parse_md` calls `yaml.safe_load` with no wrapper. The unified reader's
`on_error="raise"` must catch **both** `FrontmatterError` and
`yaml.YAMLError` (or the reader must wrap the latter in the former), or a
malformed-YAML node escapes every `except FrontmatterError` in the tree.

### Criterion 3b — P3's fourth branch (M4, new)

P3's parser on M4 returns `fm=['a', 'b']` — `yaml.safe_load(...) or {}` keeps
a non-empty list — and the parser does **not** raise. The raise happens at the
caller: `.get("next_edges")` on a list → uncaught `AttributeError`. P3's
failure semantic is four-way: no marker → `{},raw`; one marker → `{},raw`;
two markers + bad YAML → `ParserError` (in parser); two markers + non-dict
YAML → `AttributeError` (at caller). Every other parser in the tree
isinstance-checks for dict; P3 is the only one that doesn't.

### Criterion 4 — Dupe-winner divergence: pass, with a correction to the mechanism

Injected a synthetic dupe pair (`nodes/x/aa.md` and `nodes/x/zz.md`, both
`id: t:dup`). Measured: **P1 keeps `aa.md`** (sorted first-wins) and prints
`WARN: duplicate node id 't:dup': kept ...aa.md, hidden ...zz.md` plus
`graph.duplicate_ids=[('t:dup', aa, zz)]`; **P5 keeps `zz.md`** (dict assign
over `sorted(rglob)` = sorted **last-wins**) silently. The two bulk readers
select **opposite winners for the same dupe** — the divergence is real and
needs no filesystem trick.

**Correction to the hypothesis:** P5 is *not* OS-enumeration-order.
`snapshot-goals.py:424` is `for md_path in sorted(NODES_DIR.rglob("*.md"))` —
sorted. Both bulk readers are already path-deterministic; what diverges is
first-wins vs last-wins over the *same* deterministic order. The hypothesis's
claim ("only P1's rule is a function of the file path alone") is therefore
overstated — P5's rule is path-deterministic too; the unified reader's real
job is picking *which* of the two deterministic rules survives, and P1's is
the only one with a warning and a `duplicate_ids` trail.

### Acceptance divergence (M5, bonus probe)

A file with one leading space before `---` is **accepted** by P1, P2, P3, P4,
P5, P6, P7, P8 but **rejected** by P9 (`text.startswith("---")`, no strip) and
P10 (`lines[0] != "---"`). Pinning P1's acceptance rule would make the unified
reader see one more shape of file than P9's scan sees today — observable, so
worth pinning deliberately rather than inheriting.

## Evidence

Full output, verbatim:

```
== T1: parser matrix on synthetic shapes ==
--- W: '---\nid: t:ok\nname: w\n---\n\nBody W.\n'
  P1: fm={'id': 't:ok', 'name': 'w'} body='Body W.'
  P2: loaded=1/1
  P3: fm={'id': 't:ok', 'name': 'w'} body='\n\nBody W.\n'
  P4: fm={'id': 't:ok', 'name': 'w'} body='\n\nBody W.\n'
  P5: present fm={'id': 't:ok', 'name': 'w'} body='\n\nBody W.\n'
  P6: fm={'id': 't:ok', 'name': 'w'}
  P7: fm={'id': 't:ok', 'name': 'w'}
  P8: fm={'id': 't:ok', 'name': 'w'}
  P9: fm={'id': 't:ok', 'name': 'w'}
  P10: fm={'id': 't:ok', 'name': 'w'} body='\nBody W.'
--- M1: '---\nfoo: [unclosed\nno closing marker\n'
  P1: RAISES FrontmatterError: md file missing closing '---'
  P2: loaded=0/1
  P3: fm={} body='---\nfoo: [unclosed\nno closing '
  P4: None
  P5: ABSENT (swallowed)
  P6: RAISES CronsError: /tmp/g13-policy-hnpo3jb6/M1.md: unterminated frontmatter blo
  P7: RAISES SecretsError: /tmp/g13-policy-hnpo3jb6/M1.md: unterminated frontmatter blo
  P8: fm=None
  P9: fm=None
  P10: fm={} body='no closing marker'
--- M2: 'just text\n'
  P1: RAISES FrontmatterError: md file missing opening '---'
  P2: loaded=0/1
  P3: fm={} body='just text\n'
  P4: None
  P5: ABSENT (swallowed)
  P6: RAISES CronsError: /tmp/g13-policy-hnpo3jb6/M2.md: no YAML frontmatter (expecte
  P7: RAISES SecretsError: /tmp/g13-policy-hnpo3jb6/M2.md: no YAML frontmatter (expecte
  P8: fm=None
  P9: fm=None
  P10: fm={} body='just text\n'
--- M3: '---\nfoo: [unclosed\n---\nbody M3\n'
  P1: RAISES ParserError: while parsing a flow sequence
  P2: loaded=0/1
  P3: RAISES ParserError: while parsing a flow sequence
  P4: None
  P5: ABSENT (swallowed)
  P6: RAISES CronsError: /tmp/g13-policy-hnpo3jb6/M3.md: malformed YAML frontmatter —
  P7: RAISES SecretsError: /tmp/g13-policy-hnpo3jb6/M3.md: malformed YAML frontmatter —
  P8: fm=None
  P9: fm=None
  P10: fm={'foo': '[unclosed'} body='body M3'
--- M4: '---\n- a\n- b\n---\nbody M4\n'
  P1: RAISES FrontmatterError: frontmatter must be a mapping, got list
  P2: loaded=0/1
  P3: fm=['a', 'b'] body='\nbody M4\n'
  P4: None
  P5: ABSENT (swallowed)
  P6: RAISES CronsError: /tmp/g13-policy-hnpo3jb6/M4.md: frontmatter must be a YAML m
  P7: RAISES SecretsError: /tmp/g13-policy-hnpo3jb6/M4.md: frontmatter must be a YAML m
  P8: fm=None
  P9: fm=None
  P10: fm={} body='body M4'
--- M5: ' ---\nid: t5\n---\nbody M5\n'
  P1: fm={'id': 't5'} body='body M5'
  P2: loaded=1/1
  P3: fm={'id': 't5'} body='\nbody M5\n'
  P4: fm={'id': 't5'} body='\nbody M5\n'
  P5: present fm={'id': 't5'} body='\nbody M5\n'
  P6: fm={'id': 't5'}
  P7: fm={'id': 't5'}
  P8: fm={'id': 't5'}
  P9: fm=None
  P10: fm={} body=' ---\nid: t5\n---\nbody M5\n'

== T1b: policy-collapse reproduction ==
policy = try: load_node_file(p)  except Exception: <caller fallback>
M1: unified raise -> fallback engaged
M2: unified raise -> fallback engaged
M3: unified raise -> fallback engaged
M4: unified raise -> fallback engaged
M5: unified raise -> parsed (no fallback needed)
fallbacks: P2=absent  P3=({},raw)  P4/P8/P9=None  P5=absent  P6/P7=re-raise  P10=({},raw)
  P10 measured M1 body 'no closing marker' vs raw-text fallback -> MISMATCH
  P10 measured M3 fm {'foo': '[unclosed'} vs {} fallback -> MISMATCH

== T2: empty-fm ambiguity (P3 caller key reads) ==
P3(no-markers)  fm={}
P3(one-marker)  fm={}
  no-markers: caller@294 reads confidence=None verdict=None evidence_runs=None | caller@371 reads next_edges=[]
  one-marker: caller@294 reads confidence=None verdict=None evidence_runs=None | caller@371 reads next_edges=[]

== T2b: write-back consequence of P3's ({}+raw) policy ==
file after one post_wire write-back pass:
'---\nmint_id: 6848715e8ba541359dd45cadb23a123e\n---\n\n---\nfoo: [unclosed\nno closing marker\n'

== T3: P3 latent raise (two markers, bad YAML) ==
P3(M3): RAISES ParserError: while parsing a flow sequence (uncaught in post_wire)
P1(M3): RAISES ParserError (NOT FrontmatterError) -> 'raise' policy is a two-class raise: FrontmatterError + ParserError

== T3b: M4 — YAML parses but is a list, not a dict ==
P3(M4): parser returns fm=['a', 'b'] (a list, no raise in parser)
P3(M4): caller .get -> RAISES AttributeError (4th P3 branch, uncaught)

== T4: dupe-winner divergence (same id, two files) ==
P1 load_directory: loaded=1 kept=t:dup pick=n/a
   stderr: "WARN: duplicate node id 't:dup': kept /tmp/g13-policy-hnpo3jb6/nodes/x/aa.md, hidden /tmp/g13-policy-hnpo3jb6/nodes/x/zz.md"
   graph.duplicate_ids: [('t:dup', PosixPath('/tmp/g13-policy-hnpo3jb6/nodes/x/aa.md'), PosixPath('/tmp/g13-policy-hnpo3jb6/nodes/x/zz.md'))]
P5 load_existing_nodes: winner=zz.md pick=Z (silent, no warning)
P5 source line 424: for md_path in sorted(NODES_DIR.rglob('*.md')) -> sorted, NOT OS order

== T4b: acceptance divergence on M5 (leading space before ---) ==
P1 accepts (lines[0].strip()), P3 accepts (contains ---\n), P9 rejects (startswith),
P10 rejects (lines[0] != '---'), P4/P5/P6/P7/P8 accept (strip) — see T1 matrix M5 row

tmp dir: /tmp/g13-policy-hnpo3jb6
```

Interpretation against the hypothesis's criteria:

1. **Policy collapse** — reproduced for P2, P3 (M1/M2; M3/M4 are the
   *raises* the unified `on_error` exists to model), P4, P5, P6, P7, P8, P9.
   Fails for P10, which has no YAML failure class and absorbs malformed
   frontmatter as data — a disproof trigger, but on the one parser the
   hypothesis's own scope note excludes from the unified reader's population.
2. **No empty-fm ambiguity** — pass. No caller branch distinguishes the two
   `{}` cases. New: the `{}+raw` policy corrupts on write-back (T2b), an
   argument for report-and-skip as the default.
3. **P3's latent raise** — confirmed uncaught, plus P1 shares the gap
   (`ParserError` ≠ `FrontmatterError`) and P3 has a fourth, unmodeled branch
   (M4 → `AttributeError` at the caller).
4. **Dupe rule** — divergence measured (opposite winners), but the mechanism
   is first-wins vs last-wins over the *same sorted* order; the hypothesis's
   "P5 walks OS enumeration order" is wrong (`sorted(rglob)`, line 424).

No files in the repo were modified; no git commands run; corpus read-only.


## Agent Notes
Policy collapse 9/10 (P10 no-YAML exception, out of scope); no empty-fm ambiguity; P3 latent ParserError confirmed + 4th unmodeled branch (M4 list-YAML -> AttributeError); P1 raise is two-class (ParserError leaks past FrontmatterError); dupe divergence measured but P5 is sorted not OS-order