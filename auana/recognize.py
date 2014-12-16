import numpy as np
import scipy.signal as signal

#How many data in fft process 
DEFAULT_FFT_SIZE = 4096
#Sub-fingerprint bit depth
FIN_BIT = 32
#mel
mel = (2596*np.log10(1+4000/700.0))/(FIN_BIT+1.0)
#save the sub-band of upper and lower bounds 
BandTable = {}

def recognize(wdata,sdata,channels,framerate):
	'''
	open the reference file, and compare the tdata(target date) and the sdata(source data [reference])
	data format in AudioFingerData.yml:
	{"Audido1":{"channel0":data,"channel1":data},
	 "Audido2":{"channel0":data,"channel1":data},
	 "Audido3":{"channel0":data,"channel1":data},
		......			}
	'''
	match_audio = None
	max_confidence = 0
	

	tdata,avgdb=get_fingerprint(wdata,framerate)

	tlen=len(tdata)
	for key in sdata:
		confidence = find_match(np.array(sdata[key][str(channels)],dtype = np.uint32),tdata,tlen, framerate)
		#filter: if confidence more than 50%, that is to say the it is same with the reference
		if confidence >= 0.5:
			return key,confidence,avgdb
		#filter:find the max confidence, and return
		elif confidence > max_confidence:
			match_audio = key
			max_confidence = confidence
	source_data.close()
	return match_audio, max_confidence,avgdb

#######################################################
#    search function                                                                                                    
#######################################################
def find_match(sdata,tdata,tlen, framerate):
	'''
	minseq:  means the number of matched window in reference
	min_seq0:the last of minseq
	-----------------------------------------
	|-----win1------|-----win2-----|---------
	-----------------------------------------
	confidence:
	In oder to improve efficiency, there are several ways:
		1) the section that have matched, we not search it in next window,
			so we use the variable: next_begain 
		2) if confidence is too low when we have finished the majority, directly exit and search next file.
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
		dismin = 300
		tsta = a*window_size
		tend = (a+1)*window_size
		min_seq0=min_seq
		for index in  xrange(next_begain, max_index,2):#reference file
			#calculate the distant of each subfingerprint between two songs
			D = tdata[tsta : tend] ^ sdata[index : index+window_size]
			#get distant of two search-windows
			dis = np.sum([hamming_weight(long(d)) for d in D])
			if dis < dismin :
				dismin=dis
				min_seq=index
		#filter:block distance is very close, and they are Arithmetic sequence
		if dismin<threshold and dw_limit<=min_seq-min_seq0<=up_limit:
			confidence += 1
			next_begain=min_seq
		#filter:if search done,stop
		if next_begain >= max_index:break
		#filter:if confidence is too low,stop
		if a>10 and confidence<2:return 0

	return round(float(confidence)/(tlen/window_size-2), 3)


###########################################################
#   Get audio fingerprint
###########################################################
def get_fingerprint(data,framerate,db=True):
	'''
	This function generate a frame, and calculate it`s fingerprint.
	For 5sec files, the overlap is 3/4, others is 1/2.
	'''
	global DEFAULT_OVERLAP
	data_len = len(data)
	#Overlap frmate depth
	if data_len<300000:#(5s)
		DEFAULT_OVERLAP = 4
	else:
		DEFAULT_OVERLAP = 2

	scale = framerate/float(DEFAULT_FFT_SIZE)

	num = 0
	sumdb = 0
	fin= []

	sta = 0
	end = DEFAULT_FFT_SIZE
	
	while (data_len-end) > DEFAULT_FFT_SIZE:
		#generate a frame and get it`s fingerprint
		#hanning window to smooth the edge
		xs = np.multiply(data[sta:end], signal.hann(DEFAULT_FFT_SIZE, sym=0))
		#fft transfer
		xfp = 20*np.log10(np.abs(np.fft.rfft(xs)))

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
 		return fin,sumdb/num
 	else:
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