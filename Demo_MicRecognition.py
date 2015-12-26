# -*- coding: utf-8 -*-
from pyaudio import PyAudio, paInt16
import wave , sys , os, time
import numpy as np

from auana import Storage, WaveForm

print ("Title: Mic Recognition Demo")

pa      = PyAudio()
storage = Storage()

w = storage.Open()

samplerate = storage.get_framerate()
chunk = 1024
channels = 2
format = paInt16

print ("Channels: %d  Samplerate:%6d   Bits:%2d\n\n"%(channels,samplerate,16))



Time = 5
NUM = int((samplerate*Time)/float(chunk))

save_buffer = []

#open audio stream    
stream = pa.open(
            format   = format, 
            channels = channels, 
            rate     = samplerate, 
            input    = True,
            frames_per_buffer  = chunk
            )
while ("" == raw_input("Press \'Enter\' to start.")):
    N = NUM
    print ("  Listening...")
    # wave_data = []
    while N:
        save_buffer.append(stream.read(chunk))
        N -= 1

    wave_data = np.fromstring("".join(save_buffer), dtype = np.short)
    wave_data.shape = -1,2
    wave_data = wave_data.T

    w.data = wave_data

    start = time.time()
    name, confidence, position= w.recognize()
    end = time.time() - start

    if name is not None:
        print ("  Now Playing is: %s Accuracy: %.2f Position: %d'%d "%(name.split(".")[0],confidence,position/60,position%60))
    else:
        print ("  Not Found!")
    print ("-------------------------------------\n                    Time Cost: %.3f \n"%end)

    save_buffer = []

#stop stream
stream.stop_stream()
stream.close()
del save_buffer

