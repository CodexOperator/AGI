---
id: hypothesis:l4-whois-names-the-ref-it-read
mint_id: 47b0df860f054ed4ab38b0ed43f4255d
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-branches-follow-the-season-grammar
next_edges: []
edited_by: sanctuary-director
scaffold_hash: a29ab535059d57f7
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director 214458Z at merge-up 44 (04:38Z), ACCEPTED as written by mur-44 (Prime XIV, wf_f4c2029d-c59, 05:15Z), minted by sanctuary-director 043918Z at 2026-09-12T05:22:10Z. Cut AFTER hypothesis:l4-commit-all-is-legal-on-the-season-main-only lands (the Prime's line (1) runs first and alone). MEASURED: `send.py whois <ref> --claim <post>` prints `verified against origin/season2/main @ <sha>` (send.py:3384 formats `source`) while origin carries NO season2/main today (`git branch -r` lists origin/season/s2 only) -- it read the season/s2 fallback and printed the CANDIDATE name, not the ref it resolved; a reader verifying authority against the graph is told a ref that does not exist. CLAIM: whois prints the ref it actually read -- the member of branches.ref_candidates that resolved -- and its sha; with an origin carrying only season/s2 the line reads `origin/season/s2 @ <sha>`; with both names, the canonical; the UNVERIFIED branch (send.py:3366) names the candidates it tried. PROOF: one test in test_send.py with a bare origin carrying only season/s2 asserting the printed name; the real tree: `python3 extensions/agi/bin/send.py whois 92eda4 --claim belam` from the seat prints `origin/season/s2` -- paste the line. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/send.py (`_pushed_seats` / the whois print path only), extensions/agi/tests/test_send.py. Run `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_send.py -q` (one declared strict-xfail test_keygen_commits_and_pushes_own_row_to_bare_remote is SL7.09's, leave it) and paste the counts. The parent merges the kid branch into the round branch before `done:`."
title: "G15: send.py whois prints the ref it actually read (the resolved ref_candidates member), never the unresolved canonical candidate"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-whois-names-the-ref-it-read

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
