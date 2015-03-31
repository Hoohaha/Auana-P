Auana-P Version 0.4
#

Auana-P: Auana algorithm Package.<br>

Auana is a open source, light tool with the audio recognition and some basic analysis algorithms, it is based on python and c. Auana can easily find simialr audio which it heared before, and tell the user the place where the songs is playing. Broken-Frame, Volume detection also is it`s strength.<br>
Auana support microphone records and file analysis. File analysis only support "wav" file for now. 
At first, Auana is designed for audio validition. This is because pepole need to check musics/songs by manually. 
So for the automation of audio validation, it may be a good idea. It is still in developing. If you are intereted in it, welcome to contact with me by Email.<br>

##Setup:
-----------------------------------
*  Firstly, install "numpy"    (math tool)<br>
*  Besides, install "pyaudio"  (record audio or play audio)[option]<br>

##Features:
-----------------------------------
>1.Broken-frame detection                                      [support]<br>
>2.Sound recognition                                           [support]<br>
>3.Volume value detection                                      [support]<br>
>4.Audio play and record                                       [support]<br>
>5.Signal noise ratio detection                                [will]<br>
>6.Real time detection and analysis                            [will]<br>
>7.Support mp3 ,wma…etc                                        [will]<br>
>8.Detect noise                                                [will]<br>


##Quickly Start
-----------------------------------
1> Prework: The recognition need to get the reference information of audios before starting of your work.<br>
The "Preprocess" is a class can be used to memory an audio charactics. The following example<br>
shows how to use it.<br>
For example:<br>
```python
        from auana import Preprocess
        p=Preprocess
        
        #memory the audio infomation,before you start to Analyze
        p.hear("sample.wav")
        
        #show all itmes which saved in it's internal.
        p.items()
        
        #clear all items. this functions should be used with caution.
        p.clean_up()
```   
2> Recognition: There are two calss: Auana and Fana.<br>
Fana: File recognition(only support .wav)<br>
For example:<br>
```python
        from auana import Fana
        
        #mono recognition
        print Fana("sample.wav").mono_start()
        
        #stereo recognition
        print Fana("sample.wav").stereo_start()
```
3> Broken-Frame detection: This is a special funtions to be used to detect broken-frame.<br>
It will tell you wheather the audi lost frames, and will return where lost it.<br>
For example:<br>
```python
        from auna import Fana
        #broken frame detection
        Fana("sample.wav").broken_frame()
```
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
version 0.3.Auana: Optimzie parameter about recognition to make it more reliable.<br>
version 0.4.Auana: New functions: return where the match songs is playing.<br>
