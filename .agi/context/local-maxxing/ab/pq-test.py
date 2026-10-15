import time,os,subprocess,tempfile,base64 as B,sys
sys.path.insert(0,'.');from pq import *
h=8;seed=os.urandom(32);pub=b'alive-gen2';t0=time.time();T=tree(seed,pub,h);root=T[-1][0];t1=time.time()
print(f'keygen h={h} ({1<<h} signatures per generation): {t1-t0:.2f}s, ring PQ column = {root.hex()[:16]}... (32 B)')
m=b'tip time sha256 digest-of-the-tip-tree';t0=time.time();s=sign(seed,pub,h,5,m,T);t1=time.time();ok=verify(root,pub,h,m,s);t2=time.time()
print(f'sign {1000*(t1-t0):.0f} ms, verify {1000*(t2-t1):.0f} ms, signature {len(s)} B: verifies {ok}')
print('P2 tampered message:',verify(root,pub,h,m+b'x',s))
print('P3 another generation root:',verify(tree(os.urandom(32),pub,h)[-1][0],pub,h,m,s))
# NESTING: outer ssh-ed25519 signs (payload + inner); a forger holding the OUTER key (a published retired key, or a quantum break) re-signs a changed payload
d=tempfile.mkdtemp();k=d+'/k';subprocess.run(['ssh-keygen','-q','-t','ed25519','-N','','-f',k]);pk=open(k+'.pub').read().split()
open(d+'/a','w').write(f'alive@agi namespaces="agi-checkpoint" {pk[0]} {pk[1]}\n')
def outer(p):
    open(d+'/m','wb').write(p);os.path.exists(d+'/m.sig') and os.remove(d+'/m.sig');subprocess.run(['ssh-keygen','-q','-Y','sign','-n','agi-checkpoint','-f',k,d+'/m'],check=True);return open(d+'/m.sig','rb').read()
def check(payload,inner,osig):
    open(d+'/m','wb').write(payload+b'\n'+B.b64encode(inner));open(d+'/s','wb').write(osig)
    o=subprocess.run(['ssh-keygen','-Y','verify','-f',d+'/a','-I','alive@agi','-n','agi-checkpoint','-s',d+'/s'],stdin=open(d+'/m','rb'),capture_output=True).returncode==0
    return o,verify(root,pub,h,payload,inner)
inner=s;osig=outer(m+b'\n'+B.b64encode(inner))
print('N1 honest nested blob (outer, inner):',check(m,inner,osig))
m2=b'tip time sha256 FORGED-digest';osig2=outer(m2+b'\n'+B.b64encode(inner))
print('N2 forger holds the OUTER key, changes the payload, reuses the inner:',check(m2,inner,osig2))
fake=os.urandom(len(s));osig3=outer(m2+b'\n'+B.b64encode(fake))
print('N3 forger holds the OUTER key, invents an inner:',check(m2,fake,osig3))
print('N4 a quantum forger strips the outer and re-signs only the inner? needs the WOTS secrets: inner verifies =',verify(root,pub,h,m2,s))
