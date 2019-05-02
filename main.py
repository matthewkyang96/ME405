# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pyb
import task_share
 
timing = pyb.Timer(1,freq= 1000)
pinA4 =pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT)
pinA5 =pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.IN)
adc = pyb.ADC(pinA5)
Q = task_share.Queue('i',1000,thread_protect=True,overwrite=False)

def interrupt(source):
    value = adc.read()
    Q.put(value)
    
pinA4.low()
input('pressed button to start')    
timing.callback(interrupt)
while True:
    pinA4.high()
    if Q.full() == True:
        while Q.num_in() > 0:
            print(Q.get(in_ISR=True))
           
    
        
    