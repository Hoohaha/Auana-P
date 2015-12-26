#include <stdio.h>
#include <math.h>



int main(void)
{
    float c_x=0, c_y=0, r=0;
    float distance=0, dis_max=0;
    int x_max, x_min, y_max, y_min;
    int x = 0, y=0, temp_x=0, temp_y=0;

    
    scanf("%f %f %f", &c_x, &c_y, &r);
    
    printf("%f %f %f\n",c_x, c_y, r);
    x_max = c_x+r;
    x_min = c_x-r;
    y_max = c_y+r;
    y_min = c_y-r;
    
    for(x=x_min; x<=x_max; x++)
    {
        for(y=y_min; y<=y_max; y++)
        {
            distance = sqrt((x-c_x)*(x-c_x) + (y-c_y)*(y-c_y));
            if ((distance<=r)&&(dis_max<distance))
                {
                    dis_max = distance;
                    temp_x = x;
                    temp_y = y;
                }
        }
        
    }
    printf("%d %d", temp_x, temp_y);
    
    
}