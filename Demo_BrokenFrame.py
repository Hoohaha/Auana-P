import sys, os
from auana import *

if __name__ == '__main__':
	print ("Title: Broken Frame Demo")
	print "Note: This demo will find where is broken-frames in a song.\n\n"


	try:
		path = sys.argv[1]
	except IndexError:
		print "Error: Invalid file or file path!"
		os._exit(1)


	w = Open(path)

	bf = w.detect_broken_frame()

	print ("left  channel:", bf["left"])
	print ("right channel:", bf["right"])


	os.system("pause")