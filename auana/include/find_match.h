#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned __int32 uint32;  //assume this gives 64-bits  



int hamming_weight(uint32 x);

long distance(uint32 *tData,uint32 *sData, int length);

float find_match(uint32 *tData,uint32 *sData, int tlen, int slen, int wsize, int offset);
