import sys, os, random
HARNESS = os.environ.get("IFEVAL_HARNESS", "/data/work/agi/.agi/sessions/iter-SWR.01/a00-559ee702/ifeval")
sys.path.insert(0, HARNESS)
seed = int(sys.argv[1])
random.seed(seed)
from langdetect import DetectorFactory
DetectorFactory.seed = seed
del sys.argv[1]
from absl import app
import evaluation_main
app.run(evaluation_main.main)
