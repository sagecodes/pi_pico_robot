# Import required libraries
import utime  # Library for time-related functions
from machine import PWM, ADC, Pin  # Library for controlling pins, PWM, and ADC

# ---------------------------
# Pin Configuration
# ---------------------------

# Setup PWM for servos (left and right wheels)
servo_left = PWM(Pin(1))
servo_right = PWM(Pin(2))

# Setup LED pins
on_board_led = Pin(25, Pin.OUT)  # Onboard LED
led_right = Pin(15, Pin.OUT)     # Right external LED
led_left = Pin(16, Pin.OUT)      # Left external LED

# Setup photoresistors (light sensors) for left and right sides
photo_left = ADC(Pin(26))
photo_right = ADC(Pin(27))

# Setup touch sensors (bump sensors) with internal pull-down resistors
touch_right = Pin(14, Pin.IN, Pin.PULL_DOWN)
touch_left = Pin(13, Pin.IN, Pin.PULL_DOWN)

# ---------------------------
# Servo Configuration
# ---------------------------

# Set PWM frequency for servos to 50 Hz
servo_left.freq(50)
servo_right.freq(50)

# Define duty cycle values for different servo states (in nanoseconds)
servo_stop = 1500000  # Stop position
servo_forward = 2000000  # Full forward position
servo_backward = 1000000  # Full backward position

# ---------------------------
# Motor Control Functions
# ---------------------------

# Stop both servos (robot stays still)
def stop():
    servo_left.duty_ns(servo_stop)
    servo_right.duty_ns(servo_stop)

# Move both wheels forward
def both_forward():
    servo_left.duty_ns(servo_forward)
    servo_right.duty_ns(servo_backward)

# Move both wheels backward
def both_backward():
    servo_left.duty_ns(servo_backward)
    servo_right.duty_ns(servo_forward)

# Turn right by moving only the right wheel forward
def right_forward():
    servo_left.duty_ns(servo_stop)
    servo_right.duty_ns(servo_backward)

# Turn left by moving only the left wheel forward
def left_forward():
    servo_left.duty_ns(servo_forward)
    servo_right.duty_ns(servo_stop)

# Turn right by moving only the right wheel backward
def right_backward():
    servo_left.duty_ns(servo_stop)
    servo_right.duty_ns(servo_forward)

# Turn left by moving only the left wheel backward
def left_backward():
    servo_left.duty_ns(servo_backward)
    servo_right.duty_ns(servo_stop)

# ---------------------------
# Light Following Logic
# ---------------------------

# Function to make the robot follow the light
def light_follow():
    light_left = photo_left.read_u16()  # Read left light sensor
    light_right = photo_right.read_u16()  # Read right light sensor
    
    if light_right < light_left:
        # If more light is detected on the right side, turn right
        servo_right.duty_ns(servo_backward)
        servo_left.duty_ns(servo_stop)
    elif light_left < light_right:
        # If more light is detected on the left side, turn left
        servo_right.duty_ns(servo_stop)
        servo_left.duty_ns(servo_forward)

# ---------------------------
# Initial Setup
# ---------------------------

# Turn on all LEDs as an initial signal
on_board_led.value(1)
led_right.value(1)
led_left.value(1)

# Read initial light sensor values and print them
light_left = photo_left.read_u16()
light_right = photo_right.read_u16()

# Wait for 2 seconds before starting the main loop
utime.sleep(2)
print("Left Light Sensor:", light_left)
print("Right Light Sensor:", light_right)

# Turn off all LEDs after the initial setup
on_board_led.value(0)
led_right.value(0)
led_left.value(0)

# ---------------------------
# Main Loop
# ---------------------------

# Continuous loop to check touch sensors and control the robot
while True:
    if touch_right.value() == 1 and touch_left.value() == 1:
        # Both touch sensors pressed (obstacle detected on both sides)
        led_right.value(1)
        led_left.value(1)
        both_backward()  # Move backward
        utime.sleep(1)
        left_backward()  # Turn left
        utime.sleep(1)
    elif touch_right.value() == 1:
        # Right touch sensor pressed
        led_right.value(1)
        both_backward()  # Move backward
        utime.sleep(0.5)
        left_backward()  # Turn left
        utime.sleep(1)
    elif touch_left.value() == 1:
        # Left touch sensor pressed
        led_left.value(1)
        both_backward()  # Move backward
        utime.sleep(0.5)
        right_backward()  # Turn right
        utime.sleep(1)
    else:
        # No touch sensor is pressed, follow the light
        led_right.value(0)
        led_left.value(0)
        light_follow()  # Call light-following function

