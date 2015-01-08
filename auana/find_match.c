#include "find_match.h"
 
int hamming_weight(uint32 x)  
{  
	const uint32 m1  = 0x55555555; //binary: 0101...  	
	const uint32 m2  = 0x33333333; //binary: 00110011..  
	const uint32 m4  = 0x0f0f0f0f; //binary:  4 zeros,  4 ones ...
	const uint32 h01 = 0x01010101; //the sum of 256 to the power of 0,1,2,3...    

    x -= (x >> 1) & m1;             //put count of each 2 bits into those 2 bits  
    x = (x & m2) + ((x >> 2) & m2); //put count of each 4 bits into those 4 bits   
    x = (x + (x >> 4)) & m4;        //put count of each 8 bits into those 8 bits   
    return (x * h01)>>24;  //returns left 8 bits of x + (x<<8) + (x<<16) + (x<<24) + ...
}

long distance(uint32 *tData,uint32 *sData, int length)
{
	int i;
	long sum=0;
	for(i=0;i<length;i++)
		sum += hamming_weight(tData[i] ^ sData[i]);
	return sum;
}

float find_match(uint32 *tData,uint32 *sData, int tlen, int slen, int wsize, int offset)
{
	int i=0, index=0, dis=0,confidence = 0, max_index = 0, dismin = 0, min_seq=0, min_seq0 = 0,temp=0,next_begain=0; 
	
	float Threshold = wsize*32*0.3;
	int dw_limit = wsize-2, up_limit = wsize +2;

	max_index = slen - wsize;

	uint32 *tbuffer = (uint32 *)malloc(wsize*sizeof(uint32));
	uint32 *sbuffer = (uint32 *)malloc(wsize*sizeof(uint32));

	memset(tbuffer,0,wsize*sizeof(uint32));
	memset(sbuffer,0,wsize*sizeof(uint32));

	// printf(">>>>>>>>>>>>>>>>>%d  %d  %d %d\n",wsize,slen,dw_limit,up_limit);//For Debug

	for(i=0; i<(tlen/wsize); i++)
	{
		dismin = 300;
		min_seq0 = min_seq;
		memcpy(tbuffer, tData+wsize*i, wsize*sizeof(uint32));

		for(index = next_begain; index<max_index; index += offset)
		{	
			memcpy(sbuffer, sData+index, wsize*sizeof(uint32));
			dis = distance(tbuffer,sbuffer,wsize);
			if (dis < dismin)
			{
				dismin = dis;
				min_seq = index;
				if (wsize>10  && dismin <= 80)
					break;
			}
		}

		// printf("  dismin: %d  minseq: %d, minseq0: %d\n",dismin,min_seq,min_seq0);//For Debug
		temp = min_seq-min_seq0;
		// printf("  a:%d  slen; %d  dismin: %d  minseq: %d, minseq0: %d\n",i,slen,dismin,min_seq,min_seq0);//For Debug
		if ((dismin < Threshold) && temp >=dw_limit && temp <= up_limit)
		{
			confidence += 1;
			next_begain = min_seq;
		}

		if (i>15 && confidence < 3)
			break;
	}
	if (confidence <= 1)
		return 0;
	free(tbuffer);
	free(sbuffer);
	return ((float)(confidence))/(tlen/wsize);
	
}


int main()
{	int i = 0,len=2;
	long n = 0;
	// float aaa=0;
	// uint32 tdata[5]={1,2,3,4,0};
	// uint32 sdata[5]={1,2,3,4,0};
	// aaa = find_match(tdata,sdata,5,5,len);
	// printf("confidence:%f\n",aaa);
	// printf ("res:%d\n",n);
	uint32 m=0;
	n = 5;
	while(n)
	{
	scanf("%d",&m);
	printf("input value%d\n",m);
	i = hamming_weight(m);
	printf("res: %d\n",i);
		n -= 1;
	}

}