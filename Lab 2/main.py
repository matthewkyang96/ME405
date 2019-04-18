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
tim8 = pyb.Timer(8, prescaler=1, period=65535)
tim4 = pyb.Timer(4, prescaler=1, period=65535)
from EncoderDriver import Encoder
enc = Encoder(pinC6,pinC7,tim8)

pinA10 = pyb.Pin (pyb.Pin.board.PA10, pyb.Pin.OUT_PP) #defines encoder pin
pinA10.high () #set encoder pin A to on
pinB4 = pyb.Pin (pyb.Pin.board.PB4, pyb.Pin.OUT_PP) #defines pin IN1A
tim3 = pyb.Timer (3, freq=20000) #defines timer channel 3 to 20000Hz
pinB5 = pyb.Pin (pyb.Pin.board.PB5, pyb.Pin.OUT_PP) #defines pin IN2A
ch2m = tim3.channel (2, pyb.Timer.PWM, pin=pinB5) #defines Channel 2
ch1m = tim3.channel (1, pyb.Timer.PWM, pin=pinB4) #defines Channel 1
ch1m.pulse_width_percent (0) #initializes motor to off
ch2m.pulse_width_percent (0) #initializes motor to off
from motordriver2 import MotorDriver2
moe = MotorDriver2()


from Controller import Controller
loop = Controller()
import utime
for i in range(20000):
    #utime.sleep_ms(100)
    enc.read()
    theta_ref = 60000
    theta_measured = enc.position
    #enc.position = theta_measured
    loop.cloop(theta_measured,theta_ref)
    level = loop.a_s
    print(loop.a_s)
    print(enc.read())
    moe.set_duty_cycle(level)
level = 0
moe.set_duty_cycle(level)
    
    
    