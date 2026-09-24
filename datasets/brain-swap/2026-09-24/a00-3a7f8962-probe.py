#!/usr/bin/env python3
"""Loopback ceiling/compaction probe; records sizes and phases, never message text."""
import http.server,json,os,pathlib,shutil,subprocess,tempfile,threading
ROOT=pathlib.Path.cwd(); AGENT="a00-3a7f8962"; OUT=ROOT/"datasets/brain-swap/2026-09-24"
CEILING=65536; MARK="The messages above are a conversation to summarize"; state={"arm":"","log":[]}
def sse(items):
 return b"".join(("data: "+json.dumps(x)+"\n\n").encode() for x in items)+b"data: [DONE]\n\n"
def chunk(delta,finish=None,usage=None):
 x={"id":"s","object":"chat.completion.chunk","created":0,"model":"stub","choices":[{"index":0,"delta":delta,"finish_reason":finish}]}
 if usage:x["usage"]=usage; return x
class Stub(http.server.BaseHTTPRequestHandler):
 def do_POST(self):
  body=self.rfile.read(int(self.headers.get("content-length",0))); obj=json.loads(body)
  text=json.dumps(obj); summary=MARK in text; tool=any(m.get("role")=="tool" for m in obj["messages"])
  phase="summary" if summary else "turn"; over=len(body)>CEILING*3.80
  state["log"].append({"request":len(state["log"])+1,"bytes":len(body),"estimated_tokens_bytes_div_3_80":round(len(body)/3.80,1),"phase":phase,"status":400 if over else 200})
  if over:
   data=json.dumps({"error":{"message":"context length exceeded","type":"invalid_request_error","code":"context_length_exceeded"}}).encode(); self.send_response(400)
  else:
   if summary: data=sse([chunk({"role":"assistant","content":"summary"},"stop",{"prompt_tokens":0,"completion_tokens":1,"total_tokens":1})])
   elif tool and not any(x["phase"]=="summary" and x["status"]==200 for x in state["log"][:-1]): data=sse([chunk({"role":"assistant","tool_calls":[{"index":0,"id":"call","type":"function","function":{"name":"bash","arguments":json.dumps({"command":"python3 -c 'print(\"x\"*24000)'"})}}]},"tool_calls")])
   else: data=sse([chunk({"role":"assistant","content":"ok"},"stop",{"prompt_tokens":0,"completion_tokens":1,"total_tokens":1})])
   self.send_response(200)
  self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(data))); self.end_headers(); self.wfile.write(data)
 def log_message(self,*_):pass
def fixture():
 server=http.server.ThreadingHTTPServer(("localhost",0),Stub); server.daemon_threads=True; threading.Thread(target=server.serve_forever,daemon=True).start()
 for n in (100,CEILING*3):
  p=subprocess.run(["python3","-c",f"import urllib.request;u='http://localhost:{server.server_port}';d=urllib.request.Request(u,data=b'x'*({n}+1),method='POST');\ntry:urllib.request.urlopen(d)\nexcept Exception as e: print(e.code)"],capture_output=True,text=True)
  assert p.stdout.strip()==("200" if n<=100 else "400")
 return "PASS: 101-byte fixture=200; 249238-byte fixture=400"
def arm(name,declared,tmp,port):
 state.update(arm=name,log=[]); models={"providers":{"stub":{"baseUrl":f"http://localhost:{port}/v1","apiKey":"none","api":"openai-completions","models":([{"id":"stub","contextWindow":60000,"maxTokens":1024}] if declared else [])}}}
 (tmp/"models.json").write_text(json.dumps(models)); env={**os.environ,"PI_CODING_AGENT_DIR":str(tmp),"PI_OFFLINE":"1"}
 cmd=[shutil.which("pi"),"-p","--no-session","--no-context-files","--no-extensions","--no-skills","--no-prompt-templates","--no-themes","--provider","stub","--model","stub","Grow context"]
 try: p=subprocess.run(cmd,cwd=ROOT,env=env,stdin=subprocess.DEVNULL,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60); rc,err=p.returncode,p.stderr
 except subprocess.TimeoutExpired as e: rc,err="timeout",(e.stderr or b"").decode(errors="replace")
 log=state["log"]; first400=next((x["request"] for x in log if x["status"]==400),None); comp=next((x["request"] for x in log if x["phase"]=="summary"),None)
 print(name,rc,log[-2:],file=os.sys.stderr,flush=True)
 return {"arm":name,"declared_contextWindow":60000 if declared else None,"returncode":rc,"largest_request_bytes":max((x["bytes"] for x in log),default=0),"passed_65536":any(x["bytes"]>CEILING for x in log),"first_400_request":first400,"compaction_request":comp,"compacted_after_400":bool(first400 and comp and comp>first400),"request_log":log,"stderr_tail":err[-300:]}
def main():
 selftest=fixture(); server=http.server.ThreadingHTTPServer(("localhost",0),Stub); server.daemon_threads=True; threading.Thread(target=server.serve_forever,daemon=True).start()
 with tempfile.TemporaryDirectory(prefix="pi-probe-") as td:
  tmp=pathlib.Path(td); results=[arm("declared",True,tmp,server.server_port),arm("missing",False,tmp,server.server_port)]
 out={"agent_id":AGENT,"pi_version":"0.67.68","ceiling_tokens":CEILING,"reserve_tokens":16384,"selftest":selftest,"arms":results}
 (OUT/f"{AGENT}-request-log.json").write_text(json.dumps(out,indent=2)+"\n"); print(json.dumps(out,indent=2))
if __name__=="__main__":main()
