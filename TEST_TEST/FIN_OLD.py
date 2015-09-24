import numpy as np
import wave, struct, os
import time
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
# print (2596*np.log10(1+DEF_MAX_FRQ/700.0)),MEL

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

 		for n in xrange(1,DEF_FIN_BIT): 
 			p1 = 0 
			p2 = 0 

			#BandTable look-up 
 			#use a BandTable to improve the speed of calculate 
			b0 = BandTable[n][0]
 			b1 = BandTable[n][1]
 
 
 			for b in xrange(b0,b1+1): 
 				#calculate the Audio center of mass  
 				fp = xfp[b] 
 				p1 += fp*b 
 				p2 += fp 
 
 
	 		#Quantization 
			if p1/p2-(b0+b1)/2 >= 0: 
				subfin = subfin | (1<<n) 


		fin_array.append(subfin)

	fin_array = np.array(fin_array,dtype = np.uint32)

	return fin_array





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

def GET(path):
	start = time.time()
	wf = wave.open(path, 'rb')#"E:\\Auana-P\\1-broken.wav" "E:\\FFOutput\\b.wav"
	params = wf.getparams()
	nchannels, sampwidth, framerate, nframes = params[:4]
	str_data = wf.readframes(nframes)
	wf.close()

	wave_data = np.fromstring(str_data, dtype = np.short)
	wave_data.shape = -1,2
	wave_data = wave_data.T #transpose multiprocessing.Process

	return get_fingerprint(wave_data[0],framerate)




def lbrate(a, b, dp):
	WW = 0.0
	length = len(a)
	for l in xrange(length):
		wc = hamming_weight(a[l]^b[l])
		if dp is True:
			print "%s %s %d"%(hex(a[l]),hex(b[l]),wc)
		WW += wc

	return WW/length


def compare_x(f1, f2, dp=False):
	a = GET(f1)
	s = time.time()
	b = GET(f2)
	e = time.time()
	# print "time:",e-s
	rate = lbrate(a,b,dp)

	return rate



def noise_test():

	print compare_x("1-sample.wav","5.wav")
	print compare_x("1-sample.wav","10.wav")
	print compare_x("1-sample.wav","15.wav")
	print compare_x("1-sample.wav","20.wav")
	print compare_x("1-sample.wav","25.wav")
	print compare_x("1-sample.wav","30.wav")
	print compare_x("1-sample.wav","35.wav")
	print compare_x("1-sample.wav","40.wav")




def fft_size_test():
	print compare_x("1-sample.wav","f_noise_25.wav")

def time_test():
	t = []
	t.append(GET("1.wav"))
	t.append(GET("2.wav"))
	t.append(GET("3.wav"))
	t.append(GET("4.wav"))
	t.append(GET("5.wav"))
	t.append(GET("6.wav"))
	print t



print ("OLD --- OLD")
noise_test()
os.system("pause")