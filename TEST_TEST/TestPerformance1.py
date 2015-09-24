import os,time,sys
__PATH__ = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
sys.path.append(os.path.dirname(__PATH__))
from auana import *
# search .wav file
dir_audio0 = "C:\MUSIC.DIF.LENGTH"

st  = Storage()

File_num = 0
NUM = 0
NUMM = 0

files = ["1","3","5","10","20","30","40","50","60"]


path = "C:\MUSIC.DIF.LENGTH"
for f in files:
	p = path +"/"+ f + ".wav"

	s = time.time()
	w = st.Open(p)
	filename = w.filename
	res = w.recognize(Fast=False)
	e = time.time()
	print e-s