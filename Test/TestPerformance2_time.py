# -*- coding: utf-8 -*-
from pyaudio import PyAudio, paInt16
import wave , sys , os, time
import numpy as np

__PATH__ = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
sys.path.append(os.path.dirname(__PATH__))

from auana import *

print " Mic Recognition Demo\n"


storage = Storage()
w = WaveForm(storage)

chunk = 1024
channels = 2
samplerate = storage.get_framerate()
format = paInt16

import matplotlib.pyplot as plt

plt.title("Diagram")
plt.xlabel('Record Time (s)')
plt.ylabel('Search Time (s)')


Time = [1,2,3,4,5,6,7,8,9,10,15,20,25,40]
#NUM = int((samplerate*Time)/float(chunk))
b=[]
save_buffer = []


pa = PyAudio()
#open audio stream
stream = pa.open(
            format   = format, 
            channels = channels, 
            rate     = samplerate, 
            input    = True,
            frames_per_buffer  = chunk
            )
#while ("" == raw_input("Continue ?")):
for i in Time:
    N = int((samplerate*i)/float(chunk))
    print "  Listening..."
    # wave_data = []
    while N:
        save_buffer.append(stream.read(chunk))
        N -= 1

    wave_data = np.fromstring("".join(save_buffer), dtype = np.short)
    wave_data.shape = -1,2
    wave_data = wave_data.T

    w.data = wave_data

    start = time.time()
    name, confidence, db, position = w.recognize()
    end = time.time() - start

    if name is not None:
        print "  Now Playing is: %s Accuracy: %.2f Position: %d'%d "%(name.split(".")[0],confidence,position/60,position%60)
    else:
        print "  Not Found!"
    print "-------------------------------------"
    print "                    Time Cost: %.3f"%end
    print " \n"
    b.append(end)
    save_buffer = []


plt.plot(Time,b)
plt.show()  
#stop stream
stream.stop_stream()
stream.close()
del save_buffer

