from recognize import recognize,get_fingerprint
from broframe import detect_broken_frame
import wave, time, os
import cPickle as pickle
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

_work_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')

class Auana(object):

	def __init__(self):
		try:
			cfile = open(_work_dir+'/data/AudioFingerCatalog.pkl', 'rb')
			self.catalog = pickle.load(cfile)
			cfile.close()
		except EOFError:
			print("Error: No data saved in pkl file." 
			"Please fisrtly save the fingerprint of the reference audio.")
			cfile.close()
			self.__del__()
			os._exit(1)
			

	def __del__(self):
		pass

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

		It used the variable "Fast" to improve the speed of recognition. If left channel we matched 
		an audio(example "source1.wav") in firstly, then search in next channel it will compare the 
		matched audio("source1.wav"),rather than search all reference file again.

		Especially, if the accuracy is high enough, we will don't need to search in another channel. 
		'''
		chann0 = 0
		chann1 = 1

		#1> Analyze the chann0 first. 
		index_L, accuracy_L, avgdb_L, location_L= recognize(self.catalog,wdata0,framerate,chann0,Fast=None)
		#if accuracy is high enough, directly return
		if accuracy_L>0.7:
			return self.catalog[index_L], accuracy_L, avgdb_L, location_L
		#2> Analyze the chann1. 'Fast'means Fast recognition.
		index_R, accuracy_R, avgdb_R, location_R = recognize(self.catalog,wdata1,framerate,chann1,Fast=index_L)

		#handle the result from chann0 and chann1.
		accuracy   = round((accuracy_L+accuracy_R)/2,3)
		average_db = round((avgdb_L+avgdb_R)/2,3)
		if accuracy_L > accuracy_R:
			location = location_L
		else:
			location = location_R

		if (index_L != None) and (index_L == index_R):
			return self.catalog[index_L], accuracy ,average_db, location
		else:
			return None,0, average_db, 0


class Fana(Auana):
	'''
	Fana: File Analysis
	Now only support wav format.
	'''
	def __init__(self,filepath):	
		Auana.__init__(self)
		#open wav file
		wf = wave.open(filepath, 'rb')
		params = wf.getparams()
		nchannels, sampwidth, framerate, nframes = params[:4]
		str_data = wf.readframes(nframes)
		wf.close()

		wave_data = np.fromstring(str_data, dtype = np.short)
		wave_data.shape = -1,2
		wave_data = wave_data.T #transpose multiprocessing.Process

		self.name = os.path.basename(filepath)
		self.framerate =framerate
		self.wdata0=wave_data[0]
		self.wdata1=wave_data[1]

	def stereo_start(self):
		return self.stereo(self.wdata0,self.wdata1,self.framerate)

	def mono_start(self,channel):
		data = {0:self.wdata0,1:self.wdata1}
		return self.mono(data[channel],channel,self.framerate)

	def broken_frame(self):
		chann0 = detect_broken_frame(self.wdata0, self.framerate)
		chann1 = detect_broken_frame(self.wdata1, self.framerate)
		if chann0 == 0 and chann1 == 0:
			print "No Broken-Frame Found!"
		else:
			print "Numbers in Left  channel : %d"%len(chann0)
			print "Numbers in Right channel : %d"%len(chann1)
			if chann0 != 0:
				for item in chann0:
					print "+----------"
					print "| channel:%d, detect a broken frame, in time:"%0, item
					print "+----------"
			if chann1 != 0:
				for item in chann1:
					print "+----------"
					print "| channel:%d, detect a broken frame, in time:"%1, item
					print "+----------"





##################################################################################################



class Preprocess:
	def __init__(self):
		try:
			cfile = open(_work_dir+'/data/AudioFingerCatalog.pkl', 'rb')
			self.catalog = pickle.load(cfile)
		except EOFError:
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
		bin_path = "%s%s%s%s"%(_work_dir,"/data/",str(index),".bin")
		dfile = open(bin_path, 'w+')
		np.array(cache,dtype=np.uint32).tofile(bin_path)
		dfile.close()
		del cache[:]
		
		#Update catalog
		self.catalog.update({index:filename})
		cfile = open(_work_dir+'/data/AudioFingerCatalog.pkl', 'w+')	
		pickle.dump(self.catalog, cfile)
		cfile.close()
		print "HEAR<SAVE> DONE!"

	def clean_up(self):
		cfile = open(_work_dir+'/data/AudioFingerCatalog.pkl', 'w+')
		cfile.close()
		print "Already Clean Done!"

	def forget(self,filename):
		self.catalog.pop(filename)
		cfile = open(_work_dir+'/data/AudioFingerCatalog.pkl', 'w+')	
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