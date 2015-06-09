#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


struct match_info
{
	float accuarcy;
	int position;
	/* data */
};
struct compare_parameters
{
	short window_size;
	short offset;
	short threshold;
	short num_win;
};

/*
 * Author: Haley Guo, Date: 2015.1.8
 * version:0.2
 *
 */
typedef unsigned __int32 uint32;  //assume this gives 64-bits  


/*!
 * @brief Hamming weight
 *
 * Get the count of "1" in a number.
 *
 */ 
int hamming_weight(uint32 x);

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
struct match_info Compare(uint32 *tData,uint32 *sData, int tlen, int slen, struct compare_parameters con);
