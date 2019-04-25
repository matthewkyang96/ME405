# -*- coding: utf-8 -*-
#
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

pinB6 = pyb.Pin (pyb.Pin.board.PB6, pyb.Pin.IN)
pinB7 = pyb.Pin (pyb.Pin.board.PB7, pyb.Pin.IN)
tim4 = pyb.Timer(4, prescaler=1, period=65535)

pinC6 = pyb.Pin (pyb.Pin.board.PC6, pyb.Pin.IN)
pinC7 = pyb.Pin (pyb.Pin.board.PC7, pyb.Pin.IN)
tim8 = pyb.Timer(8, prescaler=1, period=65535)

motor = MotorDriver()				#creates object of class MotorDriver
enc = Encoder(pinC6,pinC7,tim8)   #creates object of class Encoder
control = Controller()				#creates object of class Controller
# Allocate memory so that exceptions raised in interrupt service routines can
# generate useful diagnostic printouts
micropython.alloc_emergency_exception_buf (100)



#theta_ref = int(10000)
#K_p = float(0.02)

def task1_encoder ():
    ''' Docstring.  '''
    while True:   
        theta_measured.put(enc.read()) 
        yield (0)


def task2_motorcontroller ():
    ''' Docstring. '''
    while True:
        x = theta_measured.get()
        level = control.closed_loop(x,10000,.02)
        
        motor.set_duty_cycle(level) 
        yield (0)
      

      


# =============================================================================

if __name__ == "__main__":

    print ('\033[2JTesting scheduler in cotask.py\n')

    # Create a share and some queues to test diagnostic printouts
    share0 = task_share.Share ('i', thread_protect = False, name = "Share_0")
    theta_measured = task_share.Share('i', name = "theta_measured")
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
    task2 = cotask.Task (task2_motorcontroller, name = 'Task_2', priority = 2, 
                         period = 1, profile = True, trace = False)
    cotask.task_list.append (task1)
    cotask.task_list.append (task2)

    # A task which prints characters from a queue has automatically been
    # created in print_task.py; it is accessed by print_task.put_bytes()

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

