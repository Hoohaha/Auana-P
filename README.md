Auana-P Version 0.6


#Auana-P:Audio Analysis algorithm Python Package<br>
########################

Auana is a open source, free and light tool with the audio recognition and basic analysis algorithms. It try to provide a professional audio recognition solutions for python. <br>
It was designed by python and c(core algorithm). So it is fast enough, it can easily find the simialr references which it heared before, the progress just like human. And also it will tell the user the position where the songs is playing. 
Auana support microphone records and file analysis. File analysis only support "wav" file for now. In addition, it also provide the functions: Broken-Frame detection and Volume value detection.<br>

Except using for recognitions, it will more focus on audio signal analysis. 
At the begaining, Auana is designed for audio validition. It is so boring to check the musics/songs by manually.  
So for the automation of audio validation, it may be a good idea. It is still in developing. Any comments, suggestions welcomed. My Email: solo.footprint@foxmail.com.

##Requirments:
-----------------------------------
*  [python2.7](https://www.python.org/)  ---  32-bit only.<br />
*  [numpy](http://www.numpy.org/)  --- Mathmatic.<br />
*  [pyaudio](http://people.csail.mit.edu/hubert/pyaudio/) --- Audio record and play, Option.<br />

##Features:
-----------------------------------
>1.Broken-frame detection                                      [support]<br>
>2.Sound recognition                                           [support]<br>
>3.Volume value computation                                    [support]<br>
>4.Audio play and record                                       [support]<br>
>5.THD+N                                		       [support]<br>
>6.Support mp3 ,wma…etc                                        [will]<br>
>7.Detect noise                                                [will]<br>


##Quickly Start
-----------------------------------
###1.Storage
The class Storage is a data management. If you want to use the recognition, you must create a storage and init it.<br>

+  **__init__(path=DEFAULT_DATA_PATH)**<br \>
  Parameters:<br \>
  DEFAULT_DATA_PATH = "./data"


####1) Functions.

+  **query(file)**:<br \>
query the file if was saved in storage.<br \>
*file*: file path.<br \>
+  **clean_up()**:<br \>
 clean all items in this storage. Should be caution to use.<br \>
+  **forget(file)**:<br \>
 forget/delete a file.<br \>
*file*: file path.<br \>
+  **items()**:<br \>
 show all item which was saved in storage<br \>
+  **commit()**:<br \>
 commit the changes<br \>
+ **Open(file)** : <br \>
 open a wave file and return a WaveForm Object. If file is None, it will open an empty WaveForm.<br \>
*file*: file path.<br \>


####2) Create a new storage.
Create a new storage to store the data. The defalut settings: framerate is 22500, data path is ../data.
Use the default configuration, see the following example.
```python
try:
    Create()
except ValueError:
    pass
```

Custom settings:
```python
#Custom framerate: 16000.
try:
    Crate(framerate=1600)
except ValueError:
    pass
```

```python
#Custom data path.
try:
    Crate(path="C:/data")
except ValueError:
    pass
```


```python
#Custom framerate and data path.
try:
    Crate(framerate=16000, path="C:/data")
except ValueError:
    pass
```


###2.WaveForm
WaveForm is a class that can be used to recognize or detect broken frame.<br \>
+  **__init__(framerate, data, storage=None, filename=None, channels=2)**<br \>
 Parameters:<br \>
	framerate --- sample rate.
	data  ---  a data list required.
	storage --- A reference storage manager. Default is None.<br \>
	filename --- Waveform filename. Default is None.<br \>
	channels --- channels number. Default is 2.<br \>
	
####1) Functions.
Basic Functions:<br \>
+  **write(data)**:<br \>
 write new data to waveform.<br \>
 *data*: a list required.<br \>
+  **detec_broken_frame(ch=None)**:<br \>
 broken frame detection.<br \>
 *ch*: default stereo mode---None, mono mode---0/1 (0: left, 1:right)<br\>
+  **get_volume(ch=None)**:<br \>
 compute the average volume of this waveform.<br \>
 *ch*: default stereo mode---None, mono mode---0/1 (0: left, 1:right)<br \>
+ **get_THD(ch==None)**:<br \>
 compute the THD+N.<br \>
 *ch*: default stereo mode---None, mono mode---0/1 (0: left, 1:right)<br \>

Recognition Functions:<br \>
+  **hear()**:<br \>
  hear/extract the fingerprints to storage.<br \>
+  **recognize(ch=None, Fast=True)**:<br \>
 audio recognition. <br \>
 *ch*: default stereo mode---None, mono mode---01/1(0: left, 1:right).<br \>
 *Fast*: means fast search, if the accuracy is high enough, it will search in right channel. default True.

###2) Examples
open an waveform
```python
from auana import Storage

sto = Storage()

w = sto.Open("sample.wav")
```

or open an empty WaveForm:

```python
from auana import Storage

sto = Storage()

w = sto.Open()

w.write(data) #w.data=data          #data:wave data
```

If you don`t use it for recognition. you can use it by the following forms.
```python
from auana import Open

w = Open("sample.wav")

w.detect_broken_frame()  #for broken frame detection
```



1> Save the fingerprints into the storage.
```python
w.hear()
```
2> For recognition:

```python
name, accuracy, position = w.recognize()
```
3>For broken frame detection:
```python
bf = w.detect_broken_frame()
```
4>Get the volume:

```python
v = w.get_volume()
```


##Demo User's Guide
-----
>1> Prework<br>
Prework Demo can memory the new files.

>2> MIC Recognition<br>
This is a Demo for showing how to recognize the data from MIC. You can double click the "Demo_MICRecognition" to run.<br>
And then you can play a song and press "Enter" to make the demo to processing.

>3> File Search<br>
Drag the sample ".wav" file into "Demo_FileSearchDemo.py".

>4> Broken Frame<br>
Drag the sample into "Demo_BrokenFrame.py". 

##Performance
-----
There are 180 files in the "./data" folder. Follow figure shows the relationships between record-time and search time.

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
