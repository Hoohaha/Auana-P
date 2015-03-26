# -*- coding: utf-8 -*-
from pyaudio import PyAudio, paInt16
import wave , sys , os
import numpy as np

_work_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
sys.path.append(_work_dir)

from auana import Auana

chunk = 1024
channels = 2
samplerate = 44100
format = paInt16
#open audio stream

pa = PyAudio()

NUM = int((samplerate/float(chunk)) * 5)

save_buffer = []    
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

    print "  Now Playing is: %s"%Auana().stereo(wave_data[0],wave_data[1],samplerate)[0].split(".")[0]
    print "---------------------------------------------------------"
    print " \n"

    save_buffer = []

#stop stream
stream.stop_stream()
stream.close()
del save_buffer