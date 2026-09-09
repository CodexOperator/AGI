# mvp-mint-map.md — goal:s29 subsystem parents for `level3.py --mint-missing-only`
#
# DATA, not code. One `rel-path-prefix | mvp:<id>` per line; blank lines and
# `#` comments ignored. Longest-prefix wins, so a specific subsystem overrides
# a general one. Read by level3.py's mint mode: a minted build node gets
# `parents: [mvp:<id>]` — a NEW build node needs an mvp behind it (goal:s29),
# one per SUBSYSTEM rather than one per file (72 mvps would be bookkeeping, not
# thought — see hypothesis:l3-engine-files-outside-the-grid). The mvp nodes
# named here each specify the class of tracked files their subsystem owns.
#
# A file matching no prefix falls back to the census parent, then parentless.

extensions/agi/bin/       | mvp:bin-modules
extensions/agi/tests/     | mvp:tests
extensions/agi/workflows/ | mvp:workflows
extensions/agi/hooks/     | mvp:hooks
extensions/agi/scripts/   | mvp:scripts
extensions/agi/src/       | mvp:sources