from auana import FileAnalysis
import os

dir_audio = 'C:/audio/twrk24f120m/kds/Debug'
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

print FileAnalysis("E:\FreeKV_demo/FreeKV_demo/auto_handle\sai_demo/audio_lib/source1.wav").stereo_start()
print FileAnalysis("E:\FreeKV_demo/FreeKV_demo/auto_handle\sai_demo/audio_lib/source2.wav").mono_start(0)
FileAnalysis("E:\FreeKV_demo/FreeKV_demo/auto_handle\sai_demo/audio_lib/source2.wav").save_fingerprint()
# for a in  xrange(0,len(audio_list)):#
# 	start = time.time()
# 	print audio_list[a]
# 	print auana(audio_list[a],False)
# 	print "Finished time: %4f"%(time.time()-start)
# 	print " "
