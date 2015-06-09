import time, os, sys
from auana import Create, Storage


print "Title: PreWork Demo\n-----------------------------------"
print "This demo will extract the fingerprints from reference files and save them. \nFor Recognitions, this is necessary."

try:
	Create()
except ValueError:
	pass
storage = Storage()
f  = storage.get_framerate()

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

			print ("-----------------\nFILE: << %s >>\n  IN PROCESSING....")%(filename)

			if storage.query(filename) is False:
				storage.openf(filepath).hear()

			end = time.time()
			
			print "time cost %f \n"%(end-start)
			print " "

storage.commit()

e = time.time()

storage.items()

print "total time %f'%f"%((e-s)/60,(e-s)%60)