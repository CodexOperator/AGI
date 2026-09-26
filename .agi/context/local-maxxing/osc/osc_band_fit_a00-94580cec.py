#!/usr/bin/env python3
"""Model-free peak-RSS preflight for an osc-band measurement (hypothesis:osc-band-fit-preflight).

hf config.json + eval ARGUMENTS only -- no weights, no torch. Projects the peak RSS and RAISES
(never asserts) naming the projection and the config budget when a run does not fit. The budget is
the BUDGET_CELLS config cell; the cgroup limit is NOT read (no paths.* cell for it exists).
"""
import argparse, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import paths  # the ONE shared path reader; supplies config_path() and the osc15_hf_dir cell
BUDGET_CELLS = ("box.memory_max", "spawn.memory_max")  # dotted config cells, preference order
RUNTIME_BYTES = 64 << 20  # python+numpy floor: a model term, not the budget
_UNITS = {"K": 1 << 10, "M": 1 << 20, "G": 1 << 30, "T": 1 << 40}
_FLAGS = ("--prompts", "--tokens", "--seeds", "--budgets")


class FitError(RuntimeError):
    """A run that does not fit. Always raised, never asserted, so it survives python -O."""


def parse_size(s):
    s = str(s).strip().upper()
    return int(float(s[:-1]) * _UNITS[s[-1]]) if s[-1] in _UNITS else int(float(s))


def budget_bytes(cfg=None, name=None):
    """(bytes, dotted_cell) read from the config -- a literal budget never appears in this file."""
    cfg = json.load(open(name or paths.config_path(HERE))) if cfg is None else cfg
    for dotted in BUDGET_CELLS:
        v = cfg
        for k in dotted.split("."):
            v = v.get(k) if isinstance(v, dict) else None
        if v:
            return parse_size(v), dotted
    raise KeyError("no memory budget cell in config; looked for %s" % (BUDGET_CELLS,))


def param_count(hf):
    """Weight count from the config: tied embed + per-layer (q,o + k,v + mlp)."""
    h, v, i, L = hf["hidden_size"], hf["vocab_size"], hf["intermediate_size"], hf["num_hidden_layers"]
    head = hf.get("num_attention_heads", 1) * hf.get("head_dim", h)
    kv = hf.get("num_key_value_heads", hf["num_attention_heads"])
    per_layer = h * head * (2 + 2 * kv / hf["num_attention_heads"]) + 3 * h * i
    return v * h * (0 if hf.get("tie_word_embeddings") else 1) + L * per_layer + h


def project_peak_rss(hf, n_prompts, n_tokens, n_seeds=1, n_budgets=4, dtype_bytes=4):
    """-> (peak_bytes, {term: bytes}). Dominant: n_prompts x n_tokens x vocab x dtype (the refs)."""
    del n_budgets  # per-budget-arm results are scalars, one live at a time
    act = n_tokens * hf["hidden_size"] * dtype_bytes * 4  # a few live activation buffers per forward
    eager = hf["num_hidden_layers"] * hf["num_attention_heads"] * n_tokens ** 2 * dtype_bytes
    terms = {"refs": n_prompts * n_tokens * hf["vocab_size"] * dtype_bytes,
             "weights": int(param_count(hf)) * dtype_bytes, "activation": n_prompts * act,
             "seeds": n_seeds * (act + eager), "runtime": RUNTIME_BYTES}
    return sum(terms.values()), terms


def fits(peak, budget):
    """-> (bool, reason). The reason names BOTH numbers, so a caller can print it verbatim."""
    return peak <= budget, "peak %.2f GiB vs budget %.2f GiB" % (peak / 2 ** 30, budget / 2 ** 30)


def max_prompts_seeds(hf, n_tokens, n_seeds=1, n_budgets=4, budget=None, cap=64, **kw):
    """Largest n_prompts that fits at this n_tokens/n_seeds (F7: p fits, p+1 does not)."""
    if budget is None:
        budget = budget_bytes()[0]
    best = 0
    for p in range(1, cap + 1):
        if not fits(project_peak_rss(hf, p, n_tokens, n_seeds, n_budgets, **kw)[0], budget)[0]:
            return p - 1
        best = p
    return best


def preflight(hf, n_prompts, n_tokens, n_seeds=1, n_budgets=4, budget=None, **kw):
    """Raise FitError naming the projection and the budget; else (peak, max_prompts)."""
    if budget is None:
        budget = budget_bytes()[0]
    peak, terms = project_peak_rss(hf, n_prompts, n_tokens, n_seeds, n_budgets, **kw)
    ok, reason = fits(peak, budget)
    if not ok:
        raise FitError("osc-band run does NOT fit: %s | refs term=%d B | args prompts=%d tokens=%d "
                       "seeds=%d budgets=%d" % (reason, terms["refs"], n_prompts, n_tokens, n_seeds, n_budgets))
    return peak, max_prompts_seeds(hf, n_tokens, n_seeds, n_budgets, budget, **kw)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    for f, d in zip(_FLAGS, (8, 512, 4, 4)):
        p.add_argument(f, type=int, default=d)
    p.add_argument("--hf-config", default=None, help="hf config.json (default: the osc15_hf_dir cell)")
    a = p.parse_args(argv)
    hf_dir = a.hf_config or paths.get("osc15_hf_dir")
    hf = json.load(open(os.path.join(hf_dir, "config.json") if os.path.isdir(hf_dir) else hf_dir))
    budget, cell = budget_bytes()
    try:
        peak, cap = preflight(hf, a.prompts, a.tokens, a.seeds, a.budgets)
    except FitError as e:
        print("REFUSED: %s | budget cell %s" % (e, cell), file=sys.stderr)
        return 3
    print("FITS peak %.2f GiB (budget cell %s) | largest prompts at this grid: %d"
          % (peak / 2 ** 30, cell, cap))
    return 0


if __name__ == "__main__":
    sys.exit(main())
