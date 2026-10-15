# POSITIVE CONTROL: proved

- verdict: "proved"
- void: false
- match_ok: true
- params_sha256: "115842dcc7250ec0c103215d80053c38b10e0bf3d638ec47ca8de14e06276747"
- script_commit: "26bc43d84d75a5049ad048b9a1c9e61cb91be345"
- script_dirty: false
- train: [{"seed": 0, "grokked": true, "grok_step": 9200, "steps": 10200, "wall_s": 962.5, "final_train_loss": 1.1263075854791012e-07, "final_train_acc": 1.0, "final_test_loss": 0.00029463309012191745, "final_test_acc": 0.9997762613267703}]
- p1: {"pass": true, "count": 509, "fraction": 0.994140625, "n_neurons": 512, "null_q999": 0.15533866017254172, "null_n": 10240, "twin_seed": 1001, "twin_max": 0.15166161924186583, "count_beat_null": 509, "count_beat_twin": 509, "flat_or_dead": 0, "pk_median": 0.5685517058076093}
- p2: {"pass": true, "n_cover": 3, "freq_counts": {"5": 151, "1": 133, "45": 128, "34": 84, "2": 13}, "cover_fraction": 0.8094302554027505}
- p3: {"pass": true, "freq": 5, "size": 151, "baseline_test_acc": 0.9997762613267703, "baseline_test_loss": 0.00029463309012191745, "ablated_test_acc": 0.40675690793153596, "ablated_test_loss": 4.923486394776334, "drop": 0.5930193533952344, "rand_drop": [0.2347018682179215, 0.11735093410896069, 0.477458328672111, 0.16959391430808812, 0.2470074952455532], "rand_test_acc": [0.7650743931088488, 0.8824253272178096, 0.5223179326546593, 0.8301823470186822, 0.7527687660812171], "rand_test_loss": [1.3783060503343982, 0.4213959920801803, 3.3252336070259974, 0.8842301356741487, 1.2539317210627805]}
- torch: "2.14.0+cu130"
