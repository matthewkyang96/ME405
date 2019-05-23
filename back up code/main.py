
import pyb
from bno055_base import BNO055_BASE
from motordriver import MotorDriver
import machine
import time

PA10 = pyb.Pin (pyb.Pin.board.PA10, pyb.Pin.OUT_PP) #defines encoder pin
PA10.high () #set encoder pin A to on
PB4 = pyb.Pin (pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
tim3 = pyb.Timer (3, freq=20000) #defines timer channel 3 to 20000Hz
PB5 = pyb.Pin (pyb.Pin.board.PB5, pyb.Pin.OUT_PP) #defines pin IN2A

motor = MotorDriver(PA10,PB4,PB5,tim3)

i2c = machine.I2C(-1, scl=machine.Pin('B8'), sda=machine.Pin('B9'))
imu = BNO055_BASE(i2c)
calibrated = False
euler_angle = imu.euler()
positionref = euler_angle[2]


while True:
    time.sleep(1)
    if not calibrated:
        calibrated = imu.calibrated()
        print('Calibration required: sys {} gyro {} accel {} mag {}'.format(*imu.cal_status()))
    print('Temperature {}°C'.format(imu.temperature()))
    
    print('Gyro      x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.gyro()))
    print('Accel     x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.accel()))
    print('Lin acc.  x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.lin_acc()))
    print('Gravity   x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.gravity()))
    print('Heading     {:4.0f} roll {:4.0f} pitch {:4.0f}'.format(*imu.euler()))
    
    newposition = euler_angle[2] - positionref
    if newposition == 0:
  
        motor.set_duty_cycle(0)
    elif newposition > positionref:
        motor.set_duty_cycle(-100)

    elif newposition < positionref:
        motor.set_duty_cycle(100)

    