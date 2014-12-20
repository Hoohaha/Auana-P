Auana-P Version 0.1
=======

Auana-P: Auana algorithm Package.<br>
Auana means:Audio Analysis Algorithm.<br>

Auana is a light tool with the audio recognition based on python.<br>
It can easily find simialr audio which it heared before. And it can detect and analyze the audio file,<br>
for example: broken-frame, noise, volume.<br>
Now Auana only support wav file. For the automation of audio validation, i don`t think that must be a bad solution.<br>
and it is still in developing. If you are intereted in it, you can contact me.<br>

###Setup:
-----------------------------------
1) Firstly, install python: numpy sicpy(math tool)<br>
2) Besides, install pyaudio (record audio or play audio)<br>



###How to use it to analysis a wave file?
-----------------------------------
    For example:<br>
              from auana import FileAnalysis<br>
              FileAnalysis("sample.wav").stereo_start()<br>
