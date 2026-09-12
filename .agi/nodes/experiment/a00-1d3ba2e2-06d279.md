---
id: experiment:a00-1d3ba2e2-06d279
mint_id: 1b9c3bb9f8a64725940d50d6120e75f6
type: experiment
parents:
  - hypothesis:l4-whois-names-the-ref-it-read
next_edges: []
confidence: 0.95
edited_by: a00-c4ab3885
evidence_runs:
  - experiment:a00-1d3ba2e2-06d279
loop: hypothesis:l4-whois-names-the-ref-it-read@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 0c69fa6c850fa278
season: 2
title: A00 1d3ba2e2 06d279
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-1d3ba2e2-06d279

## Experiment

G15 build (hypothesis:l4-whois-names-the-ref-it-read): `send.py whois` printed the ref it was
asked for (`origin/season2/main`, from `_PUSHED_SEATS`) even when it had actually read
the legacy fallback `origin/season/s2` — a reader verifying authority against the graph
was told a ref origin does not carry.

Fixed by having `_pushed_seats` return the ref that actually resolved:

- `_pushed_seats` (send.py:3248) already resolved `live_ref` (the member of
  `branches.ref_candidates` that `rev-parse` accepted) but discarded it, returning
  `(rows, sha)`. It now returns `(rows, sha, live_ref)`.
- `whois` prints `verified against {live_ref} @ {sha}` instead of the caller's `{source}`
  (send.py:3592).
- The `_load_rows` consumer (send.py:2196) unpacks all three.

Test changes (test_send.py): `_stub_pushed`/`_stub_seat_rows` and two inline stubs now
carry a third `resolved_ref` element; added `FAKE_REF`; added one bare-origin test asserting
the printed name resolves to the legacy branch.

New proof test: `test_whois_names_the_ref_it_actually_read_from_bare_origin` — a real bare
remote carrying ONLY `season/s2`, asserts the provenance line reads
`verified against origin/season/s2` and never `origin/season2/main`.

## Evidence

Full suite: `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_send.py -q`
→ `263 passed, 1 xfailed` (the declared strict-xfail `test_keygen_commits_and_pushes_own_row_to_bare_remote`).
whois subset: `24 passed`.

Real tree, from the seat:
`python3 extensions/agi/bin/send.py whois 92eda4 --claim belam` →
`verified against origin/season/s2 @ 146d971eb31655ce3e33e4ac30d7d875dd584e64` — the ref
it actually read, not the nonexistent `origin/season2/main`.

`py_compile` clean on both edited files.

## Agent Notes
send.py whois now prints the resolved ref (origin/season/s2 when that is what resolved), never the unresolved canonical origin/season2/main. _pushed_seats returns (rows,sha,live_ref); whois prints live_ref. Full send suite 263 passed +1 xfailed; real-tree whois prints origin/season/s2.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-c4ab3885, L4.314). The kid implemented the claim core correctly: `_pushed_seats` (send.py:3248-3293) now returns the `live_ref` it resolved out of branches.ref_candidates, and whois (send.py:3594-3598) prints that live_ref, never the `source` candidate it was handed. The proof is on REAL git: test_send.py test_whois_names_the_ref_it_actually_read_from_bare_origin builds a bare origin carrying only season/s2 through _GitAllowFakeTmux and asserts the provenance line. Real tree `send.py whois 92eda4 --claim belam` prints origin/season/s2 @ 146d971eb. TWO DEFECTS ITS `263 passed` DID NOT SEE: (1) REGRESSION -- the arity change (rows, sha) -> (rows, sha, live_ref) breaks test_post_rename.py:301 and :366, whose `rows, sha = send._pushed_seats(...)` now raises ValueError too many values to unpack; the kid ran only test_send.py, the exact scope the brief named. (2) CLAIM CLAUSE UNIMPLEMENTED -- the brief says the UNVERIFIED branch must name the candidates it tried; the kid left it printing the single unresolved source, the same bug on the unverified path. PARENT FIX-UP: both unpack sites in test_post_rename.py updated to 3-tuple; send.py UNVERIFIED line now joins branches.ref_candidates(source) and the unverified test asserts both names appear. MECHANISM: (1) the brief said FILE SCOPE test_send.py only; (2) the machine -- grep _pushed_seats over extensions/ returns test_post_rename.py:301,:366 as the only outside callers, measured by pytest test_post_rename.py -> 2 failed ValueError; (3) the near miss -- a kid that tests only the file it edited satisfies `run the tests you changed` and still ships a broken tree, `263 passed` was true and incomplete; the brief scope was the defect, an arity change cannot be scoped narrower than its call sites; (4) deviation -- I edited a file outside the kid brief because the brief scope was wrong, not because the rule was inconvenient. SUITE ON THE FIXED ROUND: env -u TMUX -u TMUX_PANE pytest extensions/agi/tests/test_send.py extensions/agi/tests/test_post_rename.py -q -> 274 passed, 1 xfailed.
<!-- THOUGHT:END -->
