import numpy as np
from auana.common import hann
import math


DEF_FFT_SIZE = 4096

def compute_thd(wdata,framerate,f=1000):
	#data length
	data_len = wdata.shape[-1]

	#hanning window
	hanning = hann(DEF_FFT_SIZE, sym=0)

	num = data_len/DEF_FFT_SIZE

	scale = (framerate/2)/(DEF_FFT_SIZE/2+1.0)

	max_freq = int(20000/scale)

	thd = 0

	count = 0

	zcr_last = 0

	flag = False

	f_upper = int((f+50)/scale)
	f_lower = int((f-50)/scale)

	############################IIR#############################
	# b, a = signal.iirdesign([0.043, 0.048],[0.043, 0.048], 1, 100)

	# w, h = signal.freqz(b, a)

	for n in xrange(num):

		frame = wdata[n*DEF_FFT_SIZE: (n+1)*DEF_FFT_SIZE]

		zcr = compute_zcr(frame)

		if abs(zcr_last - zcr) <=3 and zcr > 60:
			flag = True

		zcr_last = zcr

		if flag is False:
			continue

		count += 1

		#2)hanning window to smooth the edge
		xs = np.multiply(frame, hanning)

		#fft transfer
		xfp = 20*np.log10(np.abs(np.fft.rfft(xs)[0:max_freq]))#

		fundamental_scope = xfp[f_lower:f_upper]

		fundamental_freq  = fundamental_scope.max()

		fundamental_freq  = 10**(fundamental_freq/20)

		xfp[f_lower:f_upper] = 0

		v = xfp.max()

		value = 10**(v/20)

		thd += value/fundamental_freq

		if count > 6:
			thd = thd/count
			return thd*100

	if thd == 0:
		return 100



def compute_volume(wdata,framerate):
	#data length
	data_len = wdata.shape[-1]

	#hanning window
	hanning = hann(DEF_FFT_SIZE, sym=0)

	fft_size = DEF_FFT_SIZE

	num = data_len/fft_size


	scale = (framerate/2.0)/(fft_size/2+1.0)

	max_fre = int(3000.0/scale)

	db_avg = 0

	for n in xrange(num):
		#2)hanning window to smooth the edge
		xs = np.multiply(wdata[n*fft_size: (n+1)*fft_size], hanning)

		#fft transfer
		xfp = 20*np.log10(np.abs(np.fft.rfft(xs)[0:max_fre]))

		db_one_frame = xfp.mean()

		db_avg += db_one_frame

	db_avg = round(db_avg/n,2)

	return db_avg




def compute_zcr(frame):
	z = 0
	if frame[0]>0:
		x_last=1
	else:
		x_last=-1

	for x in frame:
		if x>0:
			x_now = 1
		else:
			x_now = -1

		z += abs(x_now - x_last)
		x_last = x_now

	return z