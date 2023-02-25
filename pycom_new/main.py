import ujson
from network import LoRa
import binascii
import socket
import struct
import time
import ubinascii
from scd30 import SCD30
from machine import Pin

# lora config and connection
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('245E35A837F40090C15648F94D227B62')
dev_eui = ubinascii.unhexlify('70B3D5499FE87A4C')

lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

while not lora.has_joined():
    time.sleep(2.5)
    print("Not yet joined")

s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(True)

#co2 and motion pins
scd30 = SCD30(i2c, 0x61)
readypin = Pin('P11', Pin.IN, Pin.PULL_DOWN)
pir = Pin('P20', Pin.IN, Pin.PULL_DOWN)

#config and flags for pir
hold_time_sec = 10
last_trigger = -10
pir = Pin('P20',Pin.IN, Pin.PULL_DOWN)
isAvailable = True
data = dict()

scd30.start_continous_measurement(0)

print("Starting main loop")

while True:
    isAvailable = True

    if readypin() == 1 and scd30.get_status_ready() == 1:
        time.sleep(0.5)
        message = "Co2 = {0:.0f} ppm \tTemperature = {1:.0f} °C \tHumidity = {2:.0f} % RH"
        measure = scd30.read_measurement()
        if measure[0] >= 700:
            isAvailable = False
        data = {'co2': measure[0], 'temperature': measure[1], 'humidity': measure[2], 'isAvailable':isAvailable}
        print(message.format(measure[0], measure[1], measure[2]))

    if pir() == 1:
        if time.time() - last_trigger > hold_time_sec:
            last_trigger = time.time()
            pycom.rgbled(0x007f00)
            data["isAvailable"] = False
            print("Presence detected")
    else:
        last_trigger = 0
        pycom.rgbled(0x7f0000)
        print("Not detected")

    data = ujson.dumps(data)
    s.send(bytes(data, 'utf-8'))

print("Exited main loop")
