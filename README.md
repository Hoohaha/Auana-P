Auana-P Version 0.5


#Auana-P:Auana algorithm Python Package<br>
########################

Auana is a open source, free and light tool with the audio recognition and basic analysis algorithms. It try to provide a professional audio recognition solutions for python. <br>
It was designed by python and c(core algorithm). So it is fast enough, it can easily find the simialr references which it heared before, the progress just like human. And also it will tell the user the position where the songs is playing. 
Auana support microphone records and file analysis. File analysis only support "wav" file for now. In addition, it also provide the functions: Broken-Frame detection and Volume value detection.<br>

Except using for recognitions, it will more focus on audio signal analysis. 
At the begaining, Auana is designed for audio validition. It is so boring to check the musics/songs by manually.  
So for the automation of audio validation, it may be a good idea. It is still in developing. If you are intereted in it, welcome to contact me by Email.<br>

##Setup:
-----------------------------------
*  Firstly, install python package "numpy"    (math tool)<br>
*  Besides, install python package "pyaudio"  (audio play/record library)<br>

##Features:
-----------------------------------
>1.Broken-frame detection                                      [support]<br>
>2.Sound recognition                                           [support]<br>
>3.Volume value detection                                      [support]<br>
>4.Audio play and record                                       [support]<br>
>5.Signal noise ratio detection                                [will]<br>
>6.Support mp3 ,wma…etc                                        [will]<br>
>7.Detect noise                                                [will]<br>


##Quickly Start
-----------------------------------
1> Prework: The recognition need to get the reference information of audios before starting of your work.<br>
The "Preprocess" is a class can be used to memory an audio charactics. The following example shows how to use it.<br>
For example:<br>
```python
        from auana import Preprocess
        
        #you'd better to set a path to save data. 
        #if data path is empty, it will use the default configuration: "../auana/data/"
        p=Preprocess("data_path")#p=Preprocess()
        
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
        from auana import Auana,Fana
        
        #data_path: where is the data
        aua = Auana("data_path")
        
        #mono recognition
        print Fana(aua,"sample.wav").mono_start()
        
        #stereo recognition
        print Fana(aua,"sample.wav").stereo_start()
```
3> Broken-Frame detection: This is a special funtions to be used to detect broken-frame.<br>
It will tell you wheather the audi lost frames, and will return where lost it.<br>
For example:<br>
```python
        Fana(aua,"sample.wav").broken_frame()
```
##Example User's Guide
-----
1> Prework<br>
Prework Demo can memory the new files.

2> MIC Recognition<br>
This is a Demo for showing how to recognize the data from MIC. You can double click the "Example_MICRecognition" to run.<br>
And then you can play a song and press "Enter" to make the demo to processing.

3> File Search<br>
Drag the sample ".wav" file into "Example_FileSearchDemo.py".

4> Broken Frame<br>
Drag the sample into "Example_BrokenFrame.py". 

##Performance
-----
There are 180 files in the "auana/data" folder. Follow figure shows the relationships between record-time and search time.

![7](doc/figure_2.png)


##Simple Theory
-----
![3](doc/Slide3.PNG)
![4](doc/Slide4.PNG)
![5](doc/Slide5.PNG)
![6](doc/Slide6.PNG)
![6](doc/Slide7.PNG)
![8](doc/Slide8.PNG)

##Version modification
--------------
version 0.1.Auana Pacage. <br>
version 0.2.Auana: designed by C and python.<br>
version 0.3.Auana: Optimzie parameter about recognition to make it more reliable.<br>
version 0.4.Auana: New functions: return where the match songs is playing.<br>
version 0.5.Auana: Optimize the get_fingerprint algoritms<br>
version 0.6.Auana: New algorithm for extracting fingerprints<br>
