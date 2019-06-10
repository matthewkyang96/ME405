import pyb
from EncoderDriver import Encoder
from bno055_base import BNO055_BASE
from motordriver import MotorDriver
import machine
import utime
import task_share
import cotask
import micropython
import gc
from hcsr04 import HCSR04

micropython.alloc_emergency_exception_buf(100)
## Fly Wheel##
PA10 = pyb.Pin (pyb.Pin.board.PA10, pyb.Pin.OUT_PP) #defines encoder pin
PA10.high () #set encoder pin A to on
PB4 = pyb.Pin (pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
tim3 = pyb.Timer (3, freq=20000) #defines timer channel 3 to 20000Hz
PB5 = pyb.Pin (pyb.Pin.board.PB5, pyb.Pin.OUT_PP) #defines pin IN2A
ch2m = tim3.channel (2, pyb.Timer.PWM, pin=PB5) #defines Channel 2
ch1m = tim3.channel (1, pyb.Timer.PWM, pin=PB4) #defines Channel 1
ch1m.pulse_width_percent (0) #initializes motor to off
ch2m.pulse_width_percent (0) #initializes motor to off

pinB6 = pyb.Pin (pyb.Pin.board.PB6, pyb.Pin.IN)            
pinB7 = pyb.Pin (pyb.Pin.board.PB7, pyb.Pin.IN)            
tim4 = pyb.Timer(4, prescaler=1, period=65535)
## BACK MOTOR ##
PC1 = pyb.Pin (pyb.Pin.board.PC1, pyb.Pin.OUT_PP) #defines encoder pin
PA0 = pyb.Pin (pyb.Pin.board.PA0, pyb.Pin.OUT_PP) #defines pin IN1A
PA1 = pyb.Pin (pyb.Pin.board.PA1, pyb.Pin.OUT_PP) #defines pin IN1A
tim5 = pyb.Timer (5, freq=20000) #defines timer channel 3 to 20000Hz

## IR REMOTE##
pinC0 = pyb.Pin(pyb.Pin.board.PC0,pyb.Pin.IN)

##DEFINED VARIABLES##
motor = MotorDriver(PA10,PB4,PB5,tim3)
motor1 = MotorDriver(PC1,PA0,PA1,tim5)
encoder = Encoder(pinB6,pinB7,tim4)
i2c = machine.I2C(-1, scl=machine.Pin('B8'), sda=machine.Pin('B9'))
imu = BNO055_BASE(i2c)
calibrated = False


euler_angle = imu.euler()
positionref = euler_angle[1]
print(positionref)
print(euler_angle)
print(imu.euler())


#Sensor Initialization#
sensor = HCSR04(trigger_pin=machine.Pin('A8'), echo_pin=machine.Pin('A9'))

## QUEUES
dist = task_share.Queue('i',1000,thread_protect=True,overwrite=False)


motor.set_duty_cycle(0)
#kp = input('enter kp')
#kd = input('enter kd')
#ki = input('enter ki')
#kp = float(kp)
#kd = float(kd)
#ki = float(ki)
x=input()
kp=40
kd=1
ki=.2
print(imu.euler())
positionref = imu.euler()[1]
print(positionref)

##IMU INTERRUPT TASK##
#def read_interrupt(source):
#	 angle = imu.euler()
#	 angle = angle[1]
#	 euler_angle.put(angle)

##ULTRASONIC SENSOR TASK##
def USSENSOR():
    while True:
        if sensor.distance_cm() < 10:
            motor1.set_duty_cycle(0)
            print(sensor.distance_cm())
        yield(0)
    
##CONTROLLER TASK##
def controller():
#    timing.callback(read_interrupt)
    error_old = 0
    while True:
        theta_error = imu.euler()[1] - positionref
        proportional = kp * theta_error
#        delta_theta = theta_error - error_old
        derivative = -kd * imu.gyro()[1]       
        integral = (theta_error*.00005 + error_old)*-ki
        a = derivative + proportional+integral 
        if a > 100:
            a = 100
        elif a < -100:
            a = -100
        else:
            a = a
#        error_old = theta_error
        motor.set_duty_cycle(-a)
       
        yield(0)
        
        
##REMOTE##
def remote():
    state=0
    while True:
        if state == 0:
            if pinC0.value() == 0:
                motor1.set_duty_cycle(35)
                state = 1
                print('go')
        elif state == 1:
            if pinC0.value() == 0:
                motor1.set_duty_cycle(0)
                state =0
                print('stop')
        yield(state)
            
## REMOTE CONTROLLER ##
#def remote(source):
#    '''something from remote controller interrupts'''      
        
# =============================================================================

if __name__ == "__main__":

    print ('\033[2JTesting scheduler in cotask.py\n')

    # Create a share and some queues to test diagnostic printouts
   
#   distance = task_share.Share('i', name = "distance")
#    theta_measured2 = task_share.Share('i', name = "theta_measuredB")
#    theta_ref1 = task_share.Share('i', name = "theta_refA")
#    theta_ref1 = task_share.Share('i', name = "theta_refB")
#    k_p1 = task_share.Share('f', name = "k_pA")
#    k_p2 = task_share.Share('f', name = "k_pB")
   
    


    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task (controller, name = 'Task_1', priority = 3, 
                         period = .5, profile = True, trace = False)
    task2 = cotask.Task (USSENSOR, name = 'Task_2', priority = 4, 
                       period = 500, profile = True, trace = False)
   
    task3 = cotask.Task (remote, name = 'Task_3', priority = 3, 
                         period = 75, profile = True, trace = False)
    

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

    