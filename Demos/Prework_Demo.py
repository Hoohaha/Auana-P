import time, os, sys
_work_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
sys.path.append(os.path.dirname(_work_dir))
from auana import Preprocess


p = Preprocess("E:/16data")

print "  Pre Work Demo"
print "This demo will extracct the informations from reference files and save them. \n For Recognitions, this is necessary."
print "Caution: 1> This demo will find \".wav\" in path<sample_path>."
print "         2> The sample rate of mucics or songs must be 44100, format must be \".wav\"."



sample_path = raw_input("Please input a folder path:")
if sample_path == "":
	sample_path = "E:\\16MS"

for parent, dirnames, filenames in os.walk(sample_path):
	for filename in filenames:
		if os.path.splitext(filename)[1] == '.wav':
			filepath = os.path.join(parent, filename).replace('\\','/')
			
			start = time.time()
			p.hear(filepath)
			end = time.time()
			
			print "time cost %f \n"%(end-start)
			print " "

p.items()