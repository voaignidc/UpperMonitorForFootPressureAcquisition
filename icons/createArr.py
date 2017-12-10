#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cv2
import numpy as np

def grayToBGR(gray, scale):
    if gray >= 0 and gray <= scale//4:
        B = 255
    elif gray >= scale//4 and gray <= scale//2:
        B = int(510 - 255 / (scale//4) * gray)
    else:
        B = 0
        
    if gray <= scale//4:
        G = int(255 / (scale//4) * gray)
    elif gray >= scale//4 and gray <= (scale//4)*3:
        G = 255
    else:
    # elif gray >= (scale//4)*3 and gray <= scale:
        G = int(1020 - 255 / (scale//4) * gray)
    
        
    if gray <= scale//2:
        R = 0
    elif gray >= scale//2 and gray <= (scale//4)*3:
        R = int(-510 + 255 / (scale//4) * gray)
    else:
        R = 255
    return (B, G, R)

#32 440   
    
arr = np.zeros((440,32,3), np.uint8)#440行32列，3通道
for i in range(4096):
    B,G,R = grayToBGR(i, 4096)
    
    row = 439 - 440*i//4096
    arr[row, 0:32, 2] = R#i行 32列   R通道赋值为255
    arr[row, 0:32, 1] = G
    arr[row, 0:32, 0] = B



cv2.imshow('arr',arr)
cv2.imwrite('arr2.png', arr)
cv2.waitKey(0)
cv2.destroyAllWindows()
