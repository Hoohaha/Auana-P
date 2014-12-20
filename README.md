Auana-P Version 0.1
=======

Auana-P: Auana algorithm Package.<br>

Auana is a light tool with the audio recognition based on python.It can easily find simialr audio which it heared before. And it can detect and analyze the audio file, such as: broken-frame, noise, volume etc.<br>
Now Auana only support wav file. For the automation of audio validation, i don`t think that must be a bad solution. It is still in developing. If you are intereted in it, you can contact me.<br>

###Setup:
-----------------------------------
1) Firstly, install python: numpy sicpy(math tool)<br>
2) Besides, install pyaudio (record audio or play audio)<br>



###How to use it to analysis a wave file?
-----------------------------------
    For example:<br>
              from auana import Fana
              Fana("sample.wav").save_fingerprint#save the fingerprint of audio
              Fana("sample.wav").mono_start()#mono analyze
              Fana("sample.wav").stereo_start()#stereo analyze
