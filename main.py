# init servo
import utime
from machine import PWM,Pin
servo_left = PWM(Pin(1))
servo_right = PWM(Pin(2))

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