from ctypes import *

ham = cdll.LoadLibrary("hamming_weight.dll")
# ham.argtypes = c_int
# ham.restype = c_int 

a = ham.hamming_weight(c_int(4))
print a
