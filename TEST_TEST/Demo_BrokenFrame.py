import sys, os
from auana import *

if __name__ == '__main__':
	print ("Title: Broken Frame Demo")
	print "Note: This demo will find where is broken-frames in a song.\n\n"



	p = ["1-sample.wav","b_noise_5.wav", "b_noise_10.wav", "b_noise_15.wav","b_noise_20.wav","b_noise_25.wav","b_noise_30.wav","b_noise_35.wav","b_noise_40.wav"] 

	for path in p:
		print path
		w = Open(path)

		bf = w.detect_broken_frame()

		print ("left  channel:", bf["left"])
		print ("right channel:", bf["right"])


	os.system("pause")