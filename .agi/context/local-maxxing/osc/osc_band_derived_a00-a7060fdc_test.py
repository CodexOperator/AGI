import importlib.util, os
import pytest  # skip-by-name: this module cannot run without numpy
np = pytest.importorskip('numpy')
HERE=os.path.dirname(__file__)
def load(name,file):
 s=importlib.util.spec_from_file_location(name,os.path.join(HERE,file)); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
fixed=load('fixed','osc_band_kquant_qknorm_a00-bcb6c85e.py'); new=load('new','osc_band_derived_a00-a7060fdc.py')
def test_widths_both_models():
 for np, grid in new.GRID.items():
  fixed.SPEC={'np':np,'nl':1,'nh':1,'kv':1,'group':1}
  for target,widths in grid.items(): assert abs(fixed.bits(widths)-float(target))<=.01
