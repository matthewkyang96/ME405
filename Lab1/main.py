# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pyb
pinB6 = pyb.Pin (pyb.Pin.board.PB6, pyb.Pin.IN)
pinB7 = pyb.Pin (pyb.Pin.board.PB7, pyb.Pin.IN)
pinC6 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.IN)
pinC7 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.IN)
tim8 = pyb.Timer(8, prescaler=0, period=65535)
tim4 = pyb.Timer(4, prescaler=0, period=65535)
from EncoderDriver import Encoder
enc = Encoder(pinC6,pinC7,tim8)