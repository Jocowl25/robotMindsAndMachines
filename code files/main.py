from nanonav import BLE, NanoBot
import time
from machine import Pin
Pin(28, Pin.OUT).on()

robot = NanoBot()

ble = BLE(name="NanoNav2")

SEARCH_SPEED   = 20
ALIGN_SPEED    = 15
TURN_SPEED     = 20
CROSS_SPEED    = 20
LOOP_DELAY     = 0.02

position_x = 0
position_y = 0
facing = 0

def find_and_center_on_line():
    print("Finding initial line...")
    
    while True:
        left  = robot.ir_left()
        right = robot.ir_right()

        if not left and not right:
            robot.m1_forward(SEARCH_SPEED)
            robot.m2_forward(SEARCH_SPEED)
        else:
            robot.stop()
            time.sleep(0.1)
            break
        time.sleep(LOOP_DELAY)

    print("Aligning to line...")
    while True:
        left  = robot.ir_left()
        right = robot.ir_right()

        if left and right:
            robot.stop()
            time.sleep(0.1)
            break

        if left and not right:
            robot.m1_forward(ALIGN_SPEED)
            robot.m2_backward(ALIGN_SPEED)

        elif right and not left:
            robot.m1_backward(ALIGN_SPEED)
            robot.m2_forward(ALIGN_SPEED)

        else:
            robot.m1_backward(ALIGN_SPEED)
            robot.m2_backward(ALIGN_SPEED)

        time.sleep(0.05)
        robot.stop()
        time.sleep(0.03)
    
    print("Centered on line!")

def drive_to_next_line():
    global position_x, position_y, facing
    
    print(f"Driving to next line... Current position: ({position_x}, {position_y}), Facing: {facing}")
    
    while True:
        left = robot.ir_left()
        right = robot.ir_right()
        
        if left and right:
            robot.stop()
            time.sleep(0.5)
            break
        
        robot.m1_forward(CROSS_SPEED)
        robot.m2_forward(CROSS_SPEED)
        time.sleep(LOOP_DELAY)
    
    robot.m1_forward(CROSS_SPEED)
    robot.m2_forward(CROSS_SPEED)
    time.sleep(0.3)
    robot.stop()
    time.sleep(0.2)
    
    if facing == 0:
        position_y += 1
    elif facing == 1:
        position_x -= 1
    elif facing == 2:
        position_y -= 1
    elif facing == 3:
        position_x += 1
    
    print(f"Reached next line! New position: ({position_x}, {position_y})")

def turn_right_90():
    global facing
    
    robot.set_enc1(0)
    robot.set_enc2(0)
    
    while abs(robot.get_enc1()) < robot.turn90ticks or abs(robot.get_enc2()) < robot.turn90ticks:
        robot.m1_forward(TURN_SPEED)
        robot.m2_backward(TURN_SPEED)
        time.sleep(0.02)
    
    robot.stop()
    time.sleep(0.3)
    
    facing = (facing + 1) % 4
    print(f"Turned right. Now facing: {facing}")

def turn_left_90():
    global facing
    
    robot.set_enc1(0)
    robot.set_enc2(0)
    
    while abs(robot.get_enc1()) < robot.turn90ticks or abs(robot.get_enc2()) < robot.turn90ticks:
        robot.m1_backward(TURN_SPEED)
        robot.m2_forward(TURN_SPEED)
        time.sleep(0.02)
    
    robot.stop()
    time.sleep(0.3)
    
    facing = (facing - 1) % 4
    print(f"Turned left. Now facing: {facing}")

def go_up():
    drive_to_next_line()

def go_down():
    turn_left_90()
    turn_left_90()
    drive_to_next_line()
    turn_left_90()
    turn_left_90()

def go_right():
    turn_right_90()
    drive_to_next_line()
    turn_left_90()

def go_left():
    turn_left_90()
    drive_to_next_line()
    turn_right_90()

def get_bluetooth_signal(): #0 safe, dont add, 1 wumpus m, 2 pit p, 3 glitter g, 4 gold G 5 done
    response = ble.read()
    values=[]
    while response!=5 or response!=0: #signal done or safe respectively
        if response==1: #
            values.append("m") #wumpus
        elif response==2:
            values.append("p") #pit
        elif response==3:
            values.append("g") #gold surrounding
        elif response==4:
            values.append("G") #on gold
        return values
try:
    find_and_center_on_line()
    go_up()
    go_down()
    go_left()
    go_right()
    robot.stop()

except KeyboardInterrupt:
    robot.stop()
    print("\nStopped by user")