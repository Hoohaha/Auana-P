from auana import Fana, Preprocess
import os,time

'''
*************************************Function Example**********************************
This file shows that how to use the auana to achieve our functions.
Pre process: you must save some musics or voices before Fana or others.
Fana: Means File analysis.
'''

#get the directory
work_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')


'''*****************Pre Process*****************'''
p = Preprocess()

#show the file which is saved
p.items()

#hear the file and memory it
p.hear(work_dir+"/sample/ding.wav")

p.hear(work_dir+"/sample/source1.wav")

p.hear(work_dir+"/sample/piano.wav")



'''==================File Analysis==============='''


res = Fana("sample.wav").stereo_start()#File analysis
