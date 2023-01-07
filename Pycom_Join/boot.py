# boot.py -- run on boot-up
from machine import I2C
import pycom

pycom.heartbeat(False)

i2c = I2C(0, I2C.MASTER)
# i2c.init(I2C.MASTER, baudrate=40000)
i2c.init(I2C.MASTER, baudrate=10000)

print("Ending of boot file :")
