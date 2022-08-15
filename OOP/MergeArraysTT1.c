#include<stdio.h>
#include<stdlib.h>
#define MAX 20

void main()
{
    int i, j, k = 0, found = 0;
    int arr1[] = {1, 2, 3, 4}, arr2[] = {4, 2, 7, 6};
    int arr3[MAX];

    //making first array go into the merged array
    for(i = 0; i < 4; i++) 
    {
        for(j = 0; j < k; j++)
            if(arr3[j] == arr1[i])
                found = 1;
        
        if(found != 1)    //for no repetition, if not found then only add the current element of arr1
            arr3[k++] = arr1[i];
        found = 0;        //reset the found flag
    }

    //making second array go into the merged array
    for(i = 0; i < 4; i++) 
    {
        for(j = 0; j < k; j++)
            if(arr3[j] == arr2[i])
                found = 1;
        
        if(found != 1) 
            arr3[k++] = arr2[i];
        found = 0;
    }

    //final answer
    for(i = 0; i < k; i++)
        printf("%d ", arr3[i]);
}