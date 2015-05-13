import time, os, sys
from auana import Create, Auana


try:
	Create()
except ValueError:
	pass

print "Title: PreWork Demo"
print "This demo will extract the fingerprints from reference files and save them. \nFor Recognitions, this is necessary."

au = Auana()
f  = au.get_framerate()

print "NOTE: The sample rate of songs must be %d, format must be \".wav\".\n-----------------------------------\n\n"%f


sample_path = raw_input("Please input a folder path:")

if sample_path == "":
	sample_path = "E:\FFOutput"
s = time.time()
for parent, dirnames, filenames in os.walk(sample_path):
	for filename in filenames:
		if os.path.splitext(filename)[1] == '.wav':

			filepath = os.path.join(parent, filename).replace('\\','/')
			filename = os.path.basename(filepath)

			start = time.time()

			print ("-----------------\nILE: << %s >>\n  IN PROCESSING....")%(filename)

			if au.query(filename) is False:
				au.openf(filepath).hear()

			end = time.time()
			
			print "time cost %f \n"%(end-start)
			print " "
e=time.time()
au.items()
print "total time %f'%f"%((e-s)/60,(e-s)%60)