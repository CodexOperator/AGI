#!/usr/bin/env python3
import http.server,json,os,pathlib,shutil,subprocess,sys,tempfile,threading,time,urllib.error,urllib.request
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[3]/"extensions/agi/bin"));import locations
A="a00-cdde7530";C=65536;G=locations.find_project_root(__file__);R=locations.source_root(G);O=R/locations.load_config(G)["paths"]["local_maxxing"]["brain_swap_out_dir"];M=("The messages above are a conversation to summarize","This is the PREFIX of a turn");S={"log":[]}
def ch(d,f=None,u=None):
 x={"id":"s","object":"chat.completion.chunk","created":0,"model":"stub","choices":[{"index":0,"delta":d,"finish_reason":f}]};return {**x,"usage":u} if u else x
def stream(*xs):return b"".join(("data: "+json.dumps(x)+"\n\n").encode() for x in xs)+b"data: [DONE]\n\n"
class H(http.server.BaseHTTPRequestHandler):
 def do_POST(self):
  b=self.rfile.read(int(self.headers.get("content-length",0)));o=json.loads(b);t=json.dumps(o);ms=o["messages"];summary=any(x in t for x in M);over=len(b)/3.8>C
  calls={x["id"] for m in ms if m["role"]=="assistant" for x in m.get("tool_calls",[])};results={m["tool_call_id"] for m in ms if m["role"]=="tool"};turn=sum(x["phase"]=="turn" for x in S["log"])+1
  S["log"].append({"seq":len(S["log"])+1,"bytes":len(b),"proxy_tokens":round(len(b)/3.8,1),"status":400 if over else 200,"phase":"summary" if summary else "turn","tool_results":len(results),"elided_results":t.count("[older tool result elided]"),"paired":calls==results})
  u={"prompt_tokens":round(len(b)/3.8),"completion_tokens":1,"total_tokens":round(len(b)/3.8)}
  if over:d=json.dumps({"error":{"message":"context length exceeded","type":"invalid_request_error","code":"context_length_exceeded"}}).encode()
  elif summary or turn>=40:d=stream(ch({"role":"assistant","content":"summary" if summary else "done"},"stop",u))
  else:
   call={"index":0,"id":"c","type":"function","function":{"name":"bash","arguments":json.dumps({"command":"python3 -c 'print(\"x\"*99*228)'"})}};d=stream(ch({"role":"assistant","tool_calls":[call]},"tool_calls",u))
  self.send_response(400 if over else 200);self.send_header("Content-Type","application/json");self.send_header("Content-Length",str(len(d)));self.end_headers();self.wfile.write(d)
 def log_message(self,*args):pass
def post(port,payload):
 q=urllib.request.Request(f"http://localhost:{port}",data=json.dumps(payload).encode(),method="POST")
 try:
  with urllib.request.urlopen(q) as r:return r.status,r.read()
 except urllib.error.HTTPError as e:return e.code,e.read()
def selftest(port):
 base={"messages":[{"role":"user","content":"x"}]};status,body=post(port,base);assert status==200 and b'"usage"' in body
 status,body=post(port,{"messages":[{"role":"user","content":"x"*260000}]});assert status==400 and b"context length exceeded" in body
 for mark in M:
  status,body=post(port,{"messages":[{"role":"user","content":mark}]});assert status==200 and b'"content": "summary"' in body
 return "PASS under+usage / recognised over / both summary prompts"
def arm(name,extension,port):
 S["log"]=[]
 with tempfile.TemporaryDirectory(prefix="pi-context-trim-") as td:
  home=pathlib.Path(td);model={"providers":{"stub":{"baseUrl":f"http://localhost:{port}/v1","apiKey":"none","api":"openai-completions","models":[{"id":"stub","contextWindow":60000,"maxTokens":1024}]}}};(home/"models.json").write_text(json.dumps(model))
  cmd=[shutil.which("pi"),"-p","--no-session","--no-context-files","--no-extensions","--no-skills","--no-prompt-templates","--no-themes","--provider","stub","--model","stub","Grow context"]
  if extension:cmd.extend(["-e",str(O/"a00-cdde7530-context-trim.js")])
  env={**os.environ,"PI_CODING_AGENT_DIR":str(home),"PI_OFFLINE":"1"};start=time.monotonic();timeout=False
  try:result=subprocess.run(cmd,env=env,stdin=subprocess.DEVNULL,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=180)
  except subprocess.TimeoutExpired:timeout=True;result=None
  log=S["log"];return {"arm":name,"requests":len(log),"largest_bytes":max((x["bytes"] for x in log),default=0),"largest_proxy_tokens":max((x["proxy_tokens"] for x in log),default=0),"400s":[x["seq"] for x in log if x["status"]==400],"wall_seconds":round(time.monotonic()-start,2),"timed_out":timeout,"returncode":result.returncode if result else None,"all_calls_paired":all(x["paired"] for x in log),"trace":log}
def main():
 server=http.server.ThreadingHTTPServer(("localhost",0),H);threading.Thread(target=server.serve_forever,daemon=True).start()
 try:result={"selftest":selftest(server.server_port),"arms":[]}
 finally:S["log"].clear()
 for name,extension in (("without_extension",False),("with_extension",True)):result["arms"].append(arm(name,extension,server.server_port))
 O.mkdir(parents=True,exist_ok=True);(O/f"{A}-request-log.json").write_text(json.dumps(result,indent=2)+"\n");print(json.dumps(result,indent=2));server.shutdown()
if __name__=="__main__":main()
