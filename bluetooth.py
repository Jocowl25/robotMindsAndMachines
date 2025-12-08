from nanonav import BLE, NanoBot
import time

### test motors and encoders ###

# Create a NanoBot object
robot = NanoBot()

# Create a Bluetooth object
ble = BLE(name="NanoNav2")

# send 41 as a single byte (your code expects this)
ble.send(41)

# read once and check for connection
if ble.read() == 41:
    print("connected")

# wait until something changes, indicating a response
response = ble.read()
while True:

    if response == 1:
        print("Received: ", response)
        robot.m1_forward(30)
        robot.m2_forward(30)
        robot.stop()

    if response == 2:
        print("Received: ", response)
        robot.m1_backward(30)
        robot.m2_backward(30)
        robot.stop()
    