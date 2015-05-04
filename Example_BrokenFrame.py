import sys, os
_work_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
sys.path.append(_work_dir)
from auana import Auana, Fana


if __name__ == '__main__':
	print "Title: Broken Frame Demo"
	print "Note: This demo will find where is broken-frames in a song.\n\n"
	aua = Auana()
	try:
		bf = Fana(aua, sys.argv[1]).detect_Broken_Frame()
		for b in bf:
			print "%s channel"%b
			for ti in bf[b]:
				print ti 
	except IndexError:
		print "Error: Invalid file or file path!"
	os.system("pause")