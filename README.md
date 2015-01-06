Auana-P Version 0.1
=======

Auana-P: Auana algorithm Package.<br>

Auana is a light tool with the audio recognition based on python.It can easily find simialr audio which it heared before. And it can detect and analyze the audio file, such as: broken-frame, noise, volume etc.<br>
Now Auana only support wav file. For the automation of audio validation, i don`t think that must be a bad solution. It is still in developing. If you are intereted in it, you can contact me.<br>

###Setup:
-----------------------------------
1) Firstly, install python: numpy and sicpy(math tool)<br>
2) Besides, install pyaudio (record audio or play audio)[option]<br>

###Features:
-----------------------------------
1.Broken-frame detection                                      [support]<br>
2.Sound recognition                                           [support]<br>
3.Volume value detection                                      [support]<br>
4.Audio play and record                                       [support]<br>
4.Signal noise ratio detection                                [will]<br>
5.Real time detection and analysis                            [will]<br>
6.Support mp3 ,wma…etc                                        [will]<br>
7.Detect the sound error caused by device clock frequency     [will]<br>
8.Detect noise                                                [will]<br>


###How to use it to analysis a wave file?
-----------------------------------
    For example:<br>
              from auana import Fana
              Fana("sample.wav").save_fingerprint #save the fingerprint of audio
              
              print Fana("sample.wav").mono_start() #mono analyze
              print Fana("sample.wav").stereo_start() #stereo analyze
              

