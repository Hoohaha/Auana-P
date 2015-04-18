import sys, os
_work_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
sys.path.append(os.path.dirname(_work_dir))
from auana import Fana


if __name__ == '__main__':
	print "   Broken Frame Demo Start   "
	print "This demo will find where is broken-frames in a song."
	try:
		Fana(sys.argv[1]).broken_frame()
	except IndexError:
		print "Error: Invalid file or file path!"
	os.system("pause")