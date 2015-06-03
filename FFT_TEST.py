import numpy as np
import wave, struct

DEF_FFT_SIZE = 4096
FIN_BIT = 32
DEF_OVERLAP = 2
MEL = (2596*np.log10(1+4000/700.0))/(FIN_BIT+1.0)
#The upper and lower bounds of sub-band. when framerate is 44100
BandTable_1 = [[0  ,   8], [4  ,  12], [8,    17], [12 ,  22], 
			   [17 ,  27], [22 ,  32], [27 ,  38], [32 ,  44], 
			   [38 ,  51], [44 ,  58], [51 ,  65], [58 ,  73], 
			   [65 ,  81], [73 ,  89], [81 ,  99], [89 , 108], 
			   [99 , 119], [108, 130], [119, 141], [130, 153], 
			   [141, 166], [153, 180], [166, 195], [180, 210], 
			   [195, 226], [210, 244], [226, 262], [244, 282], 
			   [262, 302], [282, 324], [302, 347], [324, 372]]

BandTable_2 = [[0  ,  16], [8  ,  25], [16 ,  34], [25 ,  44], 
			   [34 ,  54], [44 ,  65], [54 ,  76], [65 ,  89], 
			   [76 , 102], [89 , 115], [102, 130], [115, 145],
			   [130, 162], [145, 179], [162, 197], [179, 217], 
			   [197, 237], [217, 259], [237, 282], [259, 307], 
			   [282, 333], [307, 360], [333, 390], [360, 420], 
			   [390, 453], [420, 488], [453, 524], [488, 563], 
			   [524, 605], [563, 648], [605, 694], [648, 743]]

###########################################################
#   Get audio fingerprint
###########################################################
def get_fingerprint(wdata,framerate,db=True):
	'''
	Compute the fingerprint.
	'''
	#data length
	data_len = wdata.shape[-1]

	#hanning window
	hanning = _hann(DEF_FFT_SIZE, sym=0)

	#divide the frequency sub-band
	if framerate == 44100:
		BandTable = BandTable_1
	elif framerate == 22050:
		BandTable = BandTable_2
	else:
		BandTable = []
		#frequency scale
		scale = (framerate/2)/(DEF_FFT_SIZE/2+1.0)

		TEM = MEL/2596.0
		#compute the sub-band
		for n in xrange(1,FIN_BIT+1):
			b0 = int(round(700*(10**((n-1)*TEM)-1)/scale,0))
			b1 = int(round(700*(10**((n+1)*TEM)-1)/scale,0))
			BandTable.append((b0,b1))

	Max_Band = BandTable[FIN_BIT-1][1]+1

	#volume compute
	sumdb = 0
	num = 0

	fin= []
	#init index of "wdata"
	s = 0
	e = DEF_FFT_SIZE


	while e<data_len:
		#1)generate a frame and get it`s fingerprint (s:e)
		#2)hanning window to smooth the edge
		xs = np.multiply(wdata[s:e], hanning)

		#fft transfer
		xfp = 20*np.log10(np.abs(np.fft.rfft(xs)[0:Max_Band]))

		#update index
		s = s + DEF_FFT_SIZE/DEF_OVERLAP
		e = s + DEF_FFT_SIZE

		subfin = 0L

		max_n = 0
		max_max_f = 0

		for n in xrange(0,FIN_BIT):
			#BandTable look-up
			#use a BandTable to improve the speed of computation
			b0 = BandTable[n][0]
			b1 = BandTable[n][1]

			max_fp = 0
			max_b = 0

			for b in xrange(b0,b1+1):
				#Compute the max frequency value
				if (xfp[b] > max_fp): 
					max_fp = xfp[b]
					max_b = b



			#generate the fingerprint
			if max_b - (b0+b1)/2 >= 0:
				subfin |= 1<<n

			if max_fp >= max_max_f:
				max_max_f = max_fp
				max_n     = n+1

			

		# subfin = 0xffffffff>>(32-max_n)&subfin
		fin.append((subfin,max_n))

	# fin = np.array(fin,dtype = np.uint32)

	if db is True:
		return fin,0

 	return fin


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

def trail(path):
	wf = wave.open(path, 'rb')#"E:\\Auana-P\\1-broken.wav" "E:\\FFOutput\\b.wav"
	params = wf.getparams()
	nchannels, sampwidth, framerate, nframes = params[:4]
	str_data = wf.readframes(nframes)
	wf.close()

	wave_data = np.fromstring(str_data, dtype = np.short)
	wave_data.shape = -1,2
	wave_data = wave_data.T #transpose multiprocessing.Process

	return get_fingerprint(wave_data[0],44100,db=False)


ae = trail("E:/app_data\ksdk_demo\sai_demo/audio_lib\source1.wav")#)#
be = trail("E:/sample/twrk22f120m/iar/Debug/123.wav")


length = len(ae)
for n in xrange(100):
	vala = ae[n][0]
	maxa = ae[n][1]

	valb = be[n+3][0]
	maxb = be[n+3][1]


	print "-- %2d    |%32s  %2d    |%32s"%(maxa,bin(vala)[2:],maxb,bin(valb)[2:]),hamming_weight(vala^valb)
	# print "             %32s"%bin(valb)[2:]