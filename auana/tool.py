# -*- coding: utf-8 -*-
from pyaudio import PyAudio, paInt16
import wave, os,time
import numpy as np

class AudioTool:
    '''
    This function include record and play, if you want to play and record,
    please set the play is True.
    The sample rate is 44100
    Bit:16
    '''
    def __init__(self):
        self.chunk = 1024
        self.channels = 2
        self.samplerate = 44100
        self.format = paInt16
        #open audio stream
        self.pa = PyAudio()
        self.save_buffer = []
    
    def record_play(self,seconds,play=False,file_play_path=None,file_save_path=None):

        NUM = int((self.samplerate/float(self.chunk)) * seconds)

        if play is True:
            swf = wave.open(file_play_path, 'rb')
        
        stream = self.pa.open(
                        format   = self.format, 
                        channels = self.channels, 
                        rate     = self.samplerate, 
                        input    = True,
                        output   = play,
                        frames_per_buffer  = self.chunk
                        )
        # wave_data = []
        while NUM:
            data = stream.read(self.chunk)
            self.save_buffer.append(data)
            wave_data=np.fromstring(data, dtype = np.short)
            wave_data.shape = -1,2
            wave_data = wave_data.T #transpose multiprocessing.Process
            # print int(data)
            print wave_data
            NUM -= 1
            if play is True:
                data = swf.readframes(self.chunk)

                stream.write(data)
                if data == " ": break

        if play is True:
            swf.close()
        #stop stream
        stream.stop_stream()
        stream.close()

        # save wav file
        def _save_wave_file(filename,data):
            wf_save = wave.open(filename, 'wb')
            wf_save.setnchannels(self.channels)
            wf_save.setsampwidth(self.pa.get_sample_size(self.format))
            wf_save.setframerate(self.samplerate)
            wf_save.writeframes("".join(data))
            wf_save.close()

        _save_wave_file(file_save_path, self.save_buffer)
        del self.save_buffer[:]
        print file_save_path," Record Sucessful!"

    

    def play(self,filepath):

        wf = wave.open(filepath, 'rb')

        stream =self.pa.open(
                        format   = self.pa.get_format_from_width(wf.getsampwidth()), 
                        channels = wf.getnchannels(), 
                        rate     = wf.getframerate(), 
                        output   = True,
                        )

        NUM = int(wf.getframerate()/self.chunk * 15)

        print "playing.."
        while NUM:
            data = wf.readframes(self.chunk)
            if data == " ": break
            stream.write(data)
            NUM -= 1
        stream.stop_stream()
        del data
        stream.close()

    def close(self):
        
        self.pa.terminate()

if __name__ == '__main__':
    at = AudioTool()
    at.record_play(seconds = 1,file_save_path="C:/2.wav")
    at.close()
    print (-1)<<8