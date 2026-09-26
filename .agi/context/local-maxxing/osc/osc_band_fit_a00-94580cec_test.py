#!/usr/bin/env python3
"""F1..F7 for hypothesis:osc-band-fit-preflight (see that node for each test).

F2 came out DIFFERENTLY than the hypothesis predicted: the 8x512x4 np64 grid
projects to 5.87 GiB against a 6.00 GiB budget, so it is ACCEPTED, not refused --
2% under the anon-rss 6.19 GB at which the real run was killed. That is recorded
as test_f2b, not hidden.
"""
import importlib.util, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.join(HERE, "osc_band_fit_a00-94580cec.py")
_spec = importlib.util.spec_from_file_location("osc_band_fit", MOD)
fit = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(fit)

HF = json.load(open(os.path.join(os.environ["HF_DIR"], "config.json"))) if os.environ.get("HF_DIR") else {
    "vocab_size": 151936, "hidden_size": 1024, "num_hidden_layers": 28, "num_attention_heads": 16,
    "head_dim": 128, "num_key_value_heads": 8, "intermediate_size": 3072, "tie_word_embeddings": True}
BIG = dict(n_prompts=8, n_tokens=512, n_seeds=4, n_budgets=4)
OVER = dict(n_prompts=8, n_tokens=1024, n_seeds=4, n_budgets=4)
CUT = dict(n_prompts=2, n_tokens=512, n_seeds=3, n_budgets=4)


def _cell(cfg, dotted):
    for k in dotted.split("."):
        cfg = cfg[k]
    return cfg


def _cli(args, flags=()):
    return subprocess.run([sys.executable] + list(flags) + [MOD] + args,
                          capture_output=True, text=True, cwd=HERE)


def test_f1_derivation_moves_with_vocab():
    """F1: the dominant term is n_prompts x n_tokens x vocab x dtype, from the config."""
    terms = fit.project_peak_rss(HF, 1, 512)[1]
    assert terms["refs"] == 512 * HF["vocab_size"] * 4
    two = fit.project_peak_rss(dict(HF, vocab_size=HF["vocab_size"] * 2), 1, 512)[1]
    assert two["refs"] == 2 * terms["refs"] and two["weights"] == terms["weights"]
    assert max(fit.project_peak_rss(HF, 8, 512)[1], key=lambda k: fit.project_peak_rss(HF, 8, 512)[1][k]) == "refs"


def test_f2_over_budget_grid_is_refused_by_name():
    """F2 (as the CLI faces it): any grid over budget exits 3 naming projection AND budget."""
    budget, cell = fit.budget_bytes()
    for grid in (OVER, dict(BIG, n_seeds=8)):
        try:
            fit.preflight(HF, **grid)
        except fit.FitError as e:
            assert "%.2f GiB" % (budget / 2 ** 30) in str(e) and "refs term=" in str(e)
            continue
        raise AssertionError("%s was NOT refused" % (grid,))


def test_f2b_current_np64_grid_is_accepted_just_under_budget():
    """F2b THE SURPRISE: the 8x512x4 grid projects 5.87/6.00 GiB -> FITS.

    The real run died at anon-rss 6.19 GB, so a projection that says 'fits' here
    is 2% optimistic. The hypothesis' named prediction (this grid is refused) is
    therefore NOT met by a bare peak<=budget predicate.
    """
    budget, _ = fit.budget_bytes()
    peak, terms = fit.project_peak_rss(HF, **BIG)
    assert fit.fits(peak, budget)[0]
    assert 0.9 * budget < peak < budget, "5.87/6.00 GiB is the finding; a moved number is a new finding"
    assert sorted(terms, key=terms.get, reverse=True)[:3] == ["refs", "seeds", "weights"]


def test_f3_cut_grid_is_accepted():
    """F3: 2x512x3 is accepted and reports a peak plus a largest-prompts number."""
    budget, _ = fit.budget_bytes()
    peak, cap = fit.preflight(HF, **CUT)
    assert peak < budget and cap >= CUT["n_prompts"]


def test_f4_survives_python_O():
    """F4: under python -O the refusal is identical -- raise, not assert (falsifier 3)."""
    args = ["--prompts", "8", "--tokens", "1024", "--seeds", "4", "--budgets", "4"]
    plain, opt = _cli(args), _cli(args, ["-O"])
    for out in (plain, opt):
        assert out.returncode == 3, (out.returncode, out.stdout, out.stderr)
        assert "REFUSED" in out.stderr and "memory_max" in out.stderr
    assert plain.stderr.split("|")[0] == opt.stderr.split("|")[0]
    assert _cli(["--prompts", "2", "--tokens", "512", "--seeds", "3"]).returncode == 0


def test_f5_model_free_no_torch():
    """F5: with torch and transformers made un-importable the projection still computes."""
    code = (
        "import sys,importlib.util\n"
        "class B:\n"
        "    def find_spec(self, n, p=None, t=None):\n"
        "        if n.split('.')[0] in ('torch','transformers'): raise ImportError('poisoned ' + n)\n"
        "sys.meta_path.insert(0, B())\n"
        "s=importlib.util.spec_from_file_location('m', %r); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)\n"
        "hf=%r\n"
        "print(int(m.project_peak_rss(hf, 8, 512, 4, 4)[0]), m.max_prompts_seeds(hf, 512, 4, 4))\n"
        % (MOD, HF))
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, cwd=HERE)
    assert out.returncode == 0, out.stderr
    assert out.stdout.split()[0] == str(fit.project_peak_rss(HF, 8, 512, 4, 4)[0])


def test_f6_no_budget_or_path_literals():
    """F6: no '6G', no cgroup path, no spelled-out budget; the budget IS the config cell."""
    src = open(MOD).read()
    for bad in ("6G", "/sys/fs/cgroup", "6442450944", "6 * 1024", "6*1024", "/data/ml"):
        assert bad not in src, bad
    budget, cell = fit.budget_bytes(json.load(open(fit.paths.config_path(MOD))))
    assert cell in fit.BUDGET_CELLS and budget == fit.parse_size(_cell(json.load(open(fit.paths.config_path(MOD))), cell))


def test_f7_monotone_and_max_is_tight():
    """F7: monotone in prompts/tokens/seeds; max_prompts_seeds fits, +1 does not."""
    budget, _ = fit.budget_bytes()
    prev = 0
    for p in (1, 2, 4, 8, 16):
        cur = fit.project_peak_rss(HF, p, 512, 4, 4)[0]
        assert cur > prev
        prev = cur
    for k, dbl in (("n_tokens", 1024), ("n_seeds", 8)):
        a = dict(BIG); b = dict(BIG); b[k] = dbl
        assert fit.project_peak_rss(HF, **b)[0] > fit.project_peak_rss(HF, **a)[0]
    p = fit.max_prompts_seeds(HF, 512, 4, 4, budget)
    assert p > 0 and fit.fits(fit.project_peak_rss(HF, p, 512, 4, 4)[0], budget)[0]
    assert not fit.fits(fit.project_peak_rss(HF, p + 1, 512, 4, 4)[0], budget)[0]
