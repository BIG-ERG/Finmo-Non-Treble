#pip install evdev
#sudo usermod -a -G groupName userName
#   do line above if no device pop up

import evdev
from evdev import ecodes
import serial
import time

#ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

#time.sleep(2)   # allow Arduino reset

counter = 0

#---------------------------·LIST-DEVICES---------------------------------
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
     print(device.path, device.name, device.phys)

#-------------------------------------------------------------------------

prvTime = None
dt = 1

xRel = 0
yRel = 0

xAbs = 0
yAbs = 0

device = evdev.InputDevice('/dev/input/event0') #change eventn to correct peripheral

def cpiToMM(dots):
    CPI = 1000
    return dots*25.4 / CPI

print("xAbs:   |yAbs:    ")

for event in device.read_loop():

    # now = time.perf_counter

    if event.type == ecodes.EV_KEY:
        if event.code == ecodes.BTN_LEFT and event.value == 1:
            print("Left click detected — stopping")
            break

    if event.type == evdev.ecodes.EV_REL:               #if movement
        if event.code == evdev.ecodes.REL_X:            #if movement x
            xRel = cpiToMM(event.value)
            xAbs += xRel
        
        elif event.code == evdev.ecodes.REL_Y:          #if movement y
            yRel = cpiToMM(event.value)
            yAbs += yRel

    if event.type == evdev.ecodes.SYN_REPORT:           #if sync event happens i.e. every time mouse updates

        #ser.write(f'x:{xAbs}<,y:{yAbs}\n'.encode())
        print(f"{xAbs:8.2f}| {yAbs:8.2f}")
