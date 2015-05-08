import numpy as np
import wave, struct

DEF_FFT_SIZE = 4096
FIN_BIT = 32
DEF_OVERLAP = 2
mel = (2596*np.log10(1+4000/700.0))/(FIN_BIT+1.0)
#The upper and lower bounds of sub-band. when framerate is 44100
BandTable = [[0  ,   8], [4  ,  12], [8,    17], [12 ,  22], 
			 [17 ,  27], [22 ,  32], [27 ,  38], [32 ,  44], 
			 [38 ,  51], [44 ,  58], [51 ,  65], [58 ,  73], 
			 [65 ,  81], [73 ,  89], [81 ,  99], [89 , 108], 
			 [99 , 119], [108, 130], [119, 141], [130, 153], 
			 [141, 166], [153, 180], [166, 195], [180, 210], 
			 [195, 226], [210, 244], [226, 262], [244, 282], 
			 [262, 302], [282, 324], [302, 347], [324, 372]]

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
	if framerate != 44100:
		#frequency scale
		scale = (framerate/2)/(DEF_FFT_SIZE/2+1.0)

		TEM = MEL/2596.0
		#compute the sub-band
		for n in xrange(1,FIN_BIT+1):
			b0 = int(round(700*(10**((n-1)*TEM)-1)/scale,0))
			b1 = int(round(700*(10**((n+1)*TEM)-1)/scale,0))
			BandTable[n-1]=[b0,b1]

	Max_Band = BandTable[FIN_BIT-1][1]

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

		for n in xrange(2,FIN_BIT):
			#BandTable look-up
			#use a BandTable to improve the speed of computation
			b0 = BandTable[n-1][0]
			b1 = BandTable[n-1][1]

			max_fp = 0
			max_b = 0

			for b in xrange(b0,b1):
				#Compute the max frequency value
				if (xfp[b] > max_fp): 
					max_fp = xfp[b]
					max_b = b
			#generate the fingerprint
			if max_b - (b0+b1)/2 >= 0:
				subfin |= 1<<(n-2)

		fin.append(subfin)

	fin = np.array(fin,dtype = np.uint32)
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


ae = trail("E:/sample/twrk21f120m/iar/Debug/112.wav")
be = trail("E:/sample/twrk21f120m/iar/Debug/113.wav")
sa = 0
sb = 0
for r in xrange(100):
	a = ae[r]
	b = be[r]
	ah = hamming_weight(a)
	bh = hamming_weight(b)
	sa += ah
	sb += bh
	c = hamming_weight(a^b)
	print "%8x %8x %d %d  %d"%(a,b,ah,bh,c)

print sa/100.0,sb/100.0