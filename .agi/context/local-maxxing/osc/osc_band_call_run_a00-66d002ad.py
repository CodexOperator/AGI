"""RUNNER for the band call rule (hypothesis:a00-66d002ad-8cee33): the entry point
osc_band_call2_a00-cc7b25cc.py never had. One line per (cell, arm, comparator, metric):
the WORD, or `unresolved` + the reason. Exit 2 while ANY cell is unresolved, so
"called nothing" is a RED run, never a quiet pass.

NO TOLERANCE IS PINNED HERE. What the data under
paths.local_maxxing.osc_band_qknorm_dir holds CHANGES as the producers land
(seeded draws make cells resolve, foreign schemas get fixed), so any row count or
word tally written into this docstring rots; the honest state of a still-growing
dir is whatever the last run PRINTS, and it is re-measured on every run. A refusal
the rule cannot read is always a REASON, never a crash and never a word.

The default dir is read through `paths` (paths.local_maxxing.osc_band_qknorm_dir),
and that module is DISCOVERED from __file__ -- one dirname up, never a literal,
never cwd (paths.py's own rule; hypothesis:a00-95b6cd1c-6f642c). Before this a
clean interpreter died here with ModuleNotFoundError: exit 1, no cell read, while
the suite stayed green because the TEST seeded sys.path.
"""
import glob, importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.dirname(HERE)]   # paths.py, discovered -- cwd-independent
RULE = "osc_band_call2_a00-cc7b25cc"            # the rule module; this file adds no rule


def row_contract():
    """values.local_maxxing.osc_band_row_contract, read at runtime, never re-declared
    here (the sibling convention, osc_band_call_a00-ec09e83b.py:8 and its contract test)."""
    import paths
    return json.load(open(paths.config_path()))["values"]["local_maxxing"]["osc_band_row_contract"]


def budget_value(rec, fields):
    """The value carrier for one record, restricted to fields the CONTRACT declares.
    Pre-contract producers spelled it 'cell'; a name the cell does not declare (an old
    'bits') is NOT accepted -- adding one is a config edit, never a script edit."""
    for name in ("budget", "cell"):
        if name in fields and name in rec:
            return rec[name]
    return None


def load_rule():
    s = importlib.util.spec_from_file_location(RULE, os.path.join(HERE, RULE + ".py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def normalize(lines):
    """jsonl lines -> draw dicts whose 'budget' is the first cell key present (or None)."""
    out = []
    fields = row_contract()["fields"]           # the vocabulary, from the config cell
    for line in lines:
        d = json.loads(line)
        d["budget"] = budget_value(d, fields)
        out.append(d)
    return out


def report(path, rule=None, root=None):
    """[(word, reason, label)] for one cells.jsonl. TOTAL: never raises on a foreign schema."""
    rule = rule or load_rule()
    try:
        with open(path) as fh:
            draws = normalize([x for x in fh if x.strip()])
        judged = rule.judge(draws)
    except (KeyError, ValueError) as err:        # a schema the rule cannot read is a REASON
        # the label is relative (never the absolute path): evidence stays relocatable
        return [("unresolved", "record schema the rule cannot read: %s" % err,
                 os.path.relpath(path, root) if root else os.path.basename(path))]
    return [(w, r, "/".join(str(x) for x in k)) for k, (w, r) in judged.items()]


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv:                                    # an explicit dir beats the config default
        root = argv[0]
    else:
        import paths                            # on sys.path by discovery, above
        root = paths.get_local("osc_band_qknorm_dir")
    files = sorted(glob.glob(os.path.join(root, "**", "cells.jsonl"), recursive=True))
    if not files:
        print("no cells.jsonl under %s" % root)
        return 1
    tally = {}
    for f in files:
        for word, reason, label in report(f, root=root):
            tally[word] = tally.get(word, 0) + 1
            print("%-12s %-30s %s | %s" % (word, os.path.relpath(f, root), label, reason))
    print("TOTAL " + ", ".join("%s=%d" % kv for kv in sorted(tally.items())))
    return 2 if tally.get("unresolved") else 0


if __name__ == "__main__":
    raise SystemExit(main())
