---
id: hypothesis:l4-a-reader-refuses-a-forged-block-under-enforcing-and-the-value-flips-after-a-named-review
mint_id: 3ee8c72ed83e4db7a097d04d698cf009
type: hypothesis
parents:
  - goal:g15.26
  - hypothesis:l4-lockdown-is-a-reserved-boolean-that-warns-and-encrypts-nothing-until-it-is-built
next_edges: []
edited_by: sensei-director
scaffold_hash: 9ee3032b026ac6c2
season: 2
testable_claim: "goal:g15.26 (OWNER GO 22:1xZ 'go for fix and flip', doc:l4-owner-decisions:657-658; Prime XII 22:14Z: the FLIP is its OWN round on its OWN goal line, reviewed by name before any reader refuses). PRECONDITIONS on the base you are cut from (verify, do not assume): SL5.02's bytes (injective canonical form / CR-body test, ONE seatsig registry across `seatsig` and `src.seatsig`, verify-side RFC vectors, prime-gated --all-live) and the `_comms_config(root)` helper + `comms.verify` key (default \"informational\") from hypothesis:l4-lockdown-is-a-reserved-boolean-...; if either is missing on your base, STOP and say so in the experiment node — never re-implement them. CLAIM: (1) under `comms.verify: enforcing`, `read` and `peek` WITHHOLD the body of a FORGED block and print exactly one refusal line `REFUSED FORGED from <from> ts <ts> fp <fp>: withheld to <quarantine path>`; the block's bytes are APPENDED verbatim to `<sessions>/inbox/quarantine/<seat>.md` (created on first use; never deleted, never rewritten) and removed from the delivered output only — the inbox file itself is left as the reader found it except for the read cursor; (2) VERIFIED, UNSIGNED and RETIRED blocks keep today's label and print in full under both modes (UNSIGNED is not a bad signature: kids/parents are not keyed seats; RETIRED is a good signature under a retired key — the kid records in its node the one-paragraph case for/against refusing RETIRED and refuses NOTHING but FORGED); (3) `whois --sig` under enforcing exits 2 on FORGED with the same refusal line, exit 0 otherwise; (4) under `informational` (default; absent block; any value that is not exactly \"enforcing\") output is BYTE-IDENTICAL to today's — assert by capturing the same inbox under both values with the config absent vs informational; (5) the VALUE on season/s2 stays informational: this round touches .agi/config.json ONLY to document the enum in a comment-free way that the JSON allows (or not at all) — the flip to \"enforcing\" is the Prime's one-line edit after the named review, and the kid writes that sentence into its experiment node. FALSIFIERS: a FORGED body prints under enforcing; quarantine bytes != the block's inbox bytes; a non-FORGED block is withheld; informational output differs by a byte; `whois --sig` exits 0 on FORGED under enforcing; the round changes the season/s2 value. TESTS: test_send.py + test_seatsig.py + test_sensei.py + test_heal.py + test_bin_help_smoke.py, with neighbours. RULES: merge, never rebase; never lower a guard; the kid's experiment-node prose never quotes the literal THOUGHT marker; no new bin/ file. FILE SCOPE: send.py (_print_blocks_with_labels / the read+peek delivery path, whois --sig exit, one _quarantine_block helper), tests. EXCLUDED: _canonical_msg, _verify_block's label logic, _label_for_sig, keygen, seatsig, rotate.py, write.py, config:* nodes, the lockdown warning. CEILING: 1 parent, up to 2 kids ((1)+(2)+(4) / (3)+(5)), small."
thought_session: sensei-director-genV-L5
title: under comms.verify=enforcing a reader withholds a FORGED block into quarantine and prints one refusal line; nothing else is refused; informational stays byte-identical; the value flips only after the named review
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-reader-refuses-a-forged-block-under-enforcing-and-the-value-flips-after-a-named-review

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
