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
tim4 = pyb.Timer(4, prescaler=1, period=65535)

#PINC6; PINC7; Timer 8
pinC6 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.IN)
pinC7 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.IN)
tim8 = pyb.Timer(8, prescaler=1, period=65535)

motor = MotorDriver()				#creates object of class MotorDriver
enc = Encoder(pinC6,pinC7,tim8)		#creates object of class Encoder
control = Controller()				#creates object of class Controller


while True:
    x = input()
    theta_ref = control.set_point(x)
    y = input()
    K_p = control.control_gain(y)
    time = []
    position =[]
    ref_time = utime.ticks_ms()

    for i in range(2000):              # of iterations
        utime.sleep_ms(10)
        now = utime.ticks_ms()
        delta_time = now - ref_time
        time.append(delta_time)
        enc.read()
        theta_measured = enc.position
        position.append(theta_measured)
        control.closed_loop(theta_measured,theta_ref,K_p)
        level = control.a_star
        motor.set_duty_cycle(level)
    print(time)
    print(position)
    level = 0
    motor.set_duty_cycle(level)
    enc.zero()
    
    
    
    