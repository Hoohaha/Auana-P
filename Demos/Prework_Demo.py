import time, os, sys
_work_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
sys.path.append(os.path.dirname(_work_dir))
from auana import Preprocess


p = Preprocess()

print "  Pre Work Demo"
print "This demo will extracct the informations from reference files and save them. \n For Recognitions, this is necessary."
print "Caution: 1> This demo will find \".wav\" in path<sample_path>."
print "         2> The sample rate of mucics or songs must be 44100, format must be \".wav\"."

#Memory the folder
sample_path = "E:/FFOutput"
for parent, dirnames, filenames in os.walk(sample_path):
	for filename in filenames:
		if os.path.splitext(filename)[1] == '.wav':
			filepath = os.path.join(parent, filename).replace('\\','/')
			start = time.time()
			p.hear(filepath)
			end = time.time() - start
			print "time cost %f \n"%end
			print " "

p.items()