import sys, os
from auana import Storage

print ("Title: File Search Demo")
print ("Date: 2015.4.25\n")

if __name__ == '__main__':
	
	s = Storage()

	try:
		wf = s.openf(sys.argv[1])
		name, accuracy, db, position = wf.recognize(Fast=False)
		print "Match Name: %s  Accuracy: %.3f  Volume: %d  Position: %d'%d"%(name, accuracy, db, position/60, position%60)
	except IndexError:
		print "Error: Invalid file or file path!"
	os.system("pause")