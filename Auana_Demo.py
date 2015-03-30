# -*- coding: utf-8 -*-
from pyaudio import PyAudio, paInt16
import wave , sys , os, time
import numpy as np

_work_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
sys.path.append(_work_dir)

from auana import Auana

print "***** Auana Demo Start *****\n"
chunk = 1024
channels = 2
samplerate = 44100
format = paInt16


pa = PyAudio()

Time = 7
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
while ("" == raw_input("Continue ?")):

    N = NUM
    print "  Listening..."
    # wave_data = []
    while N:
        save_buffer.append(stream.read(chunk))
        N -= 1

    wave_data = np.fromstring("".join(save_buffer), dtype = np.short)
    wave_data.shape = -1,2
    wave_data = wave_data.T

    start = time.time()
    name, confidence, db, location= Auana().stereo(wave_data[0],wave_data[1],samplerate)
    end = time.time() - start

    if name != "Not Found":
        print "  Now Playing is: %s   confidence: %.2f   location: %.2f"%(name.split(".")[0],confidence,location)
    else:
        print "  Not Found!"
    print "-------------------------------------"
    print "                    Time Cost: %.3f"%end
    print " \n"

    save_buffer = []

#stop stream
stream.stop_stream()
stream.close()
del save_buffer

