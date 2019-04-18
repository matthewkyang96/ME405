## @file mainpage.py
#
#  @author Matthew Yang and Bryson Chan
#
#  @mainpage
#
#  @section Introduction
#  This code measures the position of the motor, and returns it as a value.
#  It will account for both overflow and underflow in either direction. The 
#  period of the timer module should be set at 65,535 to return accurate results. The user will 
#  define two input pins and a timer with two timer channels. When changing position and
#  executing the read method, the new location will be returned. The zero method will 
#  return the position counter back to zero.
#
#  @section Purpose
#  The drivers purpose is to set up an encoder for a motor.
#
#  @section Usage
#  The code used to create an object and use it entails:
#       
#        For pin C6 and C7 with timer 8  
#
#            tim8 = pyb.Timer(8, prescaler=1, period=65535)
#
#            pinC6 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.IN)
#
#            pinC7 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.IN)
#            
#        For pin B6 and B7 with timer 4
#
#            pinB6 = pyb.Pin (pyb.Pin.board.PB6, pyb.Pin.IN)
#
#            pinB7 = pyb.Pin (pyb.Pin.board.PB7, pyb.Pin.IN)
#
#            tim4 = pyb.Timer(4, prescaler=1, period=65535)
#
#  @section Testing
#  The code was tested by spinning the motor and executing the read function
#  The read function determines the total position that the motor rotated.  
#  The encoder accounts for the overflows when the position of the motor passes 
#  65535 and -65535.
#
#  @section Limitations 
#  Running the clock at 20,000 Hz and a motor constant having 1000 counts per revolution, 
#  the motor needs to spin faster than 655,340 revolutions per second to 
#  generate an inaccurate reading.  The bounds of the motor position were not 
#  tested.
#
#  @section Location 
#  The location of the source code at http://wind.calpoly.edu/hg/mecha11 under
#  lab1
