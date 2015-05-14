from auana import Auana, Create

try:
	Create()
except ValueError:
	pass

au = Auana()
au.items()
framerate = au.get_framerate()

print framerate

wf = au.openf("E:/FFOutput/Jason Wade-Shrek-You Belong To Me-128.wav")

wf.hear()

print wf.recognize()
print wf.recognize(Fast=False)
print wf.recognize(Mono=True,Ch=0)
print wf.detect_broken_frame()