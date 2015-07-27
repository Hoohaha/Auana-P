import numpy as np

# import os 
# current_directory = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
# from ctypes import *
# bro = cdll.LoadLibrary(current_directory+"/broken.so")
# bro.broken_frame.argtypes = [np.ctypeslib.ndpointer(dtype=np.int16, ndim=1, flags="C_CONTIGUOUS"),
# 							c_int,
# 							np.ctypeslib.ndpointer(dtype=np.float, ndim=1), #
# 							c_int]
# bro.broken_frame.restype = c_int

def detect_broken_frame(wdata,framerate):
	'''
	To detect broken frame.

	Parameters
    ----------
	wdata: wave data          					Type:[array]
	framerate: sample rate.    					Type:[int]

	Returns
    ----------
    bf: broken frame                          	Type:[list]
	 _______ _______           
	|		|		|
	|		|		|		
	|		|		|
	| amp0	| amp1	|  		
	|		|		|_______		
	|		|		|  amp	|
	|_______|_______|_______|   
	_____________          
		         \         
		          |
		          |_______

	  		 _______ _______         
			|		|		|
			|		|		|
			|		|		|
	 	    |  amp1	|  amp	|
	 _______|		|		|
	| amp0	|		|  		|
	|_______|_______|_______|   
			 ________________
			/		
			|
	________|
	'''
	# num = 0
	# bf = np.zeros(5)
	# num = bro.broken_frame(wdata,len(wdata),bf,framerate)
	# if num == 0:
	# 	bf = []
	# return list(bf)

	import matplotlib.pyplot as plt

	plt.title("Diagram")
	plt.xlabel('Noise')
	plt.ylabel('Fault rate')

	FLAG = 0
	DETECT_WIN = 256
	amp_THRESHOLD = 2000
	w = DETECT_WIN
	bf = []
	amp0 = amp1 = 0
	AMP_ARRAY = []

	x = range(len(wdata)/w)

	for i in  xrange(len(wdata)/w):
		# amp = int(np.var(wdata[i*DETECT_WIN:(i+1)*DETECT_WIN]))
		amp = np.log10(np.sum(np.abs(wdata[i*w:(i+1)*w])))#amplitude
		AMP_ARRAY.append(amp)
		# if i>0:
		# 	# if FLAG == 0:
		# 	distance0 = amp0-amp
		# 	AMP_ARRAY.append(distance0)
				#distance1 = amp1-amp

		# 		if (distance0 > amp_THRESHOLD) and (distance1 > amp_THRESHOLD) and (distance1/amp > 10) :
		# 			FLAG = 1
		# 			bftime = round(((i+1-1) * DETECT_WIN)/float(framerate),3)
		# 			print "U",distance0,distance1,i
		# 	elif FLAG == 1:
		# 		distance0 = amp - amp0
		# 		distance1 = amp1- amp0
		# 		if 323<=i<=330:
		# 			print "F",distance0,distance1,amp
		# 		if (distance0 >amp_THRESHOLD) and (distance1 > amp_THRESHOLD) and (distance0/amp0 > 10):
		# 			# print "F",distance0,distance1,i
		# 			FLAG = 0
		# 			bf.append(bftime)
		# 		#if detect a falling edge, but it can`t detect a up edge within 5 seconds, we will reset the FLAG
		# 		elif i%860 == 0:
		# 			FLAG = 0

		#amp0,amp1=amp1,amp

	plt.plot(x,AMP_ARRAY)
	plt.show()

	if len(bf) == 0:
		return 0
	else:
		return bf