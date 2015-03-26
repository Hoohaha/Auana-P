from auana import Fana, Preprocess
import os,time

'''*************************************Function Example**********************************'''
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



# '''==================File Analysis==============='''


# #sample test
# sample_path = work_dir+"/sample"
# for parent, dirnames, filenames in os.walk(sample_path):
# 	for filename in filenames:
# 		if os.path.splitext(filename)[1] == '.wav':
# 			filepath = os.path.join(parent, filename).replace('\\','/')
# 			start = time.clock()
# 			res = Fana(filepath).stereo_start()#File analysis
# 			print (filepath, res,time.clock()-start)