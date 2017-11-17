#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
def createVoltageTxtFromNone():
    with open('./voltage.txt','w') as f:
        for i in range(32 * 32):
            f.write(str(i+32*22) + ' ' + str(0.0) + '\n')
        for i in range(32 * 12):
            f.write(str(i) + ' ' + str(round(random.uniform(0, 3.3), 1)) + '\n')
        for i in range(32 * 32):
            f.write(str(i+32*22) + ' ' + str(0.0) + '\n')

# def createArrayTxtFromArray(array):
#     with open('./array.txt','w') as f:
#         f.write(str(array))
