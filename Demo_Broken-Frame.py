from auana import Fana
import sys, os

if __name__ == '__main__':
	print "********** Broken Frame Demo Start **********"
	try:
		Fana(sys.argv[1]).broken_frame()
	except IndexError:
		print "Error: Invalid file or file path!"
	os.system("pause")