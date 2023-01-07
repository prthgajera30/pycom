import time
from scd30 import SCD30
import pycom
from machine import Pin

scd30 = SCD30(i2c, 0x61)
readypin = Pin('P11', Pin.IN, Pin.PULL_DOWN)
hold_time_sec = 10
last_trigger = -10
pir = Pin('P20',mode=Pin.IN)

scd30.start_continous_measurement(0)

# main loop
print("Starting main loop")
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

	if pir() == 1:
        if time.time() - last_trigger > hold_time_sec:
            last_trigger = time.time()
            pycom.rgbled(0x007f00)
            pybytes.send_signal(4, "Detected")
            print("Presence detected")
    else:
        last_trigger = 0
        pycom.rgbled(0x7f0000)
        pybytes.send_signal(4, "Not detected")
        print("Not detected")

    time.sleep(5)

print("Exited main loop")
