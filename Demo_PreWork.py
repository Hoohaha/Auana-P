import time, os, sys
from auana import Create, Storage


print ("Title: PreWork Demo\n-----------------------------------")
print ("This demo will extract the fingerprints from reference files and save them. \nFor Recognitions, this is necessary.")


#Create a new Storage
#default framerate: 22050
#default data path: ./data
try:
	Create()
except ValueError:
	pass

#Open a default data storage
storage = Storage()


f  = storage.get_framerate()

print ("NOTE: The sample rate of songs must be %d, format must be \".wav\".\n-----------------------------------\n\n"%f)

try:
	sample_path = raw_input("Please input a folder path:")
except NameError:
	sample_path = input("Please input a folder path:")

if sample_path == "":
	sample_path = "C:\FFOutput"

s = time.time()
for parent, dirnames, filenames in os.walk(sample_path):
	for filename in filenames:
		if os.path.splitext(filename)[1] == '.wav':

			filepath = os.path.join(parent, filename).replace('\\','/')
			filename = os.path.basename(filepath)

			print (filename)
			start = time.time()

			if storage.query(filename) is False:
				storage.Open(filepath).hear()

			end = time.time()
			
			print ("time cost %f \n"%(end-start))
			print (" ")

storage.commit()

e = time.time()

storage.items()

print ("total time %f'%f"%((e-s)/60,(e-s)%60))