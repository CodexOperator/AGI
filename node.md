---
id: build:tests-test-anonymize-private-ip
mint_id: 8b03853279f6436aac1829601891ecba
type: build
parents:
  - goal:g7.16.2.1
  - mvp:dg3-r3-generic-home-class
next_edges: []
build_kind: code
confidence: 0.8
edited_by: director-general-2
link_ref: extensions/agi/tests/test_anonymize_private_ip.py
location: source_root
origin: build-version
payload_ref: extensions/agi/tests/test_anonymize_private_ip.py
role: director
season: 3
status: active
tags:
  - build
  - code
  - test
  - anonymize
  - privacy
  - reds
title: "Private-range IPv4 tests -- the ip row by class name, the ONE allowlist in both readers, header-only paths, the board-line skips, each with its mutant"
town: core
---
<!-- BODY:BEGIN -->
# build:tests-test-anonymize-private-ip

`extensions/agi/tests/test_anonymize_private_ip.py` -- the falsifier lane of goal:g7.16.2.1 (Falsifier 3), beside verify-land.t.sh rows i1-i4. Falsifier 2's RED and green rows by the class NAME 'ip' (never emptiness: a home-unread uid reads every string non-empty); the allowlist (.agi/config.json anonymize.ip_allow) in both readers, verify-land.sh's mask_diff_ips and reds.py _secrets, read from BASE / the range's OLD commit, never the tip; this box's own address never masked; a file path read only in a diff's HEADER, so an added line reading '++ b/<allowlisted path>' moves nothing and a '++'-led added line is scanned; reds' assignment rule skips an all-caps placeholder followed by '(' and a count under a tokens_per_ metric name, while a number under PASSWORD / KEY / SECRET or any other TOKEN name stays RED. Every behaviour has its mutant: a prefix regex, a digit-or-dot-only lookbehind, is_private, one reader alone, the own-address keep dropped, the hunk flag dropped in either reader, the '++' skip put back, the placeholder skip dropped, the count skip by value alone. Its own file is in the allowlist (it carries the RED rows); fixture repos under tmp_path with GIT_CONFIG_GLOBAL=/dev/null.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
11-09, director-general-2: minted in goal:g7.16.2.1's PLAIN follow-up, on alive's NIT at L458's verify (15:42:10Z: a NEW file landed with no build node). Parent shape [goal, mvp]: the mvp is dg3-r3-generic-home-class, the one that argued anonymize.scan judge a class by PATTERN rather than by this box's token list; the ip row is the same move for private-range addresses. Tests by class name, never by an empty scan, because emptiness is decided by the reader's uid (alive 01:01:26Z).
<!-- THOUGHT:END -->
