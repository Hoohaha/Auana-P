import numpy as np


class DataManager:
	def __init__(self):

		
def fingerprint():
	#compute the fingerprint and save it
	temp = []
	temp.append(get_fingerprint(wdata=self.wdata0,framerate=self.framerate,db=False))
	temp.append(get_fingerprint(wdata=self.wdata1,framerate=self.framerate,db=False))
	return np.array(temp,dtype=np.uint32)