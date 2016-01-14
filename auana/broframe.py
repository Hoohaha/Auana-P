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

def detect_broken_frame(wdata, framerate):

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
	AMP_THRESHOLD = 4
	up_edge       = False

	# print framerate

	w    = int(framerate*FRAME_LENGTH)

	amp0 = amp1 = 0
	bf   = []
	last_dis = 0

	AMP_ARRAY = []
	n = 0

	for i in  xrange(len(wdata)/w):

		tem = np.sum(np.abs(wdata[i*w:(i+1)*w]))

		if tem !=0:
			amp = np.log10(tem) #amplitude
		else:
			amp = 0

		#Up edge detection
		if up_edge is False:
			dis  = amp1-amp
			ldis = amp0-amp

			if (dis >= AMP_THRESHOLD) and (ldis>=AMP_THRESHOLD):# and (distance1 > 0):#AMP_THRESHOLD-0.2
				bft = round((i*w)/float(framerate),3)
				up_edge = True
				n = 0

		#Falling edge detection
		else:
			n += 1
			dis = amp1-amp0
			ldis = amp-amp0

			if (dis >= AMP_THRESHOLD) and (ldis>=AMP_THRESHOLD):#AMP_THRESHOLD-0.2  (distance0 > 0) and 
				# print dis-ldis,i,amp0,amp1,amp
				up_edge = False
				n = 0
				bf.append(bft)

			#if detect a falling edge, but it can`t detect a up edge within 5 seconds, we will reset the FLAG
			elif n%400 == 0:
				n = 0
				up_edge = False


		#Update amp0 & amp1
		amp0 = amp1
		amp1 = amp


		# #Up edge detection
		# if up_edge is False:
		# 	distance0 = amp0-amp

		# 	if (distance0 > AMP_THRESHOLD):# and (distance1 > 0):#AMP_THRESHOLD-0.2
		# 		bft = round((i*w)/float(framerate),3)
		# 		up_edge = True

		# #Falling edge detection
		# else:
		# 	distance0 = amp-amp0
		# 	distance1 = amp1-amp0

		# 	if (distance1 > AMP_THRESHOLD):#AMP_THRESHOLD-0.2  (distance0 > 0) and 
		# 		up_edge = False
		# 		bf.append(bft)

		# 	#if detect a falling edge, but it can`t detect a up edge within 5 seconds, we will reset the FLAG
		# 	elif i%100 == 0:
		# 		up_edge = False


		# #Update amp0 & amp1
		# amp0,amp1=amp1,amp


	# #######################################
	# import matplotlib.pyplot as plt
	# x = range(len(wdata)/w)
	# plt.title("")
	# plt.xlabel('Window')
	# plt.ylabel('Amplitude  (log)')# 
	# plt.plot(x,AMP_ARRAY)
	# plt.show()
	# #######################################



	# import matplotlib.mlab as mlab
	# import matplotlib.pyplot as plt
 
	# num_bins = 90

	# # the histogram of the data
	# n, bins, patches = plt.hist(AMP_ARRAY, num_bins, normed = True, facecolor='green', alpha=0.5)

	# plt.xlabel('Distance')
	# plt.ylabel('Probability(100%)')
	# plt.title(r'Histogram of amplitude')

	# plt.show()


	if len(bf) == 0:
		return 0
	else:
		return bf