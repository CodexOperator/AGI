import importlib.util, os, numpy as np
HERE=os.path.dirname(__file__)
_s=importlib.util.spec_from_file_location("fixed",os.path.join(HERE,"osc_band_kquant_qknorm_a00-bcb6c85e.py")); fixed=importlib.util.module_from_spec(_s); _s.loader.exec_module(fixed)
W={4.0:[3,3,3,3],5.0:[4,4,4,4],5.5:[3,3,5,5],6.0:[5,5,5,5],6.5:[4,4,6,6],7.0:[6,6,6,6],7.5:[5,5,7,7],7.75:[6,6,7,7]}
def test_widths():
 fixed.SPEC={'nl':1,'nh':1,'kv':1,'np':32,'group':1}
 for target,w in W.items(): assert abs(fixed.bits(w)-target)<=.1
def test_inverse():
 fixed.SPEC={'nl':1,'nh':1,'kv':1,'np':32,'group':1}
 E=np.arange(32.,dtype=float)[::-1][None,None,:]
 a=fixed.arm(E,[5,5,3,3],'energy',1)[0][0,:32].numpy(); b=fixed.arm(-E,[5,5,3,3],'energy',1)[0][0,:32].numpy()
 order=np.argsort(-E[0,0]); assert np.array_equal(b[order],a[order][::-1])
