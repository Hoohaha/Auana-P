import wave, os
import cPickle as pickle
import yaml
from auana.recognize import recognize,get_fingerprint
from auana.broframe import detect_broken_frame
try:
	import numpy as np
except ImportError:
	print("Please build and install the numpy Python ")

__PATH__ = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
"""
=======================================
Auana: An Audio Data Analyze Algorithm
=======================================

auana(base)
===========

   broken_frame    	-- broken frame detection.
   mono   			-- mono recognize.
   stereo 			-- stereo recognize.

Fana(Auana From File)               
=========

	broken_frame   	-- broken frame detection.
   	mono_start   	-- mono recognize.
   	stereo_start 	-- stereo recognize.


Preprocess(Prework before Analyze)
=========
	hear            -- Hear a song and save the info.
	clean_up		-- Delete all data
	forgot          -- Delete a specify song's infomation
	itmes			-- Show the items which was saved in it's internal.
"""


#catalog file name
CATALOG_FILE          = '/AudioFingerCatalog.pkl'

#default catalog path: auana/data/AudioFingerCatalog.pkl
DEFAULT_DATA_PATH  = __PATH__ + '/data'

#default framerate
DEFAULT_FRAMERATE     = 22050


#create a new place to store data
def Create(framerate=22050,path = DEFAULT_DATA_PATH):

	catalog_path = path + CATALOG_FILE

	if not os.path.exists(path):
		os.makedirs(path)
		print ("Warnning: Specify path\n\'%s\'\n is not exists, it is created."%path)
	try:
		catalog = _load__catalog(catalog_path)

		if framerate == catalog["FRAMERATE"]:
			raise ValueError("\'%s\' already exists!"%catalog_path)

	except KeyError or EOFError or IOError:
		catalog = {}
		catalog["FRAMERATE"] = framerate
		pklf = open(catalog_path, 'w+')
		pickle.dump(catalog, pklf)
		pklf.close()

	print "Create Seccussfully!"



class Auana:
	'''
	Auana is class to manage data storage.
		- init specified data storage
		- open 'AudioFingerCatalog.pkl' and get catalog
		- qurey a file if it was saved in 'path'.

	Auana Storage Operations:
		-- get_framerate: get the configuration of framerate in Auana storage.
		-- clean_up: clean all items in Auana storage.
		-- forget: delete specify item.
		-- items: show all items.

	Use this class to open a data stream.
		-- open:  open a data list and create a obejct Stream.
		-- openf: open a file and create a obejct Stream

	'''
	def __init__(self, path = DEFAULT_DATA_PATH, framerate = DEFAULT_FRAMERATE):
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
		data,framerate, nchannels = _load_file(file)

		if framerate != self.framerate:
			raise ValueError("%d is required, but the framerate is %d for this file."%(self.framerate,framerate))

		return self.open(data=data,stereo_or_mono=True)

	def open(self, data, stereo_or_mono=True):
		return Stream(self, data, self.framerate)

	def get_framerate(self):
		return self.framerate

	def clean_up(self):
		cfile = open(self.catalog_path, 'w+')
		cfile.close()
		print "Already Clean Done!"

	def forget(self,filename):
		self._catalog.pop(filename)
		cfile = open(self.catalog_path, 'w+')	
		pickle.dump(self._catalog, cfile)
		cfile.close()
		print "Already forgot << %s >>!"%filename

	def items(self):
		#sort dict, te is a tuple 
		te = sorted(self._catalog.iteritems(),key=lambda d:d[0],reverse=False)
		print "******* File List *******"
		print "Total:%d"%len(self._catalog)
		print " No.","    ","File Name"
		for item in te:
			print "  %s       %s"%(item[0],item[1])
		print "***********************"


# filename = os.path.basename(filepath)

# print ("-----------------")
# print ("FILE: << %s >>\n  IN PROCESSING....")%(filename)


class Stream:
	'''
	An audio data stream.

	Operations for data stream:
	- hear: extract fingerprints and save in Auana.
	- recognize: extract fingerprints and compare with Auana.
	- detect_broken_frame: detect broken frame

	'''
	def __init__(self, Au, wdata, framerate):
		self._parent   = Au 
		self.data      = wdata
		self.framerate = framerate
		self._catalog  = Au._catalog
		self.dpath     = self._parent.dpath

	###################################################
	###################################################
	def hear(self):
		for i in self._catalog:
			if self._catalog[i] == self._parent.filename:
				print "Notice: This File Has Been Saved Before!"
				return

		cache = []
		cache.append(get_fingerprint(wdata=self.data[0],framerate=self.framerate,db=False))
		cache.append(get_fingerprint(wdata=self.data[1],framerate=self.framerate,db=False))#Compute charatics

		index = len(self._catalog)-1

		#Creat .bin file
		bin_path = self.dpath + "/" + str(index) + ".bin"
		dfile = open(bin_path, 'w+')
		np.array(cache,dtype=np.uint32).tofile(bin_path)
		dfile.close()
		del cache[:]
		
		#Update catalog
		self._catalog.update({index:self._parent.filename})
		cfile = open(self._parent.pkl, 'w+')	
		pickle.dump(self._catalog, cfile)
		cfile.close()
		print "Hear Done!"

	def _mono(self,channel):
		'''
		Private method.
		mono recognition

		'''
		MaxID = len(self._catalog)
		#audio recognition
		match_index, accuracy, avgdb, location = recognize(MaxID,self.data[channel],self.framerate,channel,self.dpath)

		return self._catalog[match_index],accuracy,avgdb,location

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
		MaxID = len(self._catalog)
		#1> Analyze the chann0 first. 
		MatchID_L, accuracy_L, avgdb_L, location_L= recognize(MaxID,self.data[chann0],self.framerate,chann0,self.dpath,Fast=None)
		
		#Fast search switch
		if FastSearch is True:
			FastSwitch = MatchID_L
			#if accuracy is high enough, directly return
			if accuracy_L>0.7:
				return self._catalog[MatchID_L], accuracy_L, avgdb_L, location_L
		else:
			FastSwitch = None

		#2> Analyze the chann1. 'Fast'means Fast recognition.
		MatchID_R, accuracy_R, avgdb_R, location_R = recognize(MaxID,self.data[chann1],self.framerate,chann1,self.dpath,Fast=FastSwitch)

		#handle the result from chann0 and chann1.
		accuracy   = round((accuracy_L+accuracy_R)/2,3)
		average_db = round((avgdb_L+avgdb_R)/2,3)
		if accuracy_L > accuracy_R:
			location = location_L
		else:
			location = location_R

		if (MatchID_L != None) and (MatchID_L == MatchID_R):
			return self._catalog[MatchID_L], accuracy ,average_db, location
		else:
			return None,0, average_db, 0

	def detect_broken_frame(self):
		chann0 = detect_broken_frame(self.data[0], self.framerate)
		chann1 = detect_broken_frame(self.data[1], self.framerate)
		if chann0 == 0 and chann1 == 0:
			return 0
		else:
			return {"left":chann0, "right": chann1}

	def recognize(self,Mono=True,Fast=True,Ch=0):

		if Mono is True:
			return self._stereo(Fast)
		else:
			return self._mono(Ch)




##################################################################################################
def _load__catalog(path):
	"""Private method."""
	cfile   = open(path, 'rb')
	catalog = pickle.load(cfile)
	cfile.close()
	return catalog


def _load_file(f):
	"""Private method."""
	if os.path.splitext(os.path.basename(f))[1] == '.wav':
		return _wave_get_data(f)
	else:
		raise IOError("Not support yet!")


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

def fill_index(data,index):

	table_path = __PATH__+"/data" + "/IndexTable.pkl"

	itable = load_data(table_path)

	for d in data[0]:
		d = (d & 0xFFFF0000) >> 16
		if index not in itable[d] and d!= 0:
			itable[d].append(index)

	f = open(table_path,"w")
	pickle.dump(itable,f)
	f.close()

def load_data(p):
	try:
		cfile = open(p, 'rb')
		c = pickle.load(cfile)
	except EOFError:
		c = {}
	except IOError:
		c = {}
	if len(c) == 0:
		cfile = open(p, 'w+')
		for n in xrange(65537):
			c[n] = []
	cfile.close()
	return c