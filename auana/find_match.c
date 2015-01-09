#include "find_match.h"

/*!
 * @brief Hamming weight
 *
 * Get the count of "1" in a number.
 *
 */ 
int hamming_weight(uint32 x)  
{  
	const uint32 m1  = 0x55555555; //binary: 0101...  	
	const uint32 m2  = 0x33333333; //binary: 00110011..  
	const uint32 m4  = 0x0f0f0f0f; //binary:  4 zeros,  4 ones ...
	const uint32 h01 = 0x01010101; //the sum of 256 to the power of 0,1,2,3...    

    x -= (x >> 1) & m1;             //put count of each 2 bits into those 2 bits  
    x = (x & m2) + ((x >> 2) & m2); //put count of each 4 bits into those 4 bits   
    x = (x + (x >> 4)) & m4;        //put count of each 8 bits into those 8 bits   
    return (x * h01)>>24;           //returns left 8 bits of x + (x<<8) + (x<<16) + (x<<24) + ...
}

/*!
 * @brief Find the samilar file
 *
 * Compute the target and source files distcance, 
 * and give the percentage of same part.
 *
 * @param *tData: target file Data
 *        *sData: source file Data
 *        tlen: tData length
 *        slen: sData length
 *        wsize: How many data need to search in a cycle.
 *        offset: window move.
 */
float find_match(uint32 *tData,uint32 *sData, int tlen, int slen, int wsize, short offset)
{
	short _offset=1,temp=0,confidence=0;
	register int n=0,i=0,index=0;
	int max_index=0, next_begain=0;
	int dismin=0, dis=0, min_seq=0, min_seq0=0;

	const uint32 m1  = 0x55555555; //binary: 0101...  	
	const uint32 m2  = 0x33333333; //binary: 00110011..  
	const uint32 m4  = 0x0f0f0f0f; //binary:  4 zeros,  4 ones ...
	const uint32 h01 = 0x01010101; //the sum of 256 to the power of 0,1,2,3... 
	uint32 x;

	int Threshold, dw_limit, up_limit;
	Threshold = (int)((wsize<<5)*0.29);
	dw_limit = wsize-2;
	up_limit = wsize+2;
	max_index = slen - wsize;

	// printf(">>>>>>>>>>>>>>>>>%d  %d  %d %d\n",wsize,slen,dw_limit,up_limit);//For Debug

	for(i=0; i<(tlen/wsize); i++)
	{
		dismin   = Threshold;
		min_seq0 = min_seq;

		for(index = next_begain; index<max_index; index += _offset)
		{	
			//compute the distance of two buffer
			dis = 0;
			for(n=0;n<wsize;n++)
			{
				x = tData[wsize*i + n] ^ sData[wsize+index+n];
				/*hamming weight*/
				x -= (x >> 1) & m1;             //put count of each 2 bits into those 2 bits  
    			x = (x & m2) + ((x >> 2) & m2); //put count of each 4 bits into those 4 bits   
    			x = (x + (x >> 4)) & m4;        //put count of each 8 bits into those 8 bits   
    			x = (x * h01)>>24;              //returns left 8 bits of x + (x<<8) + (x<<16) + (x<<24)
    			dis += x;
				// dis += hamming_weight(tData[wsize*i + n] ^ sData[wsize+index+n]);
				if (dis > dismin) break;
			}

			//get min distance
			if (dis < dismin)
			{
				dismin  = dis;
				min_seq = index;
				if (wsize>10  && dismin<=70) break;
			}
		}

		temp = min_seq-min_seq0;
		
		if ((dismin<Threshold) && temp>=dw_limit && temp<=up_limit)
		{
			// printf("  a:%d  slen; %d  dismin: %d  minseq: %d, minseq0: %d\n",i,slen,dismin,min_seq,min_seq0);//For Debug
			confidence += 1;
			next_begain = min_seq;
			_offset = 1;
		}
		if (confidence > 3)
			_offset = offset;

		if (i>15 && confidence < 3)break;//stop find
	}

	if (confidence <= 1)
		return 0;

	return ((float)(confidence))/(tlen/wsize-1);
}

//For test
// int main()
// {	int i = 0,len=2;
// 	long n = 0;
// 	// float aaa=0;
// 	// uint32 tdata[5]={1,2,3,4,0};
// 	// uint32 sdata[5]={1,2,3,4,0};
// 	// aaa = find_match(tdata,sdata,5,5,len);
// 	// printf("confidence:%f\n",aaa);
// 	// printf ("res:%d\n",n);
// 	uint32 m=0;
// 	n = 5;
// 	while(n)
// 	{
// 	scanf("%d",&m);
// 	printf("input value%d\n",m);
// 	i = hamming_weight(m);
// 	printf("res: %d\n",i);
// 		n -= 1;
// 	}

// }