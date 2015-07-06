import wave, os
import cPickle as pickle
from auana.recognize import recognize,get_fingerprint
from auana.broframe import detect_broken_frame
from auana.frequency import compute_volume, compute_thd
try:
	import numpy as np
except ImportError:
	print("Please build and install the numpy Python ")

__PATH__ = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')


"""
=======================================
Auana: An Audio Data Analyze Algorithm
=======================================

Create
===========

	Create a new Storage to store the data.

Detect_broken_frame
===========


Load_file
===========



Storage (Data storage and Data Management)
===========
	open            -- open and init a WaveForm by data
	openf           -- open and init a WaveForm by file
	query           -- query a file if saved in specify storage
	get_framerate   -- get the framerate for this storage
	clean_up        -- delete all data
	forget          -- delete a specify file
	items           -- return all itmes which saved in storage
	commit          -- commit all changes into storage
	


WaveForm
=========
	
	wirte           -- rewrite the data
	broken_frame   	-- broken frame detection.
	recognize       -- audio recognize
	hear            -- Hear a song and save the info.
	get_volume      -- return the volume of this waveform

"""


#catalog file name
CATALOG_FILE          = '/AudioFingerCatalog.pkl'

#default catalog path: ../data/AudioFingerCatalog.pkl
DEFAULT_DATA_PATH     = os.path.dirname(__PATH__) + '/data'

#default framerate
DEFAULT_FRAMERATE     = 22050


#create a new place to store data
def Create(framerate = DEFAULT_FRAMERATE, path = DEFAULT_DATA_PATH):
	catalog = {}

	if not os.path.exists(path):
	 	os.makedirs(path)


	def _create_pkl():
		catalog["FRAMERATE"] = framerate
		pklf = open(catalog_path, 'w+')
		pickle.dump(catalog, pklf)
		pklf.close()

	catalog_path = path + CATALOG_FILE


	try:
		catalog = _load__catalog(catalog_path)
		if framerate == catalog["FRAMERATE"]:
			raise ValueError("\'%s\' already exists!"%catalog_path)
	except EOFError:
		_create_pkl()
	except KeyError:
		_create_pkl()
	except IOError:
		_create_pkl()

	print "Create Seccussfully!"




def Detect_broken_frame(dl,dr,framerate):
	if dl is not None:
		chann0 = detect_broken_frame(dl, framerate)
	if dr is not None:
		chann1 = detect_broken_frame(dr, framerate)
	
	return {"left":chann0, "right": chann1}



def Load_file(f):
	if os.path.splitext(os.path.basename(f))[1] == '.wav':
		return _wave_get_data(f)
	else:
		raise IOError("Not support yet!")




class Storage:
	'''
	Storage is class to manage data storage.
		- init specified data storage
		- open 'AudioFingerCatalog.pkl' and get catalog
		- qurey a file if it was saved in 'path'.

	Storage Operations:
		-- get_framerate: get the configuration of framerate in storage.
		-- clean_up: clean all items in storage.
		-- forget: delete specify item.
		-- items: show all items.

	Use this class to open a data stream.
		-- open:  open a data list and create a obejct Stream.
		-- openf: open a file and create a obejct Stream

	'''
	def __init__(self, path = DEFAULT_DATA_PATH):
		self.dpath        = path
		self.pkl = path + CATALOG_FILE

		if not os.path.exists(self.pkl):
			raise Warning("There is no any \'stroage\' in \'%s\', please crate a new!"%path)

		try:
			self._catalog = _load__catalog(self.pkl)
			self.framerate = self._catalog["FRAMERATE"]
		except EOFError or KeyError:
			cfile.close()
			raise Warning("The \'AudioFingerCatalog.pkl\' is empty, please crate a new.")


	def openf(self, file):
		self.filename = os.path.basename(file)
		data, framerate, nchannels = Load_file(file)

		if framerate != self.framerate:
			raise ValueError("%d is required, but the framerate is %d for this file."%(self.framerate,framerate))
		
		w = WaveForm(self)
		w.data = data

		return w

	
	def query(self,filename):
		for i in self._catalog:
			if self._catalog[i] == filename:
				return True
		return False

	def get_framerate(self):
		return self.framerate

	def clean_up(self):
		cfile = open(self.pkl, 'w+')
		cfile.close()
		print "Already Clean Done!"

	def forget(self,filename):
		self._catalog.pop(filename)

	def items(self):
		#sort dict, te is a tuple 
		te = sorted(self._catalog.iteritems(),key=lambda d:d[0],reverse=False)
		print "******* File List *******"
		print "Total:%d\n"%len(self._catalog)
		print " No.","    ","File Name"
		for item in te:
			print "  %3s       %s"%(item[0],item[1])
		print "***********************"

	def commit(self):
		cfile = open(self.pkl, 'w+')	
		pickle.dump(self._catalog, cfile)
		cfile.close()








class WaveForm:
	'''
	An audio data stream.

	Operations for data stream:
	- hear: extract fingerprints and save in Auana.
	- recognize: extract fingerprints and compare with Auana.
	- detect_broken_frame: detect broken frame

	'''
	def __init__(self, STO):
		self._parent   = STO 
		self.data      = 0
		self.framerate = STO.framerate
		self.dpath     = STO.dpath


	###################################################
	###################################################
	
	def write(self,data):
		self.data = data


	def hear(self):
		filename = self._parent.filename
		cache = []
		cache.append(get_fingerprint(wdata=self.data[0],framerate=self.framerate))
		cache.append(get_fingerprint(wdata=self.data[1],framerate=self.framerate))#Compute charatics

		index = len(self._parent._catalog)-1

		#Creat .bin file
		bin_path = self.dpath + "/" + str(index) + ".bin"
		dfile = open(bin_path, 'w+')
		np.array(cache,dtype=np.uint32).tofile(bin_path)
		dfile.close()
		del cache[:]
		
		#Update catalog
		self._parent._catalog.update({index:filename})

		return 1


	def _mono(self,channel):
		'''
		Private method.
		mono recognition

		'''
		MaxID = len(self._parent._catalog)-1
		#audio recognition
		match_index, accuracy, location = recognize(MaxID,self.data[channel],self.framerate,channel,self.dpath)
		if match_index is None:
			return None
		return self._parent._catalog[match_index],accuracy, location

	def _stereo(self,FastSearch):
		'''
		Private method.

		stereo recognition

		We used the variable "Fast" to improve the speed of recognition.
		If left channel it matched an audio(example "source1.wav") in 
		firstly, then search in next channel it will compare the matched 
		audio("source1.wav"), rather than search all reference file again.

		Especially, if the accuracy is high enough, we will does't need to
		search in another channel. 
		'''
		chann0 = 0
		chann1 = 1
		if self.data.shape[0] != 2:
			raise ValueError("This is a mono stream. it can't stereo.")

		MaxID = len(self._parent._catalog)-1
		#1> Analyze the chann0 first. 
		MatchID_L, accuracy_L, location_L= recognize(MaxID,self.data[chann0],self.framerate,chann0,self.dpath,Fast=None)
		
		#Fast search switch
		if FastSearch is True:
			FastSwitch = MatchID_L
			#if accuracy is high enough, directly return
			if accuracy_L >= 0.7:
				return self._parent._catalog[MatchID_L], accuracy_L, location_L
		else:
			FastSwitch = None

		#2> Analyze the chann1. 'Fast'means Fast recognition.
		MatchID_R, accuracy_R, location_R = recognize(MaxID,self.data[chann1],self.framerate,chann1,self.dpath,Fast=FastSwitch)

		# print accuracy_L,accuracy_R
		#handle the result from chann0 and chann1.
		accuracy   = round((accuracy_L+accuracy_R)/2,3)

		if accuracy_L > accuracy_R:
			location = location_L
		else:
			location = location_R

		if (MatchID_L != None) and (MatchID_L == MatchID_R):
			return self._parent._catalog[MatchID_L], accuracy , location
		else:
			return None, 0, 0



	def recognize(self,Mono=False,Fast=True,Ch=0):
		if Mono is True:
			return self._mono(Ch)
		else:
			return self._stereo(Fast)


	def detect_broken_frame(self):
		return Detect_broken_frame(self.data[0],self.data[1],self.framerate)

	def get_volume(self, Ch=0):
		return compute_volume(self.data[Ch], self.framerate)

	def get_THD(self, Ch=0):
		return compute_thd(self.data[Ch],self.framerate)




##################################################################################################
def _load__catalog(path):
	"""Private method."""
	cfile   = open(path, 'rb')
	catalog = pickle.load(cfile)
	cfile.close()
	return catalog

def _wave_get_data(f):
	"""Private method."""
	#open wav file
	wf = wave.open(f, 'rb')

	nchannels, sampwidth, framerate, nframes = wf.getparams()[:4]

	str_data = wf.readframes(nframes)
	
	wf.close()
	data = np.fromstring(str_data, dtype = np.short)
	data.shape = -1,2
	data = data.T #Transpose

	return data, framerate, nchannels




# def fill_index(data,index):

# 	table_path = __PATH__+"/data" + "/IndexTable.pkl"

# 	itable = load_data(table_path)

# 	for d in data[0]:
# 		d = (d & 0xFFFF0000) >> 16
# 		if index not in itable[d] and d!= 0:
# 			itable[d].append(index)

# 	f = open(table_path,"w")
# 	pickle.dump(itable,f)
# 	f.close()



# def load_data(p):
# 	try:
# 		cfile = open(p, 'rb')
# 		c = pickle.load(cfile)
# 	except EOFError:
# 		c = {}
# 	except IOError:
# 		c = {}
# 	if len(c) == 0:
# 		cfile = open(p, 'w+')
# 		for n in xrange(65537):
# 			c[n] = []
# 	cfile.close()
# 	return c