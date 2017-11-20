#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time
ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'

def getCurrentTime():
    currentTime = time.strftime(ISOTIMEFORMAT, time.localtime())
    return currentTime
