#Auther: Halye Guo  Date:2014/12
import numpy as np
# import scipy.signal as signal
import time,os,yaml
autohandle_directory = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
#How many data in fft process 
DEFAULT_FFT_SIZE = 4096
#Sub-fingerprint bit depth
FIN_BIT = 32
#mel frequency
mel = (2596*np.log10(1+4000/700.0))/(FIN_BIT+1.0)
#save the sub-band of upper and lower bounds 
BandTable = {1: [0  ,   8],  2: [4  ,  12],  3: [8  ,  17],  4: [12 ,  22], 
			 5: [17 ,  27],  6: [22 ,  32],  7: [27 ,  38],  8: [32 ,  44],
			 9: [38 ,  51], 10: [44 ,  58], 11: [51 ,  65], 12: [58 ,  73], 
			13: [65 ,  81], 14: [73 ,  89], 15: [81 ,  99], 16: [89 , 108], 
			17: [99 , 119], 18: [108, 130], 19: [119, 141], 20: [130, 153],
			21: [141, 166], 22: [153, 180], 23: [166, 195], 24: [180, 210], 
			25: [195, 226], 26: [210, 244], 27: [226, 262], 28: [244, 282], 
			29: [262, 302], 30: [282, 324], 31: [302, 347], 32: [324, 372]}

def recognize(catalog,wdata,framerate,channel,quick=None):
	'''
	This function is audio recognition.
	
	Compute the file is same with which reference-audio.
	And give the accuracy of recognition and average volume.
	The accuracy is measured by confidence value. The more similar, and the value is more
	close to "1".

	Volume is measured by db.

	Parameters
    ----------
	wdata: wave data
	sdata: source data(reference data)
	framerate: wave file sample rate

	Returns
    ----------
	match_audio: matched audio name which saved in reference file [AudioFingerData.yml].
	max_confidence: accuracy
	avgdb: average volume

	Process
	----------
	step1: get the fingerprint of wave data
	step2: compare the fingerprint with the sdata, 
		   and return the confidence(accuarce) and matched audio name.
		   confidence: 0~1, it means the how many fingerprint matched in reference file.
	'''

	tdata,avgdb    = get_fingerprint(wdata,framerate)
	max_confidence = 0
	match_audio    = None
	tlen           = tdata.shape[-1]
	
	def reference_data(index):
		dfile = open(autohandle_directory+"/data/"+index+".yml","r")
		sdata = np.array(yaml.load(dfile)[channel],dtype = np.uint32)
		dfile.close()
		return sdata
	
	if quick is not None:
		index=catalog[quick]
		sdata = reference_data(index)
		confidence = find_match(sdata,tdata,tlen)
		if confidence > 0.2:
			match_audio = quick
			max_confidence = confidence
	else:
		for audio in catalog:
			index=catalog[audio]
			sdata = reference_data(index)

			confidence = find_match(sdata,tdata,tlen)
			#filter: if confidence more than 50%, that is to say the it is same with the reference
			if confidence >= 0.5:
				return audio,confidence,avgdb
			#filter:find the max confidence, and return
			elif confidence > max_confidence:
				match_audio = audio
				max_confidence = confidence
	return match_audio, max_confidence,avgdb


#######################################################
#    search function                                                                                                    
#######################################################
def find_match(sdata,tdata,tlen):
	'''
	Compute which the audio is same with the target wave file.

	minseq:  means the number of matched window in reference
	min_seq0: the last of minseqss
	-----------------------------------------
	|-----win1------|-----win2-----|---------
	-----------------------------------------
	confidence:
	In oder to improve efficiency, there are several ways:
		1) the section that have matched, we not search it in next window,
			so we use the variable: next_begain 
		2) if confidence is too low when we have finished the majority search, directly 
		exit and search next file.
	'''
	min_seq=0
	min_seq0=0
	confidence=0
	
	if tlen < 200:
		window_size = 2
	else:
		window_size = 20

	next_begain = 0
	max_index = len(sdata)-window_size
	
	threshold = window_size*32*0.283
	
	#Arithmetic sequence tolerance uplimit and down limit
	up_limit = window_size+2
	dw_limit = window_size-2

	for a in  xrange(0,tlen/window_size):#tarhet file
		
		tsta     = a*window_size
		tend     = (a+1)*window_size
		dismin   = threshold
		min_seq0 = min_seq

		for index in  xrange(next_begain, max_index,2):#reference file
			#calculate the distant of each subfingerprint between two songs
			D = tdata[tsta : tend] ^ sdata[index : index+window_size]
			#get distant of two search-windows
			dis = np.sum([hamming_weight(long(d)) for d in D])
			if dis <= dismin :
				dismin  = dis
				min_seq = index
				if window_size>10 and dismin < 90:break

		#filter:block distance is very close, and they are Arithmetic sequence
		if dw_limit<=min_seq-min_seq0<=up_limit:
			confidence += 1
			next_begain = min_seq
		#filter:if search done,stop
		if next_begain >= max_index:break
		#filter:if confidence is too low,stop
		if a>18 and confidence<4:return 0

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
	data_len = len(wdata)
	#Overlap frmate depth
	if data_len<300000:#(5s)
		DEFAULT_OVERLAP = 4
	else:
		DEFAULT_OVERLAP = 2

	scale = framerate/float(DEFAULT_FFT_SIZE)

	fin= []
	sumdb = 0
	num = 0
	sta = 0
	end = DEFAULT_FFT_SIZE

	hanning = _hann(DEFAULT_FFT_SIZE, sym=0)

	while (data_len-end) > DEFAULT_FFT_SIZE:
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
				p1 += fp*(b**1.0001)
				p2 += fp
				num += 1
			#calculate the average volume of one fingerprint
			sumdb += p2
			
			#quantization
			if p1/p2-(b0+b1)/2 >= 0:
				subfin = subfin | (1<<(n-1))
		fin.append(subfin)

	#fin:the file`s fingerprint
	#sumdb/num:the average volume of the file`s
	if db is True:
 		return np.array(fin,dtype = np.uint32),sumdb/num
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
	In order to simplify the application, this function is come from scipy.signal
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