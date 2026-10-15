#!/usr/bin/env python3
import http.server,json,os,pathlib,shutil,subprocess,tempfile,threading,time,urllib.request,urllib.error
AGENT="a00-b6ec457f"; OUT=pathlib.Path("datasets/brain-swap/2026-09-24"); CEIL=65536; MARK="The messages above are a conversation to summarize"; S={"log":[]}
def sse(xs): return b"".join(("data: "+json.dumps(x)+"\n\n").encode() for x in xs)+b"data: [DONE]\n\n"
def ch(d,finish=None,usage=None):
 x={"id":"s","object":"chat.completion.chunk","created":0,"model":"stub","choices":[{"index":0,"delta":d,"finish_reason":finish}]}; return {**x,"usage":usage} if usage else x
class H(http.server.BaseHTTPRequestHandler):
 def do_POST(self):
  b=self.rfile.read(int(self.headers.get("content-length",0))); o=json.loads(b); text=json.dumps(o); summary=MARK in text; over=len(b)/3.8>CEIL
  S["log"].append({"request":len(S["log"])+1,"bytes":len(b),"estimated_tokens":round(len(b)/3.8,1),"status":400 if over else 200,"phase":"summary" if summary else "turn","tool_results":sum(m.get("role")=="tool" for m in o["messages"])})
  if over: d=json.dumps({"error":{"message":"context length exceeded","type":"invalid_request_error","code":"context_length_exceeded"}}).encode()
  elif summary: d=sse([ch({"role":"assistant","content":"summary"},"stop",{"prompt_tokens":0,"completion_tokens":1,"total_tokens":1})])
  else: d=sse([ch({"role":"assistant","tool_calls":[{"index":0,"id":"c","type":"function","function":{"name":"bash","arguments":json.dumps({"command":"echo "+"x"*6000})}}]},"tool_calls",{"prompt_tokens":round(len(b)/3.8),"completion_tokens":1,"total_tokens":round(len(b)/3.8)})])
  self.send_response(400 if over else 200); self.send_header("Content-Length",str(len(d))); self.end_headers(); self.wfile.write(d)
 def log_message(self,*a): pass
def post(port,body):
 q=urllib.request.Request(f"http://localhost:{port}",data=body,method="POST")
 try:
  with urllib.request.urlopen(q) as r:return r.status
 except urllib.error.HTTPError as e:return e.code
def selftest(port):
 assert post(port,json.dumps({"messages":[{"role":"user","content":"x"*1000}]}).encode())==200
 assert post(port,json.dumps({"messages":[{"role":"user","content":"x"*260000}]}).encode())==400
 return "PASS valid under/over fixtures"
def arm(name,declared,tmp,port):
 S["log"]=[]; md={"providers":{"stub":{"baseUrl":f"http://localhost:{port}/v1","apiKey":"none","api":"openai-completions","models":[{"id":"stub","contextWindow":60000,"maxTokens":1024}] if declared else []}}}; (tmp/"models.json").write_text(json.dumps(md))
 env={**os.environ,"PI_CODING_AGENT_DIR":str(tmp),"PI_OFFLINE":"1"}; cmd=[shutil.which("pi"),"-p","--no-session","--no-context-files","--no-extensions","--no-skills","--no-prompt-templates","--no-themes","--provider","stub","--model","stub","Grow context"]
 try: subprocess.run(cmd,cwd=".",env=env,stdin=subprocess.DEVNULL,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
 except subprocess.TimeoutExpired: pass
 l=S["log"]; f=next((x["request"] for x in l if x["status"]==400),None); c=next((x["request"] for x in l if x["phase"]=="summary"),None)
 return {"arm":name,"declared_window":60000 if declared else None,"largest_request_bytes":max((x["bytes"] for x in l),default=0),"first_over":f,"compaction_request":c,"400_preceded_compaction":bool(f and c and f<c),"requests":l}
def main():
 global S; srv=http.server.ThreadingHTTPServer(("localhost",0),H); threading.Thread(target=srv.serve_forever,daemon=True).start(); st=selftest(srv.server_port); out={"selftest":st,"arms":[]}
 with tempfile.TemporaryDirectory(prefix="pi-probe-") as td: out["arms"]=[arm("declared",True,pathlib.Path(td),srv.server_port),arm("missing",False,pathlib.Path(td),srv.server_port)]
 (OUT/f"{AGENT}-request-log.json").write_text(json.dumps(out,indent=2)+"\n"); print(json.dumps(out,indent=2))
if __name__=="__main__":main()
