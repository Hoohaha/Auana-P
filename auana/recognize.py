#Author: Halye Guo  Date:2014/12
import numpy as np
# import scipy.signal as signal
import os
current_directory = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
from ctypes import *

class MATCH_INFO(Structure):
    _fields_ = [("accuracy", c_float),
                ("position", c_int)]

ham = cdll.LoadLibrary(current_directory+"/Compare.so")
ham.Compare.argtypes = [np.ctypeslib.ndpointer(dtype=np.uint32, ndim=1, flags="C_CONTIGUOUS"),
						   np.ctypeslib.ndpointer(dtype=np.uint32, ndim=1, flags="C_CONTIGUOUS"), 
						   c_int,
						   c_int,
						   c_int,
						   c_short,
						   ]
ham.Compare.restype = MATCH_INFO

#How many data in fft process, this value must be 2^n. 
DEFAULT_FFT_SIZE = 4096
#Sub-fingerprint bit depth
FIN_BIT = 32
#Mel frequency
mel = (2596*np.log10(1+4000/700.0))/(FIN_BIT+1.0)
#The upper and lower bounds of sub-band. 
BandTable = {1: [0  ,   8],  2: [4  ,  12],  3: [8  ,  17],  4: [12 ,  22], 
			 5: [17 ,  27],  6: [22 ,  32],  7: [27 ,  38],  8: [32 ,  44],
			 9: [38 ,  51], 10: [44 ,  58], 11: [51 ,  65], 12: [58 ,  73], 
			13: [65 ,  81], 14: [73 ,  89], 15: [81 ,  99], 16: [89 , 108], 
			17: [99 , 119], 18: [108, 130], 19: [119, 141], 20: [130, 153],
			21: [141, 166], 22: [153, 180], 23: [166, 195], 24: [180, 210], 
			25: [195, 226], 26: [210, 244], 27: [226, 262], 28: [244, 282], 
			29: [262, 302], 30: [282, 324], 31: [302, 347], 32: [324, 372]}

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

				index0.yml
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
	tlen           = tdata.shape[-1]

	#according the data length, 
	#give different window size and offset to make the search faster.
	if tlen < 90:
		window_size, offset = 4,   1
	elif 90 <= tlen <= 900:
		window_size, offset = 16,  2
	else:
		window_size, offset = 100, 3

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
		sdata = np.fromfile(current_directory+"/data/"+str(index)+".bin",dtype=np.uint32)
		sdata.shape = 2,-1
		slen = sdata.shape[-1]
		return sdata[channel],slen

	#search
	if Fast is not None:
		sdata,slen = get_reference_data(Fast)
		accuracy,position = find_match(sdata,tdata,tlen,slen,window_size,offset)
		if accuracy > 0.1:
			match_index = Fast
			max_accuracy = accuracy
	else:
		for index in catalog:
			sdata,slen = get_reference_data(index)

			accuracy,position = find_match(sdata,tdata,tlen,slen,window_size,offset)
			#filter: if accuracy more than 50%, that is to say the it is same with the reference
			if accuracy >= 0.5:
				match_index  = index
				max_accuracy = accuracy
				break
			#filter:find the max accuracy, and return
			elif accuracy > max_accuracy:
				match_index  = index
				max_accuracy = accuracy

	#return_cha: if this variable is set True, we will return the charatics data.
	if return_cha is True:
		return match_index, tdata
	#Else we will return match_audio max_accuracy, avgdb
	return match_index, max_accuracy, avgdb, position


#######################################################
#    search function                                                                                                    
#######################################################
def find_match(sdata,tdata,tlen,slen,window_size,offset):
	'''
	Find the similar audio with target data.

	Parameters
    ----------
	sdata: source data(reference data)          Type:[array]
	tdata: target data from target wav file.    Type:[array]
	tlen: the length of tdata                   Type:[int]

	Returns
    ----------
    confidence: 0~100%                          Type:[float]


	-----------------------------------------
	|-----win1------|-----win2-----|---------
	-----------------------------------------

	In oder to improve efficiency, there are several ways:
		1) the section that have matched, we not search it in next window,
			so we use the variable: next_begain 
		2) if confidence is too low when we have finished the majority search, directly 
		exit and search next file.
	'''
	r = ham.Compare(tdata,sdata,tlen,slen,window_size,offset)
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
	global DEFAULT_OVERLAP
	data_len = wdata.shape[-1]
	#Overlap frmate depth
	DEFAULT_OVERLAP = 2

	scale = (framerate/2.0)/(DEFAULT_FFT_SIZE/2.0+1)

	fin= []
	sumdb = 0
	num = 0
	sta = 0
	end = DEFAULT_FFT_SIZE

	hanning = _hann(DEFAULT_FFT_SIZE, sym=0)

	while end<data_len:
		#generate a frame and get it`s fingerprint
		#hanning window to smooth the edge
		xs = np.multiply(wdata[sta:end], hanning)
		#fft transfer
		xfp = 20*np.log10(np.abs(np.fft.rfft(xs)[0:373]))
		
		sta=sta+DEFAULT_FFT_SIZE/DEFAULT_OVERLAP
		end=sta+DEFAULT_FFT_SIZE
		
		subfin = 0L

		for n in  xrange(1,FIN_BIT+1):
			p1 = 0
			p2 = 0
			if len(BandTable)== 32:
				#BandTable look-up
				b0 = BandTable[n][0]
				b1 = BandTable[n][1]
			else:
				#use a BandTable to improve the speed of calculate
				b0 = int(round(700*(10**((n-1)*mel/2596.0)-1)/scale,0))
				b1 = int(round(700*(10**((n+1)*mel/2596.0)-1)/scale,0))
				BandTable.update({n:[b0,b1]})

			for b in xrange(b0,b1+1):
				#calculate the Audio center of mass 
				fp = xfp[b]
				p1 += fp*b
				p2 += fp
				num += 1
			#calculate the average volume of one fingerprint
			sumdb += p2
			
			#quantization
			if p1/p2-(b0+b1)/2 >= 0:
				subfin = subfin | (1<<(n-1))
		fin.append(subfin)

	fin = np.array(fin,dtype = np.uint32)
	#fin:the file`s fingerprint
	#sumdb/num:the average volume of the file`s
	if db is True:
 		return fin,sumdb/num
 	else:
 		return fin
# def fft_transfer():


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
