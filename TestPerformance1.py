from auana import Fana, Preprocess
import os,time
current_directory = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')

# search .wav file
dir_audio0 = "E:/sample"


File_num = 0
NUM = 0

ab = time.clock()
for parent, dirnames, filenames in os.walk(dir_audio0):
	for filename in filenames:
		portion = os.path.splitext(filename)

		if portion[1] == '.wav'and (211 <= int(portion[0]) <= 215):
			path = os.path.join(parent, filename)
			path = path.replace('\\','/')
			File_num += 1
			res = Fana(path).stereo_start()
			if res[0] == "p1.wav" or res[0] == "p2.wav" or res[0] == "p3.wav" or res[0] == "p4.wav":
				NUM += 1
			else:
				print "P:%s  MName: %s   Acc: %s"%(path,res[0],res[1])

print "Time: %s"%(time.time()-ab)
print "Success: %d  Total: %d    Percent: %f"%(NUM,File_num, NUM/File_num)