from smbus2 import SMBus, i2c_msg
import time

bus = SMBus(20)
addr = 0x48

config = 0xC383
data = [(config >> 8) & 0xFF, config & 0xFF]

msg = i2c_msg.write(addr, [0x01] + data)
bus.i2c_rdwr(msg)

time.sleep(0.01)

msg = i2c_msg.write(addr, [0x00])
bus.i2c_rdwr(msg)

read = i2c_msg.read(addr, 2)
bus.i2c_rdwr(msg, read)

print(list(read))