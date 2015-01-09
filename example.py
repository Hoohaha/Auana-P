from auana import Fana, Preprocess
import os,time

'''*************************************Function Example**********************************'''
#get the directory
current_directory = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')


'''*****************Pre Process*****************'''
p = Preprocess()

#hear the file and memory it
p.hear(current_directory+"/sample/ding.wav")

p.hear(current_directory+"/sample/source1.wav")

p.hear(current_directory+"/sample/piano.wav")

#show the file which is saved
p.show()


'''=========================File Analysis==========================='''

start = time.clock()
res = Fana("E:/Come And Get Your Love.wav").stereo_start()
print "Match-File:%30s accuracy:%2.1f volume:%3.1f time-cost:%3.2f"%(res[0],res[2],res[1],time.clock()-start)
print " "


#sample test
dir_audio = current_directory+"/sample"
for parent, dirnames, filenames in os.walk(dir_audio):
	for filename in filenames:
		if os.path.splitext(filename)[1] == '.wav':
			filepath = os.path.join(parent, filename).replace('\\','/')
			start = time.clock()
			res = Fana(filepath).stereo_start()#File analysis
			print (filepath, res,time.clock()-start)