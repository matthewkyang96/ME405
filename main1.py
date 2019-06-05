import pyb
from EncoderDriver import Encoder
from bno055_base import BNO055_BASE
from motordriver import MotorDriver
import machine
import utime
import task_share
import cotask
import micropython

micropython.alloc_emergency_exception_buf(100)

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

motor = MotorDriver(PA10,PB4,PB5,tim3)
encoder = Encoder(pinB6,pinB7,tim4)
i2c = machine.I2C(-1, scl=machine.Pin('B8'), sda=machine.Pin('B9'))
imu = BNO055_BASE(i2c)
calibrated = False
euler_angle = imu.euler()
positionref = euler_angle[1]
error_old = 0

## QUEUES
euler_angle = task_share.Queue('i',1000,thread_protect=True,overwrite=False)

timing  = pyb.Timer(1,freq=1000)

motor.set_duty_cycle(0)
kp = input('enter kp')
kd = input('enter kd')
kp = float(kp)
kd = float(kd)

##IMU INTERRUPT TASK##
def read_interrupt(source):
	angle = imu.euler()
	angle = angle[1]
	euler_angle.put(angle)

##CONTROLLER TASK##
def controller():
	timing.callback(read_interrupt)
	while True:
		theta_error = euler_angle.get() - positionref
		proportional = kp * theta_error
		delta_theta = theta_error - error_old
		derivative = kd * delta_theta/1
		a = derivative + proportional
		if a > 100:
        	a = 100
    	elif a < -100:
        	a = -100
    	else:
        	a = a
        error_old = theta_error
        set_duty_cycle(a)
		yield(0)

