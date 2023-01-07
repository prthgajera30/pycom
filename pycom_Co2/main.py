import time
from scd30 import SCD30

scd30 = SCD30(i2c, 0x61)
readypin = Pin('P11', Pin.IN, Pin.PULL_DOWN)

scd30.start_continous_measurement(0)

while True:
    if readypin() == 1 and scd30.get_status_ready() == 1:
		message = "Co2 = {0:.0f} ppm \tTemperature = {1:.0f} °C \tHumidity = {2:.0f} % RH"
		measure = scd30.read_measurement()
		print(message.format(measure[0], measure[1], measure[2]))
		pybytes.send_signal(1, round(measure[0]))
		pybytes.send_signal(2, round(measure[1]))
		pybytes.send_signal(3, round(measure[2]))
    else:
        time.sleep(3)
	time.sleep(5)
