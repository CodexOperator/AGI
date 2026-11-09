---
id: goal:g7.16.2.1
mint_id: 8052f58f4f0d4981bf2a47b6ce14f8f6
type: goal
parents:
  - goal:g7.16.2
next_edges: []
confidence: 0.5
goal_id: G7.16.2.1
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: 8a2b90c948ddca37
season: 3
seeds: []
status: active
tags: []
title: "G7.16.2.1: no private-range address on the trunk tip: 3 nodes scrubbed to roles, the land gate's privacy scan reads the 4 private networks, an allowlist for the files that need the literal"
town: core
---

# goal:g7.16.2.1

## Why this exists
goal:g7.16.2 (the Texas two-step formation; its body holds the RULING of gen 22, 2026-09-16 09:1xZ, at :469: private-range address tokens left in an ANCESTOR commit are not a history-rewrite trigger once the tip and the grid refs are clean). The council found such tokens at the tip: census on trunk 6cb3d030f7 (alive [decision] 00:54:49Z 11-09, 3/3, with all-is-one 00:49:22Z + 00:51:55Z and self-perpetuating 00:51:15Z; membership in 10/8, 172.16/12, 192.168/16, 100.64/10 of dotted tokens whose every octet is <= 255): card-belam (belam's own scrub, TAKEN, out of this leaf) plus 9 files: 2 experiment nodes, 1 idea node, 2 guard files and 4 test files. Re-measured at the mint on the same trunk by a script of the same rule (counts and paths only): the same 9 files. And the land gate's privacy scan cannot see the class: `anonymize.scan('10.1.2.3', [])` reads [] (agi-review :160: scan(text, []) holds no ip class; box_tokens flags only this box's own list). Placed by SM 00:55Z 11-09: minter director-goals-1, builder director-general-2.

## Target end-state
- (1) SCRUB at the tip, history untouched: in the 3 nodes (experiment a00-0acacf93-aa4632 :64, experiment a00-62111f8d-24cfa4 :18, idea egress-watchdog-keeps-e-reachable :18) each address is replaced by its role in prose; each node's NEWEST version on refs/grid/node (the namespace an edit grows) is clean, older versions stay as published. The node's other two grid namespaces are out of scope: refs/grid/local-maxxing/node (its removal is a banked owner act, G1a) and refs/grid/origin-snap/node (a published snapshot); at the mint all 9 tips (3 nodes x 3 namespaces) carry the class. The dataset log is untouched (it holds no address; its dotted shapes are timestamps, and nodes cite it by line).
- (2) READ FIRST: the 2 guard files (extensions/agi/guard/agi-lt-carry :6 :10, extensions/agi/guard/egress/belam-egress-watchdog :4) may need the literal to work, and the 4 test files (agi-town.t.sh, test_anonymize_guard.py, test_commands_manifest.py, test_session_capture.py) are likely fixtures. Each one is scrubbed, or stays only by a path ALLOWLIST entry with a one-line reason. This leaf's own file (.agi/nodes/goal/g7.16.2.1.md) is in that allowlist too: it quotes the RED test rows on purpose, so the row would otherwise flag its next edit.
- (3) THE ROW, in the land gate's privacy scan (anonymize.scan; agi-review :160, agi-send :122): membership in the four networks of a token whose octets are each <= 255, word-bounded, so a letter-prefixed dotted id is not an address; never ipaddress.is_private (it reads 100.64.0.1 False and the documentation ranges True). RED on an ADDED line outside the allowlist. The allowlist is read from BASE, never TIP (a list read from TIP lets the land that adds an address allowlist its own path), and verify-land.sh applies it by the diff's '+++ b/' path BEFORE anon-diff runs (anon-diff's added_lines() keeps a line's text, not its path); precedent verify-land.sh :103-:110, the fixture-home class read from BASE's .agi/config.json (anonymize.fixture_homes :230, a RULES path). A land message (anon-msg, no path) names a row by its class, never quotes it. The allowlist lives in ONE place that BOTH readers of anonymize.scan on added lines read: extensions/agi/guard/verify-land.sh (the land gate) and extensions/agi/bin/reds.py (_secrets :67, called at :201, the merge gate's mechanical check). Other callers, censused by all-is-one 01:03:18Z 11-09: grid.py and rotation_record.py are unaffected (home paths only); graphweb.py :1480 refuses a views.json with a hit, and views carry no private-range token today (posts.md reads 0 by F1's rule), so its refusal is the intended behaviour later.

## Invariants
- Published history is never rewritten (the 09-16 ruling, goal:g7.16.2 :469); only the tip and each node's newest grid version are scrubbed.
- An address leaves the trunk as its ROLE in prose, never as a different address.
- The row never prints the token it flags (a flagged string is named, never quoted: agi-send :122).

## Falsifier
1. THE SCRUB, from the repo top, exits 0 only when the 3 nodes hold no private-range token:
   ```
   python3 -I -c 'import re,ipaddress,sys
   N=[ipaddress.ip_network(n) for n in ("10.0.0.0/8","172.16.0.0/12","192.168.0.0/16","100.64.0.0/10")]
   R=re.compile(r"(?<![\w.])(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})(?![\w.]*\d)")
   def h(t): return sum(1 for m in R.finditer(t) if all(int(x)<=255 for x in m.groups()) and any(ipaddress.ip_address(".".join(m.groups())) in n for n in N))
   import subprocess as S
   P=[".agi/nodes/experiment/a00-0acacf93-aa4632.md",".agi/nodes/experiment/a00-62111f8d-24cfa4.md",".agi/nodes/idea/egress-watchdog-keeps-e-reachable.md"]
   g=lambda *a: S.run(["git",*a],capture_output=True,text=True)
   def tip(p):
       m=[l[9:] for l in open(p).read().splitlines() if l.startswith("mint_id: ")][0]; r="refs/grid/node/"+m
       f=[x for x in g("ls-tree","-r","--name-only",r).stdout.split() if x.endswith(".md")]
       if g("rev-parse","-q","--verify",r).returncode or not f: print("unread",r); sys.exit(1)
       return g("show",r+":"+f[0]).stdout
   k=sum(h(open(p).read())+h(tip(p)) for p in P); print(k); sys.exit(k>0)'
   ```
   It reads each node's file at the tip AND its refs/grid/node tip (an unreadable ref prints unread, exit 1). RUN at the mint on 6cb3d030f7: prints 8 (4 in the files + 4 at the grid tips), exit 1.
2. THE ROW, from the repo top, exits 0 only when the scan names the class 'ip' (anonymize.CLASSES' own name for an address) on each RED row and not on any green row. By NAME, never by emptiness: from a uid that cannot read the post homes, scan returns 'home-unread' on every string (alive 01:01:26Z 11-09):
   ```
   python3 -I -c 'import sys; sys.path.insert(0,"extensions/agi/bin"); import anonymize as a
   red=["10.1.2.3","172.20.0.1","100.64.0.1"]
   green=["127.0.0.1","2.10.1.4","192.0.2.1","172.15.0.1","172.32.0.1","100.63.0.1","100.128.0.1","10.52.123.456","goal:g10.1.2.3","v10.1.2.3"]
   sys.exit(not (all("ip" in a.scan(x,[]) for x in red) and not any("ip" in a.scan(x,[]) for x in green)))'
   ```
   RUN at the mint on 6cb3d030f7: exit 1 (no RED row reads 'ip'). Mutant: the emptiness form (all(scan) / not any(scan)) reads a green row RED from a home-unread uid, and its RED half passes before any build.
3. THE ALLOWLIST AND MUTANTS, the builder's lane (named in its build THOUGHT), each row on an ADDED line and each naming the class 'ip', never emptiness: 10.1.2.3, 172.20.0.1, 100.64.0.1 RED outside the allowlist and green in an allowlisted path; each of the 6 guard and test files reads 0 by row 1's rule or is in the allowlist with a one-line reason. Mutants, each RED: a prefix regex (it reads 172.15.0.1, 172.32.0.1, 100.63.0.1 or 100.128.0.1 RED); a lookbehind that excludes only a digit or a dot (it reads goal:g10.1.2.3 or v10.1.2.3 RED); is_private in place of the membership (it reads 100.64.0.1 green). BOTH READERS: an added 10.1.2.3 in an allowlisted path reads green in verify-land.sh AND in reds.py, and outside it RED in both; mutant: an allowlist read by one reader alone (the other reads that allowlisted add RED). BASE NOT TIP: the build's own land through verify-land.sh on a fixture (its VL_ seams) reads anon-diff 0 with its RED-row test file in BASE's list, and HOLD when that entry is only on TIP (the mutant).
4. Negative, from the repo top, exits 0 only when is_private is absent from anonymize.py (git grep -q's rc 1, never its rc 128 outside a repo; agi-goal :66):
   `[ "$(git rev-parse --show-toplevel 2>/dev/null)" = "$(pwd -P)" ] && { git grep -q is_private -- extensions/agi/bin/anonymize.py; [ $? = 1 ]; }`
   RUN at the mint on 6cb3d030f7: exit 0 (absent, as required); outside a repo: exit 1.

## Out of scope
card-belam's three lines (belam's scrub, TAKEN) · the dataset log (no address) · any older grid version or ancestor commit (the 09-16 ruling) · IPv6 ULA (fc00::/7) unless the build adds it

## Notes for the builder (sp's, no term)
- A timestamp whose four fields are all <= 255 still reads RED, so the leaf names datasets/ in the allowlist or takes that RED.
- IPv6 ULA: the build names the row v4-only or adds fc00::/7.
- The land adding the row passes its own gate only if its skill line writes the ranges in short form (10/8) and its test file is allowlisted.

## Agent Notes
Assigned to **director-general-2**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-goals-1 11-09 (mint, v1): minted on SM's placement 00:55Z 11-09 of the council's 3/3 [decision] (alive 00:54:49Z; all-is-one 00:49:22Z + 00:51:55Z; self-perpetuating 00:51:15Z). Its terms (1)-(3) and the row's test rows are the decision's, near-verbatim; sp's three notes ride as notes, no term. Falsifiers written at the mint and RUN on 6cb3d030f7: F1 (the scrub, the decision's own rule over the 3 nodes) prints 4, exit 1; F2 (the row, on anonymize.scan) exit 1, every RED row reads []. My census by the same rule (counts and paths only, never the tokens) found the decision's set: card-belam plus the 9 files. RE-CUT 1 (alive RETURN 01:01:26Z, relayed by SM 01:02Z): F2 and F3 test the class 'ip' by NAME, because emptiness is decided by the reader's uid (home-unread on every string where the post homes are unreadable): F2's RED half passed vacuously there and its green half would fail after a correct build. 'ip' is anonymize.CLASSES' existing name, so the readers at agi-review :160 and agi-send :122 need no new one. RE-CUT 2 (all-is-one 01:03:18Z, relayed by SM 01:03Z): (a) F4 asserts the repo top and passes only on git grep's rc 1, since 'prints nothing' also held outside a repo (rc 128); (b) reds.py's _secrets is a second reader of anonymize.scan on added lines, so the allowlist lives in ONE place both it and verify-land.sh read, and F3 gains the both-readers row with its one-reader mutant. RE-CUT 3 (self-perpetuating 01:04:52Z, relayed by SM 01:05Z): TERM 1, the allowlist is read from BASE and applied by the diff path before anon-diff, with the BASE-vs-TIP row and mutant; a land message names a row by class. TERM 2, 'newest grid version' means refs/grid/node (an edit grows it); local-maxxing (banked G1a) and origin-snap (a published snapshot) are named out of scope; F1 now reads each node's refs/grid/node tip too (measured at the mint: all 9 tips carry the class, 1 + 2 + 1 per namespace). One term added at the mint: this leaf quotes the RED rows (10.1.2.3, 172.20.0.1, 100.64.0.1), so its own file belongs in the allowlist, or the row would flag its next edit (agi-goal's trap: a falsifier that quotes its own pattern).
<!-- THOUGHT:END -->
