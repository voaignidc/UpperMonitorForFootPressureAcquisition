#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
with open('./temp.txt','w') as f:
    for i in range(32*44):
        f.write( str(i) + ' ' + str(round(random.uniform(0, 3.3), 1)) + '\n')
