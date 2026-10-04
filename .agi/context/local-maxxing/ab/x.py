import sys,hashlib,base64 as B
from cryptography.hazmat.primitives import serialization as s
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey as XK,X25519PublicKey as XP
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305 as C
p=2**255-19
def xpub(line):  # a ring line's ssh-ed25519 pub -> its X25519 (Montgomery u = (1+y)/(1-y))
    b=B.b64decode(line.split()[1]);y=int.from_bytes(b[-32:],'little')&((1<<255)-1)
    return XP.from_public_bytes(((1+y)*pow(1-y,p-2,p)%p).to_bytes(32,'little'))
def xpriv(path):  # the post's own ssh key file -> the matching X25519 private
    k=s.load_ssh_private_key(open(path,'rb').read(),None);seed=k.private_bytes_raw()
    return XK.from_private_bytes(hashlib.sha512(seed).digest()[:32])
if __name__=='__main__':
    share=b'share-3-of-capsule-C:'+bytes(range(32))
    # wrap a share to alive gen1's RING LINE (public only)
    e=XK.generate();w=e.public_key().public_bytes_raw()+C(hashlib.sha256(e.exchange(xpub(open('k/alive1.pub').read()))).digest()).encrypt(bytes(12),share,None)
    # alive gen1 opens it with its own ssh key file
    z=xpriv('k/alive1');x=C(hashlib.sha256(z.exchange(XP.from_public_bytes(w[:32]))).digest()).decrypt(bytes(12),w[32:],None)
    print('gen1 opens its share:',x==share)
    # HANDOFF: gen1 re-wraps the share to gen2's ring line inside the out-line; the plaintext never leaves the post's process
    e2=XK.generate();w2=e2.public_key().public_bytes_raw()+C(hashlib.sha256(e2.exchange(xpub(open('k/alive2.pub').read()))).digest()).encrypt(bytes(12),x,None)
    x2=C(hashlib.sha256(xpriv('k/alive2').exchange(XP.from_public_bytes(w2[:32]))).digest()).decrypt(bytes(12),w2[32:],None)
    print('gen2 opens the re-wrapped share:',x2==share)
    try: C(hashlib.sha256(xpriv('k/alive1').exchange(XP.from_public_bytes(w2[:32]))).digest()).decrypt(bytes(12),w2[32:],None);print('gen1 opens gen2 share: YES (BAD)')
    except Exception: print('retired gen1 opens the new wrap: no')
    try: C(hashlib.sha256(xpriv('k/dg1').exchange(XP.from_public_bytes(w[:32]))).digest()).decrypt(bytes(12),w[32:],None);print('dg1 opens alive share: YES (BAD)')
    except Exception: print('another post opens it: no')
    print('wrap bytes',len(w))
