# Import libraries 
import utime
from machine import PWM, ADC, Pin



# Define pin IOs
servo_left = PWM(Pin(1))
servo_right = PWM(Pin(2))
on_board_led = Pin(25,Pin.OUT)
led_right = Pin(15,Pin.OUT)
led_left = Pin(16,Pin.OUT)
photo_left = ADC(Pin(26))
photo_right = ADC(Pin(27))
touch_right = Pin(14, Pin.IN, Pin.PULL_DOWN)
touch_left = Pin(13, Pin.IN, Pin.PULL_DOWN)


# Set PWM Frequency
servo_left.freq(50)
servo_right.freq(50)

#define stop,forward and reverse timing in ns
servoStop= 1500000
servo_pwr1 = 1000000
servo_pwr2 = 2000000


def stop():
    servo_left.duty_ns(servoStop)
    servo_right.duty_ns(servoStop)
    
def both_forward():
    servo_left.duty_ns(servo_pwr2)
    servo_right.duty_ns(servo_pwr1)

def both_backward():
    servo_left.duty_ns(servo_pwr1)
    servo_right.duty_ns(servo_pwr2)
    
def right_forward():
    servo_left.duty_ns(servoStop)
    servo_right.duty_ns(servo_pwr1)
    
def left_forward():
    servo_left.duty_ns(servo_pwr2)
    servo_right.duty_ns(servoStop)
    
def right_backward():
    servo_left.duty_ns(servoStop)
    servo_right.duty_ns(servo_pwr2)
    
def left_backward():
    servo_left.duty_ns(servo_pwr1)
    servo_right.duty_ns(servoStop)
    
def light_follow():
    light_left = photo_left.read_u16()
    light_right = photo_right.read_u16()
    if light_right < light_left:
        servo_right.duty_ns(servo_pwr1)
        servo_left.duty_ns(servoStop)
    elif light_left < light_right:
        servo_right.duty_ns(servoStop)
        servo_left.duty_ns(servo_pwr2)
        

on_board_led.value(1)
led_right.value(1)
led_left.value(1)
light_left = photo_left.read_u16()
light_right = photo_right.read_u16()




utime.sleep(2)
print(light_left)
print(light_right)
on_board_led.value(0)
led_right.value(0)
led_left.value(0)

while True:
    if touch_right.value() == 1 and touch_left.value() == 1:
        led_right.value(1)
        led_left.value(1)
        both_backward()
        utime.sleep(1)
        left_backward()
        utime.sleep(1)
    elif touch_right.value() == 1:
        led_right.value(1)
        both_backward()
        utime.sleep(0.5)
        left_backward()
        utime.sleep(1)
    elif touch_left.value() == 1:
        led_left.value(1)
        both_backward()
        utime.sleep(0.5)
        right_backward()
        utime.sleep(1)
    else:
        led_right.value(0)
        led_left.value(0)
        light_follow()
        # both_forward()
        #utime.sleep(2)
        #stop()