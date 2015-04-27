import sys, os
__dir__ = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
sys.path.append(_work_dir)
from auana import Auana,Fana

print ("Title: File Search Demo")
print ("Date: 2015.4.25\n")

if __name__ == '__main__':
	

	auan = Auana()

	try:
		File = Fana(auan,sys.argv[1])
		name, accuracy, db, position = File.Recognize()
		print "Match Name: %s  Accuracy: %.3f  Volume: %d  Position: %d'%d"%(name, accuracy, db, position/60, position%60)
	except IndexError:
		print "Error: Invalid file or file path!"
	os.system("pause")