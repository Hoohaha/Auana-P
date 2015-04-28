# -*- coding: utf-8 -*-
from pyaudio import PyAudio, paInt16
import wave , sys , os, time
import numpy as np

__PATH__ = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
sys.path.append(__PATH__)

from auana import Auana

print "Title: Mic Recognition Demo\n"

chunk = 1024
channels = 2
samplerate = 44100
format = paInt16

pa = PyAudio()
aua = Auana()

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
while ("" == raw_input("Press \'Enter\' to start..")):
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
    name, confidence, db, position= aua.stereo(wave_data[0],wave_data[1],samplerate)
    end = time.time() - start

    if name is not None:
        print "  Now Playing is: %s Accuracy: %.2f Position: %d'%d "%(name.split(".")[0],confidence,position/60,position%60)
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

