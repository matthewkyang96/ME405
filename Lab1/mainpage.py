## @file mainpage.py
# @author Matthew Yang and Bryson Chan
# @mainpage
# @section Introduction
# This code measures where a motor is, and captures the code in a Python class.
# This code will prin in Doxygen, test ther code thoroughly to ensure that it is reliable, 
#and manage sets of source files using Mercurial revision control software.
# @section Purpose
# The drivers purpose is to set up an encoder for a motor.
# @section Usage
#The code used to create an object and use it entails:
#       For pin C6 and C7 and timer 8  
#            tim8 = pyb.Timer(8, prescaler=1, period=65535)
#            pinC6 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.IN)
#            pinC7 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.IN)
#            
#        For pin B6 and B7 and timer 4
#            pinB6 = pyb.Pin (pyb.Pin.board.PB6, pyb.Pin.IN)
#            pinB7 = pyb.Pin (pyb.Pin.board.PB7, pyb.Pin.IN)
#            tim4 = pyb.Timer(4, prescaler=1, period=65535)
# @section Testing
# The code was tested by spinning the motor and executing the read function
# to determine the location of the encoder reading.  The encoder accounted for
# the overflows when the position of the encoder passed 65535 as an overflow
# and -65535 as underflow.
# @section Bugs/Limitations If the clock is running at 20,000 Hz and the motor has 
#1000 counts per revolution the motor needs to spin at 655,340 revolutions per second.
# @section The location of source code at http://wind.calpoly.edu/hg/mecha11
