import sys, os
from auana import Storage

print ("Title: File Search Demo")
print ("Date: 2015.4.25\n")

if __name__ == '__main__':
	
	s = Storage()

	try:
		wf = s.Open(sys.argv[1])

		name, accuracy, position = wf.recognize(Fast=False)
		print ("Match Name: %s  Accuracy: %.3f   Position: %d'%d"%(name, accuracy, position/60, position%60))
	except IndexError:
		print ("Error: Invalid file or file path!")

	os.system("pause")