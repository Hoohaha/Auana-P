import numpy as np

def detect_broken_frame(data, channel,framerate):
	FLAG = 0
	DETECT_WIN = 256
	VAR_THRESHOLD = 2000
	bf = []
	var0 = var1 = 0
	for i in  xrange(len(data)/DETECT_WIN):
		var = int(np.var(data[i*DETECT_WIN:(i+1)*DETECT_WIN]))
		if i>1:
			distance0 = abs(var-var0)
			distance1 = abs(var-var1)
			if FLAG == 0:
				if (distance0 >VAR_THRESHOLD) and (distance1 > VAR_THRESHOLD) and (var < 90) :
					FLAG = 1
			elif FLAG == 1:
				if (distance0 >VAR_THRESHOLD) and (distance1 > VAR_THRESHOLD) and (var0 < 90):
					FLAG = 0
					bf.append(round(((i+1) * DETECT_WIN)/float(framerate),3))
				elif i%86 == 0:
					FLAG = 0
		var0,var1=var1,var

	if len(bf) == 0:
		return 0
	else:
		return bf