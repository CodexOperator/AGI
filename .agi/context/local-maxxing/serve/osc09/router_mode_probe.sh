#!/bin/bash
# OSC.09 probe: does the ROUTER's own container command (models-dir mode) have the ~45 s cold first request?
set -u
NAME=coldprobe; PORT=18092; SC=/data/ml/scratch/osc02
S="$(cd "$(dirname "$0")/../../../../.." && pwd)"; OUT="$(python3 "$S/.agi/context/local-maxxing/paths.py" --local serving_sweep_cold_out_dir)"
mkdir -p $OUT/logs
docker rm -f $NAME >/dev/null 2>&1
docker run --rm -d --name $NAME --gpus all -v $SC:/models -p 127.0.0.1:$PORT:8080 \
  ghcr.io/ggml-org/llama.cpp:server-cuda \
  --host 0.0.0.0 --port 8080 --models-dir /models --models-max 1 --fit on --jinja -np 1 --cache-reuse 8 \
  --log-file /models/coldprobe_router.log >/dev/null
for i in $(seq 1 300); do curl -sf --max-time 3 http://127.0.0.1:$PORT/health >/dev/null && break; sleep 1; done
echo "health after ${i}s"
echo '{"model":"Qwen3.5-9B-Q4_K_M","messages":[{"role":"user","content":"hi"}],"max_tokens":8,"temperature":0,"chat_template_kwargs":{"enable_thinking":false}}' > $OUT/req_probe_w.json
python3 - "$PORT" "$OUT" <<'PY'
import json,sys,subprocess,time
port=sys.argv[1]; OUT=sys.argv[2]
raw=open("/data/ml/scratch/osc02/wikitext-2-raw/wiki.test.raw","rb").read()
reqs={"probe_w":{"messages":[{"role":"user","content":"hi"}]},
      "probe_a":{"messages":[{"role":"user","content":raw[10000:19000].decode("utf-8","replace")}]}}
res={}
for k,v in reqs.items():
    v.update({"model":"Qwen3.5-9B-Q4_K_M","max_tokens":8,"temperature":0,"chat_template_kwargs":{"enable_thinking":False}})
    p=OUT+"/req_%s.json"%k; json.dump(v,open(p,"w"))
    t0=time.time()
    r=subprocess.run(["curl","-s","--max-time","900","-X","POST","http://127.0.0.1:%s/v1/chat/completions"%port,"-H","Content-Type: application/json","-d","@"+p],capture_output=True,text=True)
    res[k]={"wall_s":round(time.time()-t0,2),(r.stdout[:200] and "timings"):None}
    try: res[k]["timings"]=json.loads(r.stdout).get("timings")
    except Exception: res[k]["raw"]=r.stdout[:300]
    print(k,json.dumps(res[k]),flush=True)
json.dump(res,open(OUT+"/router_mode_probe.json","w"),indent=1)
PY
docker logs $NAME 2>&1 | tail -5 > $OUT/logs/router_mode_probe_docker.log
cp $SC/coldprobe_router.log $OUT/logs/router_mode_probe_srv.log 2>/dev/null
docker rm -f $NAME >/dev/null 2>&1; echo done
