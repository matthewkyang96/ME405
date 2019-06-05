
import pyb
from EncoderDriver import Encoder
from bno055_base import BNO055_BASE
from motordriver import MotorDriver
import machine
import utime
import task_share
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
timing  = pyb.Timer(1,freq=500)

pinB6 = pyb.Pin (pyb.Pin.board.PB6, pyb.Pin.IN)            
pinB7 = pyb.Pin (pyb.Pin.board.PB7, pyb.Pin.IN)            
tim4 = pyb.Timer(4, prescaler=1, period=65535)

motor = MotorDriver(PA10,PB4,PB5,tim3)
encoder = Encoder(pinB6,pinB7,tim4)
Q = task_share.Queue('i',1000,thread_protect=True,overwrite=False)
i2c = machine.I2C(-1, scl=machine.Pin('B8'), sda=machine.Pin('B9'))
imu = BNO055_BASE(i2c)
calibrated = False
euler_angle = imu.euler()
positionref = euler_angle[2]

error_old = 0

motor.set_duty_cycle(0)
kp = input('enter kp')
kd = input('enter kd')
kp = float(kp)
kd = float(kd)

ref_time = utime.ticks_ms()

def controller(source):
    x = imu.euler()
    theta_error = x[1] - positionref
    delta_theta = theta_error- error_old
    theta_error = error_old
    proportional = kp * theta_error
    derivative = kd*delta_theta/2
    a = derivative + proportional
    if a > 100:
        a = 100
    elif a < -100:
        a = -100
    else:
        a = a
    Q.put(a)
    
timing.callback(controller)    

while True:
    motor.set_duty_cycle(Q.get(in_ISR=True))
#while True:
##    time.sleep(1)
#    if not calibrated:
#        calibrated = imu.calibrated()
#        euler_angle = imu.euler()
#        positionref = euler_angle[1]
#        print('stuck') 
#        print('Calibration required: sys {} gyro {} accel {} mag {}'.format(*imu.cal_status()))
#        calibrated = True
#        
#    print('Temperature {}°C'.format(imu.temperature()))
#    
#    print('Gyro      x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.gyro()))
#    print('Accel     x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.accel()))
#    print('Lin acc.  x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.lin_acc()))
#    print('Gravity   x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.gravity()))
#    print('Heading     {:4.0f} roll {:4.0f} pitch {:4.0f}'.format(*imu.euler()))
#    now= utime.ticks_ms()
#    delta= now - ref_time
#    ref_time= utime.ticks_ms()
#    x = imu.euler()
#    theta_error = x[1] - positionref
#    error_sum = .001*theta_error + error_sum
#    proportional = kp * theta_error
#    integral = ki * error_sum
#    a = integral + proportional
#    if a > 100:
#        a = 100
#    elif a < -100:
#        a = -100
#    else:
#        a = a
#    motor.set_duty_cycle(-a)
#   
    
 
   

    