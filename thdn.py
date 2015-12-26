from auana import Open

#open a wave file
wf = Open("C:\Users\solof\Desktop/audio12k16S.wav")


#ch: channel(0 or 1)     base_frq: sine frequency  t:(second)
#return: thd+n value(100%)
print wf.get_thdn(ch=0,base_frq=220,t=1)