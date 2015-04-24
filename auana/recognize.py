#Author: Halye Guo  Date:2014/12

import numpy as np
import os
from ctypes import *

#Match info struct Definition
class MATCH_INFO(Structure):
    _fields_ = [("accuracy", c_float),
                ("position", c_int)]

#Load the "compare" function from compare.so
__DIR = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
ham = cdll.LoadLibrary(__DIR+"/Compare.so")
ham.Compare.argtypes = [np.ctypeslib.ndpointer(dtype=np.uint32, ndim=1, flags="C_CONTIGUOUS"),
						   np.ctypeslib.ndpointer(dtype=np.uint32, ndim=1, flags="C_CONTIGUOUS"), 
						   c_int,
						   c_int,
						   c_int,
						   c_short,
						   c_int,
						   ]
ham.Compare.restype = MATCH_INFO

###########################################################################
#How many data in fft process, this value must be 2^n. 
DEF_FFT_SIZE = 4096
#Overlap frmate depth 
DEF_OVERLAP = 2
#Sub-fingerprint bit depth
FIN_BIT = 30
#Mel frequency
MEL = (2596*np.log10(1+4000/700.0))/(FIN_BIT+1.0)
#The upper and lower bounds of sub-band. when framerate is 44100
BandTable = [[8,    17], [12 ,  22], [17 ,  27], [22 ,  32], [27 ,  38], 
			 [32 ,  44], [38 ,  51], [44 ,  58], [51 ,  65], [58 ,  73], 
			 [65 ,  81], [73 ,  89], [81 ,  99], [89 , 108], [99 , 119], 
			 [108, 130], [119, 141], [130, 153], [141, 166], [153, 180], 
			 [166, 195], [180, 210], [195, 226], [210, 244], [226, 262], 
			 [244, 282], [262, 302], [282, 324], [302, 347], [324, 372]]

def recognize(catalog,wdata,framerate,channel,Fast=None,return_cha=False):
	'''
	This function is audio recognition.
	
	Compare the target data and source data weather it is same.
	And give the accuracy of recognition and average volume.
	The accuracy is measured by variable: confidence. 
	The more similar, and the confidence is more close to "1".

	Volume is measured by db.

	Parameters
    ----------
	wdata: wave data                                Type:[array]
	sdata: source data(reference data)				Type:[list]
	framerate: sample rate							Type:[int]
	channel: wave channel                           Type:[int]
	Fast: Faster recognize(defualt value is None)   Type:[int]
	return_cha: wheather return the charatics
				which has beeb computed             Type:[array]

	Returns
    ----------
	match_index: matched song's index.              Type:[int]
	max_accuracy: accuracy						 	Type:[float]
	avgdb: average Volume                           Type:[float]

	Data storage format
	----------
	AudioFingerCatalog.pkl       	Save reference audio fingerprint index.
	0.bin                        	Index:0, data
	1.bin							Index:1, data
	...                        		...

	AudioFingerCatalog.pkl
	   	{
		0:'sample0.wav',
	   	1:'sample1.wav',
	   			...
	   	indexN:'samplen.wav',
	   	}

	"1.bin" format 
	   {channel0:data,channel1:data}

	Process
	----------
	step1: get the fingerprint of wave data
	step2: compare the target fingerprint with the sdata, 
		   and return the accuarcy and matched audio index.
		   accuarcy: 0~1, it means the how many fingerprint matched in reference file.
	'''

	tdata,avgdb    = get_fingerprint(wdata,framerate)
	max_accuracy   = 0
	match_index    = None
	match_position = 0
	tlen           = tdata.shape[-1]

	#according the data length, 
	#give different window size and offset to make the search faster.
	if tlen < 90:
		window_size, offset = 4,   1
	elif 90 <= tlen <= 900:
		window_size, offset = 16,  1
	else:
		window_size, offset = 100, 3

	num_win = tlen/window_size
	print window_size,offset
	def get_reference_data(index):
		'''
		This function load data acorrding the index.

		Parameters
	    ----------
		index: the index of the reference file.          Type:[int]

		Returns
	    ----------
		sdata: source data.                				 Type:[array]
		slen: source data length                         Type:[int]
		'''
		sdata = np.fromfile(__DIR+"/data/"+str(index)+".bin",dtype=np.uint32)
		sdata.shape = 2,-1
		slen = sdata.shape[-1]
		return sdata[channel],slen

	#search
	if Fast is not None:
		sdata,slen = get_reference_data(Fast)
		accuracy,position = compare(sdata,tdata,tlen,slen,window_size,offset,num_win)
		if accuracy > 0.1:
			match_index = Fast
			max_accuracy = accuracy
			match_position = position
	else:
		for index in catalog:
			sdata,slen = get_reference_data(index)

			accuracy,position = compare(sdata,tdata,tlen,slen,window_size,offset,num_win)
			#Filter: if accuracy more than 50%, that is to say the it is same with the reference
			if accuracy >= 0.5:
				match_index  = index
				max_accuracy = accuracy
				match_position = position
				break
			#Filter:find the max accuracy, and return
			elif accuracy > max_accuracy:
				match_index  = index
				max_accuracy = accuracy
				match_position = position
	match_position = match_position * (DEF_FFT_SIZE / DEF_OVERLAP) / framerate
	#return_cha: if this variable is set True, we will return the charatics data.
	if return_cha is True:
		return match_index, tdata
	#Else we will return match_audio max_accuracy, avgdb
	return match_index, max_accuracy, avgdb, match_position


#######################################################
#    search function                                                                                                    
#######################################################
def compare(sdata,tdata,tlen,slen,window_size,offset,num_win):
	'''
	Find the similar audio with target data.

	Parameters
    ----------
	sdata: source data(reference data)          Type:[array]
	tdata: target data from target wav file.    Type:[array]
	tlen: the length of tdata                   Type:[int]
	slen: the length of sdata                   Type:[int]
	window_size: search window size             Type:[int]
	offset: window_size move offset on sdata    Type:[short]
	num_win: how many windows in tdata          Type:[int]

	Returns
    ----------
    r.accuracy: 0~100%                          Type:[float]
    r.position: index of sdata                  Type:[int]

	-----------------------------------------
	|-----win1------|-----win2-----|---------
	-----------------------------------------

	In oder to improve efficiency, there are several ways:
		1) the section that have matched, we not search it in next window,
			so we use the variable: next_begain 
		2) if confidence is too low when we have finished the majority search, directly 
		exit and search next file.
	'''
	r = ham.Compare(tdata,sdata,tlen,slen,window_size,offset,num_win)
	return r.accuracy, r.position
	
	#Old version Python
	#***********************************************************#
	#***********************************************************#
	min_seq=0
	min_seq0=0
	confidence=0
	next_begain = 0
	max_index = sdata.shape[-1]-window_size
	stop_condition = 15
	threshold = window_size*FIN_BIT*0.3

	#Arithmetic sequence tolerance uplimit and down limit
	up_limit = window_size+2
	dw_limit = window_size-2

	for a in  xrange(0,tlen/window_size):#target file

		tsta     = a*window_size
		tend     = (a+1)*window_size
		dismin   = 300
		min_seq0 = min_seq

		for index in  xrange(next_begain, max_index,offset):#reference file
			#calculate the distant of each subfingerprint between two songs
			D = tdata[tsta : tend] ^ sdata[index : index+window_size]
			#get distant of two search-windows
			dis = np.sum(np.array([hamming_weight(long(d)) for d in D]))
			# dis = ham.distance(tdata[tsta : tend],sdata[index : index+window_size],window_size)
			if dis <= dismin :
				dismin  = dis
				min_seq = index
				if window_size >10 and dismin <= 70:break

		#filter:block distance is very close, and they are Arithmetic sequence
		if dismin<threshold and dw_limit<=min_seq-min_seq0<=up_limit:
			confidence += 1
			next_begain = min_seq
		#filter:if search done,stop
		if next_begain >= max_index:break
		#filter:if confidence is too low,stop
		if a>stop_condition and confidence<2:return 0
	if (confidence <= 1):
		return 0
	return round(float(confidence)/(tlen/window_size-1), 3)


###########################################################
#   Get audio fingerprint
###########################################################
def get_fingerprint(wdata,framerate,db=True):
	'''
	This function generate a frame, and calculate it`s fingerprint.
	For 5sec files, the overlap is 3/4, others is 1/2.
	'''
	#data length
	data_len = wdata.shape[-1]

	#hanning window
	hanning = _hann(DEF_FFT_SIZE, sym=0)

	#divide the frequency sub-band
	if framerate != 44100:
		#frequency scale
		scale = (framerate>>1)/(DEF_FFT_SIZE>>1+1.0)
		for n in xrange(1,FIN_BIT+1):
			b0 = int(round(700*(10**((n-1)*MELMEL/2596.0)-1)/scale,0))
			b1 = int(round(700*(10**((n+1)*MEL/2596.0)-1)/scale,0))
			BandTable.update({n:[b0,b1]})

	fin= []

	#volume compute
	sumdb = 0
	num = 0

	#index of "wdata"
	sta = 0
	end = DEF_FFT_SIZE

	xxx = 0

	sf = 0L
	s = ""
	while end<data_len:
		#1)generate a frame and get it`s fingerprint (sta:end)
		#2)hanning window to smooth the edge
		xs = np.multiply(wdata[sta:end], hanning)
		
		#fft transfer
		xfp = 20*np.log10(np.abs(np.fft.rfft(xs)[0:373]))

		#update indexs
		sta=sta + DEF_FFT_SIZE/DEF_OVERLAP
		end=sta + DEF_FFT_SIZE

		subfin = 0L

		for n in xrange(0,FIN_BIT):
			p1 = 0
			p2 = 0

			#BandTable look-up
			#use a BandTable to improve the speed of calculate
			b0 = BandTable[n][0]
			b1 = BandTable[n][1]

			max_fp = 0
			max_b = 0
			for b in xrange(b0,b1+1):

				#calculate the Audio center of mass 
				fp = xfp[b]
				if (fp > max_fp): 
					max_fp = fp
					max_b = b

			if max_b - (b0+b1)/2 >= 0:
				subfin |= 1<<(n)

		fin.append(subfin)
	fin = np.array(fin,dtype = np.uint32)

	if db is True:
		return fin,0
 	return fin


def hamming_weight(x):
	m1  = 0x55555555 #binary: 0101...  
	m2  = 0x33333333 #binary: 00110011..  
	m4  = 0x0f0f0f0f #binary:  4 zeros,  4 ones ...  

	x -= (x >> 1) & m1             #put count of each 2 bits into those 2 bits  
	x = (x & m2) + ((x >> 2) & m2) #put count of each 4 bits into those 4 bits   
	x = (x + (x >> 4)) & m4        #put count of each 8 bits into those 8 bits   
	x += x >>  8                   #put count of each 16 bits into their lowest 8 bits  
	x += x >> 16                   #put count of each 32 bits into their lowest 8 bits  
	x += x >> 32                   #put count of each 64 bits into their lowest 8 bits  
	return x & 0x7f

def _hann(M, sym=True):
	'''
	hanning window.
	In order to simplify the application, this function come from scipy.signal.
	'''
	# Docstring adapted from NumPy's hanning function
	if M < 1:
		return np.array([])
	if M == 1:
		return np.ones(1, 'd')
	odd = M % 2
	if not sym and not odd:
		M = M + 1
		n = np.arange(0, M)
		w = 0.5 - 0.5 * np.cos(2.0 * np.pi * n / (M - 1))
	if not sym and not odd:
		w = w[:-1]
	return w