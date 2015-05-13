import os, sys
# __PATH__ = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
# sys.path.append(__PATH__)
from auana import *

try:
	Create()
except ValueError:
	pass

au = Auana()


stream = au.openf("E:/FFOutput/Jason Wade-Shrek-You Belong To Me-128.wav")

stream.hear()
print stream.recognize()
print stream.recognize(Fast=False)
print stream.recognize(Mono=True,Ch=0)
print stream.detect_broken_frame()

au.items()
print au.get_framerate()