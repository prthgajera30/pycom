import pycom
import time
from machine import Pin

pycom.heartbeat(False)
#config
hold_time_sec = 10
#flags
last_trigger = -10
pir = Pin('P20',mode=Pin.IN)

# main loop
print("Starting main loop")
while True:
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

    time.sleep_ms(500)

print("Exited main loop")
