Auana-P Version 0.1
=======

Auana-P: Auana algorithm Package.
Auana means:Audio Analysis Algorithm.
This is Auana version0.1

!!Setup:
=======
1)install python: numpy sicpy(math tool)
2)install python: yaml(save data)
3)install python: pyaudio(record audio or play audio)



Changes:
=======
1)Resconstruct the code.
2)Update the broken-frame issue.
3)Improve the Accuracy of recognition.
4)Fix some bugs.

How to use it to analysis a wave file?
=======
For example:
from auana import FileAnalysis
FileAnalysis("sample.wav").stereo_start()
