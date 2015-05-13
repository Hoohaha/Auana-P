import os,time,sys
__PATH__ = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
sys.path.append(os.path.dirname(__PATH__))
from auana import Auana,Fana
# search .wav file
dir_audio0 = "E:/sample"


File_num = 0
NUM = 0
a = Auana()
ab = time.clock()
for parent, dirnames, filenames in os.walk(dir_audio0):
	for filename in filenames:
		portion = os.path.splitext(filename)

		if portion[1] == '.wav'and (111 <= int(portion[0]) <= 126):
			path = os.path.join(parent, filename)
			path = path.replace('\\','/')
			File_num += 1
			res = Fana(a,path).recognize()
			if res[0] == "Come And Get Your Love.wav":
				NUM += 1
			else:
				print "P:%s  MName: %s   Acc: %s"%(path,res[0],res[1])

print "Time: %s"%(time.time()-ab)
print "Success: %d  Total: %d    Percent: %f"%(NUM,File_num, NUM/File_num)