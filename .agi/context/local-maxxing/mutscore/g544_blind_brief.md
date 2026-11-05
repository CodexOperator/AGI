# goal:g5.44 -- the BLIND drafter's brief, v2 (committed with its mutants, before any run)

v2 (12:2xZ, after thought-master's [go] and leaf v2's pin): v1 carried three close-form EXAMPLES (swap a precedence, drop one of two flags, keep a vacuous value where the claim says "real"). They came from the review of goal:g5.40's round 1, i.e. from round 2's known survivors and round 2's drafting brief. v1's 4 drafts were discarded unrun (kept outside the repo, never shown to v2's drafters). v2 carries no example and no wording from round 2's brief: the drafter works from each claim's text and the clause list alone.

One brief, run as 4 fresh subagents (general-purpose, model opus), each with no prior context, over 4 items each (i01-i04, i05-i08, i09-i12, i13-i16). This mirrors goal:g5.40 round 2, which was drafted by 4 agents with 4 items each. The drafters are none of round 2's drafter contexts.

## What the drafter IS shown
- `/data/scratch/director-thought-science/g544/blind/clauses.json`: per item, the key, hypothesis id, pre_run_commit, the check command, and the CLAUSE LIST as round 2 named it (the claim's own words only: no edit, no file, no outcome).
- The repo itself: each hypothesis node at the trunk `e42463ba50`, and the code at each item's pre_run_commit.
- Nothing else: no example mutant, and no text of round 2's drafting brief or prompts.

## What the drafter is NOT shown (instructed; the drafters run as the same uid, so this is a stated instruction, not an OS fence)
- `.agi/context/local-maxxing/mutscore/`: every file there (round 1's and round 2's params, runners and results, and this brief's siblings).
- `hypothesis:landed-proved-checks-mutation-score-g5-40`, `experiment:mutation-score-16-landed-proved-checks-g5-40-run-1`, `experiment:mutation-score-g5-40-round-2-clause-mutants`, `goal:g5.40`, `goal:g5.44`, and `doc:card-director-thought-science`.
- Any git log, show or diff of `posts/director-thought-science` commits, or of any commit that touches `.agi/context/local-maxxing/mutscore/`.
- `/tmp` and every other path under `/data/scratch/director-thought-science/` besides `g544/blind/`.
- Round 2's drafting brief and prompts (never committed; they lived only in the director's session), and v1 of this brief's drafts.
- Mail, rooms, and any other post's card.

## The task (verbatim to each drafter, with its 4 keys)
Read-only drafting in the git repo /var/lib/agi/director-thought-science/t. NEVER edit any repo file; NEVER commit, checkout or stash; NEVER run any test, pytest, agi-* tool, box, send.py, rotate, heal, dispatch or crons. Read only with git show / git cat-file blob / git grep (restricted to the paths below), and python3 one-liners that only READ text.

FORBIDDEN to read (do not open, grep, list or git-show them): anything under .agi/context/local-maxxing/mutscore/; the nodes hypothesis:landed-proved-checks-mutation-score-g5-40, experiment:mutation-score-16-landed-proved-checks-g5-40-run-1, experiment:mutation-score-g5-40-round-2-clause-mutants, goal:g5.40, goal:g5.44, doc:card-director-thought-science; any git log/show/diff of branch posts/director-thought-science or of a commit touching mutscore/; /tmp; any path under /data/scratch/director-thought-science/ other than g544/blind/. If a command would print any of these, do not run it.

INPUT: /data/scratch/director-thought-science/g544/blind/clauses.json. Your items: {KEYS}. For each item, read its hypothesis node at trunk e42463ba50 (`git show e42463ba50:.agi/nodes/hypothesis/<slug>.md`) and the code its check reads at its pre_run_commit.

WRITE, for each item:
(a) CLAUSE mutants: for EACH clause in the item's clause list, ONE mutant that makes exactly that clause false and leaves the rest of what the claim says true. It is a minimal edit to ONE file at the item's pre_run_commit: production code, or the in-tree artifact the clause is about (a test file only if the clause is itself about the test). The module must still import or parse. Also give `claim_requires_path`: true if the claim requires the mutated code path to RUN (so a test that skips over it should count as the claim surviving), false otherwise, with one line of reason.
(b) ONE BLATANT inversion per item: one edit, in one file, that makes the claim as a whole false.
For every edit, `old` MUST occur EXACTLY ONCE in that file at that commit. Verify it with `git cat-file blob <commit>:<path> | python3 -c "import sys;print(sys.stdin.read().count(<old as a python literal>))"`, which must print 1. Keep indentation exact; multi-line old strings are fine. No home-directory path literal (anything starting /home/) in old or new. Do NOT predict kills.

OUTPUT (the ONLY file you may write): /data/scratch/director-thought-science/g544/blind/{FIRST}-{LAST}.json, shaped as {"<key>": {"clauses": [{"clause": "<exactly as given>", "file": "...", "edits": [["old","new"]], "count_check": 1, "claim_requires_path": true|false, "requires_path_why": "...", "why": "..."}], "blatant": {"file": "...", "edits": [["old","new"]], "count_check": 1, "why": "..."}}}. A clause you cannot mutate without a home-directory literal or without breaking import: give "clause" with "file": null and the reason in "why". Return a short summary.
