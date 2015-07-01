from auana import frequency, Load_file
import os

path = "C:/Audio_SAI/twrk64f120m/armgcc/Debug"

def files():
	for parent, dirnames, filenames in os.walk(path):
		for filename in filenames:
			if os.path.splitext(filename)[1] == '.wav':

				filepath = os.path.join(parent, filename).replace('\\','/')

				data, framerate, nch = Load_file(filepath)

				c = frequency.compute_thd(data[0], framerate)
				if c<= 20:
					print filepath,c,"PASS"
				else:
					print filepath,c,"FAIL"


def file():
	data, framerate, nch = Load_file(path+"/111.wav")
	c = frequency.compute_thd(data[0], framerate)
	print c

files()