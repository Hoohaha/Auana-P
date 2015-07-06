import os,time,sys
__PATH__ = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
sys.path.append(os.path.dirname(__PATH__))
from auana import *
# search .wav file
dir_audio0 = "E:/iar/Debug"

st  = Storage()

File_num = 0
NUM = 0

ab = time.clock()
for parent, dirnames, filenames in os.walk(dir_audio0):
	for filename in filenames:
		portion = os.path.splitext(filename)

		if portion[1] == '.wav'and (111 <= int(portion[0]) <= 125):
			path = os.path.join(parent, filename)
			path = path.replace('\\','/')
			File_num += 1
			res = st.openf(path).recognize(Fast=False)

			if res[0] == "p1.wav" or res[0] == "p2.wav" or res[0] == "p3.wav" or res[0] == "p4.wav" or res[0] == "source1.wav":
				NUM += 1
			else:
				print "P:%s  MName: %s   Acc: %s"%(path,res[0],res[1])

print "Time: %s"%(time.time()-ab)
print "Success: %d  Total: %d    Percent: %f"%(NUM, File_num, float(NUM)/File_num)