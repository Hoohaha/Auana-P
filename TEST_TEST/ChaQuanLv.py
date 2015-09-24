import os,time,sys
__PATH__ = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
sys.path.append(os.path.dirname(__PATH__))
from auana import *
# search .wav file


def test(dir_audio0):

	st  = Storage()

	File_num = 0
	NUM = 0
	NUMM = 0
	SUM = 0

	ab = time.clock()
	for parent, dirnames, filenames in os.walk(dir_audio0):
		for filename in filenames:
			portion = os.path.splitext(filename)

			if portion[1] == '.wav':
				path = os.path.join(parent, filename)
				path = path.replace('\\','/')

				File_num += 1
				w = st.Open(path)
				filename = w.filename
				res = w.recognize(Fast=False)

				if res[0] is not None:
					SUM += res[1]
					NUMM += 1
					if res[0] == filename:
						# print path," ","Y"
						NUM += 1


	print "Time: %s"%(time.clock()-ab)
	print "Success: %d  Total: %d    ZHUNQUEPercent: %f  CHAQUAN: %f  ACCMEAN:%f"%(NUM, File_num, float(NUM)/File_num, float(NUMM)/File_num,float(SUM)/NUM)

dir = "C:/MUSIC.NOISE/"
noise = [5,10,15,20,25,30,35,40]
for i in noise:
	print i
	p = dir + str(i)
	test(p)
