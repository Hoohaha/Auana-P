from auana import Fana
import os,time

'''==================save_fingerprint======================'''
start = time.time()
Fana("C:/Users/b51762/Desktop/sample/piano.wav").save_fingerprint()
print time.time()-start
print " "

start = time.time()
Fana("C:/Users/b51762/Desktop/sample/source1.wav").save_fingerprint()
print time.time()-start
print " "

start = time.time()
Fana("C:/Users/b51762/Desktop/sample/ding.wav").save_fingerprint()
print time.time()-start
print " "

# # start = time.time()
# Fana("C:/Users/b51762/Desktop/sample/Come And Get Your Love.wav").save_fingerprint()
# print time.time()-start
# print " "

# '''===================function example====================='''
# print Fana("C:/Users/b51762/Desktop/music/ding2.wav").stereo_start()
# print" "
# print Fana("C:/Users/b51762/Desktop/music/ding.wav").mono_start(0)
# print" "


'''=========================test==========================='''
#search .wav file
dir_audio = 'C:/Users/b51762/Desktop/sample'
audio_list = []
file_num = 0
for parent, dirnames, filenames in os.walk(dir_audio):
	for filename in filenames:
		portion = os.path.splitext(filename)
		if portion[1] == '.wav':
			path = os.path.join(parent, filename)
			path = path.replace('\\','/')
			audio_list.append(path)
			file_num += 1

#start to handle
for a in  xrange(0,len(audio_list)):#
	start = time.time()
	print audio_list[a]
	print Fana(audio_list[a]).stereo_start()
	print "Finished time: %.3f"%(time.time()-start)
	print " "
del Fana