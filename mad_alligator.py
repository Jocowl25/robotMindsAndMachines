from nanonav import NanoBot
import time

robot = NanoBot()

# Speed constants
OUTER_SPEED = 35  # speed for the outer wheel in a turn
INNER_SPEED = 15  # speed for the inner wheel in a turn

# Duration for each half of the figure 8 (tune these values)
CIRCLE_TIME = 3.0  # seconds to complete each circle

try:
    
    print("Starting first circle (clockwise)")
    robot.m1_forward(OUTER_SPEED)  # left motor
    robot.m2_forward(INNER_SPEED)  # right motor
    time.sleep(CIRCLE_TIME)
    
    print("Starting second circle (counter-clockwise)")
    robot.m1_forward(INNER_SPEED)  # left motor
    robot.m2_forward(OUTER_SPEED)  # right motor
    time.sleep(CIRCLE_TIME)
    
    # Stop
    robot.stop()
    print("Figure 8 complete!")

except KeyboardInterrupt:
    robot.stop()
    print("Stopped by user")
