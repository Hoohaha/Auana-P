import numpy as np

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
	| var0	| var1	|  		
	|		|		|_______		
	|		|		|  var	|
	|_______|_______|_______|   
	_____________          
		         \         
		          |
		          |_______

	  		 _______ _______         
			|		|		|
			|		|		|
			|		|		|
	 	    |  var1	|  var	|
	 _______|		|		|
	| var0	|		|  		|
	|_______|_______|_______|   
			 ________________
			/		
			|
	________|
	'''
	FLAG = 0
	DETECT_WIN = 256
	VAR_THRESHOLD = 1000
	bf = []
	var0 = var1 = 0
	for i in  xrange(len(wdata)/DETECT_WIN):
		var = int(np.var(wdata[i*DETECT_WIN:(i+1)*DETECT_WIN]))
		if i>1:
			if FLAG == 0:
				distance0 = var0-var
				distance1 = var1-var
				if (distance0 > VAR_THRESHOLD) and (distance1 > VAR_THRESHOLD) and (var < 90) :
					FLAG = 1
					bftime = round(((i+1-1) * DETECT_WIN)/float(framerate),3)
					# print "U",distance0,distance1
			elif FLAG == 1:
				distance0 = var - var0
				distance1 = var1- var0
				if (distance0 >VAR_THRESHOLD) and (distance1 > VAR_THRESHOLD) and (var0 < 90):
					# print "F",distance0,distance1
					FLAG = 0
					bf.append(bftime)
				#if detect a falling edge, but it can`t detect a up edge within 5 seconds, we will reset the FLAG
				elif i%860 == 0:
					FLAG = 0
		var0,var1=var1,var

	if len(bf) == 0:
		return 0
	else:
		return bf