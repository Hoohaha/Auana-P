# from distutils.core import setup, Extension
  
# module1 = Extension('hamming_weight',
#                     sources = ['hamming_weight.c'])
  
# setup (name = 'hamming_weight',
#        version = '1.0',
#        description = 'This is a hamming_weight package',
#        ext_modules = [module1])
from distutils.core import setup, Extension
  
module1 = Extension('clip',
                    sources = ['clip.c'])
  
setup (name = 'clip',
       version = '1.0',
       description = 'This is a clip package',
       ext_modules = [module1])