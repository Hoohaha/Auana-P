from auana import Fana
import os,time
current_directory = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')

'''==================save_fingerprint======================'''
start = time.time()
Fana(current_directory+"/sample/ding.wav").save_fingerprint()
print time.time()-start
print " "

start = time.time()
Fana(current_directory+"/sample/source1.wav").save_fingerprint()
print time.time()-start
print " "

# start = time.clock()
# Fana(current_directory+"/sample/piano.wav").save_fingerprint()
# print time.clock()-start
# print " "

# start = time.clock()
# Fana(current_directory+"/sample/Come And Get Your Love.wav").save_fingerprint()
# print time.clock()-start
# print " "

# '''===================function example====================='''
# print Fana(current_directory+"/sample/piano.wav").stereo_start()
# print" "
# print Fana(current_directory+"/sample/piano.wav").mono_start(0)
# print" "


'''=========================test==========================='''
# search .wav file
dir_audio = current_directory+"/sample"
audio_list = []
file_num = 0
for parent, dirnames, filenames in os.walk(dir_audio):
	for filename in filenames:
		portion = os.path.splitext(filename)
		if portion[1] == '.wav'and (211 <= int(portion[0]) <= 215 or 111 <= int(portion[0]) <= 116 or 121 <= int(portion[0]) <= 126) :
			path = os.path.join(parent, filename)
			path = path.replace('\\','/')
			audio_list.append(path)
			file_num += 1
NUM = 0
failed=[]
#start to handle
for a in  xrange(len(audio_list)):#
	start = time.clock()
	print audio_list[a]
	res = Fana(audio_list[a]).stereo_start()
	print audio_list[a],res,time.clock()-start