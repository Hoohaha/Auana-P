from auana import WaveForm, Create, Open
import numpy as np
try:
	Create()
except ValueError:
	pass

# s = Storage()
# # s.items()
# framerate = s.get_framerate()

# print framerate
# fs = 44100
# t = np.arange(0, 1, 1.0/fs)
# x = 32767*np.sin(2*np.pi*1000*t)+50*np.sin(2*np.pi*10*t)
# wf=WaveForm(44100,x,channels=1)

wf = Open("C:\Users\solof\Desktop\Auana-P\sine/normal.wav")


# wf.hear()

# print wf.recognize()
# print wf.recognize(Fast=False)
# print wf.recognize(Mono=True,Ch=0)
# print wf.detect_broken_frame()
# print wf.get_volume()
print wf.get_thdn(ch=0)