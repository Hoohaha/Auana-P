from auana import Storage, Create

try:
	Create()
except ValueError:
	pass

s = Storage()
# s.items()
framerate = s.get_framerate()

print framerate

wf = s.Open("E:/Auana-P/2-sample.wav")

# wf.hear()

# print wf.recognize()
# print wf.recognize(Fast=False)
# print wf.recognize(Mono=True,Ch=0)
# print wf.detect_broken_frame()
print wf.get_volume()
print wf.get_THD()