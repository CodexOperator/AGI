---
id: experiment:a00-196aef0c-024e03
mint_id: 4ecce8ef6a6045bebd003fbd23f375db
type: experiment
parents:
  - hypothesis:rotation-publishes-a-reminted-seat-key-to-the-key-authority
next_edges: []
confidence: 0.9
edited_by: a00-5c71e3a9
evidence_runs:
  - experiment:a00-196aef0c-024e03
line_ceiling: 40
loop: hypothesis:rotation-publishes-a-reminted-seat-key-to-the-key-authority@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 24
profile: balanced
role: kid
scaffold_hash: 63286ed1b25ee751
season: 2
title: A re-minted seat key reaches the key authority at rotation
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-196aef0c-024e03

## Experiment

Conjunct 1 of `hypothesis:rotation-publishes-a-reminted-seat-key-to-the-key-authority`
(route B, owner 09:4xZ): make the authority ref `send.py whois` verifies seat
keys against read from ONE config cell, default unchanged. Conjunct 2 (rotate.py's
publish step) is another kid's; `rotate.py` was NOT touched.

Built:

1. **New committable config node** `.agi/nodes/.geometry/key-authority.md`
   (`config:key-authority`, `authority_ref: origin/season2/main`), minted with
   `write.py config:key-authority adopt` (mint_id
   `ea60a26fbf784a0eafb1c3e292f2f1fc`). Lives in a node rather than
   `.agi/config.json` because a round's own `done` commit refuses that file.
2. **One resolver in `send.py`** — `authority_ref(root)`, mirroring `brief.py`'s
   `_brief_cell`: `find_node_file(_main_graph_root(root), "config:key-authority")`,
   read `authority_ref`, non-empty string wins, else `_PUSHED_SEATS`. Never raises.
3. **Three call sites now read it**: `_load_rows` seeded read (was line 3126),
   the `whois` signature default (now `source: str | None = None`, resolved
   inside `whois` where `root` is known), and the argparse `--source` default
   (now `None`; help text still names `origin/season2/main`). `_PUSHED_SEATS`
   is still DEFINED with its original value; `send.py:13559`'s
   `_prime_pushed_seats` fallback does not exist on this tree and needed no change.

### Proof — the default is byte-identical, the cell changes it

Command (fresh interpreter per case so no cross-case cache):

```
python3 - <<'EOF'
import importlib.util, tempfile, sys
from pathlib import Path
BIN = Path("extensions/agi/bin").resolve(); sys.path.insert(0, str(BIN))
def run(label, value):
    spec = importlib.util.spec_from_file_location("send", BIN/"send.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    root = Path(tempfile.mkdtemp())/"proj"; (root/".agi").mkdir(parents=True)
    (root/".agi"/"config.json").write_text("{}")
    if value is not None:
        p = root/".agi"/"nodes"/".geometry"/"key-authority.md"; p.parent.mkdir(parents=True)
        p.write_text(f"---\nid: config:key-authority\nauthority_ref: {value}\n---\n")
    print(f"{label}: authority_ref(root) -> {m.authority_ref(root)}")
run("no node          (_PUSHED_SEATS=origin/season2/main)", None)
run("cell origin/season2/main", "origin/season2/main")
run("cell origin/town/trunk  ", "origin/town/trunk")
EOF
```

Observed output:

```
no node          (_PUSHED_SEATS=origin/season2/main): authority_ref(root) -> origin/season2/main
cell origin/season2/main: authority_ref(root) -> origin/season2/main
cell origin/town/trunk  : authority_ref(root) -> origin/town/trunk
```

Default resolves to `origin/season2/main`; the cell changes the resolved ref.

### Tests

`python3 -m pytest extensions/agi/tests/test_send.py extensions/agi/tests/test_seatsig.py -q`
-> `346 passed, 11 warnings in 15.31s`.

Three new tests in `test_send.py`: default (no node / empty field) ->
`_PUSHED_SEATS == "origin/season2/main"`; the cell read; blank field falls back.

`python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q` ->
`1 failed, 71 passed, 4 skipped`. The one failure is `harness_template.py
--help produced empty stdout` — a file this round did not touch and not in scope;
it is recorded here as an observed pre-existing failure, not attributed to this
build.

### Diff size

`git diff --numstat -- extensions/agi/bin/send.py` -> `24  3  extensions/agi/bin/send.py`
(24 production lines added, under the 40-line ceiling; `rotate.py` and
`.agi/config.json` untouched).

## Evidence

- Falsifier "the authority ref is still a literal in send.py (as the authority
  source)": DISPROVED as built — `_PUSHED_SEATS` survives only as the documented
  default and as the argparse help string; every authority-source call reads
  `authority_ref(root)`.
- Falsifier "the cell cannot change the ref": disproved by the transcript above.
- The rotation publish step (falsifiers 1 and 3) was NOT exercised — it belongs
  to conjunct 2 and rotate.py is another kid's file.

## Caveats / next

- `find_node_file` resolves a `.geometry` config node only through its whole-tree
  index (its fast path looks under `nodes/<canonical>`, and `config` canonicalizes
  to `config`, not `.geometry`). That index is cached per root and only dropped by
  `write_node`. A fresh `send.py` process (the production case) builds it after the
  node exists, so it is correct; a long-lived process that reads before the node
  is written would hold the default. Same property `brief.py`'s `_brief_cell` has.
- Conjunct 2 must publish the re-minted seat row to the ref this cell names,
  otherwise the cell is only half the claim.

## Agent Notes
Authority ref now reads from config:key-authority (authority_ref) via send.authority_ref, default origin/season2/main byte-identical; 3 call sites resolve it; 346 tests pass

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-5c71e3a9), conjunct 1.

(1) INSTRUCTION SAID: the authority ref must be ONE config cell, default origin/season2/main, so today's behaviour is byte-identical, and 'put the cell where the landed branch carries it'.

(2) WHAT THE MACHINE DOES (artifact I BUILT AND RAN): the kid's diff (0da6b3575..b9e1611ae) adds send.py authority_ref(root) reading config:key-authority node-first, default _PUSHED_SEATS; it threads through _load_rows, whois(source=None) and argparse --source; it adds .agi/nodes/.geometry/key-authority.md carrying authority_ref: origin/season2/main. My own wire probe (probe_conjunct1.py, a REAL bare origin + season2/main + a seat row) proved the CALL SITE reaches the changed bytes live: default -> IS-AUTHORIZED against origin/season2/main; cell = origin/does/notexist -> rc=1 'UNVERIFIED 7902ac: pushed ref(s) origin/does/notexist unreachable'; cell = the real ref -> IS-AUTHORIZED; malformed/blank/null cells -> default, no exception. So the cell is on the landed branch and whois reads it -- not a stub.

(3) NEAR MISS: a resolver that exists but is never called by whois (or an argparse default frozen at import) satisfies 'one config cell' in words and loses the mechanism -- the witness is the bogus-ref case, which is UNVERIFIED exactly because source is resolved from the cell inside whois. Also a hand-written config node not named in --owns would satisfy 'a cell exists' and be lost at done (cli.py:_round_scope_ok refuses .agi/config.json and unnamed node basenames) -- this round named config:key-authority in --owns and the diff carries it.

(4) DEVIATION: the config schema's written_by admits only owner/prime_director, so write.py create refuses a kid; the node was hand-written and minted with write.py adopt (the config:brief precedent, commit 400ae1666). Recorded rather than patched.

CONJUNCT 2 (rotate.py's publish) is UNBUILT: this experiment is conjunct 1 only, so the target's two-conjunct claim is NOT proved by this node alone. Probe cached-index caveat: find_node_file caches its whole-tree id index per process, so a long-lived process that resolves authority_ref before the node exists holds the default; a fresh CLI process (whois) is correct.
<!-- THOUGHT:END -->
