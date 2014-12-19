Auana-P Version 0.1
=======

Auana-P: Auana algorithm Package.
Auana means:Audio Analysis Algorithm.
This is Auana version0.1

Setup:
-----------------------------------
1)install python: numpy sicpy(math tool)\<br>
2)install python: yaml(save data)\<br>
3)install python: pyaudio(record audio or play audio)\<br>



###Changes:
-----------------------------------
1)Resconstruct the code.\<br>
2)Update the broken-frame issue.\<br>
3)Improve the Accuracy of recognition.\<br>
4)Fix some bugs.\<br>

###How to use it to analysis a wave file?
-----------------------------------
For example:\<br>
from auana import FileAnalysis\<br>
FileAnalysis("sample.wav").stereo_start()\<br>
