from recognize import recognize,get_fingerprint
from broframe import detect_broken_frame
import wave, time, os,re
try:
	import numpy as np
except ImportError:
	print("Please build and install the numpy Python ")
try:
	import yaml
except ImportError:
	print("Please build and install the yaml Python ")

current_directory = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')

class AuanaBase(object):
	def __init__(self):

		try:
			cfile = open(current_directory+'/data/AudioFingerCatalog.yml','r')
			self.catalog = yaml.load(cfile)
		except TypeError:
			raise ("Please save the audio-fingerprint at first")
			return
		cfile.close()

	def __del__(self):
		pass

	def mono(self,wdata,channel,framerate,quick=None):
		start = time.time()
		audio_name, confidence,avgdb=recognize(self.catalog,wdata,framerate,channel,quick)
		broframe=detect_broken_frame(wdata, framerate)
		print "time:",time.time()-start
		return {"name":audio_name,"broken_frame":broframe,"confidence":confidence,"average_db":avgdb}

	def stereo(self,wdata0,wdata1,framerate):
		result={0:"",1:""} 
		result[0] = self.mono(wdata0,0,framerate)

		if result[0]["name"] is not None:
			result[1]=self.mono(wdata1,1,framerate,quick=result[0]["name"])
		else:
			result[1]={"name":None,"broken_frame":0,"confidence":0,"average_db":0}

		average_db = int((result[1]["average_db"]+result[1]["average_db"])/2)
		confidence = round((result[0]["confidence"]+result[1]["confidence"])/2,3)
		
		if result[0]["broken_frame"]!=0 and result[1]["broken_frame"]!=0:
			for channels in  xrange(2):
				print "+----------"
				print "| channel:%d, detect a broken frame, in time:"%channels, result[channels]["broken_frame"]
				print "+----------"
			return "Broken Frame",0,average_db

		elif (result[0]["name"]!=None) and (result[0]["name"] == result[1]["name"]):
			return result[0]["name"],confidence,average_db

		else:
			return "Not Found",0,average_db

class Fana(AuanaBase):
	'''
	Fana: File Analysis
	'''
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
		'''
		catalog = {Audio: 

		}
		'''
		try:
			if self.catalog.has_key(self.name):
				print "saved before"
				return
		except AttributeError:
			self.catalog ={}

		index = str(len(self.catalog))

		temp={
				0:get_fingerprint(wdata=self.wdata0,framerate=self.framerate,db=False),
				1:get_fingerprint(wdata=self.wdata1,framerate=self.framerate,db=False)
				}
		dfile = open(current_directory+"/data/"+index+".yml", 'w+')
		yaml.dump(temp, dfile)
		dfile.close()


		self.catalog.update({self.name:index})
		cfile = open(current_directory+"/data/AudioFingerCatalog.yml", 'w+')	
		yaml.dump(self.catalog, cfile)
		cfile.close()
		print "save Audio-Fingerprint Done"

def MicAnalyis(AuanaBase):
	def __init__(self):
		AuanaBase.__init__(self)

		CHUNK         = 4096
		FORMAT        = paInt16
		CHANNELS      = 2
		SAMPLING_RATE = 44100

		#open audio stream
		pa = PyAudio()
		stream = pa.open(
						format   = FORMAT, 
						channels = CHANNELS, 
						rate     = SAMPLING_RATE, 
						input    = True,
						frames_per_buffer  = CHUNK
						)

	def __del__(self):
		pass
	def satrt(self):
		pass

	def stop(self):
		pass
	def record(self):
		while True:
			queue.put(stream.read(CHUNK))
	def volume(self):
		data = queue.get()
		xs   = np.multiply(data, signal.hann(DEFAULT_FFT_SIZE, sym=0))
		#fft transfer
		xfp  = 20*np.log10(np.abs(np.fft.rfft(xs)))
		db   = np.sum(xfp[0:200])/200