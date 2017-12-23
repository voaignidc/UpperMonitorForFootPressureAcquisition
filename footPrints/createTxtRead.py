#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
with open('./txtRead.txt','w') as f:
    for i in range(1408):
        f.write(str(round(random.uniform(0, 3.30), 2)) + ', ')


# def createArrayTxtFromArray(array):
#     with open('./array.txt','w') as f:
#         f.write(str(array))
