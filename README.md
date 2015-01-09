Auana-P Version 0.2
=======

Auana-P: Auana algorithm Package.<br>

Auana is a light tool with the audio recognition based on python and c.It can easily find simialr audio which it heared before. And it can detect and analyze the audio file, such as: broken-frame, noise, volume etc.<br>
Now Auana only support wav file. For the automation of audio validation, i don`t think that must be a bad solution. It is still in developing. If you are intereted in it, you can contact me.<br>

##Setup:
-----------------------------------
*  Firstly, install "numpy"    (math tool)<br>
*  Besides, install "pyaudio"  (record audio or play audio)[option]<br>

##Features:
-----------------------------------
1.Broken-frame detection                                      [support]<br>
2.Sound recognition                                           [support]<br>
3.Volume value detection                                      [support]<br>
4.Audio play and record                                       [support]<br>
5.Signal noise ratio detection                                [will]<br>
6.Real time detection and analysis                            [will]<br>
7.Support mp3 ,wma…etc                                        [will]<br>
8.Detect the sound error caused by device clock frequency     [will]<br>
9.Detect noise                                                [will]<br>


##How to use it to analysis a wave file?
-----------------------------------
    For example:<br>
              
              from auana import Preprocess
              p=Preprocess
              
              #memory the audio infomation,before you start to Analyze
              p.hear("sample.wav")
              
              from auana import Fana
              #mono analyze
              print Fana("sample.wav").mono_start()
              
              #stereo analyze
              print Fana("sample.wav").stereo_start() 
              
##Notice
-----------------------------------
This algorothm is not stable. <br>
Please use git pull to sync the code to get the latest update.

##Version modification
--------------
version 0.1.Auana Pacage. <br>
version 0.2.Auana: designed by C and python.<br>

##Performance
-----

