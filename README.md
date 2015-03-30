Auana-P Version 0.3
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
1> Prework: The recognition need to get the reference information of audios before starting of your work.<br>
The "Preprocess" is a class can be used to memory an audio charactics. The following example<br>
shows how to use it.

    For example:<br>
        from auana import Preprocess
        p=Preprocess
        
        #memory the audio infomation,before you start to Analyze
        p.hear("sample.wav")
        
        #show all itmes which saved in it's internal.
        p.items()
        
        #clear all items. this functions should be used with caution.
        p.clean_up()
   
2> Recognition: There are two calss: Auana and Fana.<br>
Fana: File recognition(only support .wav)<br>

    For example:<br>
        from auana import Fana
        
        #mono recognition
        print Fana("sample.wav").mono_start()
        
        #stereo recognition
        print Fana("sample.wav").stereo_start()

3> Broken-Frame detection: This is a special funtions to be used to detect broken-frame.<br>
It will tell you wheather the audi lost frames, and will return where lost it.

    For example:<br>
        from auna import Fana
        #broken frame detection
        Fana("sample.wav").broken_frame()

##Demo User's Guide
-----
1> Auana_Demo<br>
This is a Demo for showing how to recognize the data from MIC. You can double click the "Auana_Demo.py" to run.<br>
And then you can play a song and press "Enter" to make the demo to processing.

2> Broken_Frame_Demo<br>
Drag the sample into "BrokenFrameDemo.py". 

##Simple Theory
-----
![3](doc/Slide3.PNG)
![4](doc/Slide4.PNG)
![5](doc/Slide5.PNG)
![6](doc/Slide6.PNG)
![6](doc/Slide7.PNG)
![8](doc/Slide8.PNG)

##Performance
-----

##Version modification
--------------
version 0.1.Auana Pacage. <br>
version 0.2.Auana: designed by C and python.<br>

