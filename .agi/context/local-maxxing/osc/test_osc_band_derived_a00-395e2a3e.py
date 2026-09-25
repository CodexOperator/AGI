import importlib.util, os
import pytest
p=os.path.join(os.path.dirname(__file__),'osc_band_derived_a00-395e2a3e.py')
s=importlib.util.spec_from_file_location('derived',p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
@pytest.mark.parametrize('npv',[32,64])
def test_search_has_exact_bits_and_energy_order(npv):
    for tag in m.TAGS:
        w=m.search(npv,float(tag)); assert w is not None
        m.fixed.SPEC={'np':npv}
        assert abs(m.fixed.bits(w)-float(tag))<=.01
        assert w[0]>=w[1]>=w[2]>=w[3]
def test_45_crosscheck():
    assert m.search(32,4.5)==(5,5,3,3)
