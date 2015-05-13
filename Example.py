from auana import Auana, Create

try:
	Create()
except ValueError:
	pass

au = Auana()
au.items()
print au.get_framerate()

stream = au.openf("E:/FFOutput/Jason Wade-Shrek-You Belong To Me-128.wav")

stream.hear()

print stream.recognize()
print stream.recognize(Fast=False)
print stream.recognize(Mono=True,Ch=0)
print stream.detect_broken_frame()