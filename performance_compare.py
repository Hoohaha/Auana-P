from auana import Fana
import os,time
current_directory = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
start = time.time()
Fana(current_directory+"/sample/ding.wav").pre()
print time.time()-start
print " "


start = time.time()
print Fana("E:/sample/twrk22f120m/uv4/Debug/113.wav").stereo_start()
print time.time()-start
print " "

start = time.clock()
print Fana("E:/Come And Get Your Love.wav").stereo_start()
print time.clock()-start
print " "