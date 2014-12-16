from recognize import recognize,get_fingerprint
from broframe import detect_broken_frame
import wave, time, os,re
try:
	import numpy as np
except ImportError:
	print("Please build and install the numpy Python ")
try:
	import scipy.signal as signal
except ImportError:
	print("Please build and install the scipy Python ")
try:
	import yaml
except ImportError:
	print("Please build and install the yaml Python ")

autohandle_directory = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')

class AuanaBase(object):
	def __init__(self):
		try:
			source_data = open(autohandle_directory+'/AudioFingerData.yml','r')
			self.sdata = yaml.load(source_data)
		except None:
			print "Please save the audio-fingerprint in AudioFingerData.yml"
			return
		source_data.close()
	def __del__(self):
		pass
	
	def mono(self,wdata,channel,framerate):
		audio_name, confidence,avgdb=recognize(wdata,self.sdata,channel,framerate)
		broframe=detect_broken_frame(wdata, channel,framerate)
		return {channel:{"broken_frame":broframe,"name":audio_name,"confidence":confidence,"average_db":avgdb}}

	def stereo(self,wdata0,wdata1,framerate):
		result={} 
		result.update(self.mono(wdata0,0,framerate))
		result.update(self.mono(wdata1,1,framerate))

		average_db = int((result[1]["average_db"]+result[1]["average_db"])/2)
		confidence = round((result[0]["confidence"]+result[1]["confidence"])/2,3)
		
		for channels in  xrange(2):
			if result[channels]["broken_frame"]!=0:
				print "+----------"
				print "| channel:%d, detect a broken frame, in time:"%channels, result[channels]["broken_frame"]
				print "+----------"
				return "Broken Frame",0,average_db
		if (result[0]["name"]!=None) and (result[0]["name"] == result[1]["name"]):
			return result[0]["name"],confidence,average_db
		else:
			return "Not Found",0,average_db

class FileAnalysis(AuanaBase):
	def __init__(self,filepath):	
		AuanaBase.__init__(self)
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

	def save_fingerprint(self):
		try:
			yaml_data = open(autohandle_directory+"/AudioFingerData.yml", 'r+')	
			catalog = yaml.load(yaml_data)
		except None:
			catalog ={}
		for key in catalog:
			if self.name == key:
				yaml_data.close()
				print "saved before"
				return
		
		temp={self.name:{
				0:get_fingerprint(wdata=self.wdata0,framerate=self.framerate),
				1:get_fingerprint(wdata=self.wdata1,framerate=self.framerate)
				}
			}

		try:
			yaml_data = open(autohandle_directory+"/AudioFingerData.yml", 'w+')
			catalog.update(temp)
			yaml.dump(catalog, yaml_data)
		finally:
			yaml_data.close()
		print "save Audio-Fingerprint Done"

