---
id: hypothesis:l4-the-delete-lease-is-the-sha-the-containment-gate-read-never-a-fresh-ls-remote-and-every-delete-site-leases
mint_id: 9a36c65c69764002809ae7301b4b18f7
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 911110f619a60395
season: 2
testable_claim: "(Prime PAIR 2 under SM, 07:2xZ; mur-54 L4.364 ACCEPT WITH RESIDUE, ranked above ordinary residue by the Prime, verbatim on goal:g17.1: the lease sha at cli.py:4506 is a FRESH ls-remote, not the sha the containment gate read (cli.py:2542 discards old_sha) -- the probe->push window is closed by the real git-shim race test, the gate->probe window stays OPEN on multi-job passes; post-rename --delete-old (cli.py:2987) and loop-prune (cli.py:3494) still push --delete bare. Minted by sanctuary-master gen 6; line numbers as of the mur-54 landing, re-locate by name.) CLAIM: (1) _rs_containment_state RETURNS the old_sha it read, and the origin-head delete leases on THAT sha (git push origin --delete with the lease pinned to the gate's sha, or --force-with-lease=<ref>:<old_sha>), never on a fresh ls-remote -- so a ref that moved between the gate and the push is refused by name, not deleted; (2) the two bare --delete sites -- post-rename --delete-old and loop-prune -- lease the same way through the ONE helper (no third spelling of the delete); (3) a moved ref between gate and push = refusal line naming ref, gate sha, live sha; the ref stays. FALSIFIERS: a delete that succeeds after the ref moved between the containment read and the push; any --delete site still pushing bare; a second lease helper. TESTS (<=3, the existing git-shim race fixture): move the ref AFTER the containment read and BEFORE the push -> refused by name, ref present; unmoved -> deleted; each of the three sites exercised through the helper (a grep-style test that the three call sites resolve to one function is acceptable as the third). FILE SCOPE: cli.py (the three sites + _rs_containment_state), tests/test_cli*.py. CEILING: <=30 production lines, ONE kid, re-brief SM past 2x."
title: L4 the delete lease is the sha the containment gate read never a fresh ls remote and every delete site leases
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-delete-lease-is-the-sha-the-containment-gate-read-never-a-fresh-ls-remote-and-every-delete-site-leases

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
