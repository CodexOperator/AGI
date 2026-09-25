"""Acceptance test: all 24 arms are fresh, present, and bit-accounted."""
import datetime as dt, importlib.util, json, os, re, sys
import torch
HERE=os.path.dirname(__file__); sys.path[:0]=[HERE,os.path.dirname(HERE)]
import paths
_spec=importlib.util.spec_from_file_location("fresh",os.path.join(HERE,"osc_fresh_matched_qknorm_a00_e7eaf011.py"))
fresh=importlib.util.module_from_spec(_spec); _spec.loader.exec_module(fresh)

def test_all_24_fresh_cells_recompute_their_actual_bits():
    root=os.path.join(paths.get_local("osc_band_qknorm_dir"),fresh.RUN_ID)
    runs=sorted((os.path.join(root,n) for n in os.listdir(root)
                 if re.fullmatch(r"\d{8}T\d{6}Z",n)),key=os.path.getmtime)
    assert runs, "no dated output run"
    run=runs[-1]; stamp=os.path.basename(run)
    dt.datetime.strptime(stamp,"%Y%m%dT%H%M%SZ")
    summary=json.load(open(os.path.join(run,"summary.json")))
    assert summary["run_dir"]==stamp and summary["cells"]==24
    assert set(summary["models"])==set(fresh.MODELS)
    count=0
    for model,doc in summary["models"].items():
        assert doc["capture"]=="post_rope_per_layer"
        assert doc["fresh_provenance"]["source"]=="this_process"
        assert doc["fresh_provenance"]["reused_cells"]==0
        assert doc["pid"]>0 and os.path.exists(os.path.join(run,model,doc["fresh_provenance"]["bench"]))
        for target in fresh.TARGETS:
            for mode in ("key_only","uniform","random"):
                cell=doc["settings"].get(f"{target:g}:{mode}")
                assert cell and cell["agree"] is not None and cell["kl"] is not None
                assert cell["target_bits"]==target
                assert "prior" not in json.dumps(doc["fresh_provenance"]).lower()
                fresh.fixed.SPEC={"np":doc["np"]}
                recomputed=fresh.fixed.bits(cell["widths"])
                assert cell["actual_bits"]==recomputed
                assert not (isinstance(cell["actual_bits"],str) or cell["actual_bits"] is None)
                if mode=="uniform":
                    assert cell["control"]=="nearest uniform"
                    assert len(cell["widths"])==1
                    assert recomputed!=target
                else:
                    assert len(cell["widths"])==4
                count+=1
    assert count==24

def test_key_profile_mechanism_on_real_captured_tensors():
    """The allocator energy is key-only, per-layer, and not a query interaction."""
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import osc_band_prune as obp
    which="qwen2"; model_path=paths.get(fresh.MODELS[which])
    tok=AutoTokenizer.from_pretrained(model_path)
    model=AutoModelForCausalLM.from_pretrained(model_path, dtype=torch.float32,
                                                 attn_implementation="eager").eval()
    fresh.fixed.install(model); prompts, _=obp.build_eval(tok)
    fresh.fixed.CAP.clear(); fresh.fixed.forward(model, prompts[0], capture=True)
    layer=next(iter(x for x in fresh.fixed.CAP if isinstance(x,int)))
    q,k=fresh.fixed.CAP[layer]
    before=fresh.key_energy(k, fresh.fixed.SPEC)
    q2=q.clone(); q2[..., 0, :] *= 5.0
    fresh.fixed.CAP[layer]=(q2,k)
    after=fresh.key_energy(fresh.fixed.CAP[layer][1], fresh.fixed.SPEC)
    assert torch.equal(before, after)
    rows=fresh.keyprofile(model, prompts[:1], fresh.fixed.SPEC)
    assert rows.shape[0] == fresh.fixed.SPEC["nl"] and not torch.equal(rows[0], rows[1])
