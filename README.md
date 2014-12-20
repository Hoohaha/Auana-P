Auana-P Version 0.1
=======

Auana-P: Auana algorithm Package.<br>
Auana means:Audio Analysis Algorithm.<br>

It is a light tool with the audio recognition based on python.<br>
It can easily find simialr audio which it heared before.<br>
And it can detect and analyze the audio file, for example: broken-frame, noise, volume.<br>
Now it only support wav file.<br>
For the automation of audio validation, it must be a good solution.<br>
Now it is still in developing.<br>
If you are intereted in it, you can contact me.<br>

###Setup:
-----------------------------------
1) Firstly, install python: numpy sicpy(math tool)<br>
2) Besides, install pyaudio(record audio or play audio)<br>



###How to use it to analysis a wave file?
-----------------------------------
    For example:<br>
              ######from auana import FileAnalysis<br>
              ######FileAnalysis("sample.wav").stereo_start()<br>
