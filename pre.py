from auana import *

filepath = "E:/Auana-P/1-sample.wav"

#create a new storage, framerate=16000
try:
	Create(framerate=16000)
except ValueError:
	pass

au = Auana()


f  = au.get_framerate()
print "SAMPLERATE %d"%f

au.openf(filepath).hear()