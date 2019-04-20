# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pyb
from EncoderDriver import Encoder
from motordriver import MotorDriver
from Controller import Controller
import utime

##  ----DEFINED VARIABLES--- ##
#PINB6; PINB7; Timer 4
pinB6 = pyb.Pin (pyb.Pin.board.PB6, pyb.Pin.IN)
pinB7 = pyb.Pin (pyb.Pin.board.PB7, pyb.Pin.IN)
tim4 = pyb.Timer(4, prescaler=0, period=65535)

#PINC6; PINC7; Timer 8
pinC6 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.IN)
pinC7 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.IN)
tim8 = pyb.Timer(8, prescaler=0, period=65535)

motor = MotorDriver()				#creates object of class MotorDriver
enc = Encoder(pinC6,pinC7,tim8)		#creates object of class Encoder
control = Controller()				#creates object of class Controller

theta_ref = control.set_point()
K_p = control.control_gain()

for i in range(20000):              # of iterations
    #utime.sleep_ms(100)
    enc.read()
    theta_measured = enc.position
    loop.closed_loop(theta_measured,theta_ref,K_p)
    level = loop.a_star
    print(level)
    print(theta_measured)
    motor.set_duty_cycle(level)
level = 0
moe.set_duty_cycle(level)
    
    
    