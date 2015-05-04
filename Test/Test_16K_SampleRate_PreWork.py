import time, os, sys
__PATH__ = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
sys.path.append(os.path.dirname(__PATH__))
from auana import Preprocess


p = Preprocess(u"E:/16data")

print "Title: PreWork Demo"
print "This demo will extracct the informations from reference files and save them. \n For Recognitions, this is necessary."
print "NOTE: 1> This demo will find \".wav\" in specify folder path. "
print "      2> The sample rate of songs must be 44100, format must be \".wav\".\n"



sample_path = "E:/16MS"

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