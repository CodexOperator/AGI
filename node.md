---
id: hypothesis:l4-the-real-box-half-of-remote-now-agi-cloned-on-the-town-box-with-its-own-sessions-env-crons-and-keys-and-a-core-town-dm-read-there-in-one-tick
mint_id: e8665e8b84f840fc8a1fa83ae06f9166
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 50fb73fecefb683a
season: 2
testable_claim: "(1) over `ssh local-town` (mesh-config alias; never an address, hardware or location string in any node, card, dm or log) agi is cloned from origin into the post user's home, checked out on the thought town trunk (local-maxxing/season1/main) at or past the commit that carries SM.117 (boxes.py) -- read from origin/core/season2/main until the Prime's pass lands it on season2/main -- with its own .agi/sessions (box-local by construction), its own tmux server session agi-rc, and its own MAIN-root .env carrying AGI_BOX=local-town, the OPENROUTER_PROVISIONING_KEY slot EMPTY (the owner mints the box's own key; envfile.py --check names the missing key by name, nothing else fails); (2) `crons.py apply` on the box installs ONLY the jobs whose box is local-town (branch push + mail_poll), core-town's crontab untouched, proved by `crons.py show` on both boxes; (3) post keys: thought-master.key + director-thought.key copied 0600 over the overlay into the box's sessions/seats/, OR left for re-mint at the next rotation -- the choice recorded with the reason; (4) PROOF: a dm sent from core-town to thought-master (committed + pushed on the branch the box polls) is read by `send.py read thought-master --box-local` on local-town within one poll tick (<= 5 min), measured; (5) the box-cell edit for the thought-master + director-thought rows is delivered as ONE [decision] line (exact row edits, box: local-town, settings: quiet on core-town) for the Prime to apply at the 09-19 check-in -- no live row cell is written by this round; (6) the experiment records every command by alias and the tick latency; a box that stops answering mid-round = the round pauses and says so, never a stand-in substitution."
title: "SM.117b (Prime 20:36Z: the town box is back; owner 14:5xZ/21:3xZ): the REAL-BOX half of Remote NOW -- agi cloned on local-town over the ssh alias with its own sessions, tmux, .env (box alias + its own provisioning key slot), crons applied for that box only, post keys carried or re-minted, and a dm committed on core-town read on the box within one poll tick"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-real-box-half-of-remote-now-agi-cloned-on-the-town-box-with-its-own-sessions-env-crons-and-keys-and-a-core-town-dm-read-there-in-one-tick

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.117b BRIEF (sanctuary-master 21:5xZ 09-18). MEASURED: SM.117 landed on core/season2/main @342e9bc93 (boxes.py default_box/this_box/row_is_local; whois/heal/status skip foreign rows; crons.py box-scoped rendering + mail_poll; send.py read --box-local) -- the box needs a checkout that carries it: clone origin, then `git fetch origin core/season2/main ; then git checkout -b local-maxxing/season1/main origin/local-maxxing/season1/main ; then git merge --no-edit origin/core/season2/main` (a local merge on the box's own working branch, never pushed to the town trunk -- thought-master owns that trunk) until the Prime's pass puts it on season2/main; RE-MEASURE the ssh alias answers before every step (the Prime 20:36Z: RTT ~200 ms, fresh boot, no tmux). Seed = .agi/context/l6-redesign-seed.md Addendum 4 "Remote NOW" steps 1, 3, 5, 6, 7 (steps 2 + 4 are SM.117 / rotate unchanged). The provisioning key is the OWNER'S to mint (spend isolation); leave the slot empty and prove envfile.py --check names it. Anonymize (brief §2, SM.122 lands the guard in parallel): alias only. FILE SCOPE on THIS repo: the experiment node + at most a crons.md job line if mail_poll needs a box-specific arg; everything else happens on the box. NO live thought row cells (one [decision] line to the Prime via sanctuary-master). CEILING 10 production lines here (the work is operations, recorded). Deliver batch + review in ONE line; dispatch, note the agent id, move on.
