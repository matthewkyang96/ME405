# -*- coding: utf-8 -*-
"""
Created on Wed May 22 18:49:46 2019

@author: melab2
"""

import bno55
from bno055_base import BNO055_BASE
import machine

i2c = machine.I2C(-1, scl=machine.Pin('B8'), sda=machine.Pin('B9'))
imu = BNO055_BASE(i2c)
