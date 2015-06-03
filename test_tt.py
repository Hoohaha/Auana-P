import time, os, pyaudio
from pyaudio import PyAudio, paInt16
import wave
from auana import *

CHUNK = 1024
#FORMAT = pyaudio.paInt16
FORMAT = paInt16
CHANNELS = 2
RATE = 16000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = (os.getcwd()+"/output.wav").replace('\\','/')
#WAVE_OUTPUT_FILENAME = 'C:\Work\new_stack\audio_anuana\Auana-P-master\'+"output.wav"
print WAVE_OUTPUT_FILENAME


#open audio stream
pa = PyAudio()

def Audio_record():
	stream = pa.open(format=FORMAT,
					channels=CHANNELS,
					rate=RATE,
					input=True,
					frames_per_buffer=CHUNK)

	print("* recording")

	frames = []

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		frame = stream.read(CHUNK)
		frames.append(frame)

	print("* done recording")

	stream.stop_stream()
	stream.close()
	pa.terminate()

	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(pa.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()


#AUANA INIT
au = Auana()
w  = WaveForm(au)


# #record audio played by audio_device	
# Audio_record()

#load file
data, framerate, nchannels = Load_file(WAVE_OUTPUT_FILENAME)
#transform data to WaveForm
w.data = data

print w.recognize()
print w.detect_broken_frame()