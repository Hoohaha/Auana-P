from recognize import recognize,get_fingerprint
from broframe import detect_broken_frame
import wave, time, os, re
import cPickle as pickle
try:
	import numpy as np
except ImportError:
	print("Please build and install the numpy Python ")

_work_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')

def _memory(wdata0,wdata1,framerate,index):
	cache = []
	cache.append(get_fingerprint(wdata=wdata0,framerate=framerate,db=False))
	cache.append(get_fingerprint(wdata=wdata1,framerate=framerate,db=False))
	np.array(cache,dtype=np.uint32).tofile(_work_dir+"/data/"+index+".bin")
	del cache[:]

class Auana(object):

	def __init__(self):
		try:
			cfile = open(_work_dir+'/data/AudioFingerCatalog.pkl', 'rb')
			self.catalog = pickle.load(cfile)
		except EOFError:
			self.catalog = {}
		cfile.close()

	def __del__(self):
		pass

	def broken_frame(self, wdata, framerate):
		broframe = detect_broken_frame(wdata, framerate)
		return broframe

	def mono(self,wdata,channel,framerate,quick=None):
		'''
		To improve the speed of recognition, we use the "quick" to do it.
		If it matched an audio(example "source1.wav") in channel0, when search in channel1 we will directly
		compare the matched audio("source1.wav"), rather than search all reference file again. 
		'''
		if len(self.catalog)==0:
			print("Error: No data saved in pkl file." 
				"Please fisrtly save the fingerprint of the reference audio.")
			self.__del__()
			os._exit(1)
		broframe = 0

		#audio recognition
		audio_name, confidence, avgdb = recognize(self.catalog,wdata,framerate,channel,quick)
		#broken frame detection
		# broframe=detect_broken_frame(wdata, framerate)

		return {"name":audio_name,"broken_frame":broframe,"confidence":confidence,"average_db":avgdb}

	def stereo(self,wdata0,wdata1,framerate):
		channel0 = 0
		channel1 = 1

		result={channel0:"",channel1:""}

		#1> Analyze the channel0 first. 
		result[channel0] = self.mono(wdata0,channel0,framerate)
		if result[channel0]["confidence"]>0.7:#if confidence is high, directly return
			return result[channel0]["name"], result[channel0]["confidence"], result[channel0]["average_db"]
		#2> Analyze the channel1.
		#'quick'means quick recognition.
		result[channel1]=self.mono(wdata1,channel1,framerate,quick=result[channel0]["name"])

		#handle the result from channel0 and channel1.
		average_db = round((result[channel0]["average_db"]+result[channel1]["average_db"])/2,1)
		confidence = round((result[channel0]["confidence"]+result[channel1]["confidence"])/2,3)
		
		if (result[channel0]["name"]!=None) and (result[channel0]["name"] == result[channel1]["name"]):
			return result[channel1]["name"], confidence ,average_db
		else:
			return "Not Found",0, average_db

class Fana(Auana):
	'''
	Fana: File Analysis
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

#developing...
def MicAnalyis(Auana):
	def __init__(self):
		Auana.__init__(self)

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
	def start(self):
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
		catalog = {"sample.wav":index}
		'''
		filename = os.path.basename(filepath)
		#judge the file if saved before.
		if self.catalog.has_key(filename):
			print "\"%s\" Have heared before!"%filename
			return "continue.."

		index = str(len(self.catalog))

		#creat .bin file
		dfile = open(_work_dir+"/data/"+index+".bin", 'w+')
		dfile.close()

		wf = wave.open(filepath, 'rb')
		nchannels, sampwidth, framerate, nframes = wf.getparams()[:4]
		wave_data = np.fromstring(wf.readframes(nframes), dtype = np.short)
		wave_data.shape = -1,2
		wave_data = wave_data.T #transpose
		wf.close()

		#save data
		_memory(wave_data[0],wave_data[1],framerate,index)

		#update catalog
		self.catalog.update({filename:index})
		cfile = open(_work_dir+'/data/AudioFingerCatalog.pkl', 'w+')	
		pickle.dump(self.catalog, cfile)
		cfile.close()
		print "Hear/Save Done"

	def clean_up(self):
		cfile = open(_work_dir+'/data/AudioFingerCatalog.pkl', 'w+')
		cfile.close()
		print "Already Clean Done!"

	def forget(self,filename):
		self.catalog.pop(filename)
		cfile = open(_work_dir+'/data/AudioFingerCatalog.pkl', 'w+')	
		pickle.dump(self.catalog, cfile)
		cfile.close()
		print "Already forgot <<%s>>!"%filename
	
	def items(self):
		#sort dict, te is a tuple 
		te = sorted(self.catalog.iteritems(),key=lambda asd:asd[1],reverse=False)
		print "******* File List *******"
		print "Total:%d"%len(self.catalog)
		print " No.","    ","File Name"
		for item in te:
			print "  %s       %s"%(item[1],item[0])
		print "***********************"