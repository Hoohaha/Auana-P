import sys, os
_work_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
sys.path.append(os.path.dirname(_work_dir))
from auana import Fana


if __name__ == '__main__':

	print "  File Search Demo"
	print "This demo will seach an audio file in it`s internal database."
	
	try:
		name, accuracy, db, position = Fana(sys.argv[1]).stereo_start()
		print "Match Name: %s  Accuracy: %.3f  Volume: %d  Position: %d'%d"%(name, accuracy, db, position/60, position%60)
	except IndexError:
		print "Error: Invalid file or file path!"
	os.system("pause")