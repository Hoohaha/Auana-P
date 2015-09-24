import math
import numpy as np
from auana.common import hann


DEF_FFT_SIZE = 4096.0

def compute_thdn(wdata,framerate,f=1000):

	STANDARD_ZCR = int(DEF_FFT_SIZE/framerate*f*2)

	#data length
	data_len = len(wdata)

	#hanning window
	hanning = hann(DEF_FFT_SIZE, sym=0)

	num = int(data_len/DEF_FFT_SIZE)

	scale = (framerate/2.0)/(DEF_FFT_SIZE/2.0+1.0)

	max_freq = int(20000/scale)

	thd = 0

	count = 0

	zcr_last = 0

	flag  = False
	start = False

	f_upper = int((f+400)/scale)
	f_lower = int((f-400)/scale)


	for n in xrange(num):#num

		frame = wdata[n*DEF_FFT_SIZE: (n+1)*DEF_FFT_SIZE]

		zcr = compute_zcr(frame)

		if (STANDARD_ZCR-2) <= zcr <= (STANDARD_ZCR+2):
			flag  = True
			start = True
		else:
			continue

		if start is True and flag is False:
			return 100


		count += 1

		#hanning window to smooth the edge
		xs = np.multiply(frame, hanning)
		xfp = np.absolute(np.fft.rfft(xs))

		#fft transfer
		# xfp = 20*np.log10(xc)#

		#Note: xun zhao jian feng suan fa
		fund_scope = xfp[f_lower:f_upper]
		fun  = fund_scope.max()
		xfp[f_lower:f_upper] = -200


		d = xfp[int(40/scale):int(1500/scale)].max()
		d = d**2

		for i in xrange(10):
			temp = xfp[(1500+i*2000)/scale:(1500+(i+1)*2000)/scale].max()
			d += temp**2

		thd += np.sqrt(d)/fun

	if count == 0:
		return 100

	thd = thd/count
	return thd*100


def vvv_transfer(db):
	return 10**(db/20)


def compute_mm(data):
	w = 4096
	length = len(data)
	s = 0
	e = w

	max_m = []

	for i in xrange(length/w):
		d = data[s:e]
		s = e
		e += w

		a = d.max()
		b = d.min()

		f = (a-b)*0.707

		max_m.append(f)
	return np.mean(max_m)



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

	return z/2