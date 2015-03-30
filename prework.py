from auana import Preprocess
import time,os

p = Preprocess()


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