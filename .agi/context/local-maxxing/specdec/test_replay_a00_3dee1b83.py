import importlib.util, os
P=os.path.join(os.path.dirname(__file__),"replay_a00_3dee1b83.py")
s=importlib.util.spec_from_file_location("replay",P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
def test_copy_accepts():
    prompt=list(range(12))*10; target=list(range(12))*5
    for r in m.RULES:
        x=m.replay(prompt,target,r)
        assert x["accepted"] >= 48 and x["rate"] > .9
def test_novel_has_no_acceptance():
    x=m.replay(list(range(1000)),list(range(100000,100100)),"ngram-simple")
    assert x=={"drafted":0,"accepted":0,"rate":0.0,"hit_rate":0.0}
def test_curve_is_monotone():
    assert all(b[1]>=a[1] for a,b in zip(m.curve([(0,.7),(.5,1),(1,2)]),m.curve([(0,.7),(.5,1),(1,2)])[1:]))
def test_parts_labels():
    p=m.parts({"content":[{"type":"thinking","thinking":"x"},{"type":"text","text":"y"},{"type":"toolCall","name":"edit","arguments":{}}]})
    assert [x[0] for x in p]==["thinking","text","edit"]
