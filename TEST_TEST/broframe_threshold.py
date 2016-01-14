# -*- coding: utf-8 -*-
import numpy as np
import wave

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

	# frame length: 5ms
	FRAME_LENGTH  = 0.005
	AMP_THRESHOLD = 0.5
	up_edge       = False

	w    = int(framerate*FRAME_LENGTH)
	amp0 = amp1 = 0
	bf   = []

	AMP_ARRAY = []
	ENG_ARRAY = []
	for i in  xrange(len(wdata)/w):

		tem = np.sum(np.abs(wdata[i*w:(i+1)*w]))

		if tem !=0:
			amp = np.log10(tem) #amplitude
		else:
			amp = 0

		if i>0:
			dis = abs(amp - amp0)
			AMP_ARRAY.append(dis)


		amp0 = amp

		ENG_ARRAY.append(amp)


		# #Up edge detection
		# if up_edge is False:
		# 	distance0 = amp0-amp
		# 	distance1 = amp1-amp

		# 	if (distance0 > AMP_THRESHOLD) and (distance1 > AMP_THRESHOLD):
		# 		bft = round((i*w)/float(framerate),3)
		# 		up_edge = True

		# #Falling edge detection
		# else:
		# 	distance0 = amp-amp0
		# 	distance1 = amp1-amp0

		# 	if (distance0 > AMP_THRESHOLD) and (distance1 > AMP_THRESHOLD):
		# 		up_edge = False
		# 		bf.append(bft)

		# 	#if detect a falling edge, but it can`t detect a up edge within 5 seconds, we will reset the FLAG
		# 	elif i%1000 == 0:
		# 		up_edge = False


		# #Update amp0 & amp1
		# amp0,amp1=amp1,amp


	#######################################
	import matplotlib.pyplot as plt
	x = range(len(wdata)/w)

	plt.title("Amplitude Figure")
	plt.xlabel('Frames')
	plt.ylabel('Amplitude  (log)')# 
	plt.plot(x,ENG_ARRAY)#,marker =".")
	# plt.ylim((4,7))
	# plt.xlim((0,3000))
	num_array=len(AMP_ARRAY)
	plt.show()

	num_bins = 40
	n, bins, patches = plt.hist(AMP_ARRAY, num_bins, range=(0,0.65), facecolor='green', alpha=0.5)
	plt.yticks(np.linspace(0,num_array,101), ("0", 1,2,3,4,5,6,7,8,9,10,11,"10", "20","30","40","50","60","70","80","90","100") ) 
	plt.xlabel(r'Energy distance')
	plt.ylabel(r'probability(100%)')
	plt.ylim((0,400))
	plt.title(r'Histogram of energy distance')

	
	plt.show()
	#######################################








# 	plt.show()


# 	if len(bf) == 0:
# 		return 0
# 	else:
# 		return bf

def _wave_get_data(f):
	"""Private method."""
	#open wav file
	wf = wave.open(f, 'rb')

	nchannels, sampwidth, framerate, nframes = wf.getparams()[:4]

	str_data = wf.readframes(nframes)
	
	wf.close()
	data = np.fromstring(str_data, dtype = np.short)
	data.shape = -1,2
	data = data.T #Transpose

	return data, framerate, nchannels

data,fra,nch=_wave_get_data("C:/SourceCode/Auana-P/TEST_TEST/noise_system.wav")
detect_broken_frame(data[0], fra)

data,fra,nch=_wave_get_data("C:/SourceCode/Auana-P/TEST_TEST/SINE.wav")
detect_broken_frame(data[0], fra)

data,fra,nch=_wave_get_data("C:/SourceCode/Auana-P/TEST_TEST/211.wav")
detect_broken_frame(data[0], fra)

data,fra,nch=_wave_get_data("C:/SourceCode/Auana-P/TEST_TEST/test.wav")
detect_broken_frame(data[0], fra)

# data,fra,nch=_wave_get_data("C:/SourceCode/Auana-P/TEST_TEST/test2.wav")
# detect_broken_frame(data[0], fra)

# data,fra,nch=_wave_get_data("C:/SourceCode/Auana-P/TEST_TEST/test3.wav")
# detect_broken_frame(data[0], fra)