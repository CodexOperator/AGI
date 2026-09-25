#!/usr/bin/env python3
import http.server,json,os,pathlib,shutil,subprocess,sys,tempfile,threading,time,urllib.request,urllib.error
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[3]/".agi/context/local-maxxing"));import paths
A="a00-d0e2727c";OUT=pathlib.Path(paths.get_local("brain_swap_out_dir"));C=65536;S={"log":[]}
def stream(*xs):return b"".join(("data: "+json.dumps(x)+"\n\n").encode() for x in xs)+b"data: [DONE]\n\n"
def chunk(d,finish=None,u=None):
 x={"id":"s","object":"chat.completion.chunk","created":0,"model":"stub","choices":[{"index":0,"delta":d,"finish_reason":finish}]};return {**x,"usage":u} if u else x
def compactions(log):return [x["seq"] for x in log[1:] if x["tool_results"]<log[x["seq"]-2]["tool_results"]]
class Handler(http.server.BaseHTTPRequestHandler):
 def do_POST(self):
  b=self.rfile.read(int(self.headers.get("content-length",0)));o=json.loads(b);ms=o["messages"];results=sum(m.get("role")=="tool" for m in ms);prev=S["log"][-1]["tool_results"] if S["log"] else None;compact=prev is not None and results<prev;over=len(b)/3.8>C;seq=len(S["log"])+1
  S["log"].append({"seq":seq,"bytes":len(b),"estimated_tokens":round(len(b)/3.8,1),"status":400 if over else 200,"tool_results":results,"is_compaction":compact})
  u={"prompt_tokens":round(len(b)/3.8),"completion_tokens":1,"total_tokens":round(len(b)/3.8)}
  if over:d=json.dumps({"error":{"message":"context length exceeded","type":"invalid_request_error","code":"context_length_exceeded"}}).encode()
  elif compact:d=stream(chunk({"role":"assistant","content":"summary"},"stop",u))
  else:d=stream(chunk({"role":"assistant","tool_calls":[{"index":0,"id":"c","type":"function","function":{"name":"bash","arguments":json.dumps({"command":"echo "+"x"*6000})}}]},"tool_calls",u))
  self.send_response(400 if over else 200);self.send_header("Content-Length",str(len(d)));self.end_headers();self.wfile.write(d)
 def log_message(self,*args):pass
def post(port,payload):
 q=urllib.request.Request(f"http://localhost:{port}",data=json.dumps(payload).encode(),method="POST")
 try:
  with urllib.request.urlopen(q) as r:return r.status,r.read()
 except urllib.error.HTTPError as e:return e.code,e.read()
def selftest(port):
 S["log"]=[];status,body=post(port,{"messages":[{"role":"user","content":"x"*1000}]});assert status==200 and b'"usage"' in body
 status,body=post(port,{"messages":[{"role":"user","content":"x"*260000}]});assert status==400 and b"context length exceeded" in body
 fake=[{"seq":i,"tool_results":n} for i,n in enumerate([0,1,2,1],1)];assert compactions(fake)==[4]
 S["log"]=[];return "PASS under+usage / recognised over / shape 0,1,2,1 flags only 4"
def arm(name,declared,port):
 S["log"]=[]
 with tempfile.TemporaryDirectory(prefix="pi-d0e2727c-") as td:
  tmp=pathlib.Path(td);models=[] if not declared else [{"id":"stub","contextWindow":60000,"maxTokens":1024}];md={"providers":{"stub":{"baseUrl":f"http://localhost:{port}/v1","apiKey":"none","api":"openai-completions","models":models}}};(tmp/"models.json").write_text(json.dumps(md))
  env={**os.environ,"PI_CODING_AGENT_DIR":str(tmp),"PI_OFFLINE":"1"};cmd=[shutil.which("pi"),"-p","--no-session","--no-context-files","--no-extensions","--no-skills","--no-prompt-templates","--no-themes","--provider","stub","--model","stub","Grow context"];start=time.monotonic()
  try:subprocess.run(cmd,env=env,stdin=subprocess.DEVNULL,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
  except subprocess.TimeoutExpired:pass
  path=str(tmp);log=S["log"];first=next((x["seq"] for x in log if x["status"]==400),None);comp=next(iter(compactions(log)),None);return {"arm":name,"declared_window":60000 if declared else None,"temp_dir":path,"largest_request_bytes":max((x["bytes"] for x in log),default=0),"first_over":first,"compaction_request":comp,"400_preceded_compaction":bool(first and comp and first<comp),"wall_seconds":round(time.monotonic()-start,2),"requests":log}
def main():
 server=http.server.ThreadingHTTPServer(("localhost",0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start();result={"selftest":selftest(server.server_port),"arms":[]};S["log"]=[]
 for name,declared in (("declared",True),("missing",False)):result["arms"].append(arm(name,declared,server.server_port))
 OUT.mkdir(parents=True,exist_ok=True);(OUT/f"{A}-request-log.json").write_text(json.dumps(result,indent=2)+"\n");print(json.dumps(result,indent=2));server.shutdown()
if __name__=="__main__":main()
