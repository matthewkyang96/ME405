# -*- coding: utf-8 -*-

## @privatesection - Stuff in this file doesn't need to be Doxygen-ed
#
#  @author jr

import pyb
import micropython
import gc

import cotask
import task_share
import print_task


from EncoderDriver import Encoder
from motordriver import MotorDriver
from Controller import Controller
#import utime

#pinB6 = pyb.Pin (pyb.Pin.board.PB6, pyb.Pin.IN)
#pinB7 = pyb.Pin (pyb.Pin.board.PB7, pyb.Pin.IN)
#tim4 = pyb.Timer(4, prescaler=1, period=65535)
#
#pinC6 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.IN)
#pinC7 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.IN)
#tim8 = pyb.Timer(8, prescaler=1, period=65535)

PA10 = pyb.Pin (pyb.Pin.board.PA10, pyb.Pin.OUT_PP) #defines encoder pin
PB4 = pyb.Pin (pyb.Pin.board.PB4, pyb.Pin.OUT_PP) #defines pin IN1A
PB5 = pyb.Pin (pyb.Pin.board.PB5, pyb.Pin.OUT_PP) #defines pin IN1A
tim3 = pyb.Timer (3, freq=20000) #defines timer channel 3 to 20000Hz

PC1 = pyb.Pin (pyb.Pin.board.PC1, pyb.Pin.OUT_PP) #defines encoder pin
PA0 = pyb.Pin (pyb.Pin.board.PA0, pyb.Pin.OUT_PP) #defines pin IN1A
PA1 = pyb.Pin (pyb.Pin.board.PA1, pyb.Pin.OUT_PP) #defines pin IN1A
tim5 = pyb.Timer (5, freq=20000) #defines timer channel 3 to 20000Hz

##  ----DEFINED VARIABLES--- ##
#PINB6; PINB7; Timer 4
PB6 = pyb.Pin (pyb.Pin.board.PB6, pyb.Pin.IN)
PB7 = pyb.Pin (pyb.Pin.board.PB7, pyb.Pin.IN)
tim4 = pyb.Timer(4, prescaler=1, period=65535)

#PINC6; PINC7; Timer 8
PC6 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.IN)
PC7 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.IN)
tim8 = pyb.Timer(8, prescaler=1, period=65535)

motor1 = MotorDriver(PA10,PB4,PB5,tim3)				#creates object of class MotorDriver
motor2 = MotorDriver(PC1,PA0,PA1,tim5)
enc1 = Encoder(PB6,PB7,tim4)   #creates object of class Encoder
enc2 = Encoder(PC6,PC7,tim8)
control1 = Controller()	 			#creates object of class Controller
control2 = Controller()
# Allocate memory so that exceptions raised in interrupt service routines can
# generate useful diagnostic printouts
micropython.alloc_emergency_exception_buf (100)



#theta_ref = int(10000)
#K_p = float(0.02)

def task1_encoder ():
    ''' Docstring.  '''
    while True:   
        theta_measured1.put(enc1.read()) 
        theta_measured2.put(enc2.read())
        yield (0)


def task2_motorcontroller1 ():
    ''' Docstring. '''
    while True:
        x = theta_measured1.get()
        
        level1 = control1.closed_loop(x,10000,.02)
        
        motor1.set_duty_cycle(level1) 
        yield (0)

def task2_motorcontroller2 ():
    ''' Docstring. '''
    while True:
      
        y = theta_measured2.get()
        
        level2 = control2.closed_loop(y,10000,1)
         
        motor2.set_duty_cycle(level2) 
       
        yield (0)    

      


# =============================================================================

if __name__ == "__main__":

    print ('\033[2JTesting scheduler in cotask.py\n')

    # Create a share and some queues to test diagnostic printouts
    share0 = task_share.Share ('i', thread_protect = False, name = "Share_0")
    theta_measured1 = task_share.Share('i', name = "theta_measured")
    theta_measured2 = task_share.Share('i', name = "theta_measured")
    q0 = task_share.Queue ('B', 6, thread_protect = False, overwrite = False,
                           name = "Queue_0")
    q1 = task_share.Queue ('B', 8, thread_protect = False, overwrite = False,
                           name = "Queue_1")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task (task1_encoder, name = 'Task_1', priority = 1, 
                         period = 0.5, profile = True, trace = False)
    task2 = cotask.Task (task2_motorcontroller1, name = 'Task_2', priority = 2, 
                         period = 1, profile = True, trace = False)
    task3 = cotask.Task (task2_motorcontroller2, name = 'Task_3', priority = 2, 
                         period = 1, profile = True, trace = False)
    cotask.task_list.append (task1)
    cotask.task_list.append (task2)
    cotask.task_list.append (task3)

    # A task which prints characters from a queue has automatically been
    # created in print_task.py; it is accessed by print_task.put_bytes()
#    motor1.p1.low()
#    motor2.p1.low()
    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

    # Run the scheduler with the chosen scheduling algorithm. Quit if any 
    # character is sent through the serial por
    vcp = pyb.USB_VCP ()
    while not vcp.any ():
        cotask.task_list.pri_sched ()

    # Empty the comm port buffer of the character(s) just pressed
    vcp.read ()

    # Print a table of task data and a table of shared information data
    print ('\n' + str (cotask.task_list) + '\n')
    print (task_share.show_all ())
    print (task1.get_trace ())
    print ('\r\n')
   

