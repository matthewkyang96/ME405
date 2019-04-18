# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

''' @file EncoderDriver.py '''

import pyb
''' Imports pyboard library'''


class Encoder(): 
    ''' This class initializes the encoder in a DC motor with specified
    input pins and timer for the ME405 board.'''

    def __init__(self,input_pin1,input_pin2,input_timer):
        '''Set up a timer/counter in quadrature decoding mode to read an 
        optical encoder. User must specify which pin and timers the 
        which the encoder is connected to.  To declare which pins you are 
        using, use the following code (NUCLEO-L476RG):
            
        For pin C6 and C7 and timer 8  
            tim8 = pyb.Timer(8, prescaler=1, period=65535)
            pinC6 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.IN)
            pinC7 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.IN)
            
        For pin B6 and B7 and timer 4
            pinB6 = pyb.Pin (pyb.Pin.board.PB6, pyb.Pin.IN)
            pinB7 = pyb.Pin (pyb.Pin.board.PB7, pyb.Pin.IN)
            tim4 = pyb.Timer(4, prescaler=1, period=65535)
        
            
        @param input_pin1 pin that connects first input from the encoder to the
        microcontroller.
        @param input_pin2 pin that connects second input from the encoder to 
        the microcontroller.
        @param input_timer sets up timer for timer channels'''
        self.timer= input_timer #creates a shared variable in methods among 
                                #encoder class
        self.ch1 = input_timer.channel (1, pyb.Timer.ENC_AB, pin = input_pin1)
                                #creates a timer channel in encoder counting 
                                #mode in timer channel 1
        self.ch2 = input_timer.channel (2, pyb.Timer.ENC_AB, pin = input_pin2)
                                #creates a timer channel in encoder counting 
                                #mode in timer channel 2
        self.position = int(0)  #initializes position into type interger and
                                #sets it at zero
        self.theta_old = 0      #initizles shared variable theta old at zero
        
        print ('Creating a motor driver') #prints specified message to command line
        
    def read(self):
        '''update and return the encoder position using the number in the
        encoder counter. Do this by taking the difference of the new position 
        from the old position.  The read function takes into account the over
        flows and underflow of the encoder. '''
        theta_new = self.timer.counter()    #sets variable theta_new to the position of the encoder
        delta = theta_new - self.theta_old  #takes the difference of the new position from the old position.
        
        if delta < -32767                    #if true execute the code below
            delta += 65536                  #add 65535 to delta
       
        elif delta >32767:                  #if true execute the code below
            delta -= 65536                  #add 65535 to delta
           
        else:                               #if true execute the code below
          pass                              #continue through code
              
        self.position += delta              #add the value of delta to position
        self.theta_old = theta_new          #set theta old to theta new
        
        return self.position                #returns the value from the method
    
    def zero(self):
        '''Set the encoder counter to zero.Reinitializes share variables
        position, theta_old and timer.counter() to zero'''
        self.position = int(0)         #sets position to zero
        self.theta_old = int(0)        #sets theta_old to zero
        self.timer.counter(0)          #sets timer.counter() to zero
        return self.position           #returns the value from the method