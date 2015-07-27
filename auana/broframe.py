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

	  		 _______________         
			|		|		|
			|		|		|
			|		|		|
	 	    | 		|  amp	|
	 _______|		|		|
	| amp0	|  amp1	|  		|
	|_______|_______|_______|   
					 _________
					/		
					|
	________________|
	'''
	# num = 0
	# bf = np.zeros(5)
	# num = bro.broken_frame(wdata,len(wdata),bf,framerate)
	# if num == 0:
	# 	bf = []
	# return list(bf)

	DETECT_WIN    = 128
	AMP_THRESHOLD = 0.5
	up_edge       = False

	w    = DETECT_WIN
	amp0 = amp1 = 0
	bf   = []

	AMP_ARRAY = []

	for i in  xrange(len(wdata)/w):

		tem = np.sum(np.abs(wdata[i*w:(i+1)*w]))

		if tem !=0:amp = np.log10(tem) #amplitude
		else:amp = 0
			

		AMP_ARRAY.append(amp)


		#Up edge detection
		if up_edge is False:
			distance0 = amp0-amp
			distance1 = amp1-amp

			if (distance0 > AMP_THRESHOLD) and (distance1 > AMP_THRESHOLD):
				bft = round((i*w)/float(framerate),3)
				up_edge = True

		#Falling edge detection
		else:
			distance0 = amp-amp0
			distance1 = amp1-amp0

			if (distance0 > AMP_THRESHOLD) and (distance1 > AMP_THRESHOLD):
				up_edge = False
				bf.append(bft)

			#if detect a falling edge, but it can`t detect a up edge within 5 seconds, we will reset the FLAG
			elif i%1000 == 0:
				up_edge = False


		#Update amp0 & amp1
		amp0,amp1=amp1,amp


	#######################################
	import matplotlib.pyplot as plt
	x = range(len(wdata)/w)
	plt.title("")
	plt.xlabel('Window')
	plt.ylabel('Amplitude  (log)')# 
	plt.plot(x,AMP_ARRAY)
	plt.show()
	#######################################

	if len(bf) == 0:
		return 0
	else:
		return bf