import wave, os
import cPickle as pickle
from auana.recognize import recognize,get_fingerprint
from auana.broframe import detect_broken_frame
try:
	import numpy as np
except ImportError:
	print("Please build and install the numpy Python ")

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


Preprocess(Pre work before Analyze)
=========
	hear            -- Hear a song and save the info.
	clean_up		-- Delete all data
	forgot          -- Delete a specify song's infomation
	itmes			-- Show the items which was saved in it's internal.
"""

class Auana(object):
	def __init__(self, DataPath=""):
		if DataPath == "":
			self.dpath = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')+"/data"
		else:
			self.dpath = DataPath

		self.pkl = self.dpath+'/AudioFingerCatalog.pkl'

		if not os.path.exists(self.dpath):
			print("Error: Invalid path: %s")%(self.dpath)
			os._exit(1)

		elif not os.path.exists(self.pkl):
			print("Error: \'AudioFingerCatalog.pkl\' is not exists,"
				"Please use Preprocess to save data firstly!")
			os._exit(1)
		
		try:
			cfile = open(self.pkl, 'rb')
			self.catalog = pickle.load(cfile)
			cfile.close()
		except EOFError:
			print("Error: There is no data was saved in \'AudioFingerCatalog.pkl\'.")
			cfile.close()
			os._exit(1)
			

	def broken_frame(self, wdata, framerate):
		return detect_broken_frame(wdata, framerate)

	def mono(self,wdata,channel,framerate):
		'''
		mono recognition

		'''
		#audio recognition
		match_index, accuracy, avgdb, location = recognize(self.catalog,wdata,framerate,channel)

		return self.catalog[match_index],accuracy,avgdb,location

	def stereo(self,wdata0,wdata1,framerate):
		'''
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

		#1> Analyze the chann0 first. 
		MatchID_L, accuracy_L, avgdb_L, location_L= recognize(self.catalog,wdata0,framerate,chann0,Fast=None)
		#if accuracy is high enough, directly return
		if accuracy_L>0.7:
			return self.catalog[MatchID_L], accuracy_L, avgdb_L, location_L
		#2> Analyze the chann1. 'Fast'means Fast recognition.
		MatchID_R, accuracy_R, avgdb_R, location_R = recognize(self.catalog,wdata1,framerate,chann1,Fast=index_L)

		#handle the result from chann0 and chann1.
		accuracy   = round((accuracy_L+accuracy_R)/2,3)
		average_db = round((avgdb_L+avgdb_R)/2,3)
		if accuracy_L > accuracy_R:
			location = location_L
		else:
			location = location_R

		if (MatchID_L != None) and (MatchID_L == MatchID_R):
			return self.catalog[MatchID_L], accuracy ,average_db, location
		else:
			return None,0, average_db, 0
	

class Fana:
	'''
	Fileana: File Analysis. Now only support wav format.
	'''
	def __init__(self,auana,f):
		self.auana = auana
		self.data = []
		self.framerate = 0

		if os.path.splitext(os.path.basename(f))[1] == '.wav':
			self.__wave_get_data(f)
		else:
			print ("Not support yet!")


	def __wave_get_data(self,f):
		#open wav file
		wf = wave.open(f, 'rb')
		nchannels, sampwidth, self.framerate, nframes = wf.getparams()[:4]

		if nchannels != 2:
			print ("Error: channels is not stereo!")
			wf.close()
			os._exit(1)

		str_data = wf.readframes(nframes)
		
		wf.close()
		self.data = np.fromstring(str_data, dtype = np.short)
		self.data.shape = -1,2
		self.data = self.data.T #Transpose

	def Recognize(self,STEREO=True,CH=0):
		if STEREO is True:
			return self.auana.stereo(self.data[0],self.data[1],self.framerate)
		else:
			return self.auana.mono(self.data[CH], CH, self.framerate)
			

	def Detect_Broken_Frame(self):
		chann0 = detect_broken_frame(self.data[0], self.framerate)
		chann1 = detect_broken_frame(self.data[1], self.framerate)
		if chann0 == 0 and chann1 == 0:
			return 0
		else:
			return {"left":chann0, "right": chann1}


##################################################################################################

class Preprocess:
	def __init__(self,DataPath=""):
		if DataPath == "":
			self.dpath = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')+"/data"
		else:
			self.dpath = DataPath
		
		self.pkl = self.dpath+'/AudioFingerCatalog.pkl'

		#Create a new pkl file
		if not os.path.exists(self.dpath):
			os.makedirs(self.dpath)

		try:
			cfile = open(self.pkl, 'rb')
			self.catalog = pickle.load(cfile)
		except EOFError:
			self.catalog = {}
		except IOError:
			cfile = open(self.pkl, 'w+')
			self.catalog = {}
		cfile.close()

	def hear(self,filepath):
		'''
		catalog = {index:"sample.wav"}
		'''
		filename = os.path.basename(filepath)
		index = len(self.catalog)

		print ("FILE: << %s >>\n        IS PROCESSING....")%(filename)

		for i in self.catalog:
			if self.catalog[i] == filename:
				print "  NOTICE: This File Has Been Saved Before!"
				return

		#Get data from wav file
		wf = wave.open(filepath, 'rb')
		nchannels, sampwidth, framerate, nframes = wf.getparams()[:4]
		wave_data = np.fromstring(wf.readframes(nframes), dtype = np.short)
		wf.close()
		#Prepare data
		wave_data.shape = -1,2
		wave_data = wave_data.T#transpose


		cache = []
		cache.append(get_fingerprint(wdata=wave_data[0],framerate=framerate,db=False))
		cache.append(get_fingerprint(wdata=wave_data[1],framerate=framerate,db=False))#Compute charatics

		#Creat .bin file
		bin_path = self.dpath + "/" + str(index) + ".bin"
		dfile = open(bin_path, 'w+')
		np.array(cache,dtype=np.uint32).tofile(bin_path)
		dfile.close()
		del cache[:]
		
		#Update catalog
		self.catalog.update({index:filename})
		cfile = open(self.pkl, 'w+')	
		pickle.dump(self.catalog, cfile)
		cfile.close()
		print "HEAR<SAVE> DONE!"

	def clean_up(self):
		cfile = open(self.pkl, 'w+')
		cfile.close()
		print "Already Clean Done!"

	def forget(self,filename):
		self.catalog.pop(filename)
		cfile = open(self.pkl, 'w+')	
		pickle.dump(self.catalog, cfile)
		cfile.close()
		print "Already forgot << %s >>!"%filename
	
	def items(self):
		#sort dict, te is a tuple 
		te = sorted(self.catalog.iteritems(),key=lambda d:d[0],reverse=False)
		print "******* File List *******"
		print "Total:%d"%len(self.catalog)
		print " No.","    ","File Name"
		for item in te:
			print "  %s       %s"%(item[0],item[1])
		print "***********************"