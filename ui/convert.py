#!/usr/bin/python3
# -*- coding: utf-8 -*-
def grayToRGB(gray):
    if gray >= 0 and gray <= 85:
        B = int(255 / 85 * gray)
    elif gray >= 85 and gray <= 170:
        B = int(510 - 510 / 170 * gray)
    else:
        B = 0

    if gray <= 85:
        G = 0
    elif gray >= 85 and gray <= 170:
        G = int(-255 + 510 / 170 * gray)
    elif gray >= 170 and gray <= 255:
        G = int(765 - 765 / 255 * gray)

    if gray <= 170:
        R = 0
    else:
        R = int(-510 + 510 / 170 * gray)
    return (B, G, R)


with open('./temp.txt','r') as f:
    #等待接受到开头
    while True:
        text=f.readline()
        print(text)
        if text[0]=='0':
            break
    #继续接受
    voltage=float(text.split(' ')[1])
    #
    # while True:
    #     text=f.readline()
    #     print(text)
    #     if text[0]=='0':
    #         break


        
