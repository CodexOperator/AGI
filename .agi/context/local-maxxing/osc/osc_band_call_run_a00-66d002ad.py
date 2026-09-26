"""RUNNER for the band call rule (hypothesis:a00-66d002ad-8cee33): the entry point
osc_band_call2_a00-cc7b25cc.py never had. One line per (cell, arm, comparator, metric):
the WORD, or `unresolved` + the reason. Exit 2 while ANY cell is unresolved, so
"called nothing" is a RED run, never a quiet pass. Its two tolerances are MEASURED on
paths.local_maxxing.osc_band_qknorm_dir (4 of 6 real cells.jsonl have no `arm`/`budget`
key and made the rule raise KeyError; the other 2 hold one unseeded random draw per
cell). Both land as a REASON. Neither ever becomes a word.
"""
import glob, importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RULE = "osc_band_call2_a00-cc7b25cc"            # the rule module; this file adds no rule
CELL_KEYS = ("budget", "bits", "cell")          # the qknorm producers disagree; first wins


def load_rule():
    s = importlib.util.spec_from_file_location(RULE, os.path.join(HERE, RULE + ".py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def normalize(lines):
    """jsonl lines -> draw dicts whose 'budget' is the first cell key present (or None)."""
    out = []
    for line in lines:
        d = json.loads(line)
        d["budget"] = next((d[k] for k in CELL_KEYS if k in d), None)
        out.append(d)
    return out


def report(path, rule=None):
    """[(word, reason, label)] for one cells.jsonl. TOTAL: never raises on a foreign schema."""
    rule = rule or load_rule()
    try:
        with open(path) as fh:
            draws = normalize([x for x in fh if x.strip()])
        judged = rule.judge(draws)
    except (KeyError, ValueError) as err:        # a schema the rule cannot read is a REASON
        return [("unresolved", "record schema the rule cannot read: %s" % err, path)]
    return [(w, r, "/".join(str(x) for x in k)) for k, (w, r) in judged.items()]


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv:                                    # an explicit dir beats the config default
        root = argv[0]
    else:
        import paths                            # repo-relative dir lives in config, not here
        root = paths.get_local("osc_band_qknorm_dir")
    files = sorted(glob.glob(os.path.join(root, "**", "cells.jsonl"), recursive=True))
    if not files:
        print("no cells.jsonl under %s" % root)
        return 1
    tally = {}
    for f in files:
        for word, reason, label in report(f):
            tally[word] = tally.get(word, 0) + 1
            print("%-12s %-30s %s | %s" % (word, os.path.relpath(f, root), label, reason))
    print("TOTAL " + ", ".join("%s=%d" % kv for kv in sorted(tally.items())))
    return 2 if tally.get("unresolved") else 0


if __name__ == "__main__":
    raise SystemExit(main())
