from nanonav import NanoBot
import time

robot = NanoBot()

TURN_SPEED = 25  # speed for turning

def test_turn_right(tick_count):
    """Test a right turn with specified encoder ticks"""
    print(f"\nTesting RIGHT turn with {tick_count} ticks")
    print("Press Enter when ready...")
    input()
    
    robot.set_enc1(0)
    robot.set_enc2(0)
    
    # Turn right: left motor forward, right motor backward
    while abs(robot.get_enc1()) < tick_count or abs(robot.get_enc2()) < tick_count:
        robot.m1_forward(TURN_SPEED)
        robot.m2_backward(TURN_SPEED)
        time.sleep(0.01)
    
    robot.stop()
    print(f"Completed turn. Enc1: {robot.get_enc1()}, Enc2: {robot.get_enc2()}")
    print("Check if the robot turned exactly 90 degrees")
    time.sleep(1)

def test_turn_left(tick_count):
    """Test a left turn with specified encoder ticks"""
    print(f"\nTesting LEFT turn with {tick_count} ticks")
    print("Press Enter when ready...")
    input()
    
    robot.set_enc1(0)
    robot.set_enc2(0)
    
    # Turn left: left motor backward, right motor forward
    while abs(robot.get_enc1()) < tick_count or abs(robot.get_enc2()) < tick_count:
        robot.m1_backward(TURN_SPEED)
        robot.m2_forward(TURN_SPEED)
        time.sleep(0.01)
    
    robot.stop()
    print(f"Completed turn. Enc1: {robot.get_enc1()}, Enc2: {robot.get_enc2()}")
    print("Check if the robot turned exactly 90 degrees")
    time.sleep(1)

def manual_calibration():
    """Let user manually control the turn to find exact tick count"""
    print("\n=== MANUAL CALIBRATION MODE ===")
    print("The robot will turn continuously. Stop it when it reaches 90 degrees.")
    print("Press Enter to start turning right...")
    input()
    
    robot.set_enc1(0)
    robot.set_enc2(0)
    
    start_time = time.time()
    
    # Turn until user presses Ctrl+C
    try:
        while True:
            robot.m1_forward(TURN_SPEED)
            robot.m2_backward(TURN_SPEED)
            time.sleep(0.01)
    except KeyboardInterrupt:
        robot.stop()
        elapsed = time.time() - start_time
        enc1_final = robot.get_enc1()
        enc2_final = robot.get_enc2()
        avg_ticks = (abs(enc1_final) + abs(enc2_final)) / 2
        
        print(f"\n--- Results ---")
        print(f"Time elapsed: {elapsed:.2f} seconds")
        print(f"Encoder 1: {enc1_final} ticks")
        print(f"Encoder 2: {enc2_final} ticks")
        print(f"Average: {avg_ticks:.1f} ticks")
        print(f"\nUse turn90ticks = {int(avg_ticks)} in your code")

try:
    print("===== 90 DEGREE TURN CALIBRATION =====")
    print(f"Current turn90ticks setting: {robot.turn90ticks}")
    print("\nChoose calibration mode:")
    print("1. Test predefined tick values")
    print("2. Manual calibration (you stop it at 90 degrees)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        # Test a range of tick values around the current setting
        test_values = [
            robot.turn90ticks - 20,
            robot.turn90ticks - 10,
            robot.turn90ticks,
            robot.turn90ticks + 10,
            robot.turn90ticks + 20
        ]
        
        print("\n=== Testing RIGHT turns ===")
        for ticks in test_values:
            test_turn_right(ticks)
        
        print("\n=== Testing LEFT turns ===")
        for ticks in test_values:
            test_turn_left(ticks)
        
        print("\n=== Calibration Complete ===")
        print("Based on your observations, which tick count gave the best 90 degree turn?")
        best_ticks = input("Enter the best tick count: ").strip()
        print(f"\nUse turn90ticks = {best_ticks} in your robot configuration")
        
    elif choice == "2":
        manual_calibration()
    
    else:
        print("Invalid choice")

except KeyboardInterrupt:
    robot.stop()
    print("\nCalibration stopped by user")