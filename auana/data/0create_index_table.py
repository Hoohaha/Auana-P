import cPickle as pickle 
table = {}
b = [] 
for i in xrange(65537):
	table[i] = b

cfile = open("INDEX_TABLE.pkl", 'w+')	
pickle.dump(table, cfile)
cfile.close()