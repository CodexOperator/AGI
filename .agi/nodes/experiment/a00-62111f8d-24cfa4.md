---
id: experiment:a00-62111f8d-24cfa4
mint_id: 21d8b0c62aa642daa015fcca84977aca
type: experiment
parents:
  - hypothesis:anonymize-box-tokens-skip-loopback-and-link-local
next_edges: []
confidence: 0.9
edited_by: a00-e37dbeaa
evidence_runs:
  - experiment:a00-62111f8d-24cfa4
line_ceiling: 40
loop: hypothesis:anonymize-box-tokens-skip-loopback-and-link-local@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 probes.py  # real box, AGI_ANONYMIZE_FIXTURE unset, box_tokens(root)", "expected": "no loopback token; other addresses still emitted", "observed": "loopback token present=False; real ip tokens count>0=True", "result": "pass - the real ip -o addr path reaches the changed branch live"}
  - {"conjunct": 2, "class": "gate", "cmd": "synthetic ip output 192.0.2.10 + 127.0.0.1 -> scan()", "expected": "routable refused as ip; loopback note passes", "observed": "scan(peer 192.0.2.10)=[ip]; scan(llama-server on 127.0.0.1:8080)=[]", "result": "pass - guard still refuses a routable address, no longer refuses loopback"}
  - {"conjunct": 3, "class": "gate", "cmd": "synthetic ip output fe80::1%eth0 + fc00::1 + 10.9.8.7 -> box_tokens", "expected": "zoned link-local dropped; ULA and private kept", "observed": "fe80::1 absent; fc00::1 present; 10.9.8.7 present", "result": "pass - skip is neither zone-blind nor over-broad"}
production_lines: 9
profile: balanced
role: kid
scaffold_hash: 7e5491911357f66c
season: 2
title: anonymize.py box_tokens skips loopback and link-local addresses
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-62111f8d-24cfa4

## Experiment

Built the fix the parent hypothesis demands, then proved it on the built bytes.

**Pre-fix state (measured):** `box_tokens` turned every `inet`/`inet6` address from
`ip -o addr` into an `("ip", addr)` token, loopback and link-local included —
so `anonymize.py check --diff-file GOALS.md` on this box refused on the
loopback token alone (the only hit; values never printed).

**Fix:** `extensions/agi/bin/anonymize.py`
- `import ipaddress`
- in the `ip -o addr` loop, parse `m.group(1)` with `ipaddress.ip_address`;
  skip when `is_loopback` or `is_link_local`; keep every other address.
  Unparseable strings are kept (defensive — nothing new is silently dropped).

Changed lines: 9 added / 2 removed (production, `git diff --numstat`).

**Tests:** `extensions/agi/tests/test_anonymize_guard.py`, new
`test_loopback_and_link_local_skipped_others_kept`. It deletes
`AGI_ANONYMIZE_FIXTURE` (the fixture path in `box_tokens` returns before the
`ip` branch), monkeypatches `anonymize._run` with a synthetic `ip -o addr`
block, and monkeypatches `_secret_tokens` so no project root is needed. It
asserts `127.0.0.1`, `::1`, `169.254.1.1`, `fe80::1` are absent;
`192.0.2.10` (TEST-NET-1) and `2001:db8::1` (documentation) are present; the
MAC is still parsed; `scan("llama-server on 127.0.0.1:8080")` over the ip
tokens is `[]`; `scan("peer 192.0.2.10")` is `["ip"]`.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_anonymize_guard.py -q
............                                                             [100%]
12 passed in 0.48s        (was 11)

$ python3 extensions/agi/bin/anonymize.py check --diff-file GOALS.md
anonymize: ok — no box-derived physical token in 1512057 bytes
rc=0

$ git diff --numstat -- extensions/agi/bin/anonymize.py
9       2       extensions/agi/bin/anonymize.py
```

No real box value (address, hostname, mac) is printed in this node, the tests
or the diff — only TEST-NET-1 / 2001:db8 documentation ranges and fixture
strings.
<!-- BODY:END -->

## Agent Notes
box_tokens now parses each address with ipaddress and skips is_loopback/is_link_local; test drives synthetic ip -o addr with AGI_ANONYMIZE_FIXTURE unset; 12/12 green, GOALS.md check passes

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHAT THE INSTRUCTION SAID: the target testable_claim and the dispatch orders -- classify each parsed address with ipaddress.ip_address; skip is_loopback or is_link_local; keep everything else. WHAT THE MACHINE DOES: extensions/agi/bin/anonymize.py lines 42-50 now parse m.group(1) with ipaddress.ip_address, and append the token only when parsed is None or neither is_loopback nor is_link_local; I ran three probes of my own against the committed bytes (probes field above) and all six booleans came back True, plus anonymize.py check --diff-file GOALS.md printed ok rc=0. THE NEAR MISS: a prefix filter (addr.startswith 127. or == ::1) satisfies the words for the two enumerated loopback literals and silently keeps 169.254.0.0/16 and fe80::/10 -- which are the second half of the claim -- and a filter that drops the token when ipaddress raises would silently lose addresses. The committed bytes do neither: parsing failure keeps the token, and the classification is the stdlib predicate. DEVIATION: none. This edit is my review version; the kid authored the code and its test, I added probes, thought and note only.
<!-- THOUGHT:END -->

PARENT REVIEW a00-e37dbeaa: accepted proved. Diff carries all three named deliverables (anonymize.py ip branch, the new test, the node). 12/12 green here. My probes: P1 wire real-box loopback absent, P2 gate routable still refused, P3 scope zone/ULA correctly classified. One caveat: on this box's Python 3.12 an IPv4-mapped ::ffff:127.0.0.1 is neither is_loopback nor is_link_local, but ip -o addr does not emit that form and the claim enumerates 127.0.0.0/8, ::1, 169.254.0.0/16, fe80::/10 only -- not a falsifier.
