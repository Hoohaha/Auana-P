#include "Compare.h"

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
 *		  num_win: numbers of window
 */
struct match_info Compare(uint32 *tData, uint32 *sData, int tlen, int slen, struct compare_parameters con)
{
	const uint32 m1  = 0x55555555; //binary: 0101...  	
	const uint32 m2  = 0x33333333; //binary: 00110011..  
	const uint32 m4  = 0x0f0f0f0f; //binary:  4 zeros,  4 ones ...
	const uint32 h01 = 0x01010101; //the sum of 256 to the power of 0,1,2,3... 


	uint32 x=0;

	register int n=0,i=0,index=0;

	struct match_info m = {0,0};

	short wsize     = con.window_size;
	short threshold = con.threshold;
	short offset    = con.offset;
	short num_win   = con.num_win;

	int dw_limit = wsize-1;
	int up_limit = wsize+2;

	int max_index   = slen-wsize;
	int next_begain = 0;

	short temp=0, confidence=0;
	int dismin=0, dis =0, min_seq=0, min_seq0=0;

	// printf(">>>>>>>>>>>>>>>>>%d  %d  %d %d\n",wsize,slen,dw_limit,up_limit);//For Debug

	for(i=0; i<num_win; i++)//target file
	{
		dismin   = threshold;
		min_seq0 = min_seq;

		for(index = next_begain; index<max_index; index += offset)//source file
		{	
			//compute the distance of two buffer
			dis = 0;
			for(n=0;n<wsize;n++)
			{
				x = tData[wsize*i + n] ^ sData[index+n];
				/*hamming weight*/
				x -= (x >> 1) & m1;             //put count of each 2 bits into those 2 bits  
    			x = (x & m2) + ((x >> 2) & m2); //put count of each 4 bits into those 4 bits   
    			x = (x + (x >> 4)) & m4;        //put count of each 8 bits into those 8 bits   
    			x = (x * h01)>>24;              //returns left 8 bits of x + (x<<8) + (x<<16) + (x<<24)
    			dis += x;
			}

			//get min distance and the index in source data
			if (dis < dismin)
			{
				dismin  = dis;
				min_seq = index;
			}
		}

		temp = min_seq-min_seq0;
		
		if (dismin<threshold && temp>=dw_limit && temp<=up_limit)
		{
			// printf("  a:%d  slen; %d  dismin: %d  minseq: %d, minseq0: %d\n",i,slen,dismin,min_seq,min_seq0);//For Debug
			confidence ++;
			next_begain = min_seq;
		}

		if (i>20 && confidence < 3)
			return m;//stop search
	}

	if(confidence<1)
	{
		m.accuarcy = 0;
		return m;
	}
	else
	{
		m.accuarcy = ((float)(confidence+1))/num_win;
		if (m.accuarcy < 0.1)
		{
			m.accuarcy = 0;
		}
		m.position = next_begain+1;
		return m;
	}
}


//For test
// int main()
// {	int i = 0,len=2;
// 	long n = 0;
// 	struct match_info a;
// 	uint32 tdata[6]={395465836,843686630, 740887446, 631982742, 631855766,631982742};
// 	uint32 sdata[6]={395465836,843686630, 740887446, 631982742, 631855766,631982742};;
// 	a = Compare(tdata,sdata,6,6,2,1,3);
// 	printf("confidence:%f\n",a.accuarcy);
// 	printf ("res:%d\n",n);
// 	// uint32 m=0;
// 	// n = 5;
// 	// while(n)
// 	// {
// 	// scanf("%d",&m);
// 	// printf("input value%d\n",m);
// 	// i = hamming_weight(m);
// 	// printf("res: %d\n",i);
// 	// 	n -= 1;
// 	// }

// }
