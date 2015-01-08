import numpy as np
from scipy import signal 
def snr(wdata,framerate):

	global DEFAULT_OVERLAP
	data_len = wdata.shape[-1]
	#Overlap frmate depth
	DEFAULT_OVERLAP = 1

	scale = (framerate/2.0)/(DEFAULT_FFT_SIZE/2.0+1)

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
		xfp = 20*np.log10(np.abs(np.fft.rfft(xs)))
		
		sta=sta+DEFAULT_FFT_SIZE/DEFAULT_OVERLAP
		end=sta+DEFAULT_FFT_SIZE
		
		subfin = 0L