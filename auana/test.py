# from Queue import Queue
# from pyaudio import PyAudio, paInt16
# import threading
# import numpy as np
# import scipy.signal as signal
# from broframe import detect_broken_frame
# import matplotlib.pyplot as plt
# queue=Queue()
# FFT=4096
# def volume(queue):

# 	sdb=0
# 	i=0
# 	hanning = signal.hann(FFT, sym=0)
# 	plt.figure(1)
# 	while True:

# 		wdata = queue.get()
# 		wdata.shape = -1,2
# 		wdata = wdata.T
# 		res = detect_broken_frame(wdata[0],44100)
# 		if res != 0:
# 			print res
# 		xfp = 20*np.log10(np.abs(np.fft.rfft(np.multiply(wdata[0], hanning))))
# 		sdb += np.sum(xfp[20:400])/380
# 		freqs = np.linspace(0, 44100/2, FFT/2+1)[0:100]
# 		plt.plot(freqs,xfp[0:100])
# 		plt.show()
# 		if i>=3:
# 			print int(sdb/4)
# 			i=0
# 			sdb=0
# 		else:
# 			i += 1

# def record(queue):
# 		CHUNK         = FFT
# 		FORMAT        = paInt16
# 		CHANNELS      = 2
# 		SAMPLING_RATE = 44100

# 		#open audio stream
# 		pa = PyAudio()
# 		stream = pa.open(
# 						format   = FORMAT, 
# 						channels = CHANNELS, 
# 						rate     = SAMPLING_RATE, 
# 						input    = True,
# 						frames_per_buffer  = CHUNK
# 						)
# 		while True:
# 			queue.put(np.fromstring(stream.read(CHUNK), dtype=np.short))

# if __name__ == '__main__':
# 	# plt.bar(left = 0,height = 1)
# 	# plt.show()
# 	task1=threading.Thread(target=record,args=(queue,))
# 	task2=threading.Thread(target=volume,args=(queue,))
# 	task1.setDaemon(True)
# 	task2.setDaemon(True)
# 	task1.start()
# 	task2.start()
# 	task1.join()
