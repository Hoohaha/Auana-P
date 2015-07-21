#Author: Halye Guo  Date:2014/12
import os
import numpy as np
from ctypes import *
from auana.common import hann

#############################################################################
#Structure Definition:
#1>
#Match Info Structure Definition
class MATCH_INFO(Structure):
    _fields_ = [("accuracy",  c_float),
                ("position",  c_int)]

#2>
#Compare Parameters Structure Definition
class COMPARE_PARAMETERS(Structure):
	_fields_ = [("window_size", c_short),
				("offset"     , c_short),
				("threshold"  , c_short),
				("num_win"    , c_short)]

__PATH = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')

############################################################################
#Load the "compare" function from compare.so
com = cdll.LoadLibrary(__PATH + "/Compare.so")

com.Compare.argtypes = [np.ctypeslib.ndpointer(dtype=np.uint32, ndim=1, flags="C_CONTIGUOUS"),
						np.ctypeslib.ndpointer(dtype=np.uint32, ndim=1, flags="C_CONTIGUOUS"), 
						c_int,
						c_int,
						COMPARE_PARAMETERS]

com.Compare.restype = MATCH_INFO

###########################################################################
#Global Parameters
#Default FFT Size: How many data in FFT process, this value must be 2^n. 
DEF_FFT_SIZE = 2048
#Default Overlap Frame Depth: 0~1
DEF_OVERLAP  = 0.5
#Default Fingerprint Bit Depth
DEF_FIN_BIT  = 32
#Default Max frequency
DEF_MAX_FRQ  = 4000.0

###########################################################################
#Max Mel Frequency
MEL = (2596*np.log10(1+DEF_MAX_FRQ/700.0))/(DEF_FIN_BIT+1.0)


###########################################################################
# The upper and lower bounds of sub-band. 
# framerate/fft_size = 44100/4096 = 22050/2048
BandTable_1 = [[0  ,   8], [4  ,  12], [8,    17], [12 ,  22], 
			   [17 ,  27], [22 ,  32], [27 ,  38], [32 ,  44], 
			   [38 ,  51], [44 ,  58], [51 ,  65], [58 ,  73], 
			   [65 ,  81], [73 ,  89], [81 ,  99], [89 , 108], 
			   [99 , 119], [108, 130], [119, 141], [130, 153], 
			   [141, 166], [153, 180], [166, 195], [180, 210], 
			   [195, 226], [210, 244], [226, 262], [244, 282], 
			   [262, 302], [282, 324], [302, 347], [324, 372]]
# framerate/fft_size = 44100/2048
 
# framerate/fft_szie = 22050/4096
BandTable_2 = [[0 ,   16], [8  ,  25], [16 ,  34], [25 ,  44], 
			   [34 ,  54], [44 ,  65], [54 ,  76], [65 ,  89], 
			   [76 , 102], [89 , 115], [102, 130], [115, 145],
			   [130, 162], [145, 179], [162, 197], [179, 217], 
			   [197, 237], [217, 259], [237, 282], [259, 307], 
			   [282, 333], [307, 360], [333, 390], [360, 420], 
			   [390, 453], [420, 488], [453, 524], [488, 563], 
			   [524, 605], [563, 648], [605, 694], [648, 743]]



def recognize(MaxID,wdata,framerate,channel,datapath,Fast=None):
	'''
	This function is audio recognition.
	
	Compare the target data and source data weather it is same.
	And give the accuracy of recognition and average volume.
	The accuracy is measured by variable: confidence. 
	The more similar, and the confidence is more close to "1".

	Volume is measured by db.

	Parameters
    ----------
    MaxID: Max ID                                   Type:[int]
	wdata: Wave data stream                         Type:[array]
	framerate: Frame rate							Type:[int]
	channel: Wave channel                           Type:[int]
	datapath: Where the data was saved				Type:[string]
	Fast: Faster recognize(default:None)   			Type:[int]

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
				0: 'sample0.wav',
				1: 'sample1.wav',
				...
				MaxID:'samplen.wav',
		   	}

		"1.bin" format 
		   {channel0:data,channel1:data}

	Steps
	----------
	step1: get the fingerprint of PCM stream
	step2: compare the target fingerprint with the sdata, 
		   and return the accuarcy and matched audio index.
		   accuarcy: 0~1, it means the how percentage fingerprint matched in reference file.
	'''

	tdata          = get_fingerprint(wdata,framerate)
	max_accuracy   = 0
	match_index    = None
	match_position = 0
	tlen           = tdata.shape[-1]


	#Adaptive parameters configure:
	#window_size: How many fingerprints in a window.
	#offset     : window move offset
	#fault_tolerant: How many fault bits in a 32-bit fingerprints

	if tlen < 90:
	 	window_size, offset, fault_tolerant = 4,   1,  12
	elif 90 <= tlen <= 900:
		window_size, offset, fault_tolerant = 16,  1,  13
	else:
		window_size, offset, fault_tolerant = 128, 2,  13


	compare_config = COMPARE_PARAMETERS()

	compare_config.window_size = window_size
	compare_config.offset      = offset
	compare_config.threshold   = (int)(window_size*fault_tolerant)
	compare_config.num_win     = (int)(tlen/window_size)
	


	def get_reference_data(index):
		'''
		This function load data by the index.

		Parameters
		----------
		index: the index of the reference file.          Type:[int]

		Returns
	    ----------
		sdata: source data.                				 Type:[array]
		slen: source data length                         Type:[int]
		'''
		sdata = np.fromfile(datapath + "/" +str(index)+".bin",dtype=np.uint32)
		sdata.shape = 2,-1
		slen = sdata.shape[-1]
		return sdata[channel], slen

	#search
	if Fast is not None:
		sdata,slen = get_reference_data(Fast)
		accuracy,position = compare(sdata, tdata, tlen, slen, compare_config)
		if accuracy > 0.1:
			match_index = Fast
			max_accuracy = accuracy
			match_position = position
	else:
		for index in range(MaxID):
			sdata,slen = get_reference_data(index)
			accuracy,position = compare(sdata, tdata, tlen, slen, compare_config)
			#Filter: if accuracy more than 50%, that is to say the it is same with the reference
			if accuracy >= 0.5:
				match_index    = index
				max_accuracy   = accuracy
				match_position = position
				break
			#Filter: find the max accuracy, and return
			elif accuracy > max_accuracy:
				match_index    = index
				max_accuracy   = accuracy
				match_position = position

	#transfer to time scale
	match_position = match_position * (DEF_FFT_SIZE * DEF_OVERLAP) / framerate
	return match_index, max_accuracy, match_position





#######################################################
#    search function                                                                                                    
#######################################################
def compare(sdata,tdata,tlen,slen, compare_config):
	'''
	Find the similar audio with target data.

	Parameters
    ----------
	sdata: source data(reference data)          Type:[array]
	tdata: target data from target wav file.    Type:[array]
	tlen: the length of tdata                   Type:[int]
	slen: the length of sdata                   Type:[int]
	compare_config: configuration               Type:[COMPARE_PARAMETERS]

	Returns
    ----------
    r: compare result                           Type:[MATCH_INFO]
		r.accuracy: 0~100%                          Type:[float]
		r.position: index of sdata                  Type:[int]

	-----------------------------------------
	|-----win1------|-----win2-----|---------
	-----------------------------------------

	To improve efficiency, there are several method to be adopted:
		1) The section that have matched, we don't search it in next time.
		2) If accuracy is too low when we have finished the majority search, directly search next file.
		3) Use ".so".
	'''
	r = com.Compare(tdata, sdata, tlen, slen, compare_config)
	return r.accuracy, r.position
	






###########################################################
#   Get audio fingerprint
###########################################################
def get_fingerprint(wdata,framerate):
	'''
	Compute the fingerprint.
	'''
	#data length
	data_len = wdata.shape[-1]

	#hanning window
	hanning = _hann(DEF_FFT_SIZE, sym=0)

	#divide the frequency sub-band
	if (framerate==44100 and DEF_FFT_SIZE==4096) or(framerate==22050 and DEF_FFT_SIZE==2048):
		BandTable = BandTable_1
	elif (framerate==22050 and DEF_FFT_SIZE==4096):
		BandTable = BandTable_2
	else:
		#compute Band table
		BandTable = []
		#frequency scale
		scale = (framerate/2)/(DEF_FFT_SIZE/2+1.0)
		#temp variable
		TEM = MEL/2596.0
		#compute the sub-band
		for n in range(1,DEF_FIN_BIT+1):
			b0 = int(round(700*(10**((n-1)*TEM)-1)/scale,0))
			b1 = int(round(700*(10**((n+1)*TEM)-1)/scale,0))
			BandTable.append((b0,b1))

	Max_Band = BandTable[DEF_FIN_BIT-1][1]+1

	fin_array= []

	#init index of "wdata"
	s = 0
	e = DEF_FFT_SIZE

	while data_len > e:
		#1)generate a frame and get it`s fingerprint (s:e)
		#2)hanning window to smooth the edge
		xs = np.multiply(wdata[s:e], hanning)

		#fft transfer
		xfp = 20*np.log10(np.abs(np.fft.rfft(xs)[0:Max_Band]))

		#update index
		s = s + DEF_FFT_SIZE*DEF_OVERLAP
		e = s + DEF_FFT_SIZE

		subfin = 0

		for n in range(0, DEF_FIN_BIT):
			#BandTable look-up
			#use a BandTable to improve the speed of computation
			b0 = BandTable[n][0]
			b1 = BandTable[n][1]

			max_fp = 0
			max_b  = 0

			for b in range(b0,b1):

				#Compute the max frequency value
				if (xfp[b]  >  max_fp):
					max_fp = xfp[b]
					max_b  = b

			#generate the fingerprint
			if (max_b - (b0+b1)/2 > 0):
				subfin |= 1<<n

		fin_array.append(subfin)

	fin_array = np.array(fin_array,dtype = np.uint32)

	return fin_array
