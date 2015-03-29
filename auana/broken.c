#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define bool char
#define true 1
#define false 0

#define DETECT_WIN 256U
#define THRESHOLD 1000U
#define VAR_CMP 60U
/*!
 * @brief Broken Frame Detection
 *
 * Compute and find the Broken-Frame, 
 * and return the place in file.
 *
 * @param *tData: target file Data
 *        *sData: source file Data
 *        tlen: tData length
 *        slen: sData length
 *        wsize: How many data need to search in a cycle.
 *        offset: window move.
 */
int broken_frame(int16_t *pBuffer, uint32_t length, float *resBuffer, int framerate)
{
    register uint32_t i=0, index=0, utemp=0;
    uint32_t var=0, var0=0, var1=0, var2=0;// var
    int16_t avg=0;//average
    
    uint16_t count=0, NUM=0;
    float timeplace=0;
    bool flag = false;
    uint16_t size = length/DETECT_WIN;
    char chn;
    for(chn=0;chn<2;chn)
    for(index=1; index<= size; index++)
    {
        /*Caculate the average value*/
        for(i=0;i<DETECT_WIN;i ++)
        {
            avg += pBuffer[(index-1)*DETECT_WIN+i];
        }
        avg = avg/DETECT_WIN;
        /*Caculate the var value*/
        for(i=0;i<DETECT_WIN;i++)
        {
            utemp = abs(pBuffer[(index-1)*DETECT_WIN+i]-avg);
            var += utemp*utemp;
        }
        var = var/DETECT_WIN;

        /*Update var. Everytime the var2 is the latest vale*/
        utemp = var2;
        var2 = var;
        var0 = var1;
        var1 = utemp;

        if(!flag)
        {
             /*Detect up edge*/
            if((var2 < VAR_CMP)&&((int32_t)(var0-var2)>THRESHOLD)&&((int32_t)(var1-var2)>THRESHOLD))
            {
                flag = true;
                timeplace=((index-1)*DETECT_WIN)/(float)framerate;
            }

        }
        else
        {
            /*Detect down edge*/
            if((var0 < VAR_CMP)&&((int32_t)(var2-var0)>THRESHOLD)&&((int32_t)(var1-var0)>THRESHOLD))
            {
                resBuffer[NUM] = timeplace;
                NUM ++; 
                flag = false;
                count = 0;
            }
            else if(count>600)//if not detect a fall edge after 4seconds, the falg of up edge will be cleared.
            {
                flag = false;
                count = 0;
            }
            count++;
        }
    }
    return NUM;
}