# -*- coding: utf-8 -*-
from pyaudio import PyAudio, paInt16
import wave, os

def Audio_record_play(seconds,play,filename):
    '''
    This function include record and play, if you want to play and record,
    please set the play is True.
    The sample rate is 44100
    Bit:16
    '''
    CHUNK = 1024
    CHANNELS = 2
    SAMPLING_RATE = 44100
    FORMAT = paInt16
    NUM = int(SAMPLING_RATE/CHUNK * seconds)

    save_buffer = []

    if play is True:
        source_file = autohandle_directory + '/audio_lib/'+'source1.wav'
        swf = wave.open(source_file, 'rb')
    
    #open audio stream
    pa = PyAudio()
    default_input = pa.get_default_host_api_info().get('defaultInputDevice')
    stream = pa.open(
                    format   = FORMAT, 
                    channels = CHANNELS, 
                    rate     = SAMPLING_RATE, 
                    input    = True,
                    output   = play,
                    frames_per_buffer  = CHUNK,
                    input_device_index = default_input
                    )

    logging.info(">> START TO RECORD AUDIO")
    while NUM:
        save_buffer.append(stream.read(CHUNK))
        NUM -= 1
        if play is True:
            data = swf.readframes(CHUNK)
            stream.write(data)
            if data == " ": break

    #close stream
    stream.stop_stream()
    stream.close()
    pa.terminate()

    # save wav file
    def save_wave_file(filename,data):
        wf_save = wave.open(filename, 'wb')
        wf_save.setnchannels(CHANNELS)
        wf_save.setsampwidth(pa.get_sample_size(FORMAT))
        wf_save.setframerate(SAMPLING_RATE)
        wf_save.writeframes("".join(data))
        wf_save.close()

    save_wave_file(filename, save_buffer)

    del save_buffer[:]
    

def Audio_play(filepath):
    '''
    play audio
    '''
    CHUNK = 1024

    wf = wave.open(filepath, 'rb')
    pa = PyAudio()
    default_output = pa.get_default_host_api_info().get('defaultOutputDevice')
    stream =pa.open(format   = pa.get_format_from_width(wf.getsampwidth()), 
                    channels = wf.getnchannels(), 
                    rate     = wf.getframerate(), 
                    output   = True,
                    output_device_index = default_output)

    NUM = int(wf.getframerate()/CHUNK * 15)
    logging.info(">> START TO  PLAY  AUDIO")
    while NUM:
        data = wf.readframes(CHUNK)
        if data == " ": break
        stream.write(data)
        NUM -= 1
    stream.stop_stream()
    stream.close()
    del data
    pa.terminate()