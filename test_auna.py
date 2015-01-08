from auana import Fana
import os,time
current_directory = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')

'''==================save_fingerprint======================'''
Fana(current_directory+"/sample/ding.wav").pre()
Fana(current_directory+"/sample/source1.wav").pre()
Fana("E:/sample/twrk24f120m/atl/Debug/211.wav").pre()
print " "
Fana("E:/Come And Get Your Love.wav").pre()
print " "

'''=========================test==========================='''
# search .wav file
dir_audio1 = "E:/sample"
dir_audio0 = "E:/none"
audio_list = []
file_num = 0
for parent, dirnames, filenames in os.walk(dir_audio1):
	for filename in filenames:
		portion = os.path.splitext(filename)
		if portion[1] == '.wav'and (211 <= int(portion[0]) <= 215 or 111 <= int(portion[0]) <= 116 or 121 <= int(portion[0]) <= 126) :
			path = os.path.join(parent, filename)
			path = path.replace('\\','/')
			audio_list.append(path)
			file_num += 1

# start = time.time()
# print Fana("E:/Come And Get Your Love.wav").stereo_start()
# print time.time()-start
# print " "

start = time.time()
print Fana("E:/none/s/121.wav").stereo_start()
print time.time()-start
print " "

ab = time.clock()
NUM = 0
failed=[]
#start to handle
for a in  xrange(len(audio_list)):#
	start = time.clock()
	# print audio_list[a]
	res = Fana(audio_list[a]).stereo_start()

	if res[0] != "Not Found" and res[0] != "Broken Frame" or res[0] == "ding":
		NUM += 1
		print audio_list[a],res,time.clock()-start
	else:
		print "                              ",audio_list[a],res,time.clock()-start

del Fana
print len(audio_list),NUM,(time.clock()-ab)/60
print "%.3f"%(float(NUM)/len(audio_list))