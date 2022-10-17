# init servo
import utime
from machine import PWM,Pin
servo_left = PWM(Pin(1))
servo_right = PWM(Pin(2))
on_board_led = Pin(25,Pin.OUT)

led_right = Pin(15,Pin.OUT)
led_left = Pin(16,Pin.OUT)



servo_left.freq(50)
servo_right.freq(50)

#define stop,forward and reverse timing in ns
servoStop= 1500000
servo_pwr1 = 1000000
servo_pwr2 = 2000000


def stop():
    servo_left.duty_ns(servoStop)
    servo_right.duty_ns(servoStop)
    
def forward():
    servo_left.duty_ns(servo_pwr2)
    servo_right.duty_ns(servo_pwr1)

def backward():
    servo_left.duty_ns(servo_pwr1)
    servo_right.duty_ns(servo_pwr2)
    
def right():
    servo_left.duty_ns(servoStop)
    servo_right.duty_ns(servo_pwr1)
    
def left():
    servo_left.duty_ns(servo_pwr2)
    servo_right.duty_ns(servoStop)

on_board_led.value(1)
led_right.value(1)
led_left.value(1)


utime.sleep(2)
on_board_led.value(0)
led_right.value(0)
led_left.value(0)

forward()
utime.sleep(2)
stop()
utime.sleep(2)
backward()
utime.sleep(2)
stop()
utime.sleep(2)
left()
utime.sleep(2)
stop()
utime.sleep(2)
right()
utime.sleep(2)
stop()