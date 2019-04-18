## @file MotorDriver2.py
#  Brief doc for MotorDriver2.py
#
#  Detailed doc for MotorDriver2.py 
#
#  @author Bryson Chan and Matthew Yang
#
#  @copyright License Info
#
#  @date April 18, 2019
import pyb
class MotorDriver2:
    ''' This class implements a motor driver for the
    ME405 board. '''
    
    def __init__ (self):
        ''' Creates a motor driver by initializing GPIO
        pins and turning the motor off for safety. '''
        pinA10 = pyb.Pin (pyb.Pin.board.PA10, pyb.Pin.OUT_PP) #defines encoder pin
        pinA10.high () #set encoder pin A to on
        pinB4 = pyb.Pin (pyb.Pin.board.PB4, pyb.Pin.OUT_PP) #defines pin IN1A
        tim3 = pyb.Timer (3, freq=20000) #defines timer channel 3 to 20000Hz
        pinB5 = pyb.Pin (pyb.Pin.board.PB5, pyb.Pin.OUT_PP) #defines pin IN2A
        ch2m = tim3.channel (2, pyb.Timer.PWM, pin=pinB5) #defines Channel 2
        ch1m = tim3.channel (1, pyb.Timer.PWM, pin=pinB4) #defines Channel 1
        ch1m.pulse_width_percent (0) #initializes motor to off
        ch2m.pulse_width_percent (0) #initializes motor to off
        print ('Creating a motor driver') #prints message

    def set_duty_cycle (self, level):
        ''' This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level A signed integer holding the duty
        cycle of the voltage sent to the motor '''
#        pinA10 = pyb.Pin (pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
#        pinA10.high ()
        pinB4 = pyb.Pin (pyb.Pin.board.PB4, pyb.Pin.OUT_PP) #defines pin IN1A
        tim3 = pyb.Timer (3, freq=20000) #defines timer 3 to 20000Hz
        pinB5 = pyb.Pin (pyb.Pin.board.PB5, pyb.Pin.OUT_PP) #defines pin IN2A
        ch2m = tim3.channel (2, pyb.Timer.PWM, pin=pinB5) #defines Channel 2
        ch1m = tim3.channel (1, pyb.Timer.PWM, pin=pinB4) #defines Channel 1
        if level < 0: #if duty cycle is negative rotate counter clockwise
            ch1m.pulse_width_percent (-level)
            ch2m.pulse_width_percent (0)
        else: #if duty cycle is positive rotate clockwise
            ch1m.pulse_width_percent (0)
            ch2m.pulse_width_percent (level)
            

        #print ('Setting duty cycle to ' + str (level)) #print message