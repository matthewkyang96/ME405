# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pyb

#tim = pyb.Timer(8, prescaler=1, period=65535)
#pinC6 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.IN)
#pinC7 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.IN)
#ch1 = tim.channel (1, pyb.Timer.ENC_AB, pin = pinC6)
#ch2 = tim.channel (2, pyb.Timer.ENC_AB, pin = pinC7)

#pinB6 = pyb.Pin (pyb.Pin.board.PB6, pyb.Pin.IN)
#pinB7 = pyb.Pin (pyb.Pin.board.PB7, pyb.Pin.IN)
#tim2 = pyb.Timer(4, prescaler=1, period=65535)
#ch1a = tim2.channel (1, pyb.Timer.ENC_AB, pin = pinB6)
#ch2a = tim2.channel (2, pyb.Timer.ENC_AB, pin = pinB7)

class ED:
    

    def __init__(self):
        '''Set up a timer/counter in quadrature decoding mode to read an 
        optical encoder.'''
        tim = pyb.Timer(8, prescaler=1, period=65535)
        pinC6 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.IN)
        pinC7 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.IN)
        ch1 = tim.channel (1, pyb.Timer.ENC_AB, pin = pinC6)
        ch2 = tim.channel (2, pyb.Timer.ENC_AB, pin = pinC7)
        
        print ('Creating a motor driver')
        
    def read(self):
        '''update and return the encoder position using the number in the
        encoder counter.'''
        self.tim = pyb.Timer(8, prescaler=1, period=65535)
#        pinC6 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.IN)
#        pinC7 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.IN)
#        ch1 = tim.channel (1, pyb.Timer.ENC_AB, pin = pinC6)
#        ch2 = tim.channel (2, pyb.Timer.ENC_AB, pin = pinC7)
        print (self.tim.counter())
        
    def zero(self):
        '''Set the encoder counter to zero.'''
        tim = pyb.Timer(8, prescaler=0, period=65535)
        pinC6 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.IN)
        pinC7 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.IN)
        ch1 = tim.channel (1, pyb.Timer.ENC_AB, pin = pinC6)
        ch2 = tim.channel (2, pyb.Timer.ENC_AB, pin = pinC7)
    