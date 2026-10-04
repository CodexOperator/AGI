# conflict 1: the SEAL column is its own X25519 key per generation (rotated at the same out-line, deleted, NEVER published); the SIGN key is published once sealed
import os,hashlib,subprocess,tempfile
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey as XK,X25519PublicKey as XP
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305 as C
from cryptography.hazmat.primitives import serialization as s
import sys;sys.path.insert(0,'.');from x import xpub,xpriv
share=b'share-3-of-C:'+os.urandom(32)
def wrap(pub,x):e=XK.generate();return e.public_key().public_bytes_raw()+C(hashlib.sha256(e.exchange(pub)).digest()).encrypt(bytes(12),x,None)
def opens(priv,w):
    try:C(hashlib.sha256(priv.exchange(XP.from_public_bytes(w[:32]))).digest()).decrypt(bytes(12),w[32:],None);return True
    except Exception:return False
seal1=XK.generate();sign1='k/alive1'   # gen1: a separate seal key + its ssh sign key
w=wrap(seal1.public_key(),share)
print('S1 the gen1 SEAL key opens its wrap:',opens(seal1,w))
print('S2 the gen1 SIGN key, PUBLISHED, opens it:',opens(xpriv(sign1),w))
w_same=wrap(xpub(open('k/alive1.pub').read()),share)
print('S3 (for contrast, the folded design) the published SIGN key opens a wrap made to it:',opens(xpriv(sign1),w_same))
seal2=XK.generate();w2=wrap(seal2.public_key(),share);del seal1
print('S4 hand-off: gen2 SEAL opens the re-wrap:',opens(seal2,w2),'· ring seal column line =',len(seal2.public_key().public_bytes_raw()),'B raw')
