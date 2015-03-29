from auana import Preprocess
import time,os

p = Preprocess()

start = time.time()
# #sample test
sample_path = "E:/FFOutput"
for parent, dirnames, filenames in os.walk(sample_path):
	for filename in filenames:
		if os.path.splitext(filename)[1] == '.wav':
			filepath = os.path.join(parent, filename).replace('\\','/')
			p.hear(filepath)
			print " "
end = start - time.time()
print "time cost",end/60
p.items()
# res = Fana(filepath).stereo_start()
