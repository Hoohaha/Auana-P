import numpy as np
from common import hann
import math


DEF_FFT_SIZE = 4096

def compute_thd(wdata,framerate):
	#data length
	data_len = wdata.shape[-1]

	#hanning window
	hanning = hann(DEF_FFT_SIZE, sym=0)

	num = data_len/DEF_FFT_SIZE

	scale = (framerate/2)/(DEF_FFT_SIZE/2+1.0)

	max_freq = int(20000/scale)

	db_avg = 0

	max_har_num = 11

	th = 0

	for n in xrange(num-1,num):
		#2)hanning window to smooth the edge
		xs = np.multiply(wdata[n*DEF_FFT_SIZE: (n+1)*DEF_FFT_SIZE], hanning)

		#fft transfer
		xfp = 20*np.log10(np.abs(np.fft.rfft(xs)[0:max_freq]))

		base_freq = xfp[int(1000/scale)]

		if base_freq >= 120:
			base_freq = 0

		base_freq = 10**(base_freq/20)

		sum_har   = 0.0

		for har_n in xrange(2, max_har_num):

			index = int(1000*har_n / scale)
			value = int(xfp[index])

			if value >= 120:
				value = 120
			value = value - 120

			value = 10**(value/20)

			value = value**2
			sum_har += value

		sum_har = math.sqrt(sum_har)
		
		th = sum_har/base_freq

	return th*100



def compute_volume(wdata,framerate):
	#data length
	data_len = wdata.shape[-1]

	#hanning window
	hanning = hann(DEF_FFT_SIZE, sym=0)

	num = data_len/DEF_FFT_SIZE

	scale = (framerate/2)/(DEF_FFT_SIZE/2+1.0)

	max_fre = int(3000/scale)

	db_avg = 0

	for n in xrange(num):
		#2)hanning window to smooth the edge
		xs = np.multiply(wdata[n*DEF_FFT_SIZE: (n+1)*DEF_FFT_SIZE], hanning)

		#fft transfer
		xfp = 20*np.log10(np.abs(np.fft.rfft(xs)[0:max_fre]))

		db_one_frame = xfp.mean()

		db_avg += db_one_frame

	db_avg = round(db_avg/n,2)

	return db_avg